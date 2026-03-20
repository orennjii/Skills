# Gemini CLI Context Files

这份 reference 只整理 Gemini CLI 官方文档里与上下文文件和 memory 直接相关的规则。只要对文件名、加载顺序、imports、`/memory` 命令或配置项有疑问，就应重新打开官方页面确认最新规范。

官方来源：

- [Gemini CLI configuration](https://geminicli.com/docs/reference/configuration/)
- [Provide context with GEMINI.md files](https://geminicli.com/docs/cli/gemini-md/)

当前官方文档里最关键的规则如下。

`GEMINI.md` 是默认上下文文件名，但不是硬编码唯一值。`context.fileName` 可以是单个字符串，也可以是字符串数组。给 Gemini CLI 写上下文前，先检查项目或用户配置是否已经指定了别的文件名；如果配置已经改成 `AGENTS.md`、`CONTEXT.md` 或多个文件名组合，就必须把这视为仓库事实。

Gemini CLI 的上下文是分层加载的。官方文档把它描述为全局文件、工作区与祖先目录文件、以及 JIT 子目录文件三层。更具体的文件会补充或覆盖更宽泛的文件。默认全局位置是 `~/.gemini/<configured-context-filename>`。

项目级和祖先级文件会从当前工作目录开始向上查找，直到 git 根目录或用户主目录。子目录上下文文件会在当前工作目录以下扫描；扫描深度默认上限是 200 个目录，可以通过 `context.discoveryMaxDirs` 调整。

如果项目把 `context.fileName` 配成数组，那么 Gemini CLI 会把这些名字都当成可加载的上下文文件名。不要把 Gemini 的模型硬写成“永远只有 `GEMINI.md`”。在这个 skill 里，Gemini 的文件名判断顺序应是：

1. 用户明确给出的文件名
2. 项目配置中的 `context.fileName`
3. 默认 `GEMINI.md`

Gemini CLI 支持在上下文文件里用 `@file.md` 导入其他 Markdown 文件，也支持通过 `/memory refresh` 重新扫描加载，通过 `/memory show` 查看当前实际生效的合并结果。如果对实际加载顺序、最终拼接结果或路径解析有疑问，直接让模型查 `/memory show` 和官方文档，不要凭猜测决定。

这意味着给 Gemini CLI 写上下文时，重点不是死记一个默认文件名，而是先确认配置，再确认层级，再决定根目录文件和子目录文件分别应该承担什么内容。

如果后续 Gemini CLI 官方文档更新了 `context.fileName`、加载顺序、imports 或 `/memory` 相关能力，应以新文档为准，并同步更新这份 reference。
