# PDF邮件合并工具开发计划

## 项目概述

开发一个PDF邮件合并工具，能够：
- 输入PDF模板（含表单域或可替换文本标记）
- 输入数据源（CSV/Excel/JSON）
- 批量填充数据，生成个性化PDF
- 支持打包下载和可选邮件发送

## 技术栈

- **语言**：Python 3.8+
- **PDF处理**：pypdf（轻量、MIT协议）
- **数据处理**：pandas（CSV/Excel）
- **文本替换**：Jinja2（非表单PDF）
- **CLI界面**：argparse
- **开源协议**：MIT

## 项目结构

```
pdf-mail-merge/
├── src/                    # 源代码
│   ├── __init__.py
│   ├── pdf_processor.py    # PDF处理核心
│   ├── data_loader.py      # 数据读取模块
│   ├── template_engine.py  # 模板引擎（文本替换）
│   ├── cli.py              # 命令行入口
│   └── utils.py            # 工具函数
├── tests/                  # 测试用例
│   ├── test_pdf_processor.py
│   ├── test_data_loader.py
│   └── test_template_engine.py
├── examples/               # 示例文件
│   ├── template_form.pdf   # 表单PDF模板
│   ├── template_text.pdf   # 文本替换模板
│   └── sample_data.csv     # 示例数据
├── docs/                   # 文档
│   ├── README.md
│   ├── LICENSE
│   └── CONTRIBUTING.md
├── requirements.txt        # 依赖清单
├── setup.py                # 安装配置
└── .gitignore              # Git忽略文件
```

## 开发阶段

### 阶段1：技术方案确认

#### 1.1 PDF处理库选择
- **pypdf**：轻量级、原生Python、MIT协议，适合基础操作
- 替代方案：PyMuPDF（速度快，但GPL协议可能影响开源）

#### 1.2 核心功能设计
1. **表单PDF处理**：
   - 使用pypdf读取PDF表单域
   - 填充表单字段值
   - 保存为新PDF

2. **非表单PDF文本替换**：
   - 使用Jinja2解析`{{field_name}}`标记
   - 定位并替换文本
   - 处理中文和特殊字符

3. **数据加载**：
   - 使用pandas读取CSV/Excel
   - 自动识别编码（UTF-8、GBK等）
   - 返回统一的数据格式

#### 1.3 性能优化
- 使用multiprocessing处理批量PDF生成
- 支持100+条数据的高效处理
- 内存优化，避免泄漏

### 阶段2：核心模块开发

#### 2.1 数据加载模块 (data_loader.py)
- `load_csv(file_path, encoding='auto')` - 读取CSV文件
- `load_excel(file_path)` - 读取Excel文件
- `load_json(file_path)` - 读取JSON文件
- `detect_encoding(file_path)` - 自动检测编码

#### 2.2 PDF处理模块 (pdf_processor.py)
- `read_form_fields(pdf_path)` - 读取表单域
- `fill_form_pdf(pdf_path, data, output_path)` - 填充表单PDF
- `get_text_positions(pdf_path)` - 获取文本位置（非表单）
- `replace_text(pdf_path, replacements, output_path)` - 替换文本

#### 2.3 模板引擎 (template_engine.py)
- `parse_template(content)` - 解析Jinja2模板
- `render_template(template, data)` - 渲染模板
- `detect_fields(pdf_path)` - 检测可替换字段

### 阶段3：CLI和批量处理

#### 3.1 命令行界面
```
pdf-mail-merge.exe --template template.pdf --data data.csv --output output/
pdf-mail-merge.exe --template template.pdf --data data.csv --mode form --output output/
pdf-mail-merge.exe --template template.pdf --data data.csv --mode text --output output/
```

#### 3.2 批量处理
- `batch_process(template, data_source, output_dir, mode)` - 批量生成PDF
- 支持自定义命名规则（如 `{id}_{name}.pdf`）
- 进度显示和统计信息
- ZIP打包功能

### 阶段4：测试和文档

#### 4.1 测试用例
- 数据加载测试（不同编码、不同格式）
- PDF表单填充测试
- 文本替换测试
- 批量处理性能测试
- 错误处理测试

#### 4.2 文档
- README.md：项目介绍、安装、使用说明
- CONTRIBUTING.md：贡献指南
- 示例文件和测试结果

### 阶段5：开源发布

#### 5.1 GitHub仓库设置
- 创建仓库：pdf-mail-merge
- 添加LICENSE（MIT）
- 配置.gitignore
- 设置releases和tags

#### 5.2 发布检查清单
- [ ] 代码审查
- [ ] 测试通过
- [ ] 文档完整
- [ ] 示例可用
- [ ] 版本号标注

## 关键实现细节

### PDF表单处理流程
```
1. 读取PDF → PdfReader
2. 获取表单域 → reader.get_fields()
3. 更新字段值 → fields[field_name].update({"/V": value})
4. 保存PDF → PdfWriter.write()
```

### 文本替换流程
```
1. 使用PyMuPDF提取PDF文本
2. 使用正则匹配 {{field_name}} 模式
3. Jinja2渲染替换内容
4. 使用PyMuPDF覆盖文本（支持中文字体）
5. 保存PDF
```

### 数据映射流程
```
1. 检测PDF模板中的字段（表单域或 {{field}}）
2. 读取数据源（CSV/Excel/JSON）
3. 显示字段映射界面（可选CLI）
4. 验证映射完整性
5. 批量生成PDF
```

## 性能目标

- 处理100条数据 < 60秒
- 内存占用 < 500MB
- 支持并发处理（多进程）
- 跨平台运行（Windows/macOS/Linux）

## 错误处理

- 文件不存在：友好提示，列出检查建议
- 字段不匹配：显示未匹配字段列表
- 编码错误：自动尝试多种编码
- 权限错误：提示输出目录权限
- PDF损坏：跳过并记录，跳转下一条

## 验证标准

1. **功能验证**：
   - 表单PDF：填充后字段值正确显示
   - 文本PDF：`{{name}}` 正确替换为"张三"
   - 批量处理：所有数据行生成对应PDF

2. **性能验证**：
   - 100条数据处理时间
   - 内存占用峰值
   - 并发处理效率

3. **兼容性验证**：
   - PDF 1.4-1.7 版本
   - UTF-8、GBK编码数据
   - Windows/macOS/Linux运行

4. **开源验证**：
   - 代码无硬编码敏感信息
   - 许可证正确
   - 文档完整准确