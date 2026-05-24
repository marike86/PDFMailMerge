# PDF邮件合并工具 - 纯脚本版本

## 版本说明

**版本类型**：纯脚本版本（Script Version）  
**目标用户**：技术用户、开发者  
**特点**：灵活性高、可定制、需手动配置环境

---

## 📁 目录结构

```
pdf-mail-merge-script/
│
├── src/                          # 源代码
│   ├── __init__.py
│   ├── data_loader.py           # 数据加载模块
│   ├── pdf_processor.py         # PDF处理核心
│   ├── template_engine.py       # 模板引擎
│   ├── cli.py                   # 命令行接口
│   └── utils.py                 # 工具函数
│
├── tests/                        # 测试用例
│   ├── test_data_loader.py
│   ├── test_pdf_processor.py
│   └── test_template_engine.py
│
├── examples/                     # 示例文件
│   ├── sample_data.csv
│   ├── template_form.pdf        # 需自行创建
│   └── template_text.pdf        # 需自行创建
│
├── docs/                         # 文档
│   ├── README.md                # 本文件
│   ├── QUICK_START.md          # 快速开始
│   ├── TROUBLESHOOTING.md      # 故障排除
│   ├── COMMAND_REFERENCE.md     # 命令参考
│   └── DEVELOPER_GUIDE.md       # 开发者指南
│
├── scripts/                      # 辅助脚本
│   ├── install_deps.bat         # Windows依赖安装
│   ├── install_deps.sh          # Linux/macOS依赖安装
│   ├── run_tests.bat           # Windows测试脚本
│   ├── run_tests.sh            # Linux/macOS测试脚本
│   └── validate_env.bat         # 环境验证脚本
│
├── config/                       # 配置文件
│   └── default_settings.json    # 默认配置
│
├── requirements.txt             # Python依赖清单
├── setup.py                     # 安装脚本
├── README.md                    # 项目说明
├── LICENSE                     # MIT开源协议
└── .gitignore                  # Git忽略文件
```

---

## 🔧 环境要求

### 系统要求

| 项目 | 要求 | 说明 |
|------|------|------|
| 操作系统 | Windows 7+ / macOS 10.13+ / Linux | 跨平台 |
| Python | 3.8+ | 必须 |
| 内存 | 4GB+ | 推荐8GB |
| 硬盘空间 | 200MB | - |

### 必需依赖

```
pypdf>=3.0.0        # PDF表单处理
pandas>=1.5.0       # 数据处理
Jinja2>=3.0.0       # 模板引擎
chardet>=4.0.0      # 编码检测
openpyxl>=3.0.0     # Excel支持
PyMuPDF>=1.23.0     # 文本替换（可选）
```

---

## 🚀 安装步骤

### 方法1：自动安装（推荐）

#### Windows系统

```bash
# 1. 进入脚本目录
cd pdf-mail-merge-script

# 2. 运行安装脚本
scripts\install_deps.bat

# 3. 验证安装
scripts\validate_env.bat
```

#### Linux/macOS系统

```bash
# 1. 进入脚本目录
cd pdf-mail-merge-script

# 2. 添加执行权限
chmod +x scripts/install_deps.sh
chmod +x scripts/run_tests.sh

# 3. 运行安装脚本
./scripts/install_deps.sh

# 4. 验证安装
./scripts/validate_env.sh
```

### 方法2：手动安装

```bash
# 1. 检查Python版本
python --version

# 2. 安装依赖
pip install -r requirements.txt

# 3. 验证安装
python -c "import pypdf, pandas, jinja2, chardet, openpyxl; print('OK')"
```

---

## 📖 基本使用

### 命令行语法

```bash
python -m src.cli [OPTIONS]

# 必选参数
  --template, -t    PDF模板文件路径
  --data, -d        数据源文件路径

# 可选参数
  --output, -o      输出目录（默认：./output）
  --mode, -m        处理模式（form/text/auto）
  --name, -n        输出文件命名规则
  --zip             生成ZIP压缩包
  --clean           清空输出目录
  --verbose, -v     详细输出
  --validate-only   仅验证配置
```

### 使用示例

#### 示例1：基本操作

```bash
# 1. 准备文件
#    - template.pdf（PDF模板）
#    - data.csv（数据源）

# 2. 执行合并
python -m src.cli --template template.pdf --data data.csv --output ./output

# 3. 查看结果
dir output
```

#### 示例2：表单模式

```bash
python -m src.cli \
  --template employee_form.pdf \
  --data employees.csv \
  --output ./cards \
  --mode form \
  --name "card_{id}"
```

#### 示例3：文本模式

```bash
python -m src.cli \
  --template certificate.pdf \
  --data awards.xlsx \
  --output ./certificates \
  --mode text \
  --name "cert_{name}"
```

---

## 🔍 故障排除

### 常见问题

#### 问题1：Python未找到

**错误**：`'python' 不是内部或外部命令`

**解决**：
1. 下载Python 3.8+：https://www.python.org/downloads/
2. 安装时勾选"Add Python to PATH"
3. 重新打开命令行窗口

#### 问题2：依赖安装失败

**错误**：`pip install` 失败

**解决**：
```bash
# 升级pip
python -m pip install --upgrade pip

# 单独安装依赖
pip install pypdf
pip install pandas
pip install jinja2
pip install chardet
pip install openpyxl
```

#### 问题3：文件编码错误

**错误**：`UnicodeDecodeError`

**解决**：
1. 使用UTF-8编码保存CSV文件
2. 或在Excel中另存为CSV（UTF-8）

#### 问题4：找不到模板

**错误**：`FileNotFoundError: template.pdf`

**解决**：
1. 使用绝对路径
2. 检查文件扩展名是否正确

### 详细故障排除指南

请参阅 [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

---

## 📚 文档列表

| 文档 | 说明 |
|------|------|
| README.md | 本文件，使用概览 |
| QUICK_START.md | 快速开始指南（5分钟上手） |
| TROUBLESHOOTING.md | 详细故障排除指南 |
| COMMAND_REFERENCE.md | 命令行完整参考 |
| DEVELOPER_GUIDE.md | 开发者自定义指南 |

---

## 🔧 高级配置

### 配置文件

编辑 `config/default_settings.json`：

```json
{
  "default_output": "./output",
  "default_mode": "auto",
  "naming_pattern": "document_{row}",
  "zip_enabled": false,
  "verbose": false,
  "max_workers": 4
}
```

### 环境变量

```bash
# 设置默认输出目录
export PDF_MERGE_OUTPUT="./my_output"

# 设置默认模式
export PDF_MERGE_MODE="form"

# 启用详细输出
export PDF_MERGE_VERBOSE="1"
```

---

## 🧪 测试

### 运行测试

```bash
# Windows
scripts\run_tests.bat

# Linux/macOS
./scripts/run_tests.sh
```

### 测试内容

- 数据加载测试（CSV/Excel/JSON）
- PDF处理测试（表单/文本）
- 模板引擎测试
- 错误处理测试

---

## 📞 技术支持

- **问题反馈**：GitHub Issues
- **文档更新**：请查看docs目录
- **版本信息**：查看VERSION文件

---

## 📄 许可证

MIT License - 详见 [LICENSE](../LICENSE)

---

**版本信息**：
- 版本号：1.0.0
- 发布日期：2026-05-18
- 类型：纯脚本版本