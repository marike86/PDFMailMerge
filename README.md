# PDF Mail Merge 2.0

中文 PDF 批量合并工具，提供 WinUI 3 / Fluent 风格桌面界面和 Windows x64 便携版。

界面基于 **PySide6 / Qt Widgets**，采用 Windows 11 风格的侧栏、圆角卡片和蓝色操作按钮；并非原生 WinUI 3 控件。

## 便携版

下载构建产物 `PDFMailMerge-2.0.0-windows-x64-portable.zip`，解压整个 `PDFMailMerge` 文件夹，双击 `PDFMailMerge.exe`。

- Windows 10 1809 / Windows 11，x64；无需安装 Python、.NET 或 Windows App SDK。
- 保留 `_internal` 文件夹；不能只复制 EXE。
- 程序在本地处理文件，无需联网，不保存账号或凭据。
- 自带 `examples` 演示模板和数据，可先试用再导入自己的文件。

## 桌面操作

1. 在「导入与设置」选择 PDF 模板和 CSV、XLSX、XLS 或 JSON 数据，点击「加载并检查」。
2. 在「字段映射」把模板字段关联到数据列。同名字段自动匹配，未映射时禁止生成。
3. 点击「预览效果」检查所选记录；底部页码支持查看多页 PDF。
4. 选择输出目录及文件名规则，点击「开始批量生成」。
5. 在「生成结果」查看成功数及错误原因，或打开结果文件夹。

文件名支持 `{row}`、`{timestamp}` 和 `{数据列名}`，例如 `{id}_{name}`。重名文件自动添加编号，已有文件保留。ZIP 只包含本次成功生成的 PDF。取消会在当前文档处理完成后停止，保留已完成结果。

## 模板与数据

- **表单模式**：填充 PDF AcroForm 的文本、选择和勾选字段，保留可编辑字段；中文文本字段会嵌入字体。勾选值支持 `true/false`、`1/0`、`是/否` 或模板中的导出值。
- **文本模式**：替换 `{{name}}` 或 `{{ 姓名 }}` 形式的单行占位符。保留周边文字、图片、线条和背景；优先保持原字号，必要时缩小到不低于 6pt。
- 文本模式使用右侧可用空间，过长或多行值会明确报错。复杂排版建议改用表单模板。
- CSV 自动识别 UTF-8 / GB18030 等编码；CSV 和 Excel 的文本编号保留前导零，缺失单元格写为空字符串。
- Excel 中以数值存储、仅通过单元格格式显示前导零的编号，请先转为文本。
- JSON 支持对象数组、单个对象或 `{"data": [...]}`。
- 不支持扫描件 OCR、需要密码的 PDF、签名字段写入或跨行占位符。已签名 PDF 的内容修改可能影响原有签名。
- 文本替换支持拉丁文字及 CJK 字体包含的字符；复杂文字、旋转占位符和特殊模板请先预览确认。

## 从源码运行

Python 3.14 x64 为当前验证环境。依赖要求 Python 3.10+；其他版本需自行验证对应安装包。

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements-lock.txt
python main.py
```

也可安装 `requirements.txt` 允许范围内的依赖；`requirements-lock.txt` 记录本次便携版实际使用的版本。

## 命令行

```powershell
python -m src.cli --template examples/invitation_template.pdf --data examples/demo_data.csv --output ./output --mode auto --name "{id}_{name}" --zip
python -m src.cli --template template.pdf --data data.csv --mapping "name=姓名,email=邮箱" --validate-only
```

便携包内 `PDFMailMerge-CLI.exe` 支持相同参数。`--validate-only` 不写入或清理输出目录；未匹配字段直接返回错误，不再等待交互输入。`--clean` 仅供明确需要清空结果目录的命令行任务使用，并禁止清空包含输入文件的目录。旧版终端引导仍可通过 `python main.py --interactive` 使用。

Python API：

```python
from src.merge_service import inspect_inputs, run_merge
plan = inspect_inputs('template.pdf', 'data.csv', mapping={'name': '姓名'})
result = run_merge(plan, './output', pattern='{row}_{姓名}')
print(result.files, result.errors)
```

## 测试与构建

```powershell
python -m pip install -r requirements-dev.txt
python -m pytest -q
python -m ruff check src main.py scripts tests/test_gui.py tests/test_regressions.py --select F
./build.ps1
./dist/PDFMailMerge/PDFMailMerge-CLI.exe --self-test ./dist/self-test
```

`--self-test` 自动完成导入、预览、生成 3 份 PDF 和 ZIP，保存界面截图与 JSON 结果，并通过退出码报告成功或失败。无需网络。

GitHub Actions 自动运行测试、构建便携 ZIP 并验证打包后的桌面程序。构建产物包含源码 ZIP、示例、依赖版本和第三方许可说明。

## 许可

本仓库原有代码使用 [MIT](LICENSE) 许可；打包依赖保留各自许可。PyMuPDF / MuPDF 使用 AGPL-3.0 或商业许可，PySide6 / Qt 提供 LGPL / GPL 或商业许可。查看 [第三方说明](THIRD_PARTY_NOTICES.md) 和 `licenses/`；便携包也包含对应的应用源码。
