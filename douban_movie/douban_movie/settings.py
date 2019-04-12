# -*- coding: utf-8 -*-

# Scrapy settings for douban_movie project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import os

BOT_NAME = 'douban_movie'

SPIDER_MODULES = ['douban_movie.spiders']
NEWSPIDER_MODULE = 'douban_movie.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'


# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 2
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
    r'Accept':r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    r'Accept-Language':r'zh-CN,zh;q=0.9',
    r'Connection':r'keep-alive',
    r'Host':r'movie.douban.com',
    r'Cookie':r'bid=3l4ZQTkZpMQ; ll="118172"; __yadk_uid=Yy7c14z1FNuys2gQ2KUOYdc3CEaleM1r; push_noty_num=0; push_doumail_num=0; _vwo_uuid_v2=D641EB067D86A7D6B3E6CF1ED1D925523|6a905ef32430799b038ed18c433803ea; douban-fav-remind=1; ps=y; dbcl2="194671841',
    r'Upgrade-Insecure-Requests':r'1',
    r'Accept-Encoding':r'gzip, deflate, br',
    r'User-Agent':r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'douban_movie.middlewares.DoubanMovieSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'douban_movie.middlewares.DoubanMovieDownloaderMiddleware': 543,
}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   'douban_movie.pipelines.DoubanMoviePipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 输出文件格式
FEED_EXPORT_ENCODING = 'utf-8'

JSON_FILE = os.path.join(os.getcwd(), "movie.json")

DOWNLOAD_TIMEOUT = 10

COOKIE = {
            r'push_doumail_num':r'0',
            r'push_noty_num':r'0',
            r'_vwo_uuid_v2':r'D641EB067D86A7D6B3E6CF1ED1D925523|6a905ef32430799b038ed18c433803ea',
            r'_pk_ses.100001.4cf6':r'*',
            r'__yadk_uid':r'Yy7c14z1FNuys2gQ2KUOYdc3CEaleM1r',
            r'_pk_ref.100001.4cf6':r'%5B%22%22%2C%22%22%2C1554955895%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%3Fredir%3Dhttps%253A%252F%252Fmovie.douban.com%252F%22%5D',
            r'douban-fav-remind':r'1',
            r'bid':r'3l4ZQTkZpMQ',
            r'_pk_id.100001.4cf6':r'dae3408bf61073a5.1554714338.5.1554955895.1554783055.',
            r'ps':r'y',
            r'll':r'"118172"',
            r'ck':r'BYhW',
            r'dbcl2':r'"194671841:XFxuAMaZ5ME"',
         }