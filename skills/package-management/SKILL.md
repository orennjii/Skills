---
name: package-management
description: 包管理工具选择标准与使用规范。涉及新建项目、安装依赖、运行脚本等包管理操作时必须查阅。
---

# Package Management Standards

## General Principles

1. **已有项目**：沿用项目现有的包管理工具；以仓库中的**锁文件与 CI 使用的命令**为准，禁止擅自切换。
2. **新建项目**：按下表选择指定工具；未经用户同意禁止使用替代方案。
3. **模板优先**：初始化优先使用官方脚手架（如 `pnpm create vite`、`uv init --lib`、`cargo new`），避免手动配置。

## Language-Specific Tools

| 语言                    | 指定工具 | 用途                     | 禁止使用           |
| ----------------------- | -------- | ------------------------ | ------------------ |
| Python                  | `uv`     | 依赖管理、虚拟环境、运行 | pip, conda, poetry |
| JavaScript / TypeScript | `pnpm`   | 包管理                   | npm, yarn          |
| Rust                    | `cargo`  | 依赖管理、构建           | —                  |
