"""
HTML to Markdown 转换器
使用 markdownify 库将 HTML 文件转换为 Markdown 格式
"""

import os
from pathlib import Path
from markdownify import markdownify as md


def convert_html_to_markdown(html_file_path, output_dir):
    """
    将单个HTML文件转换为Markdown

    Args:
        html_file_path (str): HTML文件路径
        output_dir (str): 输出目录路径
    """
    try:
        # 读取HTML文件
        with open(html_file_path, "r", encoding="utf-8") as file:
            html_content = file.read()

        # 转换为Markdown
        markdown_content = md(html_content)  # 移除脚本和样式标签

        # 获取文件名（不含扩展名）
        file_name = Path(html_file_path).stem

        # 创建输出文件路径
        output_file = Path(output_dir) / f"{file_name}.md"

        # 写入Markdown文件
        with open(output_file, "w", encoding="utf-8") as file:
            file.write(markdown_content)

        print(f"✅ 成功转换: {html_file_path} -> {output_file}")
        return True

    except Exception as e:
        print(f"❌ 转换失败 {html_file_path}: {str(e)}")
        return False


def batch_convert_html_to_markdown(html_dir, output_dir):
    """
    批量转换HTML文件为Markdown

    Args:
        html_dir (str): HTML文件目录
        output_dir (str): 输出目录
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 获取HTML文件列表
    html_files = list(Path(html_dir).glob("*.html"))

    if not html_files:
        print(f"在目录 {html_dir} 中没有找到HTML文件")
        return

    print(f"找到 {len(html_files)} 个HTML文件，开始转换...")
    print("-" * 50)

    success_count = 0
    total_count = len(html_files)

    # 逐个转换文件
    for html_file in html_files:
        if convert_html_to_markdown(html_file, output_dir):
            success_count += 1

    print("-" * 50)
    print(f"转换完成！成功: {success_count}/{total_count}")


def main():
    """主函数"""
    # 设置路径
    current_dir = Path(__file__).parent.parent  # 获取项目根目录
    html_dir = current_dir / "html"  # HTML文件目录
    output_dir = current_dir / "markdown"  # 输出目录

    print("HTML to Markdown 转换器")
    print("=" * 50)
    print(f"HTML目录: {html_dir}")
    print(f"输出目录: {output_dir}")
    print("=" * 50)

    # 检查HTML目录是否存在
    if not html_dir.exists():
        print(f"❌ HTML目录不存在: {html_dir}")
        return

    # 执行批量转换
    batch_convert_html_to_markdown(html_dir, output_dir)


if __name__ == "__main__":
    main()
