# -*- coding: utf-8 -*-
# Scrapy settings for dirbot project

SPIDER_MODULES = ['dirbot.spiders']
NEWSPIDER_MODULE = 'dirbot.spiders'
DEFAULT_ITEM_CLASS = 'dirbot.items.Website'
#USER_AGENT='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.115 Safari/537.36'
USER_AGENT='Mozilla/5.0 (iPad; CPU OS 7_0 like Mac OS X) AppleWebKit/537.51.1 (KHTML, like Gecko) Version/7.0 Mobile/11A465 Safari/9537.53'
ROBOTSTXT_OBEY = False
FEED_URI=u'file:///C:/Users/xuyuming/PycharmProjects/dirbot/doubanbook.csv'
FEED_FORMAT='CSV'
ITEM_PIPELINES = {
   #'dirbot.pipelines.FilterWordsPipeline': 1,
   'dirbot.pipelines.MySQLStoreFundInvestinfoPipeline':2
   #'scrapy.pipelines.images.ImagesPipeline': 300,

}
IMAGES_URLS_FIELD = 'img_url'
IMAGES_STORE = r'./images'
DOWNLOADER_MIDDLEWARES = {
   'dirbot.middlewares.middleware.urllib2Middleware':543,#键为中间件类的路径，值为中间件的顺序
   'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,#禁止内置的中间件
}

# start MySQL database configure setting
MYSQL_HOST = '127.0.0.1'
MYSQL_DBNAME = 'python'
MYSQL_USER = 'fundbi'
MYSQL_PASSWD = 'fundbi'
MYSQL_DBPORT = '3306'
# end of MySQL database configure setting