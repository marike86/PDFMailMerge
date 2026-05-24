# 纯脚本版本 - 快速开始指南

## ⏱️ 5分钟快速上手

本指南将帮助您在5分钟内完成PDF邮件合并工具的配置和使用。

---

## 第一步：环境检查

### 检查Python是否安装

```bash
# 打开命令行，输入：
python --version

# 预期输出：Python 3.8.0 或更高版本
# 如果显示"不是内部命令"，请先安装Python
```

### 安装Python（如果未安装）

1. 访问 https://www.python.org/downloads/
2. 下载Python 3.8或更高版本
3. 运行安装程序
4. **重要**：勾选"Add Python to PATH"
5. 点击"Install Now"

---

## 第二步：安装依赖

### Windows系统

```bash
# 1. 进入项目目录
cd pdf-mail-merge-script

# 2. 运行安装脚本
scripts\install_deps.bat

# 3. 等待安装完成（约2-3分钟）
```

### Linux/macOS系统

```bash
# 1. 进入项目目录
cd pdf-mail-merge-script

# 2. 添加执行权限
chmod +x scripts/*.sh

# 3. 运行安装脚本
./scripts/install_deps.sh

# 4. 等待安装完成
```

### 手动安装（如自动安装失败）

```bash
# 逐个安装依赖
pip install pypdf>=3.0.0
pip install pandas>=1.5.0
pip install Jinja2>=3.0.0
pip install chardet>=4.0.0
pip install openpyxl>=3.0.0

# 验证安装
python -c "import pypdf, pandas, jinja2, chardet, openpyxl; print('All OK')"
```

---

## 第三步：准备文件

### 创建PDF模板

#### 方式1：表单模式模板

```
1. 使用Adobe Acrobat打开或创建PDF
2. 选择"工具" → "准备表单"
3. 添加表单控件（文本框、下拉框等）
4. 为每个控件命名（与数据列名对应）
5. 保存为 template_form.pdf

示例控件命名：
- name（姓名）
- email（邮箱）
- company（公司）
- position（职位）
```

#### 方式2：文本模式模板

```
1. 使用Word或其他编辑器创建文档
2. 在需要替换的位置输入占位符：
   {{name}}
   {{email}}
   {{company}}
   {{position}}
3. 保存为PDF格式：template_text.pdf

示例内容：
姓名: {{name}}
邮箱: {{email}}
公司: {{company}}
职位: {{position}}
```

### 创建数据文件

#### CSV格式（推荐）

```csv
# 保存为 data.csv（UTF-8编码）
name,email,company,position
张三,zhangsan@example.com,百度,软件工程师
李四,lisi@example.com,阿里巴巴,产品经理
王五,wangwu@example.com,腾讯,前端开发
```

#### Excel格式

| name | email | company | position |
|------|-------|---------|----------|
| 张三 | zhangsan@example.com | 百度 | 软件工程师 |
| 李四 | lisi@example.com | 阿里巴巴 | 产品经理 |

**注意**：保存为.xlsx格式，第一行为列标题。

---

## 第四步：执行合并

### 基本命令

```bash
# 进入项目目录
cd pdf-mail-merge-script

# 执行合并（将template.pdf和data.csv替换为您的文件）
python -m src.cli --template template.pdf --data data.csv --output ./output

# 查看输出
dir output
```

### 指定模式

```bash
# 表单模式
python -m src.cli --template template_form.pdf --data data.csv --output ./output --mode form

# 文本模式
python -m src.cli --template template_text.pdf --data data.csv --output ./output --mode text
```

### 自定义文件名

```bash
# 使用数据字段命名
python -m src.cli --template template.pdf --data data.csv --output ./output --name "{name}_{row}"

# 使用行号命名
python -m src.cli --template template.pdf --data data.csv --output ./output --name "document_{row}"
```

---

## 第五步：验证结果

### 检查输出文件

```bash
# Windows
dir output

# Linux/macOS
ls output/
```

### 预期输出

```
output/
├── 张三_1.pdf
├── 李四_2.pdf
├── 王五_3.pdf
└── 赵六_4.pdf
```

### 打开PDF验证

1. 进入output目录
2. 双击打开生成的PDF文件
3. 确认数据已正确填充

---

## 常见问题快速解决

| 问题 | 快速解决 |
|------|----------|
| Python未找到 | 重新安装Python，勾选"Add to PATH" |
| 依赖安装失败 | 手动逐个安装依赖 |
| 文件找不到 | 使用绝对路径或检查文件名 |
| 中文乱码 | 将CSV保存为UTF-8编码 |
| PDF无法打开 | 重新生成模板PDF |

---

## 示例命令集合

### 示例1：基础操作

```bash
# 最简单命令
python -m src.cli -t template.pdf -d data.csv

# 指定输出目录
python -m src.cli --template template.pdf --data data.csv --output ./my_output
```

### 示例2：完整命令

```bash
python -m src.cli \
  --template employee_card.pdf \
  --data employees.csv \
  --output ./cards \
  --mode form \
  --name "card_{employee_id}" \
  --zip \
  --verbose
```

### 示例3：仅验证配置

```bash
python -m src.cli --template template.pdf --data data.csv --validate-only
```

---

## 性能参考

| 数据量 | 预计时间 | 说明 |
|--------|---------|------|
| 10条 | 3-5秒 | 快速测试 |
| 50条 | 15-20秒 | 常规批量 |
| 100条 | 30-60秒 | 大量处理 |
| 500条 | 2-5分钟 | 超大批量 |

---

## 下一步

- 查看 [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md) 了解完整命令
- 查看 [TROUBLESHOOTING.md](TROUBLESHOOTING.md) 解决遇到的问题
- 查看 [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md) 自定义开发

---

**快速参考**：
- 命令帮助：`python -m src.cli --help`
- 验证环境：`scripts\validate_env.bat`（Windows）或 `./scripts/validate_env.sh`（Linux/macOS）
- 运行测试：`scripts\run_tests.bat`（Windows）或 `./scripts/run_tests.sh`（Linux/macOS）