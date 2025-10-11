import os
from itemadapter import ItemAdapter


class HTMLSaverPipeline:
    """将HTML内容保存到文件的管道"""

    def __init__(self):
        # 获取html文件夹路径
        self.html_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "html")
        os.makedirs(self.html_dir, exist_ok=True)

    def process_item(self, item, spider):
        """处理每个爬取的item"""
        adapter = ItemAdapter(item)

        # 获取HTML内容和文件名
        html_content = adapter.get("html_content")
        filename = adapter.get("filename")

        if html_content and filename:
            # 构造完整的文件路径
            file_path = os.path.join(self.html_dir, filename)

            # 写入HTML文件
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)

                spider.logger.info(f"HTML内容已保存到: {file_path}")

            except Exception as e:
                spider.logger.error(f"保存HTML文件时出错: {e}")
        
        return item