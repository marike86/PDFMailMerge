# PDF邮件合并工具 - 完整用户指南

## 📖 目录

1. [软件简介](#软件简介)
2. [技术要求](#技术要求)
3. [模板PDF文件规范](#模板pdf文件规范)
4. [数据源文件规范](#数据源文件规范)
5. [安装与配置](#安装与配置)
6. [核心功能操作](#核心功能操作)
7. [命令行使用](#命令行使用)
8. [常见问题与解决方案](#常见问题与解决方案)

---

## 一、软件简介

PDF邮件合并工具是一款**离线批量PDF生成工具**，无需联网，无需注册账户。

### 核心功能

- ✅ **双模式处理**：支持表单填充和文本替换两种PDF处理模式
- ✅ **多数据源支持**：CSV、Excel、JSON格式
- ✅ **批量生成**：一次处理上百条数据
- ✅ **跨平台运行**：Windows、macOS、Linux
- ✅ **自动编码检测**：智能识别文件编码，避免中文乱码

### 应用场景

- 📄 生成个性化证书、邀请函
- 📋 批量制作员工工牌、名片
- 📊 创建定制化报告、发票
- 💌 制作个性化邮件附件

---

## 二、技术要求

### 2.1 系统要求

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 7+ / macOS 10.13+ / Ubuntu 18.04+ | Windows 10+ / macOS 11+ |
| 内存 | 4GB | 8GB+ |
| 硬盘空间 | 200MB | 500MB+ |
| Python版本 | 3.8+ | 3.10+ |

### 2.2 软件依赖

```bash
pypdf>=3.0.0        # PDF表单处理
pandas>=1.5.0       # 数据处理
Jinja2>=3.0.0       # 模板引擎
chardet>=4.0.0      # 编码检测
openpyxl>=3.0.0     # Excel支持
PyMuPDF>=1.23.0     # 文本替换（可选）
```

### 2.3 性能指标

- 处理100条数据：< 60秒
- 最大并发处理：50个PDF
- 支持最大数据量：10,000条
- 最大模板文件：50MB

---

## 三、模板PDF文件规范

### 3.1 文件格式要求

| 属性 | 规范 |
|------|------|
| 文件格式 | PDF（推荐1.4-1.7版本） |
| 文件大小 | 最大50MB |
| 页面尺寸 | A4、Letter或自定义 |
| 颜色模式 | RGB或CMYK |
| 字体嵌入 | 建议嵌入，避免字体缺失 |

### 3.2 表单模式要求

#### 字段命名规范

```python
# 字段名称必须符合以下规则：
- 仅包含字母、数字、下划线
- 以字母或下划线开头
- 长度：1-50个字符
- 区分大小写（Name ≠ name）

# 正确示例：
name
email_address
Company_Name_123
_position

# 错误示例：
my email        # 包含空格
company-name    # 包含连字符
2nd_field       # 以数字开头
```

#### 字段类型支持

| 字段类型 | 支持情况 | 说明 |
|---------|---------|------|
| 文本框 | ✅ 完全支持 | 单行或多行文本 |
| 下拉框 | ✅ 完全支持 | 选择预定义选项 |
| 复选框 | ✅ 完全支持 | 是/否布尔值 |
| 单选按钮 | ✅ 完全支持 | 互斥选项 |
| 日期字段 | ✅ 完全支持 | 格式需符合数据源 |

### 3.3 文本替换模式要求

#### 占位符语法

```python
# 占位符格式：{{field_name}}
# field_name：数据源中的列名（不含空格）

# 正确示例：
{{name}}
{{email}}
{{company_name}}
{{position_123}}

# 错误示例：
{{ name }}           # 包含空格
{{my email}}          # 包含空格
{{company-address}}  # 包含连字符
```

#### 文本替换规则

- 占位符区分大小写：`{{Name}}` ≠ `{{name}}`
- 支持嵌套替换：`{{greeting}} {{name}}`
- 支持条件判断：`{% if VIP %}VIP客户{% endif %}`
- 支持循环处理：`{% for item in items %}{{item}}{% endfor %}`

### 3.4 PDF模板示例

#### 示例1：表单PDF

```
┌─────────────────────────────────┐
│  员工信息卡                      │
│                                 │
│  姓名：[张三] ← 表单域 name      │
│  邮箱：[zhangsan@example.com]   │
│  公司：[百度] ← 表单域 company   │
│  职位：[软件工程师]             │
│                                 │
└─────────────────────────────────┘
```

#### 示例2：文本PDF

```
┌─────────────────────────────────┐
│  员工信息卡                      │
│                                 │
│  姓名: {{name}}                 │
│  邮箱: {{email}}                │
│  公司: {{company}}              │
│  职位: {{position}}             │
│                                 │
└─────────────────────────────────┘
```

---

## 四、数据源文件规范

### 4.1 支持的文件格式

#### CSV文件

| 属性 | 规范 |
|------|------|
| 编码 | UTF-8（推荐）、GBK、GB18030、Latin-1 |
| 分隔符 | 逗号（默认）、分号、制表符 |
| 引号 | 双引号（推荐）或单引号 |
| 行结束符 | Windows（CRLF）、Unix（LF） |

#### Excel文件

| 属性 | 规范 |
|------|------|
| 格式 | .xlsx（推荐）、.xls |
| 引擎 | openpyxl |
| 最大行数 | 10,000 |
| 最大列数 | 256 |
| 工作表 | 第一个工作表（默认） |

#### JSON文件

| 属性 | 规范 |
|------|------|
| 格式 | JSON数组或包含data字段的对象 |
| 编码 | UTF-8 |
| 缩进 | 可选（不影响解析） |

### 4.2 数据格式要求

#### 列命名规范

```python
# 列名必须符合以下规则：
- 仅包含字母、数字、下划线
- 以字母或下划线开头
- 长度：1-100个字符
- 避免使用Python保留字

# 正确示例：
name
email
company_name
position123

# 错误示例：
my email      # 包含空格
company-name  # 包含连字符
```

#### 数据类型支持

| 数据类型 | CSV示例 | Excel示例 | 说明 |
|---------|--------|----------|------|
| 文本 | `张三` | `张三` | 无限制 |
| 数字 | `25000` | `25000` | 整数或小数 |
| 日期 | `2024-03-01` | `2024/3/1` | ISO或常规格式 |
| 布尔 | `true`/`false` | `TRUE`/`FALSE` | 复选框字段 |
| 空值 | `空`/`N/A` | 空单元格 | 留空或使用默认值 |

### 4.3 数据源示例

#### CSV示例（sample_data.csv）

```csv
name,email,company,position,salary,start_date
张三,zhangsan@example.com,百度,软件工程师,25000,2024-03-01
李四,lisi@example.com,阿里巴巴,产品经理,30000,2024-01-15
王五,wangwu@example.com,腾讯,前端开发,22000,2024-02-20
赵六,zhaoliu@example.com,字节跳动,数据分析师,28000,2024-04-10
```

#### Excel示例（sample_data.xlsx）

| name | email | company | position | salary | start_date |
|------|-------|---------|----------|--------|------------|
| 张三 | zhangsan@example.com | 百度 | 软件工程师 | 25000 | 2024-03-01 |
| 李四 | lisi@example.com | 阿里巴巴 | 产品经理 | 30000 | 2024-01-15 |

#### JSON示例（sample_data.json）

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
# 自动验证项目：
1. 文件存在性检查
2. 文件格式验证
3. 编码检测
4. 列名规范检查
5. 数据类型推断
6. 空值统计
7. 数据完整性检查

# 验证失败处理：
- 提示错误信息
- 列出具体问题
- 给出修复建议
- 允许跳过继续（可选）
```

---

## 五、安装与配置

### 5.1 环境检查

```bash
# 检查Python版本
python --version

# 输出应为：Python 3.8.0 或更高
```

### 5.2 安装依赖

```bash
# 方法1：使用requirements.txt
pip install -r requirements.txt

# 方法2：手动安装
pip install pypdf pandas Jinja2 chardet openpyxl PyMuPDF
```

### 5.3 目录结构

```
pdf-mail-merge/
├── src/                  # 源代码（勿修改）
├── tests/                # 测试用例
├── examples/             # 示例文件
├── docs/                 # 文档
├── output/               # 输出目录（需手动创建）
├── template.pdf          # 您的PDF模板
├── data.csv              # 您的数据源
└── requirements.txt      # 依赖清单
```

---

## 六、核心功能操作

### 6.1 完整操作流程

#### 步骤1：准备PDF模板

```
1. 创建或获取PDF模板文件
2. 根据需求选择模式：
   - 表单模式：使用表单设计工具（如Adobe Acrobat）创建表单域
   - 文本模式：在PDF中添加{{field_name}}占位符
3. 保存模板文件（建议命名为：template_*.pdf）
```

#### 步骤2：准备数据源

```
1. 创建数据文件（CSV/Excel/JSON）
2. 确保列名与模板字段匹配
3. 检查数据完整性和格式
4. 保存文件（建议命名为：data_*.csv）
```

#### 步骤3：验证配置

```bash
# 验证命令（不生成PDF）
python -m src.cli --template template.pdf --data data.csv --validate-only

# 输出示例：
PDF Mail Merge Tool
==================================================
Loading data from: data.csv
Loaded 8 records
Processing mode: auto
Template fields: name, email, company, position
Data fields: name, email, company, position
Validation passed!
```

#### 步骤4：执行合并

```bash
# 基本命令
python -m src.cli --template template.pdf --data data.csv --output ./output

# 高级选项
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output \
  --mode form \
  --name "{name}_{company}" \
  --zip
```

#### 步骤5：检查输出

```
output/
├── 张三_百度.pdf
├── 李四_阿里巴巴.pdf
├── 王五_腾讯.pdf
└── ...
```

### 6.2 批量处理功能

#### 多线程处理

```bash
# 自动使用多核CPU加速处理
python -m src.cli --template template.pdf --data data.csv --output ./output --workers 4
```

#### 进度显示

```
Processing: 10/100 [========>          ] 10% | Time: 2.5s
Processing: 50/100 [===================>] 50% | Time: 12.3s
Processing: 100/100 [===================] 100% | Time: 24.7s
```

#### ZIP打包

```bash
# 生成后自动打包
python -m src.cli --template template.pdf --data data.csv --output ./output --zip

# 生成文件：pdf_mail_merge_20240101_120000.zip
```

---

## 七、命令行使用

### 7.1 完整参数说明

```bash
python -m src.cli [OPTIONS]

必选参数：
  --template, -t    PDF模板文件路径
  --data, -d        数据源文件路径

可选参数：
  --output, -o      输出目录（默认：./output）
  --mode, -m        处理模式
                   - form: PDF表单填充
                   - text: 文本替换
                   - auto: 自动检测（默认）
  --name, -n        输出文件命名规则
                   - {field}: 使用数据字段
                   - {row}: 行号
                   - 示例：document_{row}、{name}_{id}
  --zip             生成ZIP压缩包
  --clean           处理前清空输出目录
  --verbose, -v     显示详细输出
  --validate-only   仅验证配置，不生成PDF
  --help, -h        显示帮助信息
```

### 7.2 使用示例

#### 示例1：表单PDF填充

```bash
python -m src.cli \
  --template employee_form.pdf \
  --data employee_data.csv \
  --output ./output \
  --mode form \
  --name "employee_{id}"

# 说明：使用表单模式，按员工ID命名输出文件
```

#### 示例2：文本替换

```bash
python -m src.cli \
  --template certificate_template.pdf \
  --data award_list.xlsx \
  --output ./certificates \
  --mode text \
  --name "certificate_{name}_{date}"

# 说明：使用文本模式，按姓名和日期命名
```

#### 示例3：自动模式

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output

# 说明：自动检测模板类型并处理
```

#### 示例4：仅验证

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --validate-only

# 说明：检查配置是否正确，不生成PDF
```

### 7.3 命名规则

```python
# 可用占位符：
{field_name}      # 数据源的列名
{row}             # 行号（从1开始）
{timestamp}       # 时间戳（YYYYMMDD_HHMMSS）

# 示例：
document_{row}              # document_1.pdf, document_2.pdf
{name}_{id}                 # 张三_001.pdf, 李四_002.pdf
{company}_{timestamp}       # 百度_20240101_120000.pdf
```

---

## 八、常见问题与解决方案

### 问题1：文件编码错误

**症状**：
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4...
```

**解决方案**：
1. 使用UTF-8编码重新保存CSV文件
2. 或使用：`--encoding gbk` 参数
3. 工具会自动尝试多种编码

### 问题2：字段不匹配

**症状**：
```
Warning: Template fields not found in data: [name, email]
```

**解决方案**：
1. 检查数据源列名与模板字段是否一致
2. 确认是否区分大小写
3. 使用`--validate-only`提前发现问题

### 问题3：PDF模板无表单域

**症状**：
```
Error: No form fields found in PDF template
```

**解决方案**：
1. 确认使用表单模式还是文本模式
2. 检查PDF是否包含表单域（Adobe Acrobat可查看）
3. 文本模式需要添加`{{field_name}}`占位符

### 问题4：中文显示乱码

**症状**：
```
PDF中的中文显示为方块或乱码
```

**解决方案**：
1. 确保PDF模板使用嵌入字体
2. 检查数据源文件编码是否为UTF-8
3. 使用支持中文的字体重新生成模板

### 问题5：输出文件无法打开

**症状**：
```
生成的PDF文件损坏或无法打开
```

**解决方案**：
1. 检查原始模板PDF是否正常
2. 确保输出目录有写入权限
3. 关闭所有打开的PDF文件后再生成

### 问题6：处理速度慢

**症状**：
```
处理100条数据需要超过60秒
```

**解决方案**：
1. 使用较新的Python版本（3.10+）
2. 减少PDF模板的复杂度和页数
3. 关闭杀毒软件实时监控
4. 使用固态硬盘存储临时文件

---

## 九、错误代码说明

| 错误代码 | 说明 | 解决方案 |
|---------|------|---------|
| E001 | 文件不存在 | 检查文件路径是否正确 |
| E002 | 格式不支持 | 使用支持的CSV/Excel/JSON格式 |
| E003 | 编码错误 | 使用UTF-8编码保存文件 |
| E004 | 字段缺失 | 检查数据源列名 |
| E005 | 字段不匹配 | 确认列名与模板一致 |
| E006 | PDF损坏 | 重新生成模板 |
| E007 | 权限不足 | 以管理员身份运行 |
| E008 | 磁盘空间不足 | 清理磁盘空间 |

---

## 十、技术规格总结

### 10.1 文件格式支持

| 类型 | 格式 | 最大大小 | 编码支持 |
|------|------|---------|---------|
| PDF模板 | .pdf | 50MB | - |
| CSV数据 | .csv | 20MB | UTF-8, GBK, GB18030 |
| Excel数据 | .xlsx, .xls | 10MB | - |
| JSON数据 | .json | 5MB | UTF-8 |

### 10.2 处理限制

| 项目 | 限制 |
|------|------|
| 最大数据行数 | 10,000 |
| 最大并发进程 | 50 |
| 最大文件大小 | 50MB |
| 字段名称长度 | 1-50字符 |
| 列名长度 | 1-100字符 |

### 10.3 兼容性

- ✅ Windows 7/8/10/11
- ✅ macOS 10.13+
- ✅ Ubuntu 18.04+
- ✅ CentOS 7+
- ✅ Python 3.8/3.9/3.10/3.11

---

**文档版本**：1.0.0  
**最后更新**：2026-05-18  
**无需联网，无需注册账户，完全脱机使用**