    # -*- coding=utf-8 -*-
from scrapy.spiders import Spider
from scrapy.selector import Selector

from dirbot.items import Website


class DmozSpider(Spider):
    name = "dmoz"  #一般以网站域名命名SPIDER
    allowed_domains = ["dmoz.org"] #可选。包含了spider允许爬取的域名(domain)列表(list)
    start_urls = [
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Books/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/",
    ]#当没有制定特定的URL时，spider将从该列表中开始进行爬取,后续的URL将会从获取到的数据中提取

    def parse(self, response):
        #当response没有指定回调函数时，该方法是Scrapy处理下载的response的默认方法
        #负责处理response并返回处理的数据以及(/或)跟进的URL
        """
        The lines below is a spider contract. For more info see:
        http://doc.scrapy.org/en/latest/topics/contracts.html

        @url http://www.dmoz.org/Computers/Programming/Languages/Python/Resources/
        @scrapes name
        """
        sel = Selector(response)
        sites = sel.xpath('//div[@class="title-and-desc"]')
        print len(sites)
        items = []

        for site in sites:
            item = Website()
            item['name'] = site.xpath('a/div/text()').extract()
            item['url'] = site.xpath('a/@href').extract()
            item['description'] = site.xpath('div[@class="site-descr "]/text()').extract()[0].replace('  ',' ').replace('\n','').replace('\t','').replace('\r','')
            items.append(item)

        return items #该方法及其他的Request回调函数必须返回一个包含 Request 及(或) Item 的可迭代的对象

    #log(message[, level, component])  # scrapy.log.msg() 自动记录以name命名的爬虫日志
    #closed(reason) 当spider关闭，函数供调用， 该方法提供了一个替代调用signals.connect()来监听 spider_closed 信号的快捷方式。
    #make_requests_from_url(url)   该方法接受一个URL并返回用于爬取的 Request 对象，默认子类实现时
    #start_requests()  #如果需要想要修改最初爬取某个网站的request对象，则需要重载该方法
