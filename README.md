# 🌸 Hydrangea CLI

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](https://github.com/XRain66/hydrangea-cli)

> 🚀 一个强大的命令行工具，用于查询和管理 Hydrangea 缺陷数据集

## 📖 项目简介

Hydrangea CLI 是基于 [Hydrangea 数据集](https://github.com/ecnusse/Hydrangea/blob/main/defect.csv) 构建的专业命令行工具。我们通过复现和验证原始缺陷库中的 bug，完善了数据集内容，并开发了这个便捷的 CLI 工具，让您能够轻松查询和管理 AI 应用缺陷信息。

### ✨ 主要特性

- 🔍 **智能查询**: 支持多维度过滤和搜索缺陷信息
- 📊 **丰富数据**: 包含完整的应用元数据和缺陷详情
- 🎯 **精确匹配**: 支持按应用、LLM、向量数据库等条件筛选
- 🧪 **测试支持**: 提供缺陷复现和测试信息
- 🚀 **高效便捷**: 简洁的命令行界面，快速获取所需信息

### 🎯 适用场景

- **AI 安全研究**: 分析 AI 应用中的常见缺陷模式
- **质量保证**: 在开发过程中参考已知缺陷案例
- **学术研究**: 为 AI 安全相关论文提供数据支持
- **开发调试**: 快速定位和复现特定类型的缺陷

---


## 📦 安装

### 环境要求

- Python 3.8+
- pip 包管理器

### 快速安装

```bash
# 克隆仓库
git clone https://github.com/Ungifted77/HydrangeaPro
cd hydrangea-cli

# 安装依赖
pip install -e .
```



---

## 🚀 使用方法

### 📋 目录

- [命令概览](#-命令概览)
- [apps 指令](#1-apps指令列出应用)
- [bids 指令](#2-bids指令列出缺陷id)
- [info 指令](#3-info指令查看缺陷详细信息)
- [test 指令](#4-test指令显示测试信息)

### 🎯 命令概览

| 命令 | 功能描述 | 主要参数 |
|------|----------|----------|
| `apps` | 📱 列出所有应用，支持多维度过滤 | `--classification`, `--llm`, `--vdb`, `--language`等 |
| `bids` | 🐛 列出所有缺陷ID，支持按应用过滤 | `--app` |
| `info` | 📊 显示特定缺陷的元数据信息 | `app`, `bid` |
| `test` | 🧪 显示测试信息（仅打印，不执行） | `app`, `bid`, `--trigger` |

### 📁 数据格式

- **应用数据**: 存储在 `application.csv` 文件中
- **缺陷数据**: 存储在 `db/` 目录下的 YAML 文件中

---

## 1. 📱 apps指令——列出应用

### 基础用法

```bash
# 列出所有应用
hydrangea apps

# 查看详细帮助信息
hydrangea apps --help
```

### 🔍 过滤选项

#### 1.1 🏷️ 按分类过滤应用

```bash
hydrangea apps --classification chatbot
```

#### 1.2 🤖 按LLM过滤应用

```bash
hydrangea apps --llm OpenAI
```

#### 1.3 🌐 按LLM部署环境过滤应用

```bash
hydrangea apps --llm-deployment online
```

#### 1.4 🗄️ 按向量数据库过滤应用

```bash
hydrangea apps --vdb chroma
```

#### 1.5 💻 按向量数据库部署环境过滤应用

```bash
hydrangea apps --vdb-deployment local
```

#### 1.6 ⛓️ 按LangChain过滤应用

```bash
hydrangea apps --langchain 1
```

#### 1.7 💻 按编程语言过滤应用

```bash
hydrangea apps --language python
```

#### 1.8 🎯 组合过滤

```bash
# 多条件组合查询
hydrangea apps --llm OpenAI --vdb chroma --language python
hydrangea apps --classification chatbot --llm-deployment online --langchain 1
```

---

## 2. 🐛 bids指令——列出缺陷ID

### 基础用法

```bash
# 列出所有缺陷ID
hydrangea bids
```

### 🔍 按应用过滤缺陷ID

```bash
# 列出指定应用的所有缺陷ID
hydrangea bids --app LocaLAGI
```

> 💡 **提示**: 应用名称支持模糊匹配，会列出所有名字包含指定关键词的应用的缺陷ID

---

## 3. 📊 info指令——查看缺陷详细信息

### 基础用法

```bash
# 查看特定缺陷的详细信息
hydrangea info "camel" camel-ai-camel-privacy_violation-/
hydrangea info MEMGPT cpacker-MemGPT-exceeding_llm_content_limit-case1
```

### 📋 输出信息包括

- 缺陷类型
- 应用基本信息
- 缺陷描述和影响
- 缺陷源码位置


---

## 4. 🧪 test指令——显示测试信息
### 📝 参数说明

| 参数 | 类型 | 描述 |
|------|------|------|
| `app` | 必需 | 应用名称 |
| `bid` | 必需 | 缺陷ID |
| `--trigger` | 可选 | 显示详细触发测试信息 |

### 🚀 使用示例

```bash
# 显示基本测试信息
hydrangea test camel camel-ai-camel-privacy_violation-/

# 显示详细触发测试
hydrangea test camel camel-ai-camel-privacy_violation-/ --trigger
```

### 📤 输出示例

#### 🔸 基本模式输出

```bash
Test information for camel - camel-ai-camel-privacy_violation-/
Defect type: privacy violation
Case: /
Use --trigger to see detailed trigger tests
```

#### 🔸 触发测试模式输出

```bash
trigger_tests:
- 1.Set up Camel: Ensure the project is correctly set up in your local environment.
2.Configure Roles: Set up a role-playing scenario where one agent has restricted privileges (e.g., "Guest User") and another has administrative privileges.
3.Define Security Boundaries: Establish clear system message constraints about access permissions.
4.Execute Test: Initiate conversation where the restricted role attempts to access privileged operations.
5.Observe Behavior: Monitor if the AI system properly enforces access controls or inadvertently reveals sensitive information.
```

---

## 🤝 贡献指南

我们欢迎社区贡献！如果您想为 Hydrangea CLI 做出贡献，请：

1. 🍴 Fork 本仓库
2. 🌿 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 💾 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 📤 推送到分支 (`git push origin feature/AmazingFeature`)
5. 🔄 创建 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢

- 感谢 [Hydrangea 数据集](https://github.com/ecnusse/Hydrangea) 提供的基础数据
- 感谢所有贡献者和用户的支持

---

<div align="center">

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**

Made with ❤️ by [Ungifted77](https://github.com/Ungifted77/HydrangeaPro),[Evensunnn](https://github.com/Evensunnn),[SunsetB612](https://github.com/SunsetB612)

</div>
