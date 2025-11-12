import base64
import re
from pathlib import Path

from markitdown import MarkItDown


# 直接指定图片目录为 C:\Learning\Code\PythonCode\images
IMAGE_DIR_NAME = "../images"  # 相对于markdown目录的路径


def _save_embedded_images(markdown_text: str, output_file: Path) -> str:
    pattern = re.compile(
        r"(!\[[^\]]*\]\()data:image/(?P<mime>[^;]+);base64,(?P<data>[^)]+)\)",
        re.IGNORECASE,
    )

    # 使用固定的图片目录 C:\Learning\Code\PythonCode\images
    images_dir = Path("C:/Learning/Code/PythonCode/images")
    counter = 1

    def repl(match: re.Match[str]) -> str:
        nonlocal counter
        mime = match.group("mime").lower()
        data = re.sub(r"\s+", "", match.group("data"))

        ext_map = {
            "jpeg": "jpg",
            "jpg": "jpg",
            "png": "png",
            "gif": "gif",
            "bmp": "bmp",
            "webp": "webp",
        }
        ext = ext_map.get(mime, mime.replace("image/", ""))

        if not images_dir.exists():
            images_dir.mkdir(parents=True, exist_ok=True)

        image_name = f"{output_file.stem}_img{counter}.{ext}"
        image_path = images_dir / image_name

        image_bytes = base64.b64decode(data)
        image_path.write_bytes(image_bytes)

        counter += 1
        # 使用相对于markdown目录的路径 ../images/
        relative_path = Path("../images") / image_name
        return f"{match.group(1)}{relative_path.as_posix()})"

    return pattern.sub(repl, markdown_text)


def convert(input_file: Path, output_file: Path | None = None) -> Path:
    if not input_file.exists():
        raise FileNotFoundError(f"输入文件不存在: {input_file}")

    # 默认将输出文件放在 C:\Learning\Code\PythonCode\markdown 目录
    if output_file is None:
        markdown_dir = Path("C:/Learning/Code/PythonCode/markdown")
        markdown_dir.mkdir(parents=True, exist_ok=True)
        output_file = markdown_dir / (input_file.stem + ".md")
    elif output_file.is_dir():
        output_file = output_file / (input_file.stem + ".md")

    markdown = MarkItDown().convert(str(input_file), keep_data_uris=True)
    content = _save_embedded_images(markdown.text_content, output_file)

    output_file.write_text(content, encoding="utf-8")
    return output_file


def main() -> None:
    # 直接在代码中配置输入和输出路径，无需命令行参数
    # 请根据实际需要修改以下路径
    input_path = "C:\\Users\\Cbiltps\Downloads\\SCIDC PF 8.5 01 应对风险和机遇控制程序.docx"  # 修改为实际的输入文件路径
    # input_path = "C:\\Users\\Cbiltps\\Downloads\\SCIDC PF 8.5 01 应对风险和机遇控制程序.docx"  # 修改为实际的输入文件路径

    output_path = None  # 可选，修改为指定的输出路径，或保持为 None 使用默认路径

    input_file = Path(input_path).expanduser().resolve()
    output_file = (
        Path(output_path).expanduser().resolve() if output_path is not None else None
    )

    result_path = convert(input_file, output_file)
    print(f"转换完成，Markdown 已保存到: {result_path}")


if __name__ == "__main__":
    main()
