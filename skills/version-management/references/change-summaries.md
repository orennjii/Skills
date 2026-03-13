# Change Summaries

在用户想“总结这次改动”而不是直接要 commit / PR 文案时读取本文件。

## Goal

把 diff 或用户描述转成 2-5 个容易理解的要点，让用户或评审先快速看懂发生了什么。

## Core rules

- 先写用户能感知到的变化，再写实现细节
- 不要按文件名列清单，除非用户明确要求
- 同时存在 staged 与 unstaged 变化时，要明确区分
- 如果改动范围混杂，先按主题归类，再提炼要点
- 如果信息不足，只总结能确定的部分

## Default output

```text
Summary:
- <change 1>
- <change 2>
- <change 3>
```

## When to be more explicit

以下场景要额外加一句说明：

- 只基于 staged 变化总结
- 只基于用户口头描述总结
- 当前 working tree 里混有多个不相关主题

## Example

Input:
“别写 commit message，也先别写 PR。你就帮我把这次改动总结成 4 条以内的人话：我重构了导出模块、修了一个重试死循环、顺手清理了几处过时配置。”

Output:

```text
Summary:
- 重构了导出模块，整理了相关代码结构
- 修复了失败重试可能陷入死循环的问题
- 清理了几处过时配置，减少后续维护负担
```
