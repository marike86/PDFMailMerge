"""
交互式终端对话系统 - PDF邮件合并工具
提供引导式输入，用户无需记忆复杂的命令行参数
"""

import os
import sys
import time
from typing import Optional, Callable


class InteractiveCLI:
    """交互式命令行界面 - 引导用户逐步完成配置"""

    # ANSI颜色代码
    COLORS = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bold": "\033[1m",
        "reset": "\033[0m",
    }

    def __init__(self):
        self.config = {
            "template_path": None,
            "data_path": None,
            "output_dir": None,
            "mode": None,
            "naming_pattern": None,
            "zip_enabled": False,
            "clean_output": False,
        }
        self.history = []
        self.max_history = 50

    def print_header(self):
        """打印标题"""
        self.clear_screen()
        print(f"\n{self.COLORS['cyan']}{self.COLORS['bold']}")
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║                                                              ║")
        print("║           PDF邮件合并工具 - 交互式操作界面                    ║")
        print("║           PDF Mail Merge Tool - Interactive Mode             ║")
        print("║                                                              ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print(f"{self.COLORS['reset']}\n")

    def print_section(self, text: str):
        """打印分节标题"""
        print(f"\n{self.COLORS['bold']}{self.COLORS['blue']}{'─' * 60}")
        print(f"  {text}")
        print(f"{'─' * 60}{self.COLORS['reset']}\n")

    def print_success(self, text: str):
        """打印成功消息"""
        print(f"{self.COLORS['green']}✓ {text}{self.COLORS['reset']}")

    def print_error(self, text: str):
        """打印错误消息"""
        print(f"{self.COLORS['red']}✗ {text}{self.COLORS['reset']}")

    def print_warning(self, text: str):
        """打印警告消息"""
        print(f"{self.COLORS['yellow']}⚠ {text}{self.COLORS['reset']}")

    def print_info(self, text: str):
        """打印信息消息"""
        print(f"{self.COLORS['cyan']}ℹ {text}{self.COLORS['reset']}")

    def clear_screen(self):
        """清屏"""
        os.system("cls" if os.name == "nt" else "clear")

    def wait_continue(self):
        """等待用户按键继续"""
        input(f"\n{self.COLORS['yellow']}按Enter键继续...{self.COLORS['reset']}")

    def get_input(
        self,
        prompt: str,
        required: bool = True,
        validator: Optional[Callable] = None,
        default: Optional[str] = None,
        allow_empty: bool = False,
    ) -> Optional[str]:
        """
        获取用户输入并验证

        Args:
            prompt: 提示文本
            required: 是否必填
            validator: 验证函数
            default: 默认值
            allow_empty: 是否允许空输入

        Returns:
            用户输入的字符串，None表示取消
        """
        while True:
            # 显示提示
            if default:
                display = f"{prompt} [{default}]: "
            else:
                display = f"{prompt}: "

            user_input = input(display).strip()

            # 处理空输入
            if not user_input:
                if allow_empty:
                    return default
                if default is not None:
                    user_input = default
                elif required:
                    self.print_warning("此项为必填项，请输入有效信息")
                    continue
                else:
                    return None

            # 移除路径周围的双引号（不影响内部引号）
            cleaned_input = self.clean_path_quotes(user_input)

            # 验证输入
            if validator:
                is_valid, error_msg = validator(cleaned_input)
                if not is_valid:
                    self.print_error(error_msg)
                    retry = input("是否重新输入? (Y/N，默认Y): ").strip().lower()
                    if retry in ["", "y", "yes"]:
                        continue
                    return None

            self.history.append(
                {"prompt": prompt, "value": cleaned_input, "timestamp": time.time()}
            )

            return cleaned_input

    def clean_path_quotes(self, path: str) -> str:
        """
        清理路径周围的引号，不影响内部引号或特殊字符

        处理规则:
        - 移除路径开头和结尾的双引号（如果有）
        - 保留路径内部的引号
        - 清理多余空格
        """
        if not path:
            return path

        cleaned = path.strip()

        if cleaned.startswith('"') and cleaned.endswith('"') and len(cleaned) > 1:
            cleaned = cleaned[1:-1]

        cleaned = " ".join(cleaned.split())

        return cleaned

    def validate_file_exists(self, path: str) -> tuple:
        """验证文件是否存在"""
        if not path:
            return False, "文件路径不能为空"

        if not os.path.exists(path):
            return False, f"文件不存在: {path}\n  请检查路径是否正确"

        if not os.path.isfile(path):
            return False, f"路径不是文件: {path}"

        return True, ""

    def validate_directory_exists(self, path: str) -> tuple:
        """验证目录是否存在或可创建"""
        if not path:
            return False, "目录路径不能为空"

        parent = os.path.dirname(path) or "."
        if not os.path.exists(parent):
            return False, f"上级目录不存在: {parent}"

        return True, ""

    def validate_pdf_file(self, path: str) -> tuple:
        """验证PDF文件"""
        valid, msg = self.validate_file_exists(path)
        if not valid:
            return valid, msg

        if not path.lower().endswith(".pdf"):
            return False, "文件必须是PDF格式 (.pdf)"

        return True, ""

    def validate_data_file(self, path: str) -> tuple:
        """验证数据文件"""
        valid, msg = self.validate_file_exists(path)
        if not valid:
            return valid, msg

        valid_extensions = [".csv", ".xlsx", ".xls", ".json"]
        if not any(path.lower().endswith(ext) for ext in valid_extensions):
            return (
                False,
                f"文件格式不支持。请使用以下格式: {', '.join(valid_extensions)}",
            )

        return True, ""

    def print_menu(self, options: list, title: str = "选项"):
        """打印菜单"""
        self.print_section(title)
        for i, option in enumerate(options, 1):
            print(f"  {self.COLORS['cyan']}{i}{self.COLORS['reset']}. {option}")

    def get_choice(self, options: list, prompt: str = "请选择") -> Optional[int]:
        """获取用户选择"""
        while True:
            choice = input(f"\n{prompt} (1-{len(options)}): ").strip()

            if not choice:
                self.print_warning("请输入有效选项")
                continue

            try:
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return choice_num
                else:
                    self.print_warning(f"请输入1到{len(options)}之间的数字")
            except ValueError:
                self.print_warning("请输入数字")
                continue

    def step_template(self) -> bool:
        """步骤1：选择PDF模板"""
        self.print_section("步骤1: 选择PDF模板")

        print("请提供PDF模板文件的路径")
        print("支持相对路径和绝对路径")
        print("示例:")
        print(
            f"  {self.COLORS['yellow']}相对路径: ./template.pdf, ../../docs/template.pdf{self.COLORS['reset']}"
        )
        print(
            f"  {self.COLORS['yellow']}绝对路径: C:\\Users\\Admin\\template.pdf{self.COLORS['reset']}"
        )
        print(
            f'  {self.COLORS["yellow"]}拖拽路径: "C:\\Users\\Admin\\template.pdf"{self.COLORS["reset"]}'
        )

        # 显示当前配置
        if self.config["template_path"]:
            print(
                f"\n{self.COLORS['green']}当前选择: {self.config['template_path']}{self.COLORS['reset']}"
            )

        # 获取输入
        template = self.get_input(
            "\nPDF模板路径", validator=self.validate_pdf_file, allow_empty=False
        )

        if template is None:
            return False

        self.config["template_path"] = template
        self.print_success(f"已选择模板: {template}")

        # 验证PDF类型
        try:
            from .pdf_processor import get_form_field_names, detect_text_placeholders

            form_fields = get_form_field_names(template)
            text_placeholders = detect_text_placeholders(template)

            print(f"\n{self.COLORS['cyan']}模板分析结果:{self.COLORS['reset']}")

            if form_fields:
                print(f"  发现 {len(form_fields)} 个表单域")
                print(
                    f"  字段名: {', '.join(form_fields[:5])}"
                    + (" ..." if len(form_fields) > 5 else "")
                )

            if text_placeholders:
                print(f"  发现 {len(text_placeholders)} 个文本占位符")
                print(
                    f"  占位符: {', '.join(text_placeholders[:5])}"
                    + (" ..." if len(text_placeholders) > 5 else "")
                )

        except Exception as e:
            print(
                f"\n{self.COLORS['yellow']}警告: 无法分析PDF模板类型: {e}{self.COLORS['reset']}"
            )

        return True

    def step_data(self) -> bool:
        """步骤2：选择数据文件"""
        self.print_section("步骤2: 选择数据文件")

        print("请提供数据源文件的路径")
        print("支持的格式: CSV, Excel (.xlsx/.xls), JSON")
        print("\n示例文件格式:")
        print(f"  {self.COLORS['yellow']}CSV: data.csv{self.COLORS['reset']}")
        print(f"  {self.COLORS['yellow']}Excel: employees.xlsx{self.COLORS['reset']}")
        print(f"  {self.COLORS['yellow']}JSON: records.json{self.COLORS['reset']}")

        if self.config["data_path"]:
            print(
                f"\n{self.COLORS['green']}当前选择: {self.config['data_path']}{self.COLORS['reset']}"
            )

        data = self.get_input(
            "\n数据文件路径", validator=self.validate_data_file, allow_empty=False
        )

        if data is None:
            return False

        self.config["data_path"] = data
        self.print_success(f"已选择数据文件: {data}")

        # 验证数据文件并显示信息
        try:
            from .data_loader import load_data

            df = load_data(data)

            print(f"\n{self.COLORS['cyan']}数据分析结果:{self.COLORS['reset']}")
            print(f"  数据行数: {len(df)}")
            print(f"  数据列数: {len(df.columns)}")
            print(
                f"  列名: {', '.join(df.columns.tolist()[:8])}"
                + (" ..." if len(df.columns) > 8 else "")
            )

        except Exception as e:
            print(
                f"\n{self.COLORS['yellow']}警告: 无法读取数据文件: {e}{self.COLORS['reset']}"
            )

        return True

    def step_output_dir(self) -> bool:
        """步骤3：设置输出目录"""
        self.print_section("步骤3: 设置输出目录")

        print("请指定PDF文件的输出目录")
        print("目录不存在时会自动创建")
        print("\n示例:")
        print(
            f"  {self.COLORS['yellow']}相对路径: ./output, ./pdf_results{self.COLORS['reset']}"
        )
        print(
            f"  {self.COLORS['yellow']}绝对路径: C:\\Users\\Admin\\output{self.COLORS['reset']}"
        )

        if self.config["output_dir"]:
            print(
                f"\n{self.COLORS['green']}当前选择: {self.config['output_dir']}{self.COLORS['reset']}"
            )

        default = self.config["output_dir"] or "./output"

        output = self.get_input(
            "\n输出目录路径",
            validator=self.validate_directory_exists,
            default=default,
            allow_empty=True,
        )

        if output is None:
            return False

        self.config["output_dir"] = output
        self.print_success(f"已设置输出目录: {output}")

        return True

    def step_mode(self) -> bool:
        """步骤4：选择处理模式"""
        self.print_section("步骤4: 选择处理模式")

        print("请选择PDF处理模式:")
        print("\n模式说明:")
        print(f"  {self.COLORS['cyan']}1. 表单模式 (Form Mode){self.COLORS['reset']}")
        print("     - 适用于包含可填充表单域的PDF")
        print("     - 需要使用Adobe Acrobat等工具创建表单域")
        print("     - 数据直接填充到表单域中")

        print(
            f"\n  {self.COLORS['cyan']}2. 文本替换模式 (Text Mode){self.COLORS['reset']}"
        )
        print("     - 适用于普通PDF，包含占位符如 {{name}}, {{email}}")
        print("     - 将占位符替换为实际数据")
        print("     - 无需特殊工具，普通PDF即可")

        print(f"\n  {self.COLORS['cyan']}3. 自动检测 (Auto){self.COLORS['reset']}")
        print("     - 系统自动检测PDF类型")
        print("     - 推荐新手使用")

        choice = self.get_choice(
            ["表单模式 (Form)", "文本替换模式 (Text)", "自动检测 (Auto)"],
            prompt="请选择处理模式",
        )

        if choice is None:
            return False

        mode_map = {1: "form", 2: "text", 3: "auto"}
        self.config["mode"] = mode_map[choice]

        mode_names = {1: "表单模式", 2: "文本替换模式", 3: "自动检测"}
        self.print_success(f"已选择模式: {mode_names[choice]}")

        return True

    def step_naming(self) -> bool:
        """步骤5：设置命名规则"""
        self.print_section("步骤5: 设置输出文件命名规则")

        print("请设置输出PDF文件的命名规则")
        print("\n可用占位符:")
        print(
            f"  {self.COLORS['yellow']}{{row}}{self.COLORS['reset']} - 行号 (1, 2, 3...)"
        )
        print(
            f"  {self.COLORS['yellow']}{{列名}}{self.COLORS['reset']} - 数据列名 (如 {{name}}, {{email}})"
        )
        print(
            f"  {self.COLORS['yellow']}{{timestamp}}{self.COLORS['reset']} - 时间戳 (20240101_120000)"
        )

        print("\n示例:")
        print(
            f"  {self.COLORS['yellow']}document_{{row}}{self.COLORS['reset']} → document_1.pdf, document_2.pdf"
        )
        print(
            f"  {self.COLORS['yellow']}{{name}}_{{row}}{self.COLORS['reset']} → 张三_1.pdf, 李四_2.pdf"
        )
        print(
            f"  {self.COLORS['yellow']}{{company}}_{{name}}{self.COLORS['reset']} → 百度_张三.pdf, 阿里_李四.pdf"
        )

        if self.config["naming_pattern"]:
            print(
                f"\n{self.COLORS['green']}当前规则: {self.config['naming_pattern']}{self.COLORS['reset']}"
            )

        default = self.config["naming_pattern"] or "document_{row}"

        pattern = self.get_input("\n命名规则", default=default, allow_empty=True)

        if pattern is None:
            return False

        self.config["naming_pattern"] = pattern or "document_{row}"
        self.print_success(f"已设置命名规则: {self.config['naming_pattern']}")

        return True

    def step_options(self) -> bool:
        """步骤6：设置其他选项"""
        self.print_section("步骤6: 设置其他选项")

        # ZIP打包选项
        print("是否生成ZIP压缩包?")
        print("  将所有生成的PDF打包成一个ZIP文件，方便分享")

        choice = self.get_choice(["是", "否"], prompt="是否生成ZIP")

        if choice is None:
            return False

        self.config["zip_enabled"] = choice == 1

        if self.config["zip_enabled"]:
            self.print_success("将生成ZIP压缩包")
        else:
            self.print_info("不生成ZIP压缩包")

        # 清空输出目录选项
        print("\n处理前是否清空输出目录?")
        print("  清空目录可确保输出文件不会与历史文件混淆")

        choice = self.get_choice(["是", "否"], prompt="是否清空输出目录")

        if choice is None:
            return False

        self.config["clean_output"] = choice == 1

        if self.config["clean_output"]:
            self.print_warning("将在处理前清空输出目录")
        else:
            self.print_info("将保留输出目录中的现有文件")

        return True

    def step_summary(self) -> bool:
        """步骤7：显示摘要并确认"""
        self.print_section("配置摘要")

        print(f"\n{self.COLORS['bold']}请确认以下配置:{self.COLORS['reset']}\n")

        print(f"{self.COLORS['cyan']}1. PDF模板:{self.COLORS['reset']}")
        print(f"   {self.config['template_path']}")

        print(f"\n{self.COLORS['cyan']}2. 数据文件:{self.COLORS['reset']}")
        print(f"   {self.config['data_path']}")

        print(f"\n{self.COLORS['cyan']}3. 输出目录:{self.COLORS['reset']}")
        print(f"   {self.config['output_dir']}")

        print(f"\n{self.COLORS['cyan']}4. 处理模式:{self.COLORS['reset']}")
        mode_names = {"form": "表单模式", "text": "文本替换模式", "auto": "自动检测"}
        print(f"   {mode_names.get(self.config['mode'], self.config['mode'])}")

        print(f"\n{self.COLORS['cyan']}5. 命名规则:{self.COLORS['reset']}")
        print(f"   {self.config['naming_pattern']}")

        print(f"\n{self.COLORS['cyan']}6. 其他选项:{self.COLORS['reset']}")
        print(f"   ZIP压缩包: {'是' if self.config['zip_enabled'] else '否'}")
        print(f"   清空输出: {'是' if self.config['clean_output'] else '否'}")

        print(f"\n{self.COLORS['bold']}{'─' * 60}")

        while True:
            confirm = input("\n确认以上配置并开始处理? (Y/N): ").strip().lower()

            if confirm in ["y", "yes", "是", "确认"]:
                return True
            elif confirm in ["n", "no", "否", "取消"]:
                print("\n已取消执行")
                return False
            else:
                self.print_warning("请输入 Y (确认) 或 N (取消)")

    def step_process(self) -> bool:
        """Use the same validation and output rules as the desktop."""
        from .merge_service import inspect_inputs, run_merge
        self.print_section("正在处理...")
        try:
            plan = inspect_inputs(self.config["template_path"], self.config["data_path"], self.config["mode"])
            result = run_merge(
                plan, self.config["output_dir"], self.config["naming_pattern"],
                zip_enabled=self.config["zip_enabled"], clean=self.config["clean_output"],
                data_path=self.config["data_path"],
                progress=lambda current, total, message: print(f"{current}/{total}  {message}"),
            )
            print(f"处理完成: 成功 {len(result.files)}，失败 {len(result.errors)}")
            for error in result.errors:
                self.print_error(error)
            return not result.errors and not result.cancelled
        except (Exception, KeyboardInterrupt) as exc:
            self.print_error(str(exc))
            return False

    def run_interactive(self):
        """运行交互式对话"""
        while True:
            try:
                self.print_header()

                print(
                    f"{self.COLORS['yellow']}欢迎使用PDF邮件合并工具!{self.COLORS['reset']}"
                )
                print("本工具将引导您完成所有配置，无需记忆复杂的命令行参数\n")

                print("操作说明:")
                print("  - 输入信息后按Enter确认")
                print("  - 输入 N 取消当前步骤")
                print("  - 输入 Q 退出程序")
                print("  - 支持拖拽文件到终端")
                print("  - 路径两端的引号会自动移除\n")

                input("按Enter键开始...")

                steps = [
                    ("选择PDF模板", self.step_template),
                    ("选择数据文件", self.step_data),
                    ("设置输出目录", self.step_output_dir),
                    ("选择处理模式", self.step_mode),
                    ("设置命名规则", self.step_naming),
                    ("设置其他选项", self.step_options),
                    ("确认配置", self.step_summary),
                ]

                restart = False
                for step_name, step_func in steps:
                    if not step_func():
                        retry = input("\n是否重新开始? (Y/N): ").strip().lower()
                        if retry in ["y", "yes", "是", ""]:
                            self.config = {
                                "template_path": None,
                                "data_path": None,
                                "output_dir": None,
                                "mode": None,
                                "naming_pattern": None,
                                "zip_enabled": False,
                                "clean_output": False,
                            }
                            self.history = []
                            restart = True
                            break
                        else:
                            print("\n已退出程序")
                            return False

                if restart:
                    self.print_header()
                    print("已重置配置，请重新开始\n")
                    continue

                if self.step_process():
                    print("\n感谢使用PDF邮件合并工具!")
                else:
                    print("\n处理未完成")

                return True

            except KeyboardInterrupt:
                print(f"\n\n{self.COLORS['yellow']}程序已退出{self.COLORS['reset']}")
                return False

    def run(self, args=None):
        """运行CLI - 支持交互模式和参数模式"""
        # 如果没有参数或只有 --interactive，运行交互模式
        if args is None or len(args) == 0 or "--interactive" in args:
            return 0 if self.run_interactive() else 1

        # 否则运行传统的参数模式
        from .cli import MailMergeCLI as BaseCLI

        base_cli = BaseCLI()
        return base_cli.run(args)


def main():
    """主入口"""
    cli = InteractiveCLI()

    if "--interactive" in sys.argv or len(sys.argv) == 1:
        sys.exit(cli.run(["--interactive"]))
    else:
        sys.exit(cli.run(sys.argv[1:]))


if __name__ == "__main__":
    main()
