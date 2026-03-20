# Codex Context Files

这份 reference 只整理 OpenAI 官方公开材料里与 `AGENTS.md` 和 `AGENTS.override.md` 直接相关的规则和做法。只要对作用域、优先级、发现顺序或最新产品行为有疑问，就应重新打开官方页面确认，而不是把这份摘要当成最终规范。

官方来源：

- [Custom instructions with AGENTS.md](https://developers.openai.com/codex/guides/agents-md)
- [Introducing Codex](https://openai.com/index/introducing-codex/)
- [Harness engineering: leveraging Codex in an agent-first world](https://openai.com/index/harness-engineering)

当前公开材料里最关键的规则如下。

`AGENTS.md` 是 Codex 的项目指令文件，`AGENTS.override.md` 是同目录下优先级更高的覆盖文件。Codex 不会任意遍历仓库外目录。当前官方文档描述的发现范围是：先看全局 Codex home，再看 project root 到当前工作目录之间的各级目录；如果找不到 project root，则只看当前工作目录。

对最终会触碰到的每个文件，都必须遵守所有作用域覆盖该文件的指令文件。更深层目录中的文件在冲突时优先。同一目录内，优先顺序是 `AGENTS.override.md`，然后是 `AGENTS.md`。官方还允许在同一层级配置 fallback 文件名，但默认情况下可以先按这两个名字理解。直接的 system、developer、user 指令仍然优先于这些文件。

官方当前文档强调的是“每个目录最多取一个指令文件”。如果同一目录同时存在 `AGENTS.override.md` 和 `AGENTS.md`，前者会遮蔽后者；不要把它们当成同层合并加载。

如果 `AGENTS.md` 里写了程序化检查，官方系统消息要求在完成改动后运行这些检查，并尽力确认通过。这个要求不只适用于代码改动，文档改动也一样。

对这个 skill 来说，默认做法应是先判断目标作用域目录，再在那个目录找现有的 `AGENTS.override.md` 或 `AGENTS.md`。已有就优先更新现有文件；没有再创建新的。不要把 Codex 的模型写成“永远只在仓库根目录有一份 `AGENTS.md`”。

如果用户明确说要写覆盖文件、临时覆盖、局部覆盖，或仓库里该目录已经存在 `AGENTS.override.md`，优先沿用 override 文件。否则默认仍以 `AGENTS.md` 作为主路径。

OpenAI 近期公开的工程实践也给了一个重要方向：不要把 `AGENTS.md` 写成一份冗长百科全书。更合适的做法是让它保持简短、像目录或地图，把更深层的事实放进 `docs/` 或其他更稳定的真相来源中，再从 `AGENTS.md` 指过去。

因此，当用户让你为 Codex 写上下文时，应优先把 `AGENTS.md` 或 `AGENTS.override.md` 当成入口页：写清目录结构、关键命令、验证方式、作用域边界，以及应该继续去哪里读更细的资料。只有那些必须常驻上下文的约定，才直接写进指令文件。

目前没有查到 OpenAI 官方公开的 `AGENTS.local.md` 一类配套变体。除非仓库自身已经在用其他命名，否则不要为 Codex 主动扩展到未有官方依据的文件名。

如果后续 OpenAI 发布了新的 Codex 文档、AGENTS 规范页面或产品设置页，应优先以更新后的官方页面为准，并回写这份 reference。
