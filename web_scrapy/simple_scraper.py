"""
简化版网页爬取工具
直接使用requests库爬取网页HTML内容并保存
"""

import os
from urllib.parse import urlparse, urljoin
import re

from requests import get, exceptions
import zstandard as zstd
from bs4 import BeautifulSoup
from markdownify import markdownify as md

# URL 配置入口：将要爬取的网站写在这里
TARGET_URL_SIMPLE = (
    "https://www.runoob.com/java/java-override-overload.html"  # 修改为你要爬取的网页URL
)


def clean_filename(title, url):
    """清理文件名，移除特殊字符"""
    if not title or title.strip() == "":
        # 如果没有标题，使用域名
        parsed_url = urlparse(url)
        title = parsed_url.netloc.replace("www.", "")

    # 移除特殊字符
    safe_title = "".join(
        c for c in title if c.isalnum() or c in (" ", "-", "_", ".")
    ).strip()

    # 限制长度
    if len(safe_title) > 100:
        safe_title = safe_title[:100]

    return safe_title.replace(" ", "_")


def download_image(img_url, save_dir, index, headers):
    """
    下载单个图片

    Args:
        img_url (str): 图片URL
        save_dir (str): 保存目录
        index (int): 图片序号（用于去重时的后缀）
        headers (dict): 请求头

    Returns:
        str: 成功返回本地文件名，失败返回None
    """
    try:
        response = get(img_url, headers=headers, timeout=30)
        response.raise_for_status()

        # 从URL中提取原始文件名
        parsed_url = urlparse(img_url)
        original_filename = os.path.basename(parsed_url.path)
        
        # 如果URL路径没有文件名，使用默认名称
        if not original_filename or '.' not in original_filename:
            # 从Content-Type获取扩展名
            content_type = response.headers.get("Content-Type", "")
            if "jpeg" in content_type or "jpg" in content_type:
                ext = ".jpg"
            elif "png" in content_type:
                ext = ".png"
            elif "gif" in content_type:
                ext = ".gif"
            elif "webp" in content_type:
                ext = ".webp"
            else:
                ext = ".jpg"
            original_filename = f"image_{index:03d}{ext}"
        else:
            # 清理文件名中的特殊字符
            original_filename = clean_filename(original_filename, img_url)
        
        # 检查文件是否已存在，如果存在则添加序号
        filepath = os.path.join(save_dir, original_filename)
        if os.path.exists(filepath):
            name, ext = os.path.splitext(original_filename)
            original_filename = f"{name}_{index}{ext}"
            filepath = os.path.join(save_dir, original_filename)

        with open(filepath, "wb") as f:
            f.write(response.content)

        print(f"  ✓ 下载图片: {original_filename} ({len(response.content)} bytes)")
        return original_filename  # 返回文件名

    except Exception as e:
        print(f"  ✗ 下载图片失败 {img_url}: {e}")
        return None


def extract_and_download_images(html_content, base_url, headers):
    """
    从HTML中提取并下载所有图片，保持图片顺序和位置

    Args:
        html_content (str): HTML内容
        base_url (str): 网页基础URL
        headers (dict): 请求头

    Returns:
        tuple: (成功下载的图片数量, 图片URL到本地文件名的映射字典)
    """
    # 创建images文件夹
    images_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images")
    os.makedirs(images_dir, exist_ok=True)

    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # 查找所有图片标签
    img_tags = soup.find_all("img")
    print(f"\n🔍 发现 {len(img_tags)} 个图片标签")

    # 使用列表保持图片顺序，使用字典去重
    img_url_to_filename = {}  # URL -> 本地文件名的映射
    img_urls_ordered = []  # 按出现顺序的URL列表

    # 从img标签提取URL，保持顺序
    for img in img_tags:
        # 尝试多个可能的属性
        for attr in ["src", "data-src", "data-original", "data-lazy-src"]:
            img_url = img.get(attr)
            if img_url and isinstance(img_url, str):
                # 转换为绝对URL
                absolute_url = urljoin(base_url, img_url)
                # 如果这个URL还没有被记录，添加到列表中
                if absolute_url not in img_url_to_filename:
                    img_urls_ordered.append(absolute_url)
                    img_url_to_filename[absolute_url] = None  # 先占位
                break  # 找到第一个有效属性后就退出

    print(f"📸 共找到 {len(img_urls_ordered)} 个唯一图片URL（按HTML中出现顺序）")

    if not img_urls_ordered:
        print("⚠️  未找到任何图片")
        return 0, {}

    # 下载所有图片，保持顺序
    success_count = 0
    for index, img_url in enumerate(img_urls_ordered, 1):
        # 下载图片并获取本地文件名
        local_filename = download_image(img_url, images_dir, index, headers)
        if local_filename:
            img_url_to_filename[img_url] = local_filename
            success_count += 1

    return success_count, img_url_to_filename


def convert_html_to_markdown_with_local_images(html_content, base_url, img_url_mapping, output_path):
    """
    将HTML转换为Markdown，并将图片URL替换为本地路径

    Args:
        html_content (str): HTML内容
        base_url (str): 网页基础URL
        img_url_mapping (dict): 图片URL到本地文件名的映射
        output_path (str): 输出Markdown文件路径

    Returns:
        bool: 转换是否成功
    """
    try:
        # 使用BeautifulSoup解析HTML，替换图片URL
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 替换所有img标签的src属性
        img_tags = soup.find_all("img")
        replaced_count = 0
        
        for img in img_tags:
            # 尝试多个可能的属性
            for attr in ["src", "data-src", "data-original", "data-lazy-src"]:
                img_url = img.get(attr)
                if img_url and isinstance(img_url, str):
                    # 转换为绝对URL
                    absolute_url = urljoin(base_url, img_url)
                    
                    # 如果这个URL在映射中，替换为本地路径
                    if absolute_url in img_url_mapping and img_url_mapping[absolute_url]:
                        local_filename = img_url_mapping[absolute_url]
                        # 使用相对路径：../images/filename
                        local_path = f"../images/{local_filename}"
                        img["src"] = local_path
                        # 清除其他懒加载属性
                        for remove_attr in ["data-src", "data-original", "data-lazy-src"]:
                            if img.get(remove_attr):
                                del img[remove_attr]
                        replaced_count += 1
                        break
        
        print(f"\n🔄 替换了 {replaced_count} 个图片链接为本地路径")
        
        # 将修改后的HTML转换为Markdown
        modified_html = str(soup)
        markdown_content = md(modified_html, heading_style="ATX")
        
        # 保存Markdown文件
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"✅ 成功转换为Markdown: {output_path}")
        return True
        
    except Exception as e:
        print(f"❌ 转换Markdown失败: {e}")
        return False


def scrape_simple(url):
    """
    简单的网页爬取功能，同时下载页面中的所有图片

    Args:
        url (str): 要爬取的网站URL
    """
    # 创建html文件夹
    html_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "html")
    os.makedirs(html_dir, exist_ok=True)

    # 设置请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    try:
        print(f"正在爬取: {url}")

        # 发送请求
        response = get(url, headers=headers, timeout=30)
        response.raise_for_status()

        # 查看响应头中的 Content-Encoding
        encoding = response.headers.get("Content-Encoding")
        print("Content-Encoding: ", encoding)

        # 获取HTML内容
        html_content = None
        # 根据编码类型进行解压缩处理
        if encoding == "gzip":
            html_content = response.text
        elif encoding == "deflate":
            html_content = response.text
        elif encoding == "br":
            html_content = response.text
        elif encoding == "zstd":
            dctx = zstd.ZstdDecompressor()
            decompressed_data = dctx.decompress(response.content)
            html_content = decompressed_data.decode("utf-8")
        else:
            html_content = response.text

        # 尝试从HTML中提取标题
        title = ""
        if "<title>" in html_content and "</title>" in html_content:
            start = html_content.find("<title>") + 7
            end = html_content.find("</title>")
            title = html_content[start:end].strip()

        # 生成文件名
        parsed_url = urlparse(url)
        domain = parsed_url.netloc.replace("www.", "")

        if title:
            filename = f"{domain}_{clean_filename(title, url)}.html"
        else:
            filename = f"{domain}_page.html"

        # 保存HTML文件
        file_path = os.path.join(html_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ 成功保存HTML文件: {file_path}")
        print(f"📄 页面标题: {title if title else '无标题'}")
        print(f"📊 文件大小: {len(html_content)} 字符")

        # 下载页面中的所有图片
        print("\n🖼️  开始下载图片...")
        img_count, img_url_mapping = extract_and_download_images(html_content, url, headers)
        print(f"\n✅ 成功下载 {img_count} 张图片到 images/ 文件夹")

        # 转换为Markdown
        print("\n📝 开始转换为Markdown...")
        markdown_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "markdown")
        os.makedirs(markdown_dir, exist_ok=True)
        
        # 生成Markdown文件名（与HTML同名，但扩展名为.md）
        md_filename = filename.replace(".html", ".md")
        md_path = os.path.join(markdown_dir, md_filename)
        
        convert_html_to_markdown_with_local_images(html_content, url, img_url_mapping, md_path)

        return True

    except exceptions.RequestException as e:
        print(f"❌ 请求错误: {e}")
        print()
        return False
    except Exception as e:
        print(f"❌ 保存文件时出错: {e}")
        return False


def main():
    """主函数（无需命令行参数，直接在代码中配置 URL）"""
    url = TARGET_URL_SIMPLE

    if not url:
        print("请在代码中设置 TARGET_URL_SIMPLE，例如 'https://example.com'")
        return

    # 检查URL格式
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
        print(f"自动添加协议: {url}")

    success = scrape_simple(url)

    if success:
        print("\n🎉 爬取完成！")
        print("📁 HTML文件已保存到 html/ 文件夹")
        print("🖼️  图片文件已保存到 images/ 文件夹")
        print("📝 Markdown文件已保存到 markdown/ 文件夹（图片链接已替换为本地路径）")
    else:
        print("💥 爬取失败！")


if __name__ == "__main__":
    main()
