# 纯脚本版本 - 故障排除指南

## 目录

1. [环境问题](#一环境问题)
2. [依赖问题](#二依赖问题)
3. [文件问题](#三文件问题)
4. [处理问题](#四处理问题)
5. [输出问题](#五输出问题)

---

## 一、环境问题

### 问题1.1：Python未安装

**症状**：
```
'python' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

**原因**：Python未安装或未添加到PATH

**解决方案**：

#### 步骤1：检查Python是否已安装

```bash
# 在以下位置查找Python
where python          # Windows
which python          # Linux/macOS

# 或尝试
python3 --version
```

#### 步骤2：下载并安装Python

1. 访问 https://www.python.org/downloads/
2. 下载Python 3.8或更高版本（推荐3.10）
3. 运行安装程序
4. **重要**：勾选以下选项
   - ☑ "Add Python to PATH"
   - ☑ "Install pip"
5. 点击"Install Now"
6. 等待安装完成

#### 步骤3：验证安装

```bash
# 重新打开命令行窗口
python --version

# 预期输出：Python 3.10.x 或更高
```

---

### 问题1.2：pip未安装

**症状**：
```
'pip' 不是内部或外部命令
```

**原因**：pip未正确安装

**解决方案**：

```bash
# 方法1：重新安装pip
python -m ensurepip --upgrade

# 方法2：下载get-pip.py
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py

# 方法3：使用ensurepip
python -m pip install --upgrade pip
```

---

### 问题1.3：权限不足

**症状**：
```
Permission denied: 'C:\\Program Files\\Python310\\Lib\\site-packages'
```

**原因**：需要管理员权限

**解决方案**：

#### Windows

```bash
# 方法1：以管理员身份运行命令行
# 右键点击"命令提示符" → "以管理员身份运行"

# 方法2：使用用户安装
pip install --user package_name

# 方法3：修改安装目录权限
# 右键点击Python安装目录 → 属性 → 安全 → 添加当前用户写入权限
```

#### Linux/macOS

```bash
# 方法1：使用sudo
sudo pip install package_name

# 方法2：创建虚拟环境
python -m venv myenv
source myenv/bin/activate
pip install package_name
```

---

## 二、依赖问题

### 问题2.1：单个依赖安装失败

**症状**：
```
ERROR: Could not install package pypdf
```

**解决方案**：

```bash
# 1. 升级pip
python -m pip install --upgrade pip

# 2. 单独安装失败的依赖
pip install pypdf --no-cache-dir

# 3. 如果仍然失败，尝试指定版本
pip install pypdf==3.17.0

# 4. 或使用wheel安装
pip install --upgrade pip setuptools wheel
pip install package_name
```

---

### 问题2.2：版本冲突

**症状**：
```
ERROR: pypdf 4.0.0 has requirement chardet>=5.0, but you have chardet 4.0.0
```

**解决方案**：

```bash
# 1. 升级所有依赖到最新版本
pip install --upgrade pypdf pandas jinja2 chardet openpyxl

# 2. 或使用requirements.txt指定兼容版本
# 编辑requirements.txt：
pypdf>=3.0.0
pandas>=1.5.0
jinja2>=3.0.0
chardet>=4.0.0
openpyxl>=3.0.0

# 3. 然后安装
pip install -r requirements.txt
```

---

### 问题2.3：网络问题

**症状**：
```
Connection error: [SSL: CERTIFICATE_VERIFY_FAILED]
```

**解决方案**：

```bash
# 方法1：忽略SSL验证
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org package_name

# 方法2：使用国内镜像
pip install package_name -i https://pypi.tuna.tsinghua.edu.cn/simple

# 方法3：设置SSL不验证
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
```

---

### 问题2.4：缺少Visual C++编译器

**症状**：
```
error: Microsoft Visual C++ 14.0 is required
```

**解决方案**：

#### Windows

```bash
# 方法1：安装Visual Studio Build Tools
# 1. 下载：https://visualstudio.microsoft.com/downloads/
# 2. 安装"Build Tools for Visual Studio 2022"
# 3. 勾选"Windows 10 SDK"和"C++ Build Tools"

# 方法2：使用预编译wheel
# 访问 https://www.lfd.uci.edu/~gohlke/pythonlibs/
# 下载对应版本的wheel文件
pip install package_name.whl
```

#### Linux

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc
```

---

## 三、文件问题

### 问题3.1：文件找不到

**症状**：
```
FileNotFoundError: [Errno 2] No such file or directory: 'template.pdf'
```

**原因与解决方案**：

| 原因 | 解决方案 |
|------|----------|
| 文件路径错误 | 使用绝对路径 |
| 文件名拼写错误 | 检查文件名大小写 |
| 文件未创建 | 创建示例文件 |
| 目录不存在 | 创建目录 |

**验证文件存在**：

```bash
# Windows
dir template.pdf

# Linux/macOS
ls -la template.pdf

# Python验证
import os
print(os.path.exists("template.pdf"))
```

---

### 问题3.2：CSV编码错误

**症状**：
```
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xb4 in position 0
```

**原因**：CSV文件不是UTF-8编码

**解决方案**：

#### 方法1：Excel重新保存

1. 打开CSV文件
2. 文件 → 另存为
3. 选择"CSV UTF-8"格式
4. 保存

#### 方法2：使用Python转换

```python
# 创建一个转换脚本 convert_encoding.py
import pandas as pd

def convert_to_utf8(input_file, output_file, original_encoding='gbk'):
    df = pd.read_csv(input_file, encoding=original_encoding)
    df.to_csv(output_file, index=False, encoding='utf-8')
    print(f"Converted {input_file} to UTF-8: {output_file}")

# 使用
convert_to_utf8('data_gbk.csv', 'data_utf8.csv')
```

#### 方法3：使用工具转换

```bash
# Linux/macOS
iconv -f GBK -t UTF-8 input.csv > output.csv

# Windows PowerShell
Get-Content input.csv -Encoding Default | Out-File output.csv -Encoding UTF8
```

---

### 问题3.3：文件格式不支持

**症状**：
```
DataLoadError: Unsupported file type: .txt
```

**原因**：使用了不支持的文件格式

**解决方案**：

| 当前格式 | 转换为 |
|---------|--------|
| .txt | .csv |
| .xls | .xlsx |
| .jsonl | .json |

**Excel转换**：
1. 打开.xls文件
2. 另存为.xlsx格式
3. 或导出为.csv格式

---

### 问题3.4：文件太大

**症状**：
```
MemoryError: Unable to allocate memory
```

**原因**：文件超过内存限制

**解决方案**：

```bash
# 1. 分批处理
# 将大文件拆分为多个小文件，每个1000行

# 2. 增加虚拟内存
# Windows：系统属性 → 高级 → 性能 → 设置 → 高级 → 虚拟内存
# Linux：创建swap文件

# 3. 使用64位Python
# 下载安装Python 64位版本
```

---

## 四、处理问题

### 问题4.1：找不到表单域

**症状**：
```
Error: No form fields found in PDF template
```

**原因**：PDF不是表单模式，或没有表单域

**解决方案**：

#### 检查PDF是否包含表单域

```bash
# 使用Python检查
python -c "from pypdf import PdfReader; r=PdfReader('template.pdf'); print(r.get_fields())"
```

#### 如果是文本模式

```bash
# 切换到文本模式
python -m src.cli --template template.pdf --data data.csv --mode text
```

#### 如果确实是表单模式

1. 使用Adobe Acrobat打开PDF
2. 选择"工具" → "准备表单"
3. 检查是否有表单域
4. 添加表单域并命名
5. 保存PDF

---

### 问题4.2：找不到文本占位符

**症状**：
```
Error: No text placeholders found in PDF template
```

**原因**：PDF中没有`{{field_name}}`格式的占位符

**解决方案**：

1. 检查PDF内容是否包含占位符
2. 确保占位符格式正确：`{{field_name}}`
3. 注意大小写：`{{Name}}` ≠ `{{name}}`
4. 不要有空格：`{{ name }}` 无效

**正确示例**：
```
姓名：{{name}}
邮箱：{{email}}
```

**错误示例**：
```
姓名：{{ name }}      # 有空格
姓名：{name}          # 缺少{}
姓名：{{my name}}     # 有空格
```

---

### 问题4.3：字段不匹配

**症状**：
```
Warning: Template fields not found in data: [field1, field2]
```

**原因**：模板字段与数据列名不一致

**解决方案**：

#### 1. 检查模板字段

```bash
# Windows
python -m src.cli --template template.pdf --validate-only

# 会显示：
# Template fields: name, email, company
```

#### 2. 检查数据列名

```bash
# 查看CSV列名
head -n 1 data.csv

# 查看Excel列名
python -c "import pandas as pd; df=pd.read_excel('data.xlsx'); print(df.columns)"
```

#### 3. 匹配字段名

确保模板字段和数据列名完全一致（区分大小写）

---

### 问题4.4：中文乱码

**症状**：PDF中的中文显示为方块或问号

**原因**：
- 字体未嵌入
- 字体不支持中文
- 编码错误

**解决方案**：

#### 1. 确保字体嵌入

使用Adobe Acrobat：
1. 打开PDF
2. 文件 → 打印 → Adobe PDF
3. 点击"属性" → "字体" → "嵌入所有字体"

#### 2. 使用支持中文的字体

推荐字体：
- 宋体（SimSun）
- 黑体（SimHei）
- 微软雅黑（Microsoft YaHei）

#### 3. 检查数据文件编码

```bash
# 确保CSV是UTF-8编码
file data.csv

# 如果不是，转换编码
iconv -f GBK -t UTF-8 data.csv > data_utf8.csv
```

---

### 问题4.5：处理速度慢

**症状**：处理100条数据超过60秒

**解决方案**：

#### 1. 优化PDF模板

```bash
# 减少PDF页数
# 简化图形元素
# 使用嵌入字体
```

#### 2. 关闭杀毒软件

某些杀毒软件会扫描每个生成的PDF，导致速度变慢

#### 3. 使用SSD

将临时文件放在SSD上，I/O速度更快

#### 4. 升级Python版本

Python 3.10+比3.8有更好的性能

#### 5. 增加内存

更多内存可以减少磁盘交换

---

## 五、输出问题

### 问题5.1：输出文件无法打开

**症状**：生成的PDF文件损坏或无法打开

**解决方案**：

```bash
# 1. 检查原始模板是否正常
# 用Adobe Reader打开template.pdf确认没问题

# 2. 检查输出目录权限
# 确保有写入权限

# 3. 关闭所有打开的PDF
# 如果PDF被其他程序占用，可能无法写入

# 4. 检查磁盘空间
df -h  # Linux/macOS
wmic logicaldisk get size,freespace  # Windows

# 5. 使用--clean选项重新生成
python -m src.cli --template template.pdf --data data.csv --output ./output --clean
```

---

### 问题5.2：输出文件名错误

**症状**：文件名包含非法字符或被截断

**解决方案**：

```bash
# 使用安全的命名规则
--name "document_{row}"

# 或使用数据字段（确保字段值不包含非法字符）
--name "{name}_{id}"
```

**非法字符会自动替换**：
```
/ \ : * ? " < > | → 替换为 _
```

---

### 问题5.3：ZIP打包失败

**症状**：
```
Warning: Failed to create ZIP archive
```

**解决方案**：

```bash
# 1. 检查ZIP工具是否安装
# Windows通常自带
# Linux/macOS检查：
which zip

# 2. 如果没有，安装zip工具
# Ubuntu/Debian
sudo apt-get install zip

# macOS（使用brew）
brew install zip

# 3. 手动创建ZIP
# Windows
powershell Compress-Archive -Path "output\*" -DestinationPath "output.zip"

# Linux/macOS
zip -r output.zip output/
```

---

### 问题5.4：输出目录已满

**症状**：
```
Error: [Errno 28] No space left on device
```

**解决方案**：

```bash
# 1. 清理磁盘空间
# 删除临时文件
rm -rf /tmp/*
rm -rf ~/.cache/*

# 2. 清理输出目录
rm -rf output/*
rm output.zip

# 3. 检查磁盘空间
df -h

# 4. 扩大磁盘或使用其他磁盘
```

---

## 诊断工具

### 环境验证脚本

```bash
# Windows
scripts\validate_env.bat

# Linux/macOS
./scripts/validate_env.sh

# 会检查：
# - Python版本
# - pip可用性
# - 依赖库安装
# - 文件权限
```

### 测试脚本

```bash
# Windows
scripts\run_tests.bat

# Linux/macOS
./scripts/run_tests.sh

# 会测试：
# - 数据加载（CSV/Excel/JSON）
# - PDF处理（表单/文本）
# - 模板引擎
# - 错误处理
```

---

## 获取帮助

如果以上方法都无法解决您的问题：

1. 查看 [COMMAND_REFERENCE.md](COMMAND_REFERENCE.md)
2. 查看 [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
3. 在GitHub提交Issue，包含：
   - 错误信息
   - 操作步骤
   - 系统环境信息
   - Python版本

---

**最后更新**：2026-05-18