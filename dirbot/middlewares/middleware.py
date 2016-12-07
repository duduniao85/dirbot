#encoding:utf8
'''
'''
__author__ = 'xuyuming'
from selenium import webdriver
from scrapy.http import HtmlResponse
import urllib2
import time
import sys
type = sys.getfilesystemencoding()

#定义urllib2方式的爬取方法，遇到比较难处得的中文编码可以这么处理
class urllib2Middleware(object):
    def process_request(self, request, spider):
        if spider.name =="fundInvestInfo" and request.url==(r'http://stock.finance.qq.com/fund/jzzx/kfs.js'):
            print"urllib2Middleware is starting..."
            res = urllib2.urlopen(r'http://stock.finance.qq.com/fund/jzzx/kfs.js')
            html = res.read()
            res.close()
            html = html.decode("gbk").encode(type)
            print("start crawling "+request.url)
            return HtmlResponse(res.geturl(), body=html, encoding='utf-8', request=request)
        # 以下是使用phantom.js进行网页解析的方法，该方法是最后才使用的方法，性能比较差，数据量较大时不建议使用
        # elif spider.name =="fundInvestInfo" and request.url.find(r'http://gu.qq.com/') >=0:
        #     driver = webdriver.PhantomJS(executable_path=r'C:\Users\xuyuming\AppData\Roaming\Python\Scripts\phantomjs')
        #     driver.get(request.url)
        #     time.sleep(0.1)
        #     body = driver.page_source
        #     print("visiting"+request.url)
        #     return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
        else:
            return