#!/usr/bin/env python3
"""
网页爬取工具
使用Scrapy爬取指定网页的HTML内容并保存到html文件夹中
"""

import os
import sys
from scrapy.crawler import CrawlerProcess

# 添加当前目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from spider import WebSpider

# URL 配置入口：将要爬取的网站写在这里
TARGET_URL = (
    "https://www.runoob.com/java/java-override-overload.html"  # 修改为你要爬取的网页URL
)


def scrape_website(url):
    """
    爬取指定网站的HTML内容

    Args:
        url (str): 要爬取的网站URL
    """
    # 创建自定义设置，不使用项目设置以避免模块路径问题
    settings = {
        "BOT_NAME": "web_scraper",
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1,
        "DEFAULT_REQUEST_HEADERS": {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        },
        "ITEM_PIPELINES": {
            "pipelines.HTMLSaverPipeline": 300,
        },
        "LOG_LEVEL": "INFO",
    }

    # 创建爬虫进程
    process = CrawlerProcess(settings)

    # 启动爬虫
    process.crawl(WebSpider, url=url)
    process.start()


def main():
    """主函数（无需命令行参数，直接在代码中配置 URL）"""
    # 在上方设置 TARGET_URL，例如 'https://example.com'
    url = TARGET_URL

    if not url:
        print("请在代码中设置 TARGET_URL，例如 'https://example.com'")
        return

    # 检查URL格式
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    print(f"开始爬取网站: {url}")
    print("HTML内容将保存到 html/ 文件夹中...")

    try:
        scrape_website(url)
        print("爬取完成！")
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")


if __name__ == "__main__":
    main()
