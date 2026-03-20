---
name: agent-context-writer
description: 为 Claude Code、Codex、Gemini CLI 等 coding agent 创建或更新项目级、目录级上下文文件。用户只要明确提到 `CLAUDE.md`、`.claude/CLAUDE.md`、`AGENTS.md`、`AGENTS.override.md`、`GEMINI.md`，或虽然没点名文件但明显是在要求“给 AI coding assistant 写 repo、模块、目录、子树的工作指引”，都应触发此 skill。也用于把 README、开发文档、仓库约定和已有上下文文件整理成适合分层加载的 agent context files。
---

# Agent Context Writer

为 coding agent 写上下文文件时，先判断目标工具、目标目录和输出方式。

## Use this skill for

- 新建或更新 `CLAUDE.md`、`.claude/CLAUDE.md`、`AGENTS.md`、`AGENTS.override.md`、`GEMINI.md`
- 为整个项目写 agent 上下文
- 为某个模块、目录、子树写局部上下文
- 把 README、贡献文档、脚本约定、CI 约定整理成 agent 可执行的说明
- 从已有上下文文件迁移到另一种工具的默认命名
- 规划根目录和关键子目录的多层上下文文件

像下面这类请求也应触发：

- “给这个项目写一份 AI coding assistant context”
- “帮我给 Codex / Claude Code / Gemini CLI 补一个项目指令文件”
- “给 `src/payments` / `apps/web` / `backend/auth` 写局部上下文”

## Working flow

先判断工具，再判断作用域，再判断是新建、更新，还是多层规划。

1. 判断目标工具。
   - 用户明确点名工具或文件名时，直接遵从
   - 用户只说“给 agent 写上下文”时，先从上下文推断；无法可靠判断时再追问

2. 判断目标目录。
   - 用户明确给目录时，直接使用该目录
   - 用户提到具体文件时，选最合适的模块边界目录，不要机械地只取文件所在目录
   - 用户说“整个项目”或 repo 级上下文时，默认根目录
   - 用户同时提到多个目录时，按“根目录 + 必要子树”规划

3. 判断输出方式。
   - 已有对应文件时优先更新
   - 同一作用域支持多个工具时，先提炼一份共享内容，再映射到对应文件名
   - 多层输出只在确实存在局部规则时再加子目录文件，不要为每个目录都写一份空泛说明

4. 收集事实。
   - 读 `README*`
   - 读已有上下文文件
   - 读目标目录相关的配置、脚本、测试和文档
   - 优先吸收仓库里已经明确写出的规范，不要自造流程

5. 读取 reference。
   - 目标是 Claude Code 时，读 [claude-code-context-files.md](references/claude-code-context-files.md)
   - 目标是 Codex 时，读 [codex-context-files.md](references/codex-context-files.md)
   - 目标是 Gemini CLI 时，读 [gemini-cli-context-files.md](references/gemini-cli-context-files.md)
   - 根目录任务再读 [root-context-template.md](references/root-context-template.md)
   - 子目录任务再读 [subtree-context-template.md](references/subtree-context-template.md)

先读工具 reference，再读内容模板。不要在根目录任务中加载子树模板，也不要在子树任务中加载根模板。

## Scope and layering

根目录文件负责项目定位、顶层结构、全局命令、全局验证方式、跨目录共享约定和高风险区域。子目录文件只写该子树内部的职责、局部命令、局部约定和局部禁区。

如果某条规则适用于整个仓库，放在根目录。只有当规则明显局限于某个子树时，才写进局部文件。局部文件不应大段重复根目录内容。

当用户是根据某个具体文件提出请求时，重点是为该文件所在模块写上下文，而不是围绕单个文件写一份过窄的说明。

## Updating existing files

更新时先保留仍然正确的仓库知识和用户偏好，再删除过期、重复、互相矛盾的内容。补齐缺失的命令、目录说明、验证方式和局部限制，但不要把已有内容机械改写成另一种口吻。

如果仓库里已经有多层上下文文件，要检查三件事：

- 根目录文件是否写了太多局部细节
- 子目录文件是否重复了上层内容
- 更深层文件是否只在自己的作用域内覆盖或补充规则

## Validation

完成后至少检查这些点：

- 目标工具与目标文件名匹配，除非用户明确指定了其他文件名
- 目标目录与用户意图或可推断作用域一致
- 根目录内容确实是全局上下文
- 子目录内容聚焦该子树，没有复述整份仓库介绍
- 文中的命令、路径、工具和验证方式确实存在于仓库，或能从配置可靠推断
- 多层文件之间没有互相冲突，也没有不必要的重复
