# 纯脚本版本 - 开发者指南

## 📖 目录

1. [开发环境](#一开发环境)
2. [项目结构](#二项目结构)
3. [核心模块](#三核心模块)
4. [扩展开发](#四扩展开发)
5. [测试指南](#五测试指南)
6. [性能优化](#六性能优化)

---

## 一、开发环境

### 1.1 环境要求

- Python 3.8+
- pip 22.0+
- Git
- 文本编辑器或IDE（推荐VSCode或PyCharm）

### 1.2 环境设置

```bash
# 1. 克隆项目
git clone <repository_url>
cd pdf-mail-merge-script

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows
venv\Scripts\activate

# Linux/macOS
source venv/bin/activate

# 4. 安装开发依赖
pip install -r requirements.txt
pip install pytest pytest-cov  # 测试框架

# 5. 验证环境
python -c "import pypdf, pandas, jinja2, chardet, openpyxl; print('OK')"
```

### 1.3 IDE配置

#### VSCode配置

创建 `.vscode/settings.json`：

```json
{
  "python.defaultInterpreterPath": "./venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true
}
```

#### PyCharm配置

1. File → Settings → Project → Python Interpreter
2. 选择虚拟环境路径：`<project>/venv/bin/python`
3. Apply → OK

---

## 二、项目结构

### 2.1 目录结构

```
pdf-mail-merge-script/
├── src/                    # 源代码
│   ├── __init__.py        # 包初始化
│   ├── data_loader.py     # 数据加载
│   ├── pdf_processor.py   # PDF处理
│   ├── template_engine.py # 模板引擎
│   ├── cli.py             # 命令行接口
│   └── utils.py           # 工具函数
│
├── tests/                  # 测试
│   ├── unit/             # 单元测试
│   ├── integration/       # 集成测试
│   └── fixtures/          # 测试数据
│
├── scripts/                # 辅助脚本
│   ├── install_deps.sh    # 安装脚本
│   ├── run_tests.sh       # 测试脚本
│   └── validate_env.sh    # 环境验证
│
├── docs/                   # 文档
│
├── examples/                # 示例
│
├── config/                 # 配置
│   └── default_settings.json
│
└── requirements.txt        # 依赖清单
```

### 2.2 模块依赖关系

```
cli.py (入口)
  ├── data_loader.py (数据加载)
  ├── pdf_processor.py (PDF处理)
  ├── template_engine.py (模板引擎)
  └── utils.py (工具函数)
```

---

## 三、核心模块

### 3.1 data_loader.py

**功能**：加载数据源文件（CSV/Excel/JSON）

**主要函数**：

```python
def load_csv(file_path: str, encoding: Optional[str] = None) -> pd.DataFrame
"""加载CSV文件，自动检测编码"""

def load_excel(file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame
"""加载Excel文件"""

def load_json(file_path: str) -> pd.DataFrame
"""加载JSON文件"""

def load_data(file_path: str) -> pd.DataFrame
"""自动检测文件类型并加载"""

def validate_data(df: pd.DataFrame, required_fields: Optional[List[str]] = None) -> Dict
"""验证数据完整性"""
```

**扩展方式**：

```python
# 添加新的数据源格式
def load_xml(file_path: str) -> pd.DataFrame:
    """加载XML文件"""
    # 实现XML解析逻辑
    pass

# 更新load_data函数
def load_data(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.csv':
        return load_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        return load_excel(file_path)
    elif ext == '.json':
        return load_json(file_path)
    elif ext == '.xml':  # 新增
        return load_xml(file_path)
    else:
        raise DataLoadError(f"Unsupported file type: {ext}")
```

### 3.2 pdf_processor.py

**功能**：处理PDF表单填充和文本替换

**主要函数**：

```python
def fill_form_pdf(pdf_path: str, data: Dict[str, str], output_path: str) -> bool
"""填充PDF表单域"""

def replace_text(pdf_path: str, replacements: Dict[str, str], output_path: str) -> bool
"""替换PDF中的文本占位符"""

def read_form_fields(pdf_path: str) -> Dict[str, str]
"""读取PDF表单域"""

def detect_text_placeholders(pdf_path: str) -> List[str]
"""检测文本占位符"""
```

**扩展方式**：

```python
# 添加新的PDF处理功能
def add_watermark(pdf_path: str, watermark_text: str, output_path: str) -> bool:
    """为PDF添加水印"""
    # 实现水印功能
    pass

def merge_pdfs(pdf_list: List[str], output_path: str) -> bool:
    """合并多个PDF"""
    # 实现PDF合并功能
    pass
```

### 3.3 template_engine.py

**功能**：模板解析和渲染

**主要函数**：

```python
def render_template(template_str: str, data: Dict[str, any]) -> str
"""渲染Jinja2模板"""

def detect_template_fields(text: str) -> List[str]
"""检测模板字段"""

def validate_template_fields(template_fields: List[str], data_fields: List[str]) -> Dict
"""验证字段映射"""
```

**扩展方式**：

```python
# 添加自定义过滤器
def custom_filters():
    from jinja2 import Environment
    
    def currency_format(value):
        return f"¥{value:,.2f}"
    
    def date_format(value, format='%Y-%m-%d'):
        from datetime import datetime
        if isinstance(value, str):
            dt = datetime.fromisoformat(value)
        else:
            dt = value
        return dt.strftime(format)
    
    env = Environment()
    env.filters['currency'] = currency_format
    env.filters['date'] = date_format
    
    return env
```

### 3.4 cli.py

**功能**：命令行接口

**扩展方式**：

```python
# 添加新的命令行参数
def _add_custom_args(parser):
    parser.add_argument(
        '--watermark',
        help='添加水印文本'
    )
    
    parser.add_argument(
        '--quality',
        type=int,
        default=95,
        help='PDF输出质量（0-100）'
    )

# 在run方法中处理新参数
def run(self, args):
    parsed_args = self.parser.parse_args(args)
    
    # 新增处理逻辑
    if parsed_args.watermark:
        add_watermark_to_all(parsed_args.watermark)
```

---

## 四、扩展开发

### 4.1 添加新数据格式

#### 步骤1：实现加载函数

```python
# src/data_loader.py

def load_xml(file_path: str) -> pd.DataFrame:
    """加载XML格式数据"""
    import xml.etree.ElementTree as ET
    
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    records = []
    for item in root.findall('.//record'):
        record = {}
        for child in item:
            record[child.tag] = child.text
        records.append(record)
    
    return pd.DataFrame(records)
```

#### 步骤2：更新load_data函数

```python
def load_data(file_path: str) -> pd.DataFrame:
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.csv':
        return load_csv(file_path)
    elif ext in ['.xlsx', '.xls']:
        return load_excel(file_path)
    elif ext == '.json':
        return load_json(file_path)
    elif ext == '.xml':  # 新增
        return load_xml(file_path)
    else:
        raise DataLoadError(f"Unsupported file type: {ext}")
```

#### 步骤3：添加测试

```python
# tests/test_data_loader.py

def test_load_xml():
    from src.data_loader import load_xml
    
    data = load_xml('examples/test_data.xml')
    
    assert len(data) > 0
    assert 'name' in data.columns
```

### 4.2 添加新PDF功能

#### 示例：添加水印功能

```python
# src/watermark.py

def add_watermark(pdf_path: str, text: str, output_path: str, 
                  opacity: float = 0.3, font_size: int = 48) -> bool:
    """
    为PDF添加水印
    
    Args:
        pdf_path: 源PDF路径
        text: 水印文本
        output_path: 输出路径
        opacity: 透明度（0-1）
        font_size: 字体大小
    
    Returns:
        bool: 成功返回True
    """
    try:
        from pypdf import PdfReader, PdfWriter
        from pypdf.generic import DictionaryObject
        
        reader = PdfReader(pdf_path)
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        # 添加水印逻辑
        # ...
        
        with open(output_path, 'wb') as f:
            writer.write(f)
        
        return True
        
    except Exception as e:
        raise PDFProcessError(f"Error adding watermark: {e}")
```

### 4.3 自定义字段验证

```python
# src/validators.py

from typing import Dict, List, Tuple

class FieldValidator:
    """自定义字段验证器"""
    
    @staticmethod
    def validate_email(email: str) -> Tuple[bool, str]:
        """验证邮箱格式"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(pattern, email):
            return True, ""
        return False, "Invalid email format"
    
    @staticmethod
    def validate_phone(phone: str) -> Tuple[bool, str]:
        """验证手机号格式"""
        import re
        pattern = r'^1[3-9]\d{9}$'
        if re.match(pattern, phone):
            return True, ""
        return False, "Invalid phone number"
    
    @staticmethod
    def validate_required(value: any) -> Tuple[bool, str]:
        """验证必填字段"""
        if value is None or str(value).strip() == '':
            return False, "Field is required"
        return True, ""
    
    def validate_record(self, record: Dict[str, any], rules: Dict[str, str]) -> Dict:
        """验证单条记录"""
        result = {
            'valid': True,
            'errors': []
        }
        
        for field, rule in rules.items():
            validator = getattr(self, f'validate_{rule}', None)
            if validator:
                valid, message = validator(record.get(field, ''))
                if not valid:
                    result['valid'] = False
                    result['errors'].append(f"{field}: {message}")
        
        return result
```

---

## 五、测试指南

### 5.1 测试框架

使用pytest框架：

```bash
# 安装测试依赖
pip install pytest pytest-cov

# 运行所有测试
pytest tests/

# 运行指定测试
pytest tests/test_data_loader.py

# 生成覆盖率报告
pytest tests/ --cov=src --cov-report=html
```

### 5.2 测试用例结构

```python
# tests/test_data_loader.py

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from data_loader import load_csv, load_excel, validate_data


class TestDataLoader:
    """数据加载器测试类"""
    
    def test_load_csv_basic(self):
        """测试CSV基本加载"""
        data = load_csv('examples/sample_data.csv')
        
        assert data is not None
        assert len(data) > 0
        assert 'name' in data.columns
    
    def test_load_csv_with_encoding(self):
        """测试CSV编码处理"""
        data = load_csv('examples/gbk_data.csv', encoding='gbk')
        
        assert data is not None
        assert len(data) > 0
    
    def test_validate_data_valid(self):
        """测试有效数据验证"""
        df = load_csv('examples/sample_data.csv')
        result = validate_data(df, required_fields=['name', 'email'])
        
        assert result['valid'] is True
        assert len(result['errors']) == 0
    
    def test_validate_data_missing_fields(self):
        """测试缺失字段验证"""
        df = load_csv('examples/sample_data.csv')
        result = validate_data(df, required_fields=['name', 'missing_field'])
        
        assert result['valid'] is False
        assert 'missing_field' in result['errors'][0]
    
    def test_load_nonexistent_file(self):
        """测试加载不存在的文件"""
        with pytest.raises(Exception):
            load_csv('nonexistent.csv')
```

### 5.3 集成测试

```python
# tests/integration/test_full_workflow.py

import pytest
import os
import shutil
from src.cli import MailMergeCLI


class TestFullWorkflow:
    """完整工作流集成测试"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """每个测试前后的设置"""
        self.output_dir = './test_output'
        
        yield
        
        # 清理
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)
    
    def test_form_mode_workflow(self):
        """测试表单模式完整流程"""
        cli = MailMergeCLI()
        
        result = cli.run([
            '--template', 'examples/template_form.pdf',
            '--data', 'examples/sample_data.csv',
            '--output', self.output_dir,
            '--mode', 'form',
            '--name', 'test_{row}'
        ])
        
        assert result == 0
        assert os.path.exists(self.output_dir)
        
        files = os.listdir(self.output_dir)
        assert len(files) > 0
        assert all(f.endswith('.pdf') for f in files)
    
    def test_text_mode_workflow(self):
        """测试文本模式完整流程"""
        cli = MailMergeCLI()
        
        result = cli.run([
            '--template', 'examples/template_text.pdf',
            '--data', 'examples/sample_data.csv',
            '--output', self.output_dir,
            '--mode', 'text',
            '--name', 'test_{name}'
        ])
        
        assert result == 0
        assert os.path.exists(self.output_dir)
```

---

## 六、性能优化

### 6.1 代码级优化

#### 优化数据加载

```python
# 原始代码
def load_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df

# 优化后
def load_csv(file_path: str, encoding: Optional[str] = None) -> pd.DataFrame:
    if encoding is None:
        encoding = detect_encoding(file_path)
    
    # 使用更快的读取参数
    df = pd.read_csv(
        file_path,
        encoding=encoding,
        low_memory=False,      # 避免重复检测类型
        memory_map=False,      # 对于大文件禁用内存映射
        dtype={'id': str}     # 明确指定数据类型
    )
    
    return df
```

#### 优化PDF处理

```python
# 使用上下文管理器减少资源占用
def process_batch(pdf_list: List[str], data_list: List[Dict]):
    results = []
    
    for pdf, data in zip(pdf_list, data_list):
        with fitz.open(pdf) as doc:  # 自动关闭文档
            # 处理逻辑
            pass
        
        # 定期清理内存
        if len(results) % 100 == 0:
            import gc
            gc.collect()
    
    return results
```

### 6.2 并发优化

```python
# 使用多进程处理CPU密集任务
from multiprocessing import Pool, cpu_count

def process_pdfs_parallel(pdf_path: str, data_list: List[Dict], workers: int = None):
    if workers is None:
        workers = cpu_count()
    
    tasks = [(pdf_path, data) for data in data_list]
    
    with Pool(processes=workers) as pool:
        results = pool.starmap(fill_form_pdf, tasks)
    
    return results
```

### 6.3 缓存优化

```python
# 缓存模板解析结果
from functools import lru_cache

@lru_cache(maxsize=128)
def get_template_fields(pdf_path: str) -> List[str]:
    """缓存模板字段检测结果"""
    if pdf_path.endswith('.pdf'):
        if detect_form_fields(pdf_path):
            return get_form_field_names(pdf_path)
        else:
            return detect_text_placeholders(pdf_path)
    return []
```

### 6.4 性能监控

```python
# 添加性能监控
import time
import logging

def timed_process(func):
    """性能计时装饰器"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        
        logging.info(f"{func.__name__} took {elapsed:.2f}s")
        
        return result
    return wrapper

@timed_process
def fill_form_pdf(pdf_path: str, data: Dict, output_path: str) -> bool:
    # 处理逻辑
    pass
```

---

## 七、调试指南

### 7.1 启用调试模式

```bash
# 启用详细输出
python -m src.cli --template template.pdf --data data.csv --verbose

# 启用Python调试
python -m pdb -m src.cli --template template.pdf --data data.csv

# 使用IDE调试
# 在VSCode中设置断点，按F5启动调试
```

### 7.2 日志配置

创建 `config/logging.conf`：

```ini
[loggers]
keys=root,pdfmerge

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_pdfmerge]
level=DEBUG
handlers=consoleHandler,fileHandler
qualname=pdfmerge
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('pdfmerge.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

---

## 八、发布指南

### 8.1 版本号规范

遵循语义化版本：
- 主版本号：不兼容的API修改
- 次版本号：向后兼容的功能增加
- 修订号：向后兼容的问题修复

### 8.2 发布检查清单

- [ ] 所有测试通过
- [ ] 更新版本号
- [ ] 更新文档
- [ ] 创建release标签
- [ ] 更新CHANGELOG.md

### 8.3 创建发布

```bash
# 1. 提交所有更改
git add .
git commit -m "Release v1.1.0"

# 2. 创建标签
git tag -a v1.1.0 -m "Version 1.1.0"
git push origin v1.1.0

# 3. 创建发布包
python setup.py sdist
```

---

**最后更新**：2026-05-18