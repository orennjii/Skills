# Claude Code Context Files

这份 reference 只整理 Claude Code 当前官方文档里与上下文文件直接相关的规则。它不是官方文档的替代品。只要遇到下面这些情况，就应重新打开官方页面确认最新规范：

- 要决定 `CLAUDE.md` 的放置位置、优先级或继承关系
- 要使用 `.claude/rules/`、`@import`、`claudeMdExcludes`、`--add-dir`
- 仓库里已经有 `CLAUDE.md`、`.claude/CLAUDE.md`、托管策略或其他非典型布局
- 发现现有项目行为和这份摘要不一致

官方来源：

- [How Claude remembers your project](https://code.claude.com/docs/en/memory)
- [Claude Code settings](https://code.claude.com/docs/en/settings)

当前官方文档中最稳定、最值得优先依赖的信息如下。

项目级共享上下文文件的主路径是 `./CLAUDE.md` 或 `./.claude/CLAUDE.md`。用户级文件是 `~/.claude/CLAUDE.md`。组织级托管文件由系统或管理员下发，不是这个 skill 的默认输出目标。当前官方文档没有把 `CLAUDE.local.md` 列为主路径之一。

Claude Code 会在启动时完整读取当前工作目录及祖先目录中的 `CLAUDE.md`。子目录中的 `CLAUDE.md` 不会在启动时全部读入，而是在 Claude 读取该子目录文件时按需加载。更具体的位置优先级高于更宽泛的位置。

如果项目级文件已经存在，优先更新现有位置，不要无理由同时维护 `./CLAUDE.md` 和 `./.claude/CLAUDE.md` 两份主文件。根目录文件适合放全局规则，子目录文件适合放局部规则。

当规则开始变多时，不要继续把所有内容塞进单个 `CLAUDE.md`。官方更推荐两种拆分方式：

- 用 `@path/to/file` 导入其他 Markdown 文件
- 用 `.claude/rules/` 按主题或按路径拆分规则

`.claude/rules/` 适合更大项目。没有 `paths` frontmatter 的规则会像 `.claude/CLAUDE.md` 一样无条件加载；有 `paths` frontmatter 的规则只会在 Claude 处理匹配文件时触发。这是写路径特定规则时比继续嵌套 `CLAUDE.md` 更直接的机制。

如果仓库是大型 monorepo，祖先目录或其他团队目录中的 `CLAUDE.md` 可能会被带进来。官方文档建议用 `claudeMdExcludes` 排除不相关的 `CLAUDE.md`，而不是在项目里再写一层互相抵消的说明。

如果通过 `--add-dir` 暴露了额外目录，默认不会一起加载这些目录中的 `CLAUDE.md`。只有显式启用相应环境变量时，额外目录里的 `CLAUDE.md`、`.claude/CLAUDE.md`、`.claude/rules/*.md` 才会被纳入。

不共享的个人偏好更适合放在 `~/.claude/CLAUDE.md`、导入的个人文件，或 `.claude/settings.local.json` 这类本地配置中，而不是默认新建另一份项目级主文件。

关于 `CLAUDE.local.md`：如果仓库已经在用它，先把它视为项目历史兼容约定并核对仓库自身说明。若没有现成约定，不要把它当成 Claude Code 当前官方主流程的一部分。
