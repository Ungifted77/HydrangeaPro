# HydrangeaPro

根据repo：https://github.com/ecnusse/Hydrangea/blob/main/defect.csv  复现这些bug，并检查这个缺陷库后改正错误并且尝试新加内容后，使用完善的Hydrangea库所搭建的一个命令行工具，可以在命令行中查询相关缺陷的内容。
---
根目录trans.py是我做的excel转yaml工具，下载下来后把第7行

```PTHTON
    INPUT_FILE = "defect_analysis_603-891.xlsx"
```
改成自己的那个excel文件即可

转好的db文件夹替换到hydrangea-cli/db就行，现在这个文件夹里的是我的excel部分转出来的yaml文件

---

目标：

| 命令 | 作用 | 说明 |
| --- | --- | --- |
| `apps` | 列出所有应用 | 可加 `--llm GPT-4` / `--vdb chroma` 过滤 |
| `bids` | 列出所有缺陷 ID | 等价于 Defects4J 的 bug id 列表 |
| `info <app> <bid>` | 打印缺陷元数据 | 包含 repo、commit、类型、后果、源位置、触发用例 |
| `test <app> <bid> [--trigger]` | 显示触发用例 | **这里不执行**，只打印 `trigger_tests` 字段 |

已经完成了apps bids info test

需要继续完成内部readme的书写

命令行工具的安装和使用看hydrangea-cli/README.md