# Scrapy settings for web scraper project

BOT_NAME = "web_scraper"

SPIDER_MODULES = ["web_scrapy.spiders"]
NEWSPIDER_MODULE = "web_scrapy.spiders"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure delays for requests
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 1

# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
}

# Enable or disable spider middlewares
SPIDER_MIDDLEWARES = {
    "web_scrapy.middlewares.SpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
DOWNLOADER_MIDDLEWARES = {
    "web_scrapy.middlewares.DownloaderMiddleware": 543,
}

# Configure item pipelines
ITEM_PIPELINES = {
    "web_scrapy.pipelines.HTMLSaverPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = "httpcache"
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = "web_scrapy.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = 'utf-8'