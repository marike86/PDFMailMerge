# PDF邮件合并工具 - 交互式操作指南

## 📖 概述

PDF邮件合并工具现已提供**交互式终端对话系统**，让您无需记忆复杂的命令行参数，通过清晰的引导式界面完成所有配置。

---

## 🚀 快速开始

### Windows系统

#### 方法1：双击启动器（推荐）

1. 进入 `script-version` 或 `portable-version` 目录
2. 双击 `PDF邮件合并工具.exe.bat`（脚本版本）或 `启动器.bat`（便携版本）
3. 选择菜单 `1` 进入交互式操作
4. 按照提示逐步完成配置

#### 方法2：命令行启动

```bash
# 进入目录
cd script-version

# 运行交互式界面
python -m src.interactive_cli --interactive

# 或直接运行启动器
PDF邮件合并工具.exe.bat
```

### Linux/macOS系统

```bash
# 进入目录
cd script-version

# 添加执行权限
chmod +x PDF邮件合并工具.sh

# 运行交互式界面
./PDF邮件合并工具.sh
# 选择选项1进入交互式操作

# 或直接运行Python模块
python3 -m src.interactive_cli --interactive
```

---

## 🎯 交互式操作流程

### 步骤1：选择PDF模板

```
请输入PDF模板文件的路径
示例:
  - 相对路径: ./template.pdf, ../../docs/template.pdf
  - 绝对路径: C:\Users\Admin\template.pdf
  - 拖拽路径: "C:\Users\Admin\template.pdf" (引号会自动移除)

PDF模板路径: _
```

**输入验证**：
- ✅ 检查文件是否存在
- ✅ 验证文件扩展名为 `.pdf`
- ✅ 自动移除路径两端的引号
- ✅ 支持拖拽粘贴

---

### 步骤2：选择数据文件

```
请输入数据文件路径
支持格式: CSV (.csv), Excel (.xlsx/.xls), JSON (.json)
示例:
  - data.csv
  - C:\Users\Admin\data.xlsx

数据文件路径: _
```

**输入验证**：
- ✅ 检查文件是否存在
- ✅ 验证文件格式
- ✅ 自动移除引号
- ✅ 显示数据统计（行数、列名）

---

### 步骤3：设置输出目录

```
请指定PDF文件的输出目录
目录不存在时会自动创建
示例:
  - ./output
  - C:\Users\Admin\output

输出目录路径: _ (直接回车使用 ./output)
```

---

### 步骤4：选择处理模式

```
请选择处理模式:

  1. 表单模式 (Form Mode)
     - 适用于包含可填充表单域的PDF
     - 需要使用Adobe Acrobat等工具创建表单域
     - 数据直接填充到表单域中

  2. 文本替换模式 (Text Mode)
     - 适用于普通PDF，包含占位符如 {{name}}, {{email}}
     - 将占位符替换为实际数据
     - 无需特殊工具，普通PDF即可

  3. 自动检测 (Auto)
     - 系统自动检测PDF类型
     - 推荐新手使用

请选择处理模式 (1-3): _
```

---

### 步骤5：设置命名规则

```
请设置输出PDF文件的命名规则

可用占位符:
  {row}       - 行号 (1, 2, 3...)
  {列名}      - 数据列名 (如 {name}, {email})
  {timestamp} - 时间戳 (20240101_120000)

示例:
  - document_{row}       → document_1.pdf, document_2.pdf
  - {name}_{row}        → 张三_1.pdf, 李四_2.pdf
  - {company}_{name}    → 百度_张三.pdf, 阿里_李四.pdf

命名规则: _ (直接回车使用 document_{row})
```

---

### 步骤6：设置其他选项

```
是否生成ZIP压缩包?
  将所有生成的PDF打包成一个ZIP文件，方便分享

是否生成ZIP (1-2): 1. 是  2. 否

是否清空输出目录?
  清空目录可确保输出文件不会与历史文件混淆

是否清空输出 (1-2): 1. 是  2. 否
```

---

### 步骤7：确认并执行

```
═══════════════════════════════════════════════════════════════
                    配置摘要
═══════════════════════════════════════════════════════════════

  1. PDF模板:     C:\Users\Admin\template.pdf
  2. 数据文件:    C:\Users\Admin\data.csv
  3. 输出目录:    C:\Users\Admin\output
  4. 处理模式:    自动检测
  5. 命名规则:    document_{row}
  6. 其他选项:
     ZIP压缩包: 是
     清空输出: 否

═══════════════════════════════════════════════════════════════

确认以上配置并开始处理? (Y/N): _
```

输入 `Y` 确认执行，输入 `N` 取消并返回主菜单。

---

## 🔧 输入验证功能

### 路径处理

```python
# 自动移除路径两端的引号
输入: "C:\Users\Admin\template.pdf"
处理: C:\Users\Admin\template.pdf

# 保留内部引号和特殊字符
输入: C:\Users\"Admin"\template.pdf
处理: C:\Users\"Admin"\template.pdf

# 自动去除多余空格
输入: "  C:\Users\Admin\template.pdf  "
处理: C:\Users\Admin\template.pdf
```

### 格式验证

| 输入类型 | 验证规则 | 错误提示 |
|---------|----------|----------|
| PDF模板 | `.pdf` 扩展名 | "文件必须是PDF格式" |
| 数据文件 | `.csv/.xlsx/.xls/.json` | "不支持的格式" |
| 目录路径 | 父目录存在或可创建 | "上级目录不存在" |

### 错误恢复

```
错误: 文件不存在: template.pdf

请选择操作:
  1. 重新输入路径
  2. 返回上一步
  3. 取消操作
```

---

## 📊 交互式界面特性

### 1. 清晰的视觉引导

- 使用颜色区分不同类型的信息
- 进度条显示处理进度
- 分节标题清晰划分功能区域

### 2. 智能默认选项

- 跳过只需按Enter的选项
- 记住上次的选择
- 提供合理的默认值

### 3. 实时反馈

- 每个步骤完成后显示确认信息
- 检测到问题立即提示
- 处理进度实时更新

### 4. 灵活导航

- 输入 `N` 取消当前步骤
- 输入 `Q` 退出程序
- 可以返回上一步修改

---

## 🎨 用户体验优化

### 之前（旧方法）

```bash
# 复杂且容易出错的命令行
python -m src.cli --template "C:\Users\Admin\template.pdf" --data data.csv --output ./output --mode form --name "{name}_{row}" --zip --clean --verbose

# 常见错误：
# - 引号使用不当导致路径错误
# - 参数顺序搞混
# - 忘记必需的参数
# - 拼写错误
```

### 现在（新方法）

```
步骤1: 选择PDF模板
PDF模板路径: C:\Users\Admin\template.pdf

步骤2: 选择数据文件
数据文件路径: data.csv

步骤3: 设置输出目录
输出目录路径: ./output

步骤4-7: 按照提示完成配置
```

---

## 📝 命令行兼容模式

交互式系统仍然支持传统命令行参数：

```bash
# 交互式模式（默认）
python -m src.interactive_cli --interactive

# 命令行模式（兼容旧方法）
python -m src.interactive_cli -t template.pdf -d data.csv

# 混合模式（部分参数+提示）
python -m src.interactive_cli --template template.pdf
# 缺少的参数会通过交互式提示获取
```

---

## 🔍 故障排除

### 问题1：输入路径包含空格

**解决方案**：
```
输入: C:\Program Files\template.pdf
系统自动处理，无需额外引号

如果仍然出错，手动添加引号：
输入: "C:\Program Files\template.pdf"
系统会自动移除两端引号
```

### 问题2：文件格式验证失败

**解决方案**：
```
确保文件扩展名正确：
- PDF文件: .pdf
- CSV文件: .csv
- Excel文件: .xlsx 或 .xls
- JSON文件: .json
```

### 问题3：路径包含特殊字符

**解决方案**：
```
系统会自动处理以下特殊字符：
- 空格
- 中文路径
- 括号、连字符等

如果出现问题，尝试：
1. 使用绝对路径
2. 将文件移动到简单路径
3. 重命名文件（避免特殊字符）
```

---

## 🎯 最佳实践

### 1. 准备阶段

```bash
# 整理文件结构
project/
├── template.pdf          # PDF模板
├── data.csv              # 数据文件
└── output/               # 输出目录
```

### 2. 执行阶段

```
1. 先验证模板和数据文件
2. 使用自动检测模式简化配置
3. 首次使用建议生成ZIP备份
```

### 3. 完成后

```
检查 output 目录中的文件
确认PDF内容正确
如有问题，查看 logs/ 目录中的日志
```

---

## 📞 获取帮助

### 查看帮助文档

```bash
# 在启动器菜单中选择"5. 查看帮助"
# 或直接查看文档：
docs/USER_GUIDE_CN.md
docs/TROUBLESHOOTING.md
```

### 常见问题

**Q: 如何处理中文路径？**
A: 系统完全支持中文路径，无需特殊处理。

**Q: 输入错误如何修改？**
A: 输入 `N` 取消当前输入，系统会提示重新输入或返回上一步。

**Q: 可以中途退出吗？**
A: 可以，随时输入 `Q` 退出程序。

---

**最后更新**：2026-05-18  
**版本**：2.0  
**新增功能**：交互式终端对话系统