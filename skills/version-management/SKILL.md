---
name: version-management
description: Git and version-control change analysis. Use this skill whenever the user asks for a commit message, wants to summarize `git diff` / staged changes, needs help deciding how to split work into commits, wants a PR title or PR summary, needs changelog or release-note wording from commits, asks whether a change is a major/minor/patch release, or shows repository changes and wants help describing them clearly. Also use it for requests like "帮我写 commit", "帮我整理这次改动", "这些改动该怎么拆 commit", "给我一个 PR 描述", or "这个应该 bump 哪个版本".
---

# Version Management

**核心目的：提供清晰、结构化的代码变更历史**

这个 skill 是版本控制相关任务的入口页。它负责先判断用户到底要什么，再加载对应的细分 reference，而不是把所有规则都塞进当前上下文。

## Compatibility

- Requires: `git`
- Optional context: staged diff, unstaged diff, recent commit history, tags, base branch commits

## Use this skill for

- 写 commit message
- 总结 staged / unstaged 改动
- 判断是否应该拆成多个 commit
- 写 PR title / summary / risks
- 写 changelog 或 release notes
- 判断 semantic version 应该 bump major / minor / patch

## Context collection

先收集最小必要上下文，再决定读哪个 reference。

1. 读取变更范围。
   - 先读 `git status --short`
   - 如果问题针对 staged 内容，读 `git diff --cached --stat` 和 `git diff --cached`
   - 如果问题针对 working tree，读 `git diff --stat` 和 `git diff`

2. 读取仓库风格。
   - 读 `git log -5 --oneline`
   - 如果用户问 PR、release 或版本问题，再视需要看某个 tag 之后的提交摘要

3. 判断用户意图，再按需加载 reference。

如果用户的请求跨多个目标，例如“先帮我拆 commit，再给 PR 描述”，按顺序读取相关文件，但仍然只读需要的那几份。

## General operating rules

- 优先描述行为变化、用户影响和评审价值，不要只列文件名
- 上下文不足时，先说明不确定点，不要编造不存在的改动
- commit、PR、release 文字优先跟随仓库已有语言风格；如果看不出来，再跟随用户语言
- 不要执行 `git commit`、`git tag` 或 `git push`，除非用户明确要求
- 不要混淆 staged 与 unstaged 范围；基于哪部分变更得出的结论，要说清楚

## Reference guide

- [commit-messages.md](references/commit-messages.md): commit 类型、scope、标题和 body 写法
- [change-summaries.md](references/change-summaries.md): diff summary 和 change summary 的组织方式
- [commit-splitting.md](references/commit-splitting.md): 如何判断提交边界、何时建议拆分
- [pr-and-release-notes.md](references/pr-and-release-notes.md): PR title、PR summary、risks、changelog、release notes
- [version-bumps.md](references/version-bumps.md): semantic version bump 判断标准
