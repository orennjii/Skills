---
name: oren-skill-creator
description: Guide for creating effective skills. Use this skill when users want to create a new skill, update an existing skill, or improve a skill's triggering, structure, workflow, scripts, references, or assets.
metadata:
  short-description: Create or update a skill
---

# Skill Creator

This skill provides guidance for creating effective skills and improving them through iteration.

At a high level, the process is straightforward.

- Decide what the skill should do and roughly how it should work
- Draft or update the skill
- Review it with the user
- Revise it based on feedback and real usage
- Repeat until the skill is useful and stable

Your job when using this skill is to figure out where the user is in that loop and help them move forward. If they already have a draft, skip straight to critique and revision. If they want to brainstorm informally, be flexible.

## About Skills

Skills are modular, self-contained folders that extend Agents's capabilities by providing specialized knowledge, workflows, and reusable resources. Think of them as onboarding guides for specific domains or recurring tasks.

In practice, a good skill usually provides four things.

1. Specialized workflows - Multi-step procedures for specific domains
2. Tool integrations - Instructions for working with specific file formats, systems, or APIs
3. Domain expertise - Company-specific knowledge, schemas, business rules, and conventions
4. Reusable resources - Scripts, references, and assets that help future runs avoid rediscovering the same context

<skill-types>
1. Technique: Concrete method with steps to follow (condition-based-waiting, root-cause-tracing)
2. Pattern: Way of thinking about problems (flatten-with-flags, test-invariants)
3. Reference: API docs, syntax guides, tool documentation (office docs)
</skill-types>

## When to Create a Skill

Create a skill when The technique isn't intuitively obvious to Agents, and Agents would struggle to infer it reliably on its own. If the task is simple and well-known, a skill may not be necessary. If the task is complex, domain-specific, or has a high cost of failure, a skill can provide valuable guidance and guardrails.

## Core Principles

Keep it concise. The context window is a public good. Skills share it with the system prompt, conversation history, other skills, and the user's request.

The most important part of a skill is the `description` field in the frontmatter. This is the primary trigger mechanism, so it must clearly describe when it should be used.

Assume Agents is already smart. Only include information it would not reliably infer on its own. Prefer concise examples over long explanations.

Match the degree of freedom to the task's fragility and variability.

- High freedom: Use text guidance when multiple approaches are valid
- Medium freedom: Use structured steps when a preferred pattern exists but context still matters
- Low freedom: Use tight instructions when consistency is critical and mistakes are costly

Think in terms of terrain. A narrow bridge needs guardrails. An open field does not.

Generalize instead of overfitting. A skill should work across many future prompts, not just the examples used during development. When feedback comes from one or two cases, look for the broader pattern before editing the skill.

Follow a principle of lack of surprise. Skills must not contain malware, exploit code, or misleading behavior. A skill's behavior should align with the user's stated intent and should not conceal risky or unauthorized actions.

## Anatomy of a Skill

Every skill consists of a required `SKILL.md` file and optional bundled resources.

```text
skill-name/
├── SKILL.md
├── agents/
│   └── openai.yaml # optional: user explicitly asks
└── Bundled Resources
    ├── scripts/
    ├── references/
    └── assets/
```

Every `SKILL.md` has two parts.

- Frontmatter (YAML): Include `name` and `description`. These fields are the primary trigger mechanism, so they must clearly describe both what the skill does and when it should be used.
- Body (Markdown): Instructions for how to use the skill after it has triggered.

`agents/openai.yaml` is optional and should only be created or updated if the user explicitly asks for OpenAI or Codex UI metadata, packaging metadata, or skill-list presentation details.

If that metadata is explicitly requested, do the following.

- Read `references/openai_yaml.md` first
- Create human-facing `display_name`, `short_description`, and `default_prompt` that match `SKILL.md`
- Use repository helpers if they exist; otherwise write or update the file manually
- Only include optional interface fields if the user explicitly provides them

Bundled resources are optional. `scripts/` is for executable helpers that benefit from determinism, reuse, or lower token cost.

- When to include: Repeated code generation, fragile transformations, file processing, API interactions, or any workflow that keeps getting re-implemented
- Benefits: Improves consistency, reduces prompt bloat, and avoids rewriting the same logic in every run
- Best practice: Include only scripts that materially improve repeatability or reliability
- Note: A created skill may include scripts even though this `skill-creator` skill does not rely on them for its own workflow

`references/` holds documentation and reference material that should be loaded as needed while the skill is being used.

- When to include: Repeatedly needed schemas, policies, API notes, workflows, domain knowledge, or examples
- Benefits: Keeps `SKILL.md` lean while preserving important context
- Best practice: If files are large, tell the reader when to open them and what to look for
- Avoid duplication: Put detailed reference material in `references/`, not both there and in `SKILL.md`

`assets/` holds files that are used in the output rather than read into context.

- When to include: Templates, images, icons, boilerplate projects, sample files, or brand materials
- Benefits: Separates reusable output materials from instructions and reference text

A skill should only contain files that directly support its function. Do not create extra process documentation such as the following.

- `README.md`
- `INSTALLATION_GUIDE.md`
- `QUICK_REFERENCE.md`
- `CHANGELOG.md`
- similar auxiliary files

## Progressive Disclosure Design Principle

Skills use a three-level loading system to manage context efficiently.

1. Metadata (`name` + `description`) - always in context
2. `SKILL.md` body - loaded when the skill triggers
3. Bundled resources - loaded only when needed

Keep `SKILL.md` focused and under roughly 500 lines when possible. When a skill supports multiple domains, frameworks, or variants, keep the main workflow in `SKILL.md` and move variant-specific detail into separate reference files.

Keep a few guidelines in mind.

- Keep references one level deep from `SKILL.md`
- Link to reference files directly from `SKILL.md`
- Add a table of contents to long reference files
- Organize reference files by domain or variant when that helps avoid loading irrelevant detail

## Skill Creation Process

Follow these steps in order unless there is a clear reason to skip one.

1. Capture intent with concrete examples
2. Plan reusable contents
3. Create or update the skill structure
4. Write or revise `SKILL.md`
5. Optionally create `agents/openai.yaml` if explicitly requested
6. Validate the skill
7. Iterate on real usage

For naming, use lowercase letters, digits, and hyphens only. Normalize user-provided titles to hyphen-case. Keep names short, descriptive, and aligned with the folder name.

Start with concrete examples and capture the intent clearly.

Start by understanding the user's intent. The current conversation may already contain the workflow the user wants to capture. Extract obvious facts from the conversation first: tools used, sequence of steps, corrections the user made, recurring inputs, and expected outputs.

Useful questions include the following.

1. What should this skill enable the agent to do?
2. When should this skill trigger?
3. What would a user say that should cause the skill to be used?
4. What output format or success criteria are expected?
5. What edge cases or failure modes matter?

Avoid asking too many questions at once. Start with the highest-value gaps and follow up as needed.

Conclude this step when there is a clear sense of the tasks, trigger conditions, and outputs the skill should support.

Then plan the reusable contents. To turn examples into a reusable skill, analyze each example in two passes.

1. Considering how to execute the task from scratch
2. Identifying what scripts, references, or assets would be useful when repeating that work

For example, a few common patterns are worth calling out.

- A `pdf-editor` skill may benefit from `scripts/` containing reliable file transformation helpers
- A `frontend-webapp-builder` skill may benefit from `assets/` containing starter templates or boilerplate projects
- A `brand-guidelines` skill may benefit from `assets/` containing logos, fonts, or presentation templates
- A `big-query` skill may benefit from `references/` documenting schemas, table meanings, or common query patterns

If the same operation keeps getting re-implemented, move it into `scripts/`. If the same background context keeps getting rediscovered, move it into `references/`. If the same output scaffold or template keeps getting recreated, move it into `assets/`.

Next, create or update the skill structure. If you are creating a new skill, create the folder named after the skill and add the minimum structure needed for the task.

If repository-specific helper tooling exists, you may use it when it is helpful. Do not make the workflow depend on helper tooling that may not exist in another environment.

When updating an existing skill, keep these constraints in mind.

- Preserve the existing name unless the user explicitly asks for a rename
- Work with the current structure unless there is a clear reason to reorganize it
- Keep bundled resources only if they still support the current workflow

Then write or revise `SKILL.md`. Remember that it is being created for another instance of Agents to use. Include procedural knowledge, domain detail, and workflow guidance that would genuinely help another agent succeed.

For frontmatter, write YAML with the following fields.

- `name`: The skill name
- `description`: The primary trigger mechanism for the skill

The description should do a few things well.

- Include both what the skill does and when it should be used
- Put all trigger information in the description, not in a later "when to use" section
- Be slightly pushy when useful so the skill does not under-trigger

Do not add extra frontmatter fields unless the environment explicitly requires them.

In the body, write instructions for how to use the skill and any bundled resources.

Prefer imperative phrasing in instructions.

Use explicit output templates when the output structure matters. Use examples when examples will teach a reusable pattern instead of a one-off case.

Explain why important instructions exist. Keep the prompt lean. Prefer general guidance that transfers across similar tasks over narrow rules tailored to one example.

Only create `agents/openai.yaml` when the user explicitly asks for it.

If asked, do the following.

- Align `agents/openai.yaml` with the final `SKILL.md`
- Keep the fields human-facing, concise, and consistent with the skill's actual scope
- Read `references/openai_yaml.md` before choosing values if that file exists
- Regenerate or rewrite the file when it becomes stale relative to `SKILL.md`

Before considering the skill done, validate it.

Check the following.

- Correct folder and name alignment
- Valid YAML frontmatter
- Required fields present
- A description that covers real trigger conditions
- Script, reference, and asset files that are actually used
- No dead links, stale placeholders, or contradictory instructions

If repository validators exist, run them. Otherwise, perform the checks manually.

After the skill is used on real tasks, look for places where it was unclear, too narrow, too verbose, or missing important context.

The iteration workflow is simple.

1. Use the skill on real tasks
2. Notice struggles, inefficiencies, or under-triggering
3. Update `SKILL.md` or bundled resources
4. Test again

## Improving the Skill

This is the heart of the loop. A first draft is rarely the final version. Use feedback and transcripts from real runs to make the skill better.

When improving the skill, keep four things in mind.

1. Generalize from the feedback. Do not overfit the skill to one example if the real issue is broader.
2. Keep the prompt lean. Remove instructions that do not change outcomes in a useful way.
3. Explain the why. The model will make better decisions when the reason behind a rule is clear.
4. Look for repeated missing context or repeated implementation work. If multiple runs need the same helper logic, schema, glossary, template, or policy, bundle it once as a script, reference, or asset instead of rebuilding it every time.

Take the time to think through the user's actual goal. A good revision is often less about adding more instructions and more about adding the right ones.

After improving the skill, do the following.

1. Apply the improvements
2. Ask the user for feedback
3. Read the feedback and improve the skill again

Keep going until one of two things is true.

- The user is satisfied
- Further edits are not producing meaningful gains

## Environment Notes

Adapt your workflow to the environment you are operating in.

Web-based environments may require more sequential work and lighter validation. Agentic IDEs and CLI environments may allow deeper inspection, parallel research, or helper tooling. Use those capabilities when they genuinely improve the skill, but keep the core workflow understandable without them.

## Reference Files

If this skill folder includes supporting references, use them intentionally.

- `references/openai_yaml.md` for `agents/openai.yaml` field definitions and constraints
- `references/anthropic_best_practices.md` the SOTA for skills design released by Anthropic
- `agents/` files only when building a skill that genuinely needs multi-agent instructions

The core loop remains the same.

- Figure out what the skill is about
- Draft or edit the skill
- Review it with the user
- Improve it based on feedback and usage
- Repeat until it is actually useful

## Tone and Formatting

The contents in SKILL.md must follow this instruction set for tone and formatting. This is important to ensure that skills are consistently clear, concise, and easy to use.

Keep formatting simple and low-friction. Favor plain paragraphs, short lists, and direct examples. Avoid heavy scaffolding, excessive hierarchy, and template-like transitions. The document should feel like clear working guidance, not a formal handbook.

Prefer natural prose over rigid document structure. Use `##` headings to separate major sections when they genuinely improve navigation. Do not use `###` or deeper heading levels. When a subsection distinction is important enough to call out, use an XML tag like `<section>` or a semantically named tag to group the content — but apply this sparingly, only when the distinction genuinely aids navigation. Do not replace every removed heading with a label-like line ending in a colon. If a short sentence can introduce the next idea, prefer that.

Use the simplest syntax that preserves clarity. Bold only what demands immediate attention; italics only for terms or citations. Both should be rare. Avoid decorative phrasing, redundant labels, and mechanical patterns such as repeated "X:" lead-ins. Lists should be introduced naturally and only when they actually improve readability.

When a concept can be made concrete with a single example, skip the abstract explanation and give the example directly.Keep the tone concise, direct, and technical. Optimize for flow, readability, and decision quality. Avoid filler transitions like "In summary", "It is worth noting", or "To conclude". If a paragraph exceeds five sentences, consider whether it can be split or cut. The writing should feel calm, deliberate, and pragmatic.
