# Scrapy settings for IMDB_scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import os

POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'db')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'imdb_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'jib17_a')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')

BOT_NAME = "IMDB_scraper"

SPIDER_MODULES = ["IMDB_scraper.spiders"]
NEWSPIDER_MODULE = "IMDB_scraper.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:140.0) Gecko/20100101 Firefox/140.0"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Concurrency and throttling settings
#CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 2

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
   "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
   "Accept-Language": "en-US,en;q=0.9",
   "Accept-Encoding": "gzip, deflate, br, zstd",
   "Connection": "keep-alive",
   "Host": "www.imdb.com",
   "Priority": "u=0, i",
   "Sec-Fetch-Dest": "document",
   "Sec-Fetch-Mode": "navigate",
   "Sec-Fetch-Site": "none",
   "Sec-Fetch-User": "?1",
   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:146.0) Gecko/20100101 Firefox/146.0",
}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "IMDB_scraper.middlewares.ImdbScraperSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   # "rotating_proxies.middlewares.RotatingProxyMiddleware": 610,
   "rotating_proxies.middlewares.BanDetectionMiddleware": 620,
   "IMDB_scraper.middlewares.ImdbScraperDownloaderMiddleware": 541
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   "IMDB_scraper.pipelines.PostgresPipeline": 300,
}

# ROTATING_PROXY_LIST = [
#     'http://141.101.113.69:80',
#     'http://45.67.215.0:80',
#     'http://141.101.120.101:80',
#     'http://45.67.215.118:80',
#     'http://89.116.250.35:80',
#     'http://185.238.228.173:80',
#     'http://89.116.250.153:80',
#     'http://185.238.228.108:80',
#     'http://170.114.46.185:80',
#     'http://91.193.58.165:80',
#     'http://45.67.215.13:80',
#     'http://216.205.52.72:80',
#     'http://102.177.176.148:80',
#     'http://45.67.215.129:80',
#     'http://141.101.120.194:80',
#     'http://216.205.52.75:80',
#     'http://89.116.250.20:80',
#     'http://216.205.52.67:80',
#     'http://170.114.45.147:80',
#     'http://45.67.215.173:80',
# ]

RETRY_ENABLED = True
RETRY_TIMES = 5
RETRY_HTTP_CODES = [400, 401, 403, 429, 500, 502, 503, 522]


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 2
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 20
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
