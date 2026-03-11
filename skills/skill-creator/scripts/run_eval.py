#!/usr/bin/env python3
"""Run trigger evaluation for a skill description.

Tests whether a skill's description causes the AI agent to trigger (activate
the skill) for a set of queries. Outputs results as JSON.

Supports both Gemini CLI and Claude Code CLI as backends.
"""

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from scripts.utils import parse_skill_md


# ---------------------------------------------------------------------------
# Backend detection
# ---------------------------------------------------------------------------

def _detect_backend() -> str:
    """Auto-detect which CLI backend is available. Prefer gemini."""
    if shutil.which("gemini"):
        return "gemini"
    if shutil.which("claude"):
        return "claude"
    raise RuntimeError("Neither 'gemini' nor 'claude' CLI found on PATH")


def find_project_root() -> Path:
    """Find the project root by walking up from cwd.

    Looks for .claude/ (Claude Code) or .gemini/ (Gemini CLI).
    """
    current = Path.cwd()
    for parent in [current, *current.parents]:
        if (parent / ".claude").is_dir() or (parent / ".gemini").is_dir():
            return parent
    return current


# ---------------------------------------------------------------------------
# Skill registration helpers
# ---------------------------------------------------------------------------

def _register_skill_gemini(skill_name: str, description: str, unique_id: str) -> Path:
    """Create a temporary skill directory in ~/.agents/skills/ for Gemini CLI.

    Uses a generic probe name (eval-probe-{id}) to avoid colliding with
    an already-installed skill that has the same base name.
    """
    probe_name = f"eval-probe-{unique_id}"
    skills_dir = Path.home() / ".agents" / "skills" / probe_name
    skills_dir.mkdir(parents=True, exist_ok=True)

    indented_desc = "\n  ".join(description.split("\n"))
    skill_content = (
        f"---\n"
        f"name: {probe_name}\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {probe_name}\n\n"
        f"This skill handles: {description}\n"
    )
    (skills_dir / "SKILL.md").write_text(skill_content)
    return skills_dir


def _register_skill_claude(skill_name: str, description: str, unique_id: str, project_root: str) -> Path:
    """Create a temporary command file in .claude/commands/ for Claude Code."""
    probe_name = f"eval-probe-{unique_id}"
    project_commands_dir = Path(project_root) / ".claude" / "commands"
    command_file = project_commands_dir / f"{probe_name}.md"
    project_commands_dir.mkdir(parents=True, exist_ok=True)

    indented_desc = "\n  ".join(description.split("\n"))
    command_content = (
        f"---\n"
        f"description: |\n"
        f"  {indented_desc}\n"
        f"---\n\n"
        f"# {probe_name}\n\n"
        f"This skill handles: {description}\n"
    )
    command_file.write_text(command_content)
    return command_file


def _cleanup_skill(path: Path, backend: str) -> None:
    """Remove the temporary skill registration."""
    if backend == "gemini":
        if path.is_dir():
            shutil.rmtree(path, ignore_errors=True)
    else:
        if path.exists():
            path.unlink()


# ---------------------------------------------------------------------------
# Trigger detection
# ---------------------------------------------------------------------------

def _check_triggered_gemini(event: dict, clean_name: str) -> bool | None:
    """Check a Gemini stream-json event for skill activation.

    Returns True if triggered, False if definitively not triggered,
    None if inconclusive (keep reading).
    """
    etype = event.get("type", "")

    if etype == "tool_use":
        tool_name = event.get("tool_name", "")
        if tool_name == "activate_skill":
            activated = event.get("parameters", {}).get("name", "")
            return clean_name in activated
        # Model used a different tool first → not triggering our skill
        return False

    if etype == "result":
        return False

    return None


def _check_triggered_claude(event: dict, clean_name: str, state: dict) -> bool | None:
    """Check a Claude stream-json event for skill invocation.

    Returns True if triggered, False if definitively not triggered,
    None if inconclusive.
    """
    etype = event.get("type", "")

    # Early detection via stream events
    if etype == "stream_event":
        se = event.get("event", {})
        se_type = se.get("type", "")

        if se_type == "content_block_start":
            cb = se.get("content_block", {})
            if cb.get("type") == "tool_use":
                tool_name = cb.get("name", "")
                if tool_name in ("Skill", "Read"):
                    state["pending_tool"] = tool_name
                    state["accumulated"] = ""
                    return None
                return False

        elif se_type == "content_block_delta" and state.get("pending_tool"):
            delta = se.get("delta", {})
            if delta.get("type") == "input_json_delta":
                state["accumulated"] += delta.get("partial_json", "")
                if clean_name in state["accumulated"]:
                    return True

        elif se_type in ("content_block_stop", "message_stop"):
            if state.get("pending_tool"):
                return clean_name in state.get("accumulated", "")
            if se_type == "message_stop":
                return False

    # Fallback: full assistant message
    elif etype == "assistant":
        message = event.get("message", {})
        for item in message.get("content", []):
            if item.get("type") != "tool_use":
                continue
            tool_name = item.get("name", "")
            tool_input = item.get("input", {})
            if tool_name == "Skill" and clean_name in tool_input.get("skill", ""):
                return True
            if tool_name == "Read" and clean_name in tool_input.get("file_path", ""):
                return True
        return False

    elif etype == "result":
        return False

    return None


# ---------------------------------------------------------------------------
# Core runner
# ---------------------------------------------------------------------------

def run_single_query(
    query: str,
    skill_name: str,
    skill_description: str,
    timeout: int,
    project_root: str,
    model: str | None = None,
    backend: str = "gemini",
) -> bool:
    """Run a single query and return whether the skill was triggered."""
    unique_id = uuid.uuid4().hex[:8]
    probe_name = f"eval-probe-{unique_id}"

    if backend == "gemini":
        reg_path = _register_skill_gemini(skill_name, skill_description, unique_id)
    else:
        reg_path = _register_skill_claude(skill_name, skill_description, unique_id, project_root)

    try:
        if backend == "gemini":
            cmd = [
                "gemini",
                "-p", query,
                "--output-format", "stream-json",
            ]
            if model:
                cmd.extend(["-m", model])
        else:
            cmd = [
                "claude",
                "-p", query,
                "--output-format", "stream-json",
                "--verbose",
                "--include-partial-messages",
            ]
            if model:
                cmd.extend(["--model", model])

        # Remove env vars that block nesting
        env = {k: v for k, v in os.environ.items() if k not in ("CLAUDECODE", "GEMINI_CLI")}

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=project_root,
            env=env,
        )

        triggered = False
        start_time = time.time()
        buffer = ""
        claude_state = {}  # For Claude's stateful stream parsing

        try:
            while time.time() - start_time < timeout:
                if process.poll() is not None:
                    remaining = process.stdout.read()
                    if remaining:
                        buffer += remaining.decode("utf-8", errors="replace")
                    break

                ready, _, _ = select.select([process.stdout], [], [], 1.0)
                if not ready:
                    continue

                chunk = os.read(process.stdout.fileno(), 8192)
                if not chunk:
                    break
                buffer += chunk.decode("utf-8", errors="replace")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    if backend == "gemini":
                        result = _check_triggered_gemini(event, probe_name)
                    else:
                        result = _check_triggered_claude(event, probe_name, claude_state)

                    if result is True:
                        return True
                    if result is False:
                        return False
        finally:
            if process.poll() is None:
                process.kill()
                process.wait()

        return triggered
    finally:
        _cleanup_skill(reg_path, backend)


def run_eval(
    eval_set: list[dict],
    skill_name: str,
    description: str,
    num_workers: int,
    timeout: int,
    project_root: Path,
    runs_per_query: int = 1,
    trigger_threshold: float = 0.5,
    model: str | None = None,
    backend: str = "gemini",
) -> dict:
    """Run the full eval set and return results."""
    results = []

    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        future_to_info = {}
        for item in eval_set:
            for run_idx in range(runs_per_query):
                future = executor.submit(
                    run_single_query,
                    item["query"],
                    skill_name,
                    description,
                    timeout,
                    str(project_root),
                    model,
                    backend,
                )
                future_to_info[future] = (item, run_idx)

        query_triggers: dict[str, list[bool]] = {}
        query_items: dict[str, dict] = {}
        for future in as_completed(future_to_info):
            item, _ = future_to_info[future]
            query = item["query"]
            query_items[query] = item
            if query not in query_triggers:
                query_triggers[query] = []
            try:
                query_triggers[query].append(future.result())
            except Exception as e:
                print(f"Warning: query failed: {e}", file=sys.stderr)
                query_triggers[query].append(False)

    for query, triggers in query_triggers.items():
        item = query_items[query]
        trigger_rate = sum(triggers) / len(triggers)
        should_trigger = item["should_trigger"]
        if should_trigger:
            did_pass = trigger_rate >= trigger_threshold
        else:
            did_pass = trigger_rate < trigger_threshold
        results.append({
            "query": query,
            "should_trigger": should_trigger,
            "trigger_rate": trigger_rate,
            "triggers": sum(triggers),
            "runs": len(triggers),
            "pass": did_pass,
        })

    passed = sum(1 for r in results if r["pass"])
    total = len(results)

    return {
        "skill_name": skill_name,
        "description": description,
        "results": results,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": total - passed,
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Run trigger evaluation for a skill description")
    parser.add_argument("--eval-set", required=True, help="Path to eval set JSON file")
    parser.add_argument("--skill-path", required=True, help="Path to skill directory")
    parser.add_argument("--description", default=None, help="Override description to test")
    parser.add_argument("--num-workers", type=int, default=10, help="Number of parallel workers")
    parser.add_argument("--timeout", type=int, default=30, help="Timeout per query in seconds")
    parser.add_argument("--runs-per-query", type=int, default=3, help="Number of runs per query")
    parser.add_argument("--trigger-threshold", type=float, default=0.5, help="Trigger rate threshold")
    parser.add_argument("--model", default=None, help="Model to use (e.g. gemini-2.5-flash)")
    parser.add_argument("--backend", default=None, choices=["gemini", "claude"], help="CLI backend (auto-detected if omitted)")
    parser.add_argument("--verbose", action="store_true", help="Print progress to stderr")
    args = parser.parse_args()

    eval_set = json.loads(Path(args.eval_set).read_text())
    skill_path = Path(args.skill_path)

    if not (skill_path / "SKILL.md").exists():
        print(f"Error: No SKILL.md found at {skill_path}", file=sys.stderr)
        sys.exit(1)

    backend = args.backend or _detect_backend()
    name, original_description, content = parse_skill_md(skill_path)
    description = args.description or original_description
    project_root = find_project_root()

    if args.verbose:
        print(f"Backend: {backend}", file=sys.stderr)
        print(f"Evaluating: {description}", file=sys.stderr)

    output = run_eval(
        eval_set=eval_set,
        skill_name=name,
        description=description,
        num_workers=args.num_workers,
        timeout=args.timeout,
        project_root=project_root,
        runs_per_query=args.runs_per_query,
        trigger_threshold=args.trigger_threshold,
        model=args.model,
        backend=backend,
    )

    if args.verbose:
        summary = output["summary"]
        print(f"Results: {summary['passed']}/{summary['total']} passed", file=sys.stderr)
        for r in output["results"]:
            status = "PASS" if r["pass"] else "FAIL"
            rate_str = f"{r['triggers']}/{r['runs']}"
            print(f"  [{status}] rate={rate_str} expected={r['should_trigger']}: {r['query'][:70]}", file=sys.stderr)

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
