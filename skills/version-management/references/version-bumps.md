# Version Bumps

在用户问“这个应该发 major、minor 还是 patch”时读取本文件。

## Goal

基于 semantic versioning 判断改动的发布级别，并解释为什么。

## Decision rules

- `major`: 有破坏性变更、API 不兼容、配置迁移、行为默认值改变
- `minor`: 向后兼容的新功能
- `patch`: 向后兼容的修复、文档改进、小优化
- `no release`: 不值得单独发版的内部调整，除非团队流程要求

如果同时存在多类变化，按影响级别最高的那个判断。

## Output pattern

```text
Recommended bump:
`<major|minor|patch|no release>`

Reason:
- <影响范围>
- <为什么这属于这个级别>
```

## Example

Input:
这次发布删除了旧配置字段，并要求用户改用新的 `auth.strategy` 配置格式。

Output:

```text
Recommended bump:
`major`

Reason:
- 配置格式发生不兼容变化
- 现有用户升级后需要调整配置，属于破坏性变更
```
