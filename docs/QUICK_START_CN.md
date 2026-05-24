# PDF邮件合并工具 - 快速入门指南

## 📖 目录

1. [软件概述](#软件概述)
2. [系统要求](#系统要求)
3. [安装步骤](#安装步骤)
4. [模板文件规范](#模板文件规范)
5. [数据文件规范](#数据文件规范)
6. [使用流程](#使用流程)
7. [常见问题](#常见问题)

---

## 一、软件概述

PDF邮件合并工具是一款**离线批量PDF生成工具**，完全脱机运行，**无需联网，无需注册账户**。

### 核心特性

- ✅ **零门槛使用**：无需注册、无需联网、开箱即用
- ✅ **双模式处理**：支持表单填充和文本替换
- ✅ **多数据源**：CSV、Excel、JSON格式
- ✅ **批量生成**：一次处理100+条数据
- ✅ **跨平台**：Windows、macOS、Linux

### 应用场景

| 场景 | 示例文件类型 |
|------|-------------|
| 员工信息卡 | 工牌、员工证、员工手册 |
| 证书奖状 | 荣誉证书、培训证书、资质证明 |
| 商务文件 | 合同、协议、报价单 |
| 个性化邮件 | 邀请函、通知函、祝福卡 |

---

## 二、系统要求

### 2.1 运行环境

| 项目 | 最低要求 | 推荐配置 |
|------|---------|---------|
| 操作系统 | Windows 7+ / macOS 10.13+ | Windows 10+ |
| 内存 | 4GB | 8GB+ |
| 硬盘空间 | 200MB | 500MB+ |
| Python | 3.8+ | 3.10+ |

### 2.2 依赖库

```bash
pypdf>=3.0.0        # PDF表单处理
pandas>=1.5.0       # 数据处理
Jinja2>=3.0.0       # 模板引擎
chardet>=4.0.0      # 编码检测
openpyxl>=3.0.0     # Excel支持
PyMuPDF>=1.23.0     # 文本替换（可选）
```

### 2.3 安装依赖

```bash
# 方法1：使用requirements.txt
pip install -r requirements.txt

# 方法2：手动安装
pip install pypdf pandas Jinja2 chardet openpyxl PyMuPDF
```

---

## 三、安装步骤

### 3.1 检查Python版本

```bash
python --version
# 输出应为：Python 3.8.0 或更高
```

### 3.2 安装依赖库

```bash
cd c:\Users\marike\Desktop\pdf
pip install -r requirements.txt
```

### 3.3 验证安装

```bash
# 运行测试
python tests/test_data_loader.py
python tests/test_template_engine.py

# 检查CLI帮助
python -m src.cli --help
```

---

## 四、模板文件规范

### 4.1 文件格式要求

| 属性 | 规范 |
|------|------|
| 文件格式 | PDF（推荐1.4-1.7版本） |
| 文件大小 | 最大50MB |
| 页面尺寸 | A4、Letter或自定义 |
| 字体 | 建议嵌入，避免字体缺失 |

### 4.2 表单模式要求

#### 创建表单域

使用Adobe Acrobat或其他PDF编辑器创建表单域：

```
步骤1：打开PDF文件
步骤2：选择"准备表单"工具
步骤3：添加文本框、下拉框等表单控件
步骤4：命名表单域（需与数据列名对应）
步骤5：保存模板文件
```

#### 表单域命名规则

```python
# 正确示例
name              # 简单名称
email_address     # 带下划线
Company_Name      # 首字母大写
position_123       # 带数字后缀

# 错误示例
my email          # 包含空格
company-name      # 包含连字符
2nd_field         # 以数字开头
```

### 4.3 文本替换模式要求

#### 占位符语法

```
格式：{{field_name}}
field_name：数据源中的列名（不含空格）
```

#### 正确示例

```
姓名: {{name}}
邮箱: {{email}}
公司: {{company_name}}
职位: {{position}}
```

#### 错误示例

```
姓名: {{ name }}           # 包含空格
公司: {{company-address}}  # 包含连字符
邮箱: {{ my email }}       # 包含空格
```

### 4.4 模板示例

#### 示例1：表单PDF

```
┌─────────────────────────────────┐
│  员工信息卡                      │
│                                 │
│  姓名：[________]                │
│  邮箱：[________]                │
│  公司：[________]                │
│  职位：[________]                │
│                                 │
└─────────────────────────────────┘
```

#### 示例2：文本PDF

```
┌─────────────────────────────────┐
│  员工信息卡                      │
│                                 │
│  姓名: {{name}}                  │
│  邮箱: {{email}}                  │
│  公司: {{company}}               │
│  职位: {{position}}              │
│                                 │
└─────────────────────────────────┘
```

---

## 五、数据文件规范

### 5.1 支持的文件格式

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

#### JSON文件

| 属性 | 规范 |
|------|------|
| 格式 | JSON数组或包含data字段的对象 |
| 编码 | UTF-8 |

### 5.2 列命名规则

```python
# 正确示例
name
email
company_name
position123

# 错误示例
my email      # 包含空格
company-name  # 包含连字符
```

### 5.3 数据示例

#### CSV示例（sample_data.csv）

```csv
name,email,company,position,salary,start_date
张三,zhangsan@example.com,百度,软件工程师,25000,2024-03-01
李四,lisi@example.com,阿里巴巴,产品经理,30000,2024-01-15
王五,wangwu@example.com,腾讯,前端开发,22000,2024-02-20
```

#### Excel示例

| name | email | company | position | salary | start_date |
|------|-------|---------|----------|--------|------------|
| 张三 | zhangsan@example.com | 百度 | 软件工程师 | 25000 | 2024-03-01 |
| 李四 | lisi@example.com | 阿里巴巴 | 产品经理 | 30000 | 2024-01-15 |

#### JSON示例

```json
[
  {
    "name": "张三",
    "email": "zhangsan@example.com",
    "company": "百度",
    "position": "软件工程师"
  }
]
```

---

## 六、使用流程

### 6.1 完整操作步骤

#### 步骤1：准备文件

```
1. 创建PDF模板（表单或文本模式）
2. 准备数据源（CSV/Excel/JSON）
3. 确保文件格式符合规范
```

#### 步骤2：运行验证

```bash
# 验证配置（不生成PDF）
python -m src.cli --template template.pdf --data data.csv --validate-only
```

#### 步骤3：执行合并

```bash
# 基本命令
python -m src.cli --template template.pdf --data data.csv --output ./output

# 指定模式
python -m src.cli --template template.pdf --data data.csv --output ./output --mode form

# 自定义命名
python -m src.cli --template template.pdf --data data.csv --output ./output --name "{name}_{row}"

# 生成ZIP
python -m src.cli --template template.pdf --data data.csv --output ./output --zip
```

#### 步骤4：检查输出

```
output/
├── 张三.pdf
├── 李四.pdf
├── 王五.pdf
└── ...
```

### 6.2 命令行参数

```bash
python -m src.cli [OPTIONS]

必选参数：
  --template, -t    PDF模板文件路径
  --data, -d        数据源文件路径

可选参数：
  --output, -o      输出目录（默认：./output）
  --mode, -m        处理模式（form/text/auto）
  --name, -n        输出文件命名规则
  --zip             生成ZIP压缩包
  --clean           处理前清空输出目录
  --verbose, -v     显示详细输出
  --validate-only  仅验证配置，不生成PDF
  --help, -h        显示帮助信息
```

### 6.3 使用示例

#### 示例1：表单PDF填充

```bash
python -m src.cli \
  --template employee_form.pdf \
  --data employee_data.csv \
  --output ./output \
  --mode form \
  --name "employee_{id}"
```

#### 示例2：文本替换

```bash
python -m src.cli \
  --template certificate.pdf \
  --data award_list.xlsx \
  --output ./certificates \
  --mode text \
  --name "certificate_{name}"
```

#### 示例3：自动模式

```bash
python -m src.cli \
  --template template.pdf \
  --data data.csv \
  --output ./output
```

---

## 七、常见问题

### Q1：文件编码错误

**症状**：`UnicodeDecodeError: 'utf-8' codec can't decode...`

**解决方案**：
- 使用UTF-8编码重新保存CSV文件
- 工具会自动尝试多种编码

### Q2：字段不匹配

**症状**：`Warning: Template fields not found in data`

**解决方案**：
- 检查数据源列名与模板字段是否一致
- 确认是否区分大小写
- 使用`--validate-only`提前发现问题

### Q3：PDF无表单域

**症状**：`Error: No form fields found`

**解决方案**：
- 确认使用表单模式还是文本模式
- 检查PDF是否包含表单域
- 文本模式需添加`{{field_name}}`占位符

### Q4：中文显示乱码

**症状**：PDF中的中文显示为方块

**解决方案**：
- 确保PDF模板使用嵌入字体
- 检查数据源文件编码是否为UTF-8
- 使用支持中文的字体重新生成模板

### Q5：输出文件无法打开

**症状**：生成的PDF文件损坏

**解决方案**：
- 检查原始模板PDF是否正常
- 确保输出目录有写入权限
- 关闭所有打开的PDF文件后再生成

### Q6：处理速度慢

**症状**：处理100条数据超过60秒

**解决方案**：
- 使用较新的Python版本（3.10+）
- 减少PDF模板的复杂度和页数
- 关闭杀毒软件实时监控

---

## 八、性能指标

| 项目 | 指标 |
|------|------|
| 处理100条数据 | < 60秒 |
| 最大并发进程 | 50 |
| 最大文件大小 | 50MB |
| 支持最大数据量 | 10,000条 |

---

## 九、技术支持

- **完全离线**：无需联网，无需账户
- **开源免费**：MIT协议，完全免费使用
- **跨平台**：Windows、macOS、Linux
- **开源地址**：GitHub（需手动配置）

---

**文档版本**：1.0.0  
**最后更新**：2026-05-18  
**无需联网，无需注册账户，完全脱机使用**