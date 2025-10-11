import scrapy
import os
from urllib.parse import urljoin, urlparse


class WebScraperItem(scrapy.Item):
    """定义爬取的数据结构"""

    url = scrapy.Field()
    html_content = scrapy.Field()
    title = scrapy.Field()
    filename = scrapy.Field()


class WebSpider(scrapy.Spider):
    name = "web_spider"

    def __init__(self, url=None, *args, **kwargs):
        super(WebSpider, self).__init__(*args, **kwargs)
        if url:
            self.start_urls = [url]
        else:
            self.start_urls = ["https://example.com"]  # 默认URL

        # 创建html文件夹
        self.html_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "html")
        os.makedirs(self.html_dir, exist_ok=True)

    def parse(self, response):
        """解析网页并提取HTML内容"""
        # 获取完整的HTML内容
        html_content = response.text

        # 获取页面标题
        title = response.css("title::text").get()
        if not title:
            title = "Untitled"

        # 清理标题中的特殊字符，用于文件名
        safe_title = "".join(
            c for c in title if c.isalnum() or c in (" ", "-", "_")
        ).rstrip()
        if len(safe_title) > 100:
            safe_title = safe_title[:100]

        # 获取域名用于文件名
        parsed_url = urlparse(response.url)
        domain = parsed_url.netloc.replace("www.", "")

        # 生成文件名
        filename = f"{domain}_{safe_title}.html".replace(" ", "_")

        # 创建Item并返回
        item = WebScraperItem()
        item["url"] = response.url
        item["html_content"] = html_content
        item["title"] = title
        item["filename"] = filename

        yield item

        self.logger.info(f"成功爬取页面: {response.url}")
        self.logger.info(f'页面标题: {title}')