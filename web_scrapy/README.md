# 网页爬取工具

这个文件夹包含了使用Scrapy和简单requests库爬取网页HTML内容的工具。

## 文件说明

- `scraper.py` - 使用Scrapy框架的完整爬虫工具
- `simple_scraper.py` - 使用requests库的简单爬虫工具（推荐使用）
- `spider.py` - Scrapy爬虫类定义
- `pipelines.py` - Scrapy数据处理管道
- `settings.py` - Scrapy配置文件

## 使用方法

### 方法一：使用简单爬虫（推荐）

```bash
# 爬取指定网站
python web_scrapy/simple_scraper.py https://example.com

# 也可以不加协议，程序会自动添加https://
python web_scrapy/simple_scraper.py baidu.com
```

### 方法二：使用Scrapy框架

```bash
# 爬取指定网站
python web_scrapy/scraper_test.py https://example.com
```

## 输出

所有爬取的HTML文件都会保存在项目根目录的 `html/` 文件夹中，文件名格式为：
`域名_页面标题.html`

## 特性

- 自动创建html文件夹
- 智能文件命名（基于域名和页面标题）
- 处理中文和特殊字符
- 设置合适的请求头避免被反爬
- 错误处理和日志输出
- 支持HTTPS和HTTP协议

## 依赖

- scrapy (已在pyproject.toml中配置)
- requests (Python标准库)
- urllib.parse (Python标准库)