"""
简化版网页爬取工具
直接使用requests库爬取网页HTML内容并保存
"""

import os
from urllib.parse import urlparse

from requests import get, exceptions
import zstandard as zstd

# URL 配置入口：将要爬取的网站写在这里
TARGET_URL_SIMPLE = (
    "https://mp.weixin.qq.com/s/RAex20Ynj3K9037Xp5FhmQ"  # 修改为你要爬取的网页URL
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


def scrape_simple(url):
    """
    简单的网页爬取功能

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
        print("🎉 爬取完成！HTML文件已保存到 html/ 文件夹中")
    else:
        print("💥 爬取失败！")


if __name__ == "__main__":
    main()
