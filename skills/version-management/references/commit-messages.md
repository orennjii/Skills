# Commit Messages

在用户要提交说明时读取本文件。

## Goal

把代码变更转成清晰、可信、可直接使用的 commit message。重点是概括这次提交为什么存在，而不是机械复述文件改动。

## Core rules

- 优先描述行为变化、功能变化、修复内容、开发流程变化
- 不要只列文件名
- 如果改动混合多个主题，先指出建议拆分，再给当前最合理的一条 message
- 用祈使式、现在时
- 第一行尽量不超过 72 个字符
- 不要以句号结尾
- 优先写结果与影响，而不是过程动作
- 避免 `update files`、`misc fixes`、`change stuff` 这类空话
- 能具体说明修了什么，就不要退化成 `chore`

## Conventional commit types

如果项目已经有既定风格，优先沿用；否则默认采用 Conventional Commits。

| Type | 适用场景 |
| --- | --- |
| `feat` | 新功能、面向用户的新能力 |
| `fix` | 缺陷修复、错误处理修正 |
| `refactor` | 代码结构调整，但外部行为基本不变 |
| `perf` | 性能优化 |
| `docs` | 文档更新 |
| `test` | 测试补充或修正 |
| `build` | 构建、依赖、打包配置变化 |
| `ci` | CI/CD 流程变更 |
| `chore` | 杂项维护，且不适合更具体类型时 |
| `revert` | 回滚已有提交 |

## Scope rules

- scope 只在它真的有助于定位模块时才加
- 优先使用稳定模块名，例如 `auth`、`api`、`ui`、`release`
- 不要为了凑格式强行添加 scope

## Output patterns

### Recommended single-line commit

```text
Recommended:
`<type>(<scope>): <subject>`

Why:
- <一句话解释为什么这个标题抓住了主要改动>
```

### Full commit message

```text
<type>(<scope>): <subject>

- <补充点 1>
- <补充点 2>
```

只有在以下情况添加 body：

- 用户明确要求完整 commit message
- 改动跨多个层面，单行标题不足以说明
- 存在迁移、兼容性或风险提示，需要补充背景

## Language

- 优先跟随仓库已有提交语言
- 如果仓库历史不明显，跟随用户当前语言
- 如果用户没指定、仓库也没有明显偏好，默认英文标题

## Examples

**Example 1**

Input:
用户修复了 token 过期后刷新失败，影响登录态续期。

Output:

```text
Recommended:
`fix(auth): handle token refresh failures gracefully`

Why:
- 主题聚焦在登录态续期失败这个用户可感知的问题，而不是实现细节
```

**Example 2**

Input:
只是把 package management skill 的说明写得更清楚，没有行为变化。

Output:

```text
Recommended:
`docs(package-management): clarify package tool selection rules`

Why:
- 这是文档层面的澄清，不应误写成 feat 或 refactor
```
