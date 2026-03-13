# PR And Release Notes

在用户要 PR title、PR summary、risks、changelog 或 release notes 时读取本文件。

## Goal

把代码改动整理成适合评审或发布沟通的文案。重点是帮助读者快速理解影响，而不是复读 diff。

## PR writing rules

- 标题要概括合并后产生的主要变化
- summary 用 2-4 条说明 reviewer 真正关心的内容
- 如果有明显风险、迁移要求、兼容性问题，单独列出
- 不要把纯内部小清理放在 summary 的第一位，除非那就是主要内容

## PR template

```text
Title:
<PR title>

Summary:
- <change 1>
- <change 2>

Risks:
- <risk or "None obvious">
```

## Changelog / release notes rules

- 只写值得对外说明的变化
- 内部重构、纯格式调整、机械性清理通常不应进入面向用户的 release notes，除非用户明确要求完整列出
- 以用户视角组织内容，不要按文件组织
- 如果同时有 breaking change 和小修复，breaking change 优先呈现

## Example

Input:
“帮我把这次改动整理成 PR 描述。主要内容是：给技能导出流程加了批量模式，补了失败重试逻辑，并且更新了 README。请给我一个标题、3 条 summary，再补一条风险提示。”

Output:

```text
Title:
Add bulk export mode with retry handling

Summary:
- 为技能导出流程增加批量模式
- 补充失败重试逻辑，降低批处理过程中断概率
- 更新 README，说明新的导出用法

Risks:
- 重试逻辑可能影响长批处理任务的总执行时间
```
