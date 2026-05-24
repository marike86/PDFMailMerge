# 纯脚本版本 - 命令行完整参考

## 📖 目录

1. [命令语法](#一命令语法)
2. [必选参数](#二必选参数)
3. [可选参数](#三可选参数)
4. [使用示例](#四使用示例)
5. [高级用法](#五高级用法)
6. [退出代码](#六退出代码)

---

## 一、命令语法

### 基本语法

```bash
python -m src.cli [OPTIONS]

# 或使用python直接运行
python src/cli.py [OPTIONS]

# 或使用快捷脚本（Windows）
run_merge.bat -t template.pdf -d data.csv

# 或使用快捷脚本（Linux/macOS）
./run_merge.sh -t template.pdf -d data.csv
```

### 多行命令

```bash
# Windows PowerShell
python -m src.cli `
  --template template.pdf `
  --data data.csv `
  --output ./output

# Linux/macOS
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output
```

---

## 二、必选参数

### `--template`, `-t`

**说明**：PDF模板文件路径

**语法**：
```bash
--template <file_path>
-t <file_path>
```

**示例**：
```bash
# 相对路径
--template template.pdf

# 绝对路径
--template c:\Users\marike\Desktop\pdf\template.pdf
--template /home/user/pdf/template.pdf

# 带空格路径
--template "c:\Program Files\template.pdf"
```

---

### `--data`, `-d`

**说明**：数据源文件路径（CSV/Excel/JSON）

**语法**：
```bash
--data <file_path>
-d <file_path>
```

**示例**：
```bash
# CSV文件
--data data.csv

# Excel文件
--data employees.xlsx

# JSON文件
--data records.json

# 绝对路径
--data c:\Users\marike\Desktop\pdf\data.csv
```

---

## 三、可选参数

### `--output`, `-o`

**说明**：输出目录路径

**默认值**：./output

**示例**：
```bash
# 默认输出到./output
--output ./output

# 自定义目录
--output ./my_pdfs

# 绝对路径
--output c:\Users\marike\Desktop\output

# 使用时间戳创建目录
--output ./output_$(date +%Y%m%d)
```

---

### `--mode`, `-m`

**说明**：处理模式

**可选值**：
- `form`：PDF表单填充模式
- `text`：文本替换模式
- `auto`：自动检测模式（默认）

**示例**：
```bash
# 自动检测
--mode auto

# 表单模式
--mode form

# 文本模式
--mode text
```

**自动检测规则**：
```
1. 如果PDF包含表单域 → 使用form模式
2. 如果PDF包含{{placeholder}} → 使用text模式
3. 如果都无法检测 → 报错退出
```

---

### `--name`, `-n`

**说明**：输出文件命名规则

**默认值**：document_{row}

**可用占位符**：
| 占位符 | 说明 | 示例输出 |
|--------|------|----------|
| `{row}` | 行号（从1开始） | 1, 2, 3, ... |
| `{field}` | 数据列名 | name列的值 |
| `{timestamp}` | 时间戳 | 20240101_120000 |

**示例**：
```bash
# 使用行号
--name "document_{row}"
# 输出：document_1.pdf, document_2.pdf, ...

# 使用单个字段
--name "{name}"
# 输出：张三.pdf, 李四.pdf, ...

# 使用多个字段
--name "{company}_{name}"
# 输出：百度_张三.pdf, 阿里巴巴_李四.pdf

# 组合使用
--name "{company}_{name}_{row}"
# 输出：百度_张三_1.pdf, 阿里巴巴_李四_2.pdf

# 使用时间戳
--name "merge_{timestamp}"
# 输出：merge_20240101_120000.pdf
```

**文件名安全处理**：
```bash
# 非法字符自动替换为下划线
/ \ : * ? " < > | → _
```

---

### `--zip`

**说明**：生成ZIP压缩包

**默认值**：不生成ZIP

**示例**：
```bash
# 生成ZIP
--zip

# 输出：
# output/
# ├── 张三.pdf
# ├── 李四.pdf
# └── pdf_mail_merge_20240101_120000.zip
```

---

### `--clean`

**说明**：处理前清空输出目录

**默认值**：不清空

**示例**：
```bash
# 清空输出目录
--clean

# 等同于：
# rm -rf ./output && mkdir ./output
```

---

### `--verbose`, `-v`

**说明**：显示详细输出

**默认值**：静默模式

**示例**：
```bash
# 启用详细输出
--verbose
-v

# 输出示例：
"""
PDF Mail Merge Tool
==================================================
Template: template.pdf
Data: data.csv
Output: ./output
Mode: auto

Loading data...
✓ Loaded 100 records from data.csv

Detecting template type...
✓ Detected form fields: name, email, company

Generating PDFs...
[████████████████████] 100/100 (100%) - 25.3s

Summary:
✓ Generated 100 PDFs
✓ Total time: 25.3s
"""
```

---

### `--validate-only`

**说明**：仅验证配置，不生成PDF

**默认值**：执行完整处理

**示例**：
```bash
# 验证配置
--validate-only

# 输出：
"""
Validation Results:
✓ Template file exists
✓ Data file exists and valid
✓ Template fields: name, email, company, position
✓ Data fields: name, email, company, position
✓ All fields matched
✓ Validation passed!
"""
```

---

### `--encoding`

**说明**：指定数据文件编码

**默认值**：自动检测

**示例**：
```bash
# 指定UTF-8编码
--encoding utf-8

# 指定GBK编码
--encoding gbk

# 指定GB18030编码
--encoding gb18030

# 自动检测（默认）
--encoding auto
```

---

### `--workers`

**说明**：并发处理线程数

**默认值**：CPU核心数

**示例**：
```bash
# 使用4个线程
--workers 4

# 使用8个线程
--workers 8

# 自动检测（默认）
--workers auto
```

---

### `--help`, `-h`

**说明**：显示帮助信息

**示例**：
```bash
# 显示帮助
--help
-h

# 输出完整帮助信息
```

---

## 四、使用示例

### 示例1：基础操作

```bash
# 最简命令
python -m src.cli -t template.pdf -d data.csv

# 指定输出目录
python -m src.cli --template template.pdf --data data.csv --output ./output

# 完整参数
python -m src.cli --template template.pdf --data data.csv --output ./output --mode auto --name "document_{row}"
```

---

### 示例2：表单模式

```bash
# 表单填充
python -m src.cli \
  --template employee_form.pdf \
  --data employees.csv \
  --output ./cards \
  --mode form \
  --name "card_{employee_id}"

# 带ZIP打包
python -m src.cli \
  --template employee_form.pdf \
  --data employees.csv \
  --output ./cards \
  --mode form \
  --zip
```

---

### 示例3：文本模式

```bash
# 文本替换
python -m src.cli \
  --template certificate.pdf \
  --data awards.xlsx \
  --output ./certificates \
  --mode text \
  --name "cert_{name}_{date}"

# 详细输出
python -m src.cli \
  --template certificate.pdf \
  --data awards.xlsx \
  --output ./certificates \
  --mode text \
  --verbose
```

---

### 示例4：验证配置

```bash
# 仅验证
python -m src.cli --template template.pdf --data data.csv --validate-only

# 验证并显示详情
python -m src.cli --template template.pdf --data data.csv --validate-only --verbose
```

---

### 示例5：批量处理

```bash
# 处理多个数据文件
python -m src.cli --template template.pdf --data batch1.csv --output ./batch1
python -m src.cli --template template.pdf --data batch2.csv --output ./batch2

# 清空并重新处理
python -m src.cli --template template.pdf --data data.csv --output ./output --clean --verbose
```

---

## 五、高级用法

### 5.1 环境变量配置

```bash
# 设置默认输出目录
export PDF_MERGE_OUTPUT="./my_output"

# 设置默认模式
export PDF_MERGE_MODE="form"

# 启用详细输出
export PDF_MERGE_VERBOSE="1"

# 设置并发数
export PDF_MERGE_WORKERS="4"

# Windows设置环境变量
set PDF_MERGE_OUTPUT=./my_output
```

### 5.2 配置文件

创建 `config/default_settings.json`：

```json
{
  "default_output": "./output",
  "default_mode": "auto",
  "naming_pattern": "document_{row}",
  "zip_enabled": false,
  "verbose": false,
  "max_workers": 4,
  "encoding": "auto",
  "clean_output": false
}
```

### 5.3 批处理脚本

创建 `batch_process.bat`（Windows）：

```batch
@echo off
for %%f in (data1.csv data2.csv data3.csv) do (
    python -m src.cli --template template.pdf --data %%f --output ./output --zip --verbose
)
```

创建 `batch_process.sh`（Linux/macOS）：

```bash
#!/bin/bash
for file in data1.csv data2.csv data3.csv; do
    python -m src.cli --template template.pdf --data "$file" --output ./output --zip --verbose
done
```

---

## 六、退出代码

| 退出码 | 含义 | 说明 |
|--------|------|------|
| `0` | 成功 | 所有PDF生成成功 |
| `1` | 部分失败 | 有错误但完成处理 |
| `2` | 参数错误 | 命令行参数无效 |
| `130` | 中断 | 用户按Ctrl+C取消 |

### 检查退出码

```bash
# Windows
python -m src.cli --template template.pdf --data data.csv
echo Exit code: %ERRORLEVEL%

# Linux/macOS
python -m src.cli --template template.pdf --data data.csv
echo "Exit code: $?"
```

---

## 快捷脚本

### Windows快捷脚本

创建 `run.bat`：

```batch
@echo off
python -m src.cli %*
```

使用：`run.bat -t template.pdf -d data.csv`

### Linux/macOS快捷脚本

创建 `run.sh`：

```bash
#!/bin/bash
python -m src.cli "$@"
```

使用：`./run.sh -t template.pdf -d data.csv`

---

**最后更新**：2026-05-18