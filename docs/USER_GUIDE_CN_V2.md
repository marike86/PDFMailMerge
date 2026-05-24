# PDF邮件合并工具 - 完整分步用户指南

## 📖 目录

1. [软件概述](#一软件概述)
2. [技术要求](#二技术要求)
3. [模板PDF文件规范](#三模板pdf文件规范)
4. [数据源文件规范](#四数据源文件规范)
5. [安装与配置](#五安装与配置)
6. [分步操作流程](#六分步操作流程)
7. [高级功能使用](#七高级功能使用)
8. [命令行详解](#八命令行详解)
9. [常见问题与解决](#九常见问题与解决)
10. [技术规格附录](#十技术规格附录)

---

## 一、软件概述

### 1.1 核心定位

PDF邮件合并工具是一款**完全离线的批量PDF生成工具**，专注于帮助用户从PDF模板和数据源快速批量生成个性化PDF文档。

**重要声明**：本工具**无需联网、无需注册账户、无需登录**，所有操作均在本地完成，数据完全私密。

### 1.2 主要功能

| 功能 | 说明 | 适用场景 |
|------|------|----------|
| 表单填充 | 填充PDF表单域 | 员工信息卡、申请表、调查问卷 |
| 文本替换 | 替换{{placeholder}}占位符 | 证书、邀请函、合同模板 |
| 批量生成 | 一次处理多条数据 | 批量制作、邮件合并 |
| ZIP打包 | 自动压缩输出文件 | 方便分享和传输 |

### 1.3 核心优势

- ✅ **零配置**：下载即用，无需注册账号
- ✅ **完全离线**：所有数据本地处理，无隐私风险
- ✅ **跨平台**：Windows/macOS/Linux全支持
- ✅ **批量高效**：支持100+条数据批量处理
- ✅ **智能检测**：自动识别PDF模板类型和数据编码

---

## 二、技术要求

### 2.1 系统环境要求

#### 操作系统

| 操作系统 | 最低版本 | 推荐版本 |
|---------|---------|---------|
| Windows | Windows 7 (64位) | Windows 10/11 (64位) |
| macOS | macOS 10.13 | macOS 11+ |
| Linux | Ubuntu 18.04 | Ubuntu 20.04+ / CentOS 7+ |

#### 硬件要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| CPU | 双核2GHz | 四核3GHz+ |
| 内存 | 4GB | 8GB+ |
| 硬盘空间 | 200MB | 500MB SSD |
| 显示器 | 1024x768 | 1920x1080 |

#### Python环境

```bash
# 必须安装Python 3.8或更高版本
python --version
# 输出示例：Python 3.10.11
```

### 2.2 软件依赖清单

```bash
# 核心依赖（必须安装）
pypdf>=3.0.0        # PDF表单处理库
pandas>=1.5.0       # 数据处理库
Jinja2>=3.0.0       # 模板引擎
chardet>=4.0.0      # 编码自动检测
openpyxl>=3.0.0     # Excel文件支持

# 可选依赖（增强功能）
PyMuPDF>=1.23.0     # 文本替换增强
```

### 2.3 性能指标

| 指标 | 数值 | 说明 |
|------|------|------|
| 处理速度 | 100条/60秒 | 标准配置下测试结果 |
| 最大并发 | 50进程 | 多核CPU并行处理 |
| 最大数据量 | 10,000条 | 单批次处理上限 |
| 最大模板 | 50MB | PDF文件大小限制 |
| 最大数据文件 | 20MB | CSV文件大小限制 |

### 2.4 文件格式支持

| 类型 | 格式 | 最大大小 | 编码支持 |
|------|------|---------|---------|
| PDF模板 | .pdf (1.4-1.7) | 50MB | - |
| CSV数据 | .csv | 20MB | UTF-8/GBK/GB18030 |
| Excel数据 | .xlsx/.xls | 10MB | - |
| JSON数据 | .json | 5MB | UTF-8 |

---

## 三、模板PDF文件规范

### 3.1 文件格式要求

#### 基础规范

| 属性 | 要求 | 说明 |
|------|------|------|
| 文件格式 | PDF 1.4-1.7 | 推荐使用PDF 1.6 |
| 文件大小 | ≤50MB | 超过可能影响性能 |
| 页面尺寸 | A4/Letter/自定义 | 推荐A4 (210×297mm) |
| 颜色模式 | RGB/CMYK | 建议使用RGB |
| 字体嵌入 | 必须 | 确保跨平台一致性 |

#### 字体嵌入要求

```
✅ 正确：所有字体嵌入PDF
❌ 错误：使用系统字体未嵌入
```

**为何必须嵌入字体？**
- 避免目标用户缺少字体导致乱码
- 确保中文字符正确显示
- 保持跨平台一致性

### 3.2 表单模式规范

#### 3.2.1 表单域创建流程

```
步骤1：准备PDF文件
  ↓
步骤2：使用Adobe Acrobat打开
  ↓
步骤3：选择"准备表单"工具
  ↓
步骤4：添加表单控件（文本框、下拉框、复选框等）
  ↓
步骤5：为每个控件命名（命名规则见下方）
  ↓
步骤6：保存模板文件
```

#### 3.2.2 表单域命名规则

```python
# 命名要求：
- 字符：仅限字母（a-z、A-Z）、数字（0-9）、下划线（_）
- 开头：必须以字母或下划线开头
- 长度：1-50个字符
- 大小写：区分（Name ≠ name）

# ✅ 正确示例：
name                    # 简单名称
email_address           # 带下划线
Company_Name_123        # 混合大小写
_position                # 以下划线开头

# ❌ 错误示例：
my email                # 包含空格
company-name            # 包含连字符
2nd_field               # 以数字开头
field/name              # 包含斜杠
```

#### 3.2.3 表单域类型支持

| 域类型 | 代码 | 支持情况 | 数据格式 |
|--------|------|---------|---------|
| 文本框 | TEXT | ✅ 完全支持 | 字符串 |
| 多行文本 | TEXTAREA | ✅ 完全支持 | 字符串（含换行） |
| 下拉框 | SELECT | ✅ 完全支持 | 选项值 |
| 复选框 | CHECKBOX | ✅ 完全支持 | true/false |
| 单选按钮 | RADIO | ✅ 完全支持 | 选项值 |
| 日期字段 | DATE | ✅ 完全支持 | YYYY-MM-DD |
| 数字字段 | NUMBER | ✅ 完全支持 | 整数或小数 |

#### 3.2.4 表单模板示例

```
┌─────────────────────────────────────────────┐
│                                             │
│            员工信息登记表                     │
│                                             │
│  姓名：[张三________________]  ← name       │
│                                             │
│  部门：[技术部______________]  ← department  │
│                                             │
│  工号：[EMP2024001__________]  ← employee_id│
│                                             │
│  入职日期：[2024-03-01________]  ← hire_date│
│                                             │
│  □ 转正员工  ■ 试用期员工  ← is_probationary│
│                                             │
└─────────────────────────────────────────────┘
```

### 3.3 文本替换模式规范

#### 3.3.1 占位符语法

```python
# 格式：{{field_name}}
# field_name：对应数据源的列名

# 占位符规则：
- 字符：字母、数字、下划线
- 区分大小写：{{Name}} ≠ {{name}}
- 无空格：{{ name }} 无效
- 成对使用：必须同时有{{和}}

# ✅ 正确示例：
{{name}}
{{email_address}}
{{Company_Name}}
{{position_123}}

# ❌ 错误示例：
{{ name }}          # 包含空格
{{my email}}         # 包含空格
{{company-address}} # 包含连字符
{{field}}extra       # 缺少闭合}}
```

#### 3.3.2 文本替换规则

```
基础规则：
1. 精确匹配：{{name}}会替换为数据中的name值
2. 大小写敏感：{{Name}}和{{name}}是不同的字段
3. 空白处理：数据为空时，替换为空字符串

高级规则（Jinja2语法）：
- 条件判断：{% if vip %}VIP客户{% endif %}
- 循环处理：{% for item in items %}{{item}}{% endfor %}
- 过滤器：{{name|upper}}（转为大写）
- 默认值：{{name|default('未知')}}
```

#### 3.3.3 文本模板示例

```
┌─────────────────────────────────────────────┐
│                                             │
│            员工信息卡                         │
│                                             │
│  姓名: {{name}}                             │
│  邮箱: {{email}}                            │
│  公司: {{company}}                          │
│  职位: {{position}}                         │
│  入职日期: {{start_date}}                    │
│                                             │
│  薪资范围: {{salary_range}}                  │
│  部门: {{department}}                       │
│                                             │
│  欢迎加入{{company}}！                      │
│                                             │
└─────────────────────────────────────────────┘
```

#### 3.3.4 复杂模板示例

```
┌─────────────────────────────────────────────┐
│                                             │
│  {{greeting}} {{name}}                      │
│                                             │
│  感谢您申请{{position}}职位，               │
│  您的申请编号：{{application_id}}            │
│                                             │
│  {% if is_onboarded %}                      │
│  您已于{{onboard_date}}入职                  │
│  {% else %}                                 │
│  请于{{expected_date}}完成入职手续           │
│  {% endif %}                                │
│                                             │
└─────────────────────────────────────────────┘
```

### 3.4 PDF模板制作工具推荐

| 工具 | 平台 | 费用 | 适合场景 |
|------|------|------|----------|
| Adobe Acrobat Pro | Windows/macOS | 付费 | 专业表单制作 |
| LibreOffice Draw | 全平台 | 免费 | 简单模板 |
| Inkscape | 全平台 | 免费 | 矢量图形模板 |
| PDF-XChange Editor | Windows | 免费/付费 | 轻量级编辑 |

---

## 四、数据源文件规范

### 4.1 CSV文件规范

#### 4.1.1 文件格式要求

| 属性 | 要求 | 说明 |
|------|------|------|
| 文件扩展名 | .csv | 必须 |
| 编码格式 | UTF-8（推荐）、GBK、GB18030 | 影响中文显示 |
| 分隔符 | 逗号（,）默认 | 可自定义 |
| 引号字符 | 双引号（"）或单引号（'） | 推荐双引号 |
| 行结束符 | Windows: CRLF / Unix: LF | 影响跨平台 |

#### 4.1.2 列命名规则

```python
# 命名要求：
- 字符：字母、数字、下划线
- 开头：以字母或下划线开头
- 长度：1-100个字符
- 唯一性：同一文件中列名不能重复

# ✅ 正确示例：
name
email_address
company_name
position_123

# ❌ 错误示例：
my email      # 包含空格
company-name  # 包含连字符
```

#### 4.1.3 数据类型支持

| 数据类型 | 示例 | 说明 |
|---------|------|------|
| 文本 | `张三` | 无长度限制 |
| 数字 | `25000`、`3.14` | 整数或浮点数 |
| 日期 | `2024-03-01`、`2024/3/1` | ISO格式优先 |
| 布尔 | `true`/`false`、`1`/`0` | 表单复选框 |
| 空值 | 空、`N/A`、`null` | 处理为空白 |

#### 4.1.4 CSV示例文件

```csv
name,email,company,position,salary,start_date,department
张三,zhangsan@example.com,百度,软件工程师,25000,2024-03-01,技术部
李四,lisi@example.com,阿里巴巴,产品经理,30000,2024-01-15,产品部
王五,wangwu@example.com,腾讯,前端开发,22000,2024-02-20,技术部
赵六,zhaoliu@example.com,字节跳动,数据分析师,28000,2024-04-10,数据部
```

### 4.2 Excel文件规范

#### 4.2.1 文件格式要求

| 属性 | 要求 | 说明 |
|------|------|------|
| 文件格式 | .xlsx（推荐）、.xls | 推荐.xlsx |
| 引擎 | openpyxl | Python库 |
| 工作表 | 第一个工作表（默认） | 可指定 |
| 最大行数 | 10,000 | 超出可能出错 |
| 最大列数 | 256 | Excel限制 |

#### 4.2.2 Excel示例数据

| name | email | company | position | salary | start_date |
|------|-------|---------|----------|--------|------------|
| 张三 | zhangsan@example.com | 百度 | 软件工程师 | 25000 | 2024-03-01 |
| 李四 | lisi@example.com | 阿里巴巴 | 产品经理 | 30000 | 2024-01-15 |
| 王五 | wangwu@example.com | 腾讯 | 前端开发 | 22000 | 2024-02-20 |
| 赵六 | zhaoliu@example.com | 字节跳动 | 数据分析师 | 28000 | 2024-04-10 |

**注意**：第一行为列标题（name、email等），从第二行开始为数据。

### 4.3 JSON文件规范

#### 4.3.1 文件格式要求

| 属性 | 要求 | 说明 |
|------|------|------|
| 文件格式 | .json | 必须 |
| 编码 | UTF-8 | 必须 |
| 结构 | JSON数组或包含data字段的对象 | 见下方示例 |

#### 4.3.2 JSON示例数据

```json
[
  {
    "name": "张三",
    "email": "zhangsan@example.com",
    "company": "百度",
    "position": "软件工程师",
    "salary": 25000,
    "start_date": "2024-03-01"
  },
  {
    "name": "李四",
    "email": "lisi@example.com",
    "company": "阿里巴巴",
    "position": "产品经理",
    "salary": 30000,
    "start_date": "2024-01-15"
  }
]
```

### 4.4 数据验证规则

```python
# 工具会自动执行以下验证：

1. 文件存在性检查
   - 验证文件路径是否正确
   - 验证文件是否可读

2. 文件格式验证
   - CSV: 检查扩展名和分隔符
   - Excel: 检查工作表是否为空
   - JSON: 验证JSON语法

3. 编码检测
   - 自动检测文件编码
   - 支持UTF-8、GBK、GB18030、Latin-1

4. 列名规范检查
   - 检查是否有非法字符
   - 检查是否重复

5. 数据完整性检查
   - 统计空值数量
   - 检查数据类型一致性

6. 字段映射验证
   - 检查模板字段是否都有对应数据
   - 列出未匹配的字段
```

---

## 五、安装与配置

### 5.1 环境检查

#### 步骤1：检查Python版本

```bash
# 在命令行中执行
python --version

# 预期输出：Python 3.8.0 或更高
# 如果显示"不是内部命令"，需要安装Python
```

#### 步骤2：检查pip可用性

```bash
# 检查pip是否已安装
pip --version

# 预期输出：pip 22.x.x from ... (python 3.x)
```

### 5.2 安装依赖

#### 方法1：自动安装（推荐）

```bash
# 1. 进入项目目录
cd c:\Users\marike\Desktop\pdf

# 2. 安装所有依赖
pip install -r requirements.txt

# 3. 验证安装
python -c "import pypdf, pandas, jinja2, chardet, openpyxl; print('All dependencies installed!')"
```

#### 方法2：手动安装

```bash
# 逐个安装依赖
pip install pypdf>=3.0.0
pip install pandas>=1.5.0
pip install Jinja2>=3.0.0
pip install chardet>=4.0.0
pip install openpyxl>=3.0.0

# （可选）安装PyMuPDF增强文本替换
pip install PyMuPDF>=1.23.0
```

### 5.3 目录结构

```
pdf-mail-merge/                    ← 项目根目录
│
├── src/                          ← 源代码目录（勿修改）
│   ├── __init__.py
│   ├── data_loader.py           ← 数据加载模块
│   ├── pdf_processor.py         ← PDF处理模块
│   ├── template_engine.py       ← 模板引擎
│   ├── cli.py                   ← 命令行入口
│   └── utils.py                 ← 工具函数
│
├── tests/                        ← 测试目录
│   ├── test_data_loader.py
│   ├── test_pdf_processor.py
│   └── test_template_engine.py
│
├── examples/                     ← 示例文件
│   ├── sample_data.csv          ← 示例数据
│   └── README.md
│
├── docs/                         ← 文档目录
│   ├── USER_GUIDE_CN.md         ← 用户指南
│   ├── QUICK_START_CN.md        ← 快速入门
│   └── CONTRIBUTING.md          ← 贡献指南
│
├── output/                       ← 输出目录（需手动创建）
│
├── template.pdf                  ← 您的PDF模板
├── data.csv                      ← 您的数据源
├── requirements.txt             ← 依赖清单
├── README.md                    ← 项目说明
└── LICENSE                      ← 开源协议
```

### 5.4 验证安装

#### 运行测试脚本

```bash
# 测试数据加载
python tests/test_data_loader.py

# 测试模板引擎
python tests/test_template_engine.py

# 测试PDF处理（需要准备模板文件）
python tests/test_pdf_processor.py
```

#### 检查CLI帮助

```bash
python -m src.cli --help

# 预期输出：完整的命令行参数说明
```

---

## 六、分步操作流程

### 6.1 流程概览图

```
┌─────────────────────────────────────────────────────────────┐
│                    PDF邮件合并操作流程                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  阶段1：准备工作                                              │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │  准备模板   │────▶│  准备数据   │                        │
│  │  (PDF文件)  │     │  (CSV/XLSX) │                        │
│  └─────────────┘     └─────────────┘                        │
│         │                   │                               │
│         └─────────┬─────────┘                               │
│                   ▼                                          │
│  阶段2：验证配置                                              │
│  ┌─────────────────────────────────────┐                    │
│  │  python -m src.cli --validate-only  │                    │
│  │  检查字段匹配、编码、数据完整性        │                    │
│  └─────────────────────────────────────┘                    │
│                   │                                          │
│                   ▼                                          │
│  阶段3：执行合并                                              │
│  ┌─────────────┐     ┌─────────────┐                        │
│  │  生成PDF    │────▶│  保存文件   │                        │
│  │  (批量处理) │     │  (输出目录) │                        │
│  └─────────────┘     └─────────────┘                        │
│                           │                                   │
│                           ▼                                  │
│  阶段4：完成输出                                              │
│  ┌─────────────────────────────────────┐                    │
│  │  输出PDF文件 / 打包ZIP（可选）        │                    │
│  └─────────────────────────────────────┘                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 6.2 详细操作步骤

#### 步骤1：准备PDF模板

**选择处理模式**：
- **表单模式**：PDF包含可填充的表单域
- **文本模式**：PDF包含`{{field_name}}`占位符

**操作指南**：

```
如果是表单模式：
1. 使用Adobe Acrobat打开PDF
2. 选择"工具" → "准备表单"
3. 添加文本框、下拉框等控件
4. 为每个控件命名（与数据列名对应）
5. 保存模板文件

如果是文本模式：
1. 在Word或其他编辑器中创建文档
2. 在需要替换的位置输入 {{字段名}}
3. 转换为PDF格式
```

#### 步骤2：准备数据源

**创建数据文件**（以CSV为例）：

```
1. 打开Excel或文本编辑器
2. 在第一行输入列标题（与模板字段对应）
3. 在后续行输入数据
4. 保存为CSV格式（UTF-8编码）
```

**示例CSV内容**：
```csv
name,email,company,position
张三,zhangsan@example.com,百度,软件工程师
李四,lisi@example.com,阿里巴巴,产品经理
```

#### 步骤3：验证配置

**执行验证命令**：
```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --validate-only
```

**预期输出**：
```
PDF Mail Merge Tool
==================================================
Loading data from: data.csv
Loaded 8 records

Processing mode: auto
Template fields: name, email, company, position
Data fields: name, email, company, position

Validation passed!
```

**如果出现警告**：
```
Field mapping issues:
  Template fields without data: [missing_field]
  Data fields not in template: [extra_field]

Continue anyway? (y/n):
```

- 输入`y`继续处理（未匹配字段留空）
- 输入`n`取消并修改数据

#### 步骤4：执行合并

**基本命令**：
```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output
```

**带参数命令**：
```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --mode auto \
  --name "{name}_{row}" \
  --zip \
  --verbose
```

#### 步骤5：检查输出

**查看生成的文件**：
```bash
# Windows
dir output

# Linux/macOS
ls output/
```

**预期输出**：
```
output/
├── 张三_1.pdf
├── 李四_2.pdf
├── 王五_3.pdf
├── ...
└── pdf_mail_merge_20240101_120000.zip  # 如果使用了--zip参数
```

### 6.3 操作示例

#### 示例1：生成员工信息卡

**场景**：为50名员工生成信息卡

**准备文件**：
1. `employee_card.pdf` - 员工信息卡模板（含表单域）
2. `employees.csv` - 员工数据

**执行命令**：
```bash
python -m src.cli \
  --template employee_card.pdf \
  --data employees.csv \
  --output ./employee_cards \
  --mode form \
  --name "card_{employee_id}" \
  --zip
```

**预期结果**：
- 生成50个PDF文件
- 命名为 `card_001.pdf`, `card_002.pdf`, ...
- 打包为 `pdf_mail_merge_YYYYMMDD_HHMMSS.zip`

#### 示例2：生成证书

**场景**：为培训学员生成结业证书

**准备文件**：
1. `certificate.pdf` - 证书模板（含文本占位符）
2. `trainees.xlsx` - 学员数据

**执行命令**：
```bash
python -m src.cli \
  --template certificate.pdf \
  --data trainees.xlsx \
  --output ./certificates \
  --mode text \
  --name "certificate_{name}_{date}"
```

**预期结果**：
- 生成证书PDF文件
- 命名为 `certificate_张三_2024-03-01.pdf`

---

## 七、高级功能使用

### 7.1 自定义命名规则

#### 基础命名

```bash
# 使用行号
--name "document_{row}"
# 输出：document_1.pdf, document_2.pdf, ...

# 使用数据字段
--name "{name}"
# 输出：张三.pdf, 李四.pdf, ...

# 组合使用
--name "{company}_{name}"
# 输出：百度_张三.pdf, 阿里巴巴_李四.pdf, ...
```

#### 占位符说明

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{row}` | 行号（从1开始） | 1, 2, 3, ... |
| `{field}` | 数据列名 | name, email, ... |
| `{timestamp}` | 时间戳 | 20240101_120000 |

#### 命名规则限制

```
文件名安全处理：
- 自动替换非法字符：/ \ : * ? " < > |
- 转换为下划线：file/name.pdf → file_name.pdf
- 长度限制：最大255字符
```

### 7.2 批量处理优化

#### 多核CPU利用

```bash
# 自动检测并使用多核
python -m src.cli --template template.pdf --data data.csv --output ./output
```

#### 进度显示

```
Processing: 10/100 [========>          ] 10% | Elapsed: 2.5s | ETA: 22.5s
Processing: 50/100 [===================>] 50% | Elapsed: 12.3s | ETA: 12.3s
Processing: 100/100 [===================] 100% | Elapsed: 24.7s | Finished!
```

### 7.3 ZIP打包功能

```bash
# 生成后自动打包
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --zip

# 输出文件：
# output/
# ├── 张三.pdf
# ├── 李四.pdf
# └── pdf_mail_merge_20240101_120000.zip
```

### 7.4 输出目录管理

```bash
# 方法1：每次清空输出目录
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --clean

# 方法2：保留历史文件
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output_$(date +%Y%m%d)
```

### 7.5 详细日志输出

```bash
# 显示完整处理信息
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --verbose
```

**verbose输出示例**：
```
PDF Mail Merge Tool
==================================================
Template: template.pdf
Data: data.csv
Output: ./output
Mode: auto

Loading data...
✓ Loaded 100 records from data.csv

Detecting template type...
✓ Detected form fields: name, email, company, position

Validating field mapping...
✓ All template fields matched with data

Generating PDFs...
[████████████████████] 100/100 (100%) - 25.3s

Output:
✓ Generated 100 PDFs
✓ Created ZIP archive: pdf_mail_merge_20240101_120000.zip
```

---

## 八、命令行详解

### 8.1 完整参数列表

```bash
python -m src.cli [OPTIONS]

# 必选参数
  --template, -t    PDF模板文件路径（必须）
  --data, -d        数据源文件路径（必须）

# 处理选项
  --output, -o      输出目录（默认：./output）
  --mode, -m        处理模式
                   ├─ form: 表单填充模式
                   ├─ text: 文本替换模式
                   └─ auto: 自动检测（默认）
  --name, -n        输出文件命名规则（默认：document_{row}）

# 功能选项
  --zip             生成ZIP压缩包
  --clean           处理前清空输出目录
  --verbose, -v     显示详细输出
  --validate-only   仅验证配置，不生成PDF

# 帮助信息
  --help, -h        显示帮助信息
```

### 8.2 命令示例

#### 示例1：基本使用

```bash
# 最简命令（需准备template.pdf和data.csv）
python -m src.cli -t template.pdf -d data.csv
```

#### 示例2：指定输出目录

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./my_output
```

#### 示例3：表单模式

```bash
python -m src.cli \
  --template form_template.pdf \
  --data employees.csv \
  --output ./output \
  --mode form
```

#### 示例4：文本模式

```bash
python -m src.cli \
  --template text_template.pdf \
  --data awards.xlsx \
  --output ./certificates \
  --mode text
```

#### 示例5：自定义命名

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --name "{company}_{name}_{row}"
```

#### 示例6：生成ZIP

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --zip
```

#### 示例7：验证配置

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --validate-only
```

#### 示例8：完整命令

```bash
python -m src.cli \
  --template employee_card.pdf \
  --data employees.csv \
  --output ./employee_cards \
  --mode form \
  --name "card_{employee_id}" \
  --zip \
  --clean \
  --verbose
```

### 8.3 退出代码

| 退出码 | 含义 | 说明 |
|--------|------|------|
| 0 | 成功 | 所有PDF生成成功 |
| 1 | 部分失败 | 有错误但完成处理 |
| 130 | 中断 | 用户按Ctrl+C取消 |

---

## 九、常见问题与解决

### 9.1 文件相关问题

#### Q1：文件找不到

**错误信息**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'template.pdf'
```

**解决方案**：
1. 检查文件路径是否正确
2. 使用绝对路径：`c:\Users\marike\Desktop\pdf\template.pdf`
3. 确认文件是否存在

#### Q2：CSV编码错误

**错误信息**：
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4 in position 0
```

**解决方案**：
1. 用Excel重新保存为UTF-8编码
2. 或使用其他工具转换编码
3. 工具会自动尝试GBK编码

#### Q3：文件格式不支持

**错误信息**：
```
DataLoadError: Unsupported file type: .txt
```

**解决方案**：
1. CSV文件保存为.csv扩展名
2. Excel文件保存为.xlsx扩展名
3. JSON文件保存为.json扩展名

### 9.2 模板相关问题

#### Q4：无表单域或占位符

**错误信息**：
```
Error: No form fields found in PDF template
Error: No text placeholders found in PDF template
```

**解决方案**：
1. 确认使用正确的模式（form/text）
2. 检查PDF是否包含表单域或占位符
3. 使用Adobe Acrobat检查PDF结构

#### Q5：字段不匹配

**错误信息**：
```
Warning: Template fields not found in data: [missing_field]
```

**解决方案**：
1. 检查数据文件列名
2. 确认与模板字段完全一致
3. 注意大小写敏感性

#### Q6：中文乱码

**症状**：PDF中的中文显示为方块或问号

**解决方案**：
1. 确保PDF使用嵌入字体
2. 检查数据文件编码是否为UTF-8
3. 使用支持中文的字体

### 9.3 处理相关问题

#### Q7：处理速度慢

**症状**：处理100条数据超过60秒

**解决方案**：
1. 升级到Python 3.10+
2. 减少PDF模板复杂度
3. 关闭杀毒软件实时监控
4. 使用SSD存储临时文件

#### Q8：内存不足

**症状**：处理大数据时崩溃

**解决方案**：
1. 分批处理数据（每次1000条）
2. 增加虚拟内存
3. 关闭其他程序释放内存

#### Q9：输出文件损坏

**症状**：生成的PDF无法打开

**解决方案**：
1. 检查模板PDF是否正常
2. 确保输出目录有写入权限
3. 关闭所有打开的PDF文件

### 9.4 错误代码速查

| 错误码 | 说明 | 快速解决 |
|--------|------|----------|
| E001 | 文件不存在 | 检查路径，重试 |
| E002 | 格式不支持 | 使用.csv/.xlsx/.json |
| E003 | 编码错误 | 保存为UTF-8编码 |
| E004 | 字段缺失 | 检查列名是否匹配 |
| E005 | 字段不匹配 | 确认大小写一致 |
| E006 | PDF损坏 | 重新生成模板 |
| E007 | 权限不足 | 以管理员运行 |
| E008 | 磁盘满 | 清理磁盘空间 |

---

## 十、技术规格附录

### 10.1 文件格式详细说明

#### PDF规范

```
格式：PDF 1.4 - PDF 1.7
版本兼容性：最佳兼容性PDF 1.6
压缩：推荐Flate压缩
加密：不支持（需先解密）
签名：不支持（需先移除签名）
```

#### CSV规范

```
编码优先级：UTF-8 > GBK > GB18030 > Latin-1
分隔符：逗号（,）标准
引号：双引号（"）标准
换行：Windows CRLF / Unix LF
BOM：可选（工具会自动处理）
```

#### Excel规范

```
格式：.xlsx优先（.xls兼容）
引擎：openpyxl
工作表：默认第一个
空单元格：处理为空字符串
日期格式：推荐ISO 8601
```

### 10.2 字段映射规则

```
匹配规则：
1. 精确匹配（区分大小写）
2. 空白处理（空数据→空字段）
3. 类型转换（数字字符串→数字）
4. 日期格式（多种格式→统一格式）

特殊处理：
- 下划线命名：name_field ↔ namefield
- 首字母大写：Name ↔ name（不匹配）
```

### 10.3 性能优化建议

```
1. 模板优化：
   - 减少页数（单页最佳）
   - 简化图形（矢量优先）
   - 嵌入字体（避免加载）

2. 数据优化：
   - 清理空行
   - 统一编码
   - 简化列名

3. 系统优化：
   - 关闭杀毒软件
   - 使用SSD
   - 充足的内存
```

### 10.4 兼容性矩阵

| Python版本 | Windows | macOS | Linux | 状态 |
|-----------|---------|-------|-------|------|
| 3.8 | ✅ | ✅ | ✅ | 支持 |
| 3.9 | ✅ | ✅ | ✅ | 支持 |
| 3.10 | ✅ | ✅ | ✅ | 推荐 |
| 3.11 | ✅ | ✅ | ✅ | 推荐 |
| 3.12 | ✅ | ✅ | ✅ | 测试中 |

---

**文档信息**：

- 版本：1.0.0
- 更新日期：2026-05-18
- 作者：PDF Mail Merge Team
- 许可证：MIT License

**重要声明**：
本工具为**完全离线软件**，**无需注册账户、无需联网登录**，所有数据处理均在本地完成，完全保护用户隐私。

---

**反馈渠道**：
如有问题或建议，请通过以下方式联系：
- GitHub Issues: https://github.com/yourusername/pdf-mail-merge/issues