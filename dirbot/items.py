# -*- coding: utf-8 -*-
from scrapy.item import Item, Field


class Website(Item):

    name = Field()
    description = Field()
    url = Field()

class DoubanBookItem(Item):
    title = Field()
    title2=Field()
    info=Field()
    rate =Field()
    hot = Field()
    img_url = Field()

class fundAssetAlloc(Item):
    '''
    通过腾讯财经的基金频道，抓取4000多只开放式基金的资产配置
    '''
    fundcode=Field()
    assettype=Field()
    ratio=Field()
    reportdate=Field()

class fundIndustryAlloc(Item):
    '''
    通过腾讯财经的基金频道，抓取4000多只开放式基金的行业配置
    '''
    fundcode=Field()
    industryName=Field()
    ratio=Field()
    reportdate=Field()
class fundTop10Stock(Item):
    '''
    通过腾讯财经的基金频道，抓取4000多只开放式基金的10大股票持仓
    '''
    fundcode=Field()
    stockcode=Field()
    stockname=Field()
    marketvalue=Field()
    holdshares=Field()
    ratio=Field()
    reportdate=Field()

class fundInvestInfo(Item):
    '''
    基金投资信息，包括基金基本信息，基金代码，基金经理，基金名称，基金类型，基金最新规模，基金成立日期
    包含资产配置信息，行业配置信息，10大股票持仓数据，这里QDII可能只包括基金基本信息和资产配置信息，不包括A股行业配置
    和10大股票持仓
    '''
    fundAssetinfo=Field()#fundAssetAlloc对象的集合
    fundTop10stock=Field() #fundTop10Stock对象的集合
    fundindInfo=Field()#fundIndustryAlloc对象的集合
    fundcode=Field()
    fundmanager=Field()
    fundfullname=Field()
    fundname=Field()
    fundtype=Field()
    fundassetValue=Field()
    setupdate=Field()
    fundurl=Field()
    fundcompany=Field()

class fundNewsItem(Item):
    '''
    定义新闻聚合数据
    '''
    subject=Field() #主题
    title=Field() #标题
    source=Field() #来源
    updatetime=Field() #来源
    url=Field() #详细的URL








