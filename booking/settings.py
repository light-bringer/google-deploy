# Scrapy settings for harrods project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'booking'

SPIDER_MODULES = ['booking.spiders']
NEWSPIDER_MODULE = 'booking.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
FEED_EXPORTERS = {
    'csv': 'booking.feedexport.CSVkwItemExporter'
}
EXPORT_FIELDS = [
    'Url',
    'Property_Name',
    'Address',
    'Gps_Coordinates',
    'Date_Scraped',
    'Date_Signed_In',
    'Date_Signed_Out',
    'Room_Night',
    'Included_Tax',
    'Included_Property_Service_Charge',
    'Inclded_Other_Charges',
    'Excluded_Tax',
    'Excluded_Property_Service_Charge',
    'Excluded_Ohter_Charges',
    'No_of_Rooms',
    'Bed_Room_Type',
    'Bed_Type',
    'Amenities',
    'Room_Size',
    'Sleeps',
    'Rate',
    'Maximum_Available_Room',
    'Included',
    'Your_Choice',
    'Cancelation',
    'Overall_Rating',
    'Breakfast',
    'Cleanliness',
    'Comfort',
    'Location',
    'Facilities',
    'Staff',
    'Value_For_Money',
    'Free_Wifi',
    'Included_Breakfast',
    'Optional_Breakfast',
    'Free_Cancelation',
    # 'Cancelation_Fee',
    'Families',
    'Couples',
    'Group_of_Friends',
    'Solo_Travellers',
    'Business_Travellers',
    'Nationality_of_Reviews'
]

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     # 'Referer': 'http://www.lepper_marine.com/browse/subDivision.do?cid=6487&mlink=5058,12456145,visnav_Baby&clink=12456145'
#   # 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   # 'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'harrods.middlewares.HarrodsSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'harrods.middlewares.MyCustomDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}
EXTENSIONS = {
    'scrapy.contrib.closespider.CloseSpider': 500,
}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'harrods.pipelines.HarrodsPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# REDIRECT_ENABLED = True
# METAREFRESH_ENABLED = True

LOG_LEVEL = 'ERROR'

CLOSESPIDER_ERRORCOUNT = 1