# Contributing to PDF Mail Merge Tool

感谢您对PDF邮件合并工具的兴趣！欢迎贡献代码。

## 如何贡献

### 1. 报告问题

- 在GitHub Issues中提交问题报告
- 提供详细的问题描述和复现步骤
- 包含您的操作系统和Python版本信息

### 2. 提交代码

#### 开发流程

1. **Fork仓库**
   ```
   git clone https://github.com/YOUR_USERNAME/pdf-mail-merge.git
   cd pdf-mail-merge
   ```

2. **创建分支**
   ```
   git checkout -b feature/your-feature-name
   ```

3. **开发并测试**
   - 编写代码并添加测试
   - 运行测试确保通过
   - 遵循代码规范

4. **提交更改**
   ```
   git add .
   git commit -m "Add: 描述您的新功能"
   ```

5. **推送到分支**
   ```
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**
   - 详细描述您的更改
   - 引用相关问题

### 3. 代码规范

#### Python代码规范

- 遵循PEP 8规范
- 使用4个空格缩进
- 最大行长度：100字符
- 为所有公共函数编写文档字符串

#### 函数文档示例

```python
def fill_form_pdf(pdf_path: str, data: Dict[str, str], output_path: str) -> bool:
    """
    Fill PDF form with provided data.
    
    Args:
        pdf_path: Path to source PDF template
        data: Dictionary mapping field names to values
        output_path: Path for output PDF file
        
    Returns:
        True if successful
        
    Raises:
        PDFProcessError: If PDF cannot be filled
    """
```

#### 命名规范

- 函数：`snake_case`（如 `fill_form_pdf`）
- 类：`PascalCase`（如 `PDFProcessError`）
- 常量：`UPPER_SNAKE_CASE`（如 `MAX_FILE_SIZE`）
- 私有函数：前缀下划线（如 `_internal_function`）

### 4. 测试要求

- 所有新功能必须包含测试
- 测试覆盖率应保持在80%以上
- 运行完整测试套件：
  ```bash
  python -m pytest tests/
  ```

### 5. 提交信息规范

使用以下提交信息格式：

```
<type>: <subject>

<body>

<footer>
```

类型包括：
- `Add`: 新功能
- `Fix`: 错误修复
- `Update`: 更新现有功能
- `Docs`: 文档更新
- `Test`: 测试相关
- `Refactor`: 代码重构
- `Style`: 代码格式调整（不影响功能）

示例：
```
Add: 支持Excel数据源导入

- 添加openpyxl依赖
- 实现load_excel函数
- 添加编码自动检测

Closes #123
```

### 6. Pull Request检查清单

提交PR前请确认：

- [ ] 代码遵循规范
- [ ] 添加了测试
- [ ] 所有测试通过
- [ ] 更新了文档（如需要）
- [ ] PR描述清晰完整

## 开发环境设置

### 1. 克隆仓库
```bash
git clone https://github.com/yourusername/pdf-mail-merge.git
cd pdf-mail-merge
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # 如有开发依赖
```

### 4. 运行测试
```bash
python tests/test_data_loader.py
python tests/test_pdf_processor.py
python tests/test_template_engine.py
```

## 分支管理

- `main`: 稳定版本，只接受PR合并
- `develop`: 开发版本
- `feature/*`: 新功能分支
- `fix/*`: 错误修复分支
- `docs/*`: 文档更新分支

## 许可证

贡献的代码将使用MIT许可证。参见 [LICENSE](../LICENSE)。

## 联系方式

- GitHub Issues: https://github.com/yourusername/pdf-mail-merge/issues
- 邮箱: your.email@example.com

感谢您的贡献！