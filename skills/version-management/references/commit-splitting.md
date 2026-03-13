# Commit Splitting

在用户问“这些改动该怎么拆 commit”或“要不要拆开提交”时读取本文件。

## Goal

把混合改动拆成更容易审阅、更容易回滚、更容易理解的提交边界，同时避免为了形式而过度切碎。

## How to decide boundaries

优先按“目的”拆分，而不是按文件类型拆分。

常见可单独成组的主题：

- 新功能
- 缺陷修复
- 重构
- 测试补充
- 文档更新
- 构建 / CI / 依赖调整

## Good split heuristics

- 一组改动应该能用一句清晰的话概括
- 评审某一组时，最好不需要同时理解另一组
- 回滚某一组时，不应破坏另外一组的意图
- 如果测试只验证某个功能组，通常可以和功能一起提交，或单独成组；关键是说明理由

## When not to split

以下情况不应硬拆：

- 实现和必要测试强耦合，分开会让任一提交都不完整
- API 变更与调用方适配必须同时出现
- 迁移脚本和被迁移结构必须保持原子性

## Output pattern

```text
Recommended split:
1. <group name>
   Files/area: <范围>
   Commit: <suggested title>
   Why: <为什么单独成组>
```

## Example

Input:
用户同时改了导出命令、CLI 测试和 README，想知道要不要拆 commit。

Output:

```text
Recommended split:
1. Export command
   Files/area: CLI implementation
   Commit: feat(cli): add bulk export command for skills
   Why: 这是独立的新能力

2. Test coverage
   Files/area: CLI tests
   Commit: test(cli): cover bulk export command
   Why: 测试可以独立审阅

3. Documentation
   Files/area: README
   Commit: docs: document bulk export workflow
   Why: 文档不应和功能实现混在一起
```
