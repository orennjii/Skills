---
name: package-management
description: 包管理工具选择与使用规范。当用户需要新建项目、安装/移除/升级依赖、通过包管理器运行命令、创建虚拟环境、或初始化项目脚手架时，必须查阅此 skill 以确定正确的工具和命令。即使用户直接写出 pip install、npm install、npx、yarn add 等传统命令，也应查阅此 skill —— 用户有明确的工具偏好（Python 用 uv，JS/TS 用 pnpm），需要将这些命令替换为对应的现代工具等价命令。覆盖 Python、JavaScript/TypeScript、Rust 生态。
---

# Package Management Standards

用户在本地开发环境中对包管理工具有明确偏好。这些偏好的核心原因是：统一工具链以降低认知负担，并利用现代工具的性能优势（如 uv 比 pip 快 10-100x，pnpm 通过硬链接节省磁盘空间）。

## 判断使用哪个工具

**已有项目**：检查仓库中的锁文件来判断，按以下优先级识别：

| 锁文件              | 对应工具 |
| ------------------- | -------- |
| `uv.lock`           | uv       |
| `pnpm-lock.yaml`    | pnpm     |
| `Cargo.lock`        | cargo    |
| `poetry.lock`       | poetry   |
| `package-lock.json` | npm      |
| `yarn.lock`         | yarn     |

沿用项目已有的工具，不要擅自切换。

**新建项目**：使用下表中的指定工具，未经用户同意不要使用替代方案。

| 语言                    | 指定工具 | 禁止使用           |
| ----------------------- | -------- | ------------------ |
| Python                  | `uv`     | pip, conda, poetry |
| JavaScript / TypeScript | `pnpm`   | npm, yarn          |
| Rust                    | `cargo`  | —                  |

## 命令映射

模型在生成命令时容易回退到传统工具的习惯写法，以下是等价命令的对照：

### Python: uv 替代 pip

| 意图             | 正确                           | 错误                               |
| ---------------- | ------------------------------ | ---------------------------------- |
| 初始化项目       | `uv init`                      | 手动创建 `pyproject.toml`          |
| 初始化库         | `uv init --lib`                | —                                  |
| 添加依赖         | `uv add <pkg>`                 | `pip install <pkg>`                |
| 添加开发依赖     | `uv add --dev <pkg>`           | `pip install <pkg>`                |
| 移除依赖         | `uv remove <pkg>`              | `pip uninstall <pkg>`              |
| 同步/安装所有依赖 | `uv sync`                      | `pip install -r requirements.txt`  |
| 运行脚本         | `uv run python script.py`      | `python script.py`                 |
| 运行项目命令     | `uv run <cmd>`                 | 先激活 venv 再运行                  |
| 创建虚拟环境     | `uv venv`                      | `python -m venv .venv`             |

uv 自动管理虚拟环境，一般不需手动 `uv venv` 后再激活。直接 `uv run` 即可。

### JavaScript/TypeScript: pnpm 替代 npm

| 意图             | 正确                       | 错误                     |
| ---------------- | -------------------------- | ------------------------ |
| 安装所有依赖     | `pnpm install`             | `npm install`            |
| 添加依赖         | `pnpm add <pkg>`           | `npm install <pkg>`      |
| 添加开发依赖     | `pnpm add -D <pkg>`        | `npm install -D <pkg>`   |
| 移除依赖         | `pnpm remove <pkg>`        | `npm uninstall <pkg>`    |
| 运行脚本         | `pnpm run <script>`        | `npm run <script>`       |
| 执行一次性包     | `pnpm dlx <pkg>`           | `npx <pkg>`              |
| 脚手架初始化     | `pnpm create <template>`   | `npm create <template>`  |

### Rust

Rust 生态统一使用 `cargo`，无需映射。
