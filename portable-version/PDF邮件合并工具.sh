#!/bin/bash
# PDF邮件合并工具 - Linux/macOS启动脚本
# Portable Version v1.0.0

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印标题
print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  PDF邮件合并工具 - 开箱即用版 v1.0.0${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
}

# 检查Python环境
check_python() {
    echo -e "${YELLOW}正在检查Python环境...${NC}"
    
    # 检查绑定的Python
    if [ -f "$SCRIPT_DIR/Python/bin/python" ]; then
        PYTHON="$SCRIPT_DIR/Python/bin/python"
        echo -e "${GREEN}[OK] 找到绑定的Python环境${NC}"
    elif command -v python3 &> /dev/null; then
        PYTHON="python3"
        echo -e "${GREEN}[OK] 使用系统Python环境${NC}"
    elif command -v python &> /dev/null; then
        PYTHON="python"
        echo -e "${GREEN}[OK] 使用系统Python环境${NC}"
    else
        echo -e "${RED}[ERROR] 未找到Python环境！${NC}"
        echo ""
        echo "请确保已正确解压软件包，或安装Python 3.8+"
        echo "下载地址：https://www.python.org/downloads/"
        echo ""
        read -p "按Enter键退出..."
        exit 1
    fi
    
    # 显示Python版本
    echo ""
    $PYTHON --version
    echo ""
}

# 检查依赖
check_dependencies() {
    echo -e "${YELLOW}正在检查依赖库...${NC}"
    
    $PYTHON -c "import pypdf, pandas, jinja2, chardet, openpyxl" 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}[WARNING] 缺少依赖库，正在安装...${NC}"
        $PYTHON -m pip install --quiet pypdf pandas jinja2 chardet openpyxl PyMuPDF
        
        if [ $? -ne 0 ]; then
            echo -e "${RED}[ERROR] 依赖安装失败！${NC}"
            echo "请检查网络连接后重试"
            read -p "按Enter键退出..."
            exit 1
        fi
        
        echo -e "${GREEN}[OK] 依赖安装完成${NC}"
    else
        echo -e "${GREEN}[OK] 所有依赖已就绪${NC}"
    fi
    
    echo ""
}

# 显示主菜单
show_menu() {
    clear
    print_header
    
    echo "  1. 图形界面模式（推荐给初学者）"
    echo "  2. 命令行模式（适合高级用户）"
    echo "  3. 查看帮助文档"
    echo "  4. 运行测试"
    echo "  5. 检查更新"
    echo "  0. 退出"
    echo ""
    echo -e "${BLUE}================================================${NC}"
    read -p "请输入选项 (0-5): " choice
    
    case $choice in
        1) gui_mode ;;
        2) cli_mode ;;
        3) help_doc ;;
        4) run_tests ;;
        5) check_update ;;
        0) exit_program ;;
        *) 
            echo "无效选项，请重新选择"
            sleep 2
            show_menu
            ;;
    esac
}

# 图形界面模式
gui_mode() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  图形界面模式${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo "正在启动图形界面..."
    echo ""
    echo "[提示] 如果没有图形界面，将启动命令行模式"
    echo ""
    
    # 尝试启动GUI（如果有）
    $PYTHON -m app.src.gui 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}[INFO] 图形界面未实现，将启动命令行模式${NC}"
        echo ""
        cli_mode
    fi
    
    read -p "按Enter键返回菜单..."
    show_menu
}

# 命令行模式
cli_mode() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  命令行模式${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo "请输入命令行参数，或按Enter使用默认参数："
    echo "格式：--template 模板.pdf --data 数据.csv --output ./output"
    echo ""
    read -p "参数: " args
    
    if [ -z "$args" ]; then
        args="--template template.pdf --data data.csv --output ./output"
    fi
    
    echo ""
    echo "正在执行：$args"
    echo ""
    
    $PYTHON -m app.src.cli $args
    
    echo ""
    read -p "按Enter键返回菜单..."
    show_menu
}

# 帮助文档
help_doc() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  帮助文档${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo "可用文档："
    echo "  1. 使用说明 (使用说明.txt)"
    echo "  2. 快速开始 (docs/QUICK_START.md)"
    echo "  3. 命令参考 (docs/COMMAND_REFERENCE.md)"
    echo "  4. 故障排除 (docs/TROUBLESHOOTING.md)"
    echo "  5. 用户指南 (docs/USER_GUIDE_CN.md)"
    echo ""
    read -p "请选择 (1-5): " doc_choice
    
    case $doc_choice in
        1) cat "使用说明.txt" ;;
        2) cat "docs/QUICK_START.md" ;;
        3) cat "docs/COMMAND_REFERENCE.md" ;;
        4) cat "docs/TROUBLESHOOTING.md" ;;
        5) cat "docs/USER_GUIDE_CN.md" ;;
        *) echo "无效选项" ;;
    esac
    
    echo ""
    read -p "按Enter键返回菜单..."
    show_menu
}

# 运行测试
run_tests() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  运行测试${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo "正在运行测试套件..."
    echo ""
    
    $PYTHON tests/test_data_loader.py
    echo ""
    $PYTHON tests/test_pdf_processor.py
    echo ""
    $PYTHON tests/test_template_engine.py
    echo ""
    
    read -p "按Enter键返回菜单..."
    show_menu
}

# 检查更新
check_update() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  检查更新${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo "当前版本：v1.0.0"
    echo "发布日期：2026-05-18"
    echo ""
    echo -e "${GREEN}[INFO] 这是一个开源项目，如需更新请访问：${NC}"
    echo "   https://github.com/yourusername/pdf-mail-merge"
    echo ""
    
    read -p "按Enter键返回菜单..."
    show_menu
}

# 退出程序
exit_program() {
    clear
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  感谢使用 PDF邮件合并工具！${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    exit 0
}

# 主程序
main() {
    print_header
    check_python
    check_dependencies
    show_menu
}

# 执行主程序
main