# 一、Hydrangea CLI

Hydrangea CLI 是一个命令行工具，用于查询和管理 Hydrangea 数据集。

==此处再详细介绍一下这个项目内容==

---


# 二、安装

```bash
pip install -e .
```

# 三、使用方法

## 1.列出应用

```bash
hydrangea apps
```
详细内容可以在命令行中输入
```bash
hydrangea apps --help
```
查看分类以输出想要查看的软件类型，以下也进行罗列：

### 1.1 按分类过滤应用

```bash
hydrangea apps --classification chatbot
```


### 1.2 按LLM过滤应用

```bash
hydrangea apps --llm OpenAI
```

### 1.3 按LLM部署环境过滤应用

```bash
hydrangea apps --llm-deployment online
```

### 1.4 按向量数据库过滤应用

```bash
hydrangea apps --vdb chroma
```

### 1.5 按向量数据库部署环境过滤应用

```bash
hydrangea apps --vdb-deployment local
```

### 1.6 按LangChain过滤应用

```bash
hydrangea apps --langchain 1
```

### 1.7 按编程语言过滤应用

```bash
hydrangea apps --language python
```

### 1.8 组合过滤

```bash
hydrangea apps --llm OpenAI --vdb chroma --language python
hydrangea apps --classification chatbot --llm-deployment online --langchain 1
```

---

## 2. 列出缺陷ID

```bash
hydrangea bids
```

### 按应用过滤缺陷ID

```bash
hydrangea bids --app LocaLAGI
```

### 查看缺陷详细信息

```bash
hydrangea info LocaLAGI LocaLAGI-Loop-case1
```

### 显示测试信息

```bash
hydrangea test -w ./work --trigger
```

## 命令说明

- `apps`: 列出所有应用，支持按LLM和向量数据库过滤
- `bids`: 列出所有缺陷ID，支持按应用过滤
- `info`: 显示特定缺陷的元数据信息
- `test`: 显示测试信息（仅打印，不执行）

## 数据格式

应用数据存储在 `application.csv` 文件中，缺陷数据存储在 `db/` 目录下的 YAML 文件中。
