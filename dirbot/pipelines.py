# -*- coding: utf-8 -*-
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy import signals
import json
import codecs
from twisted.enterprise import adbapi
from datetime import datetime
from hashlib import md5
import MySQLdb
import MySQLdb.cursors
from scrapy.utils.project import get_project_settings
settings = get_project_settings()

class FilterWordsPipeline(object):
    """A pipeline for filtering out items which contain certain words in their
    description"""

    # put all words in lowercase
    words_to_filter = ['politics', 'religion']

    def process_item(self, item, spider):
        for word in self.words_to_filter:
            if word in unicode(item['description']).lower():
                raise DropItem("Contains forbidden word: %s" % word)
        else:
            return item

class DoubandemoPipeline(object):
    def process_item(self, item, spider):
        return item

class MySQLStoreFundInvestinfoPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        '''
        构建一个实方法，确保只有一个数据库连接池，避免无限的数据库连接
        :param settings:
        :return:
        '''
        print 'start create connection'
        dbargs = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWD'],
            #port=settings['MYSQL_DBPORT'],
            charset='utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode= True,
        )
        dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
        return cls(dbpool)

    #pipeline默认调用
    def process_item(self, item, spider):
        #如果SPIDER是基金投资季报爬虫，则需要单独存入指定的相表结构当中
        if spider.name=='fundInvestInfo':
            print 'start save fundcode'+item['fundcode']
            d = self.dbpool.runInteraction(self._conditional_insert_fundinvestinfo, item, spider)
            print 'run mysql sql '
            d.addErrback(self._handle_error, item, spider)
            d.addBoth(lambda _: item)
            return d
        else:#不作处理
            return item
        #d.addBoth(lambda _: item)
        #return item
    #将每行更新或写入数据库中
    def _conditional_insert_fundinvestinfo(self, conn, item, spider):
        self.saveFundbaseinfo(conn, item)
        # 开始保存大类资产配置数据表，同样采用增量更新的方法，如果存在则更新，不存在则插入
        self.saveAssetAlloc(conn,item)
        # 开始保存行业配置数据，同样采用增量更新的方法，按照指定条件，先删除，再插入
        self.saveIndustryAlloc(conn,item)
        # 开始保存股票10大持仓股票数据，同样采用增量更新的方法，按照指定条件，先删除，再插入
        self.saveTop10StockAlloc(conn,item)

    def saveAssetAlloc(self, conn, item):
        AssetAllocList=item['fundAssetinfo']
        print "assetalloclist's len "+str(len(AssetAllocList))
        for i in AssetAllocList:
            fundcode=i['fundcode']
            assettype=i['assettype']
            ratio =i['ratio']
            reportdate =i['reportdate']
            now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
            #先删除再插入
            conn.execute("""
                delete from openfund_assetalloc where fundcode = %s and reportdate= %s and assettype= %s
            """, (fundcode,reportdate,assettype))
            conn.execute("""
                INSERT INTO openfund_assetalloc (fundcode, assettype, ratio, reportdate, updatetime) VALUES (%s, %s, %s, %s, %s)
            """, (fundcode, assettype, ratio, reportdate, now,))
    def saveIndustryAlloc(self, conn, item):
        '''
        保存行业配置信息，先删除再插入，支持重载
        :param conn: 数据库链接信息
        :param item: 前期爬取到的信息
        :return:无
        '''
        fundindInfoList=item['fundindInfo']
        print "fundindInfoList's length is  "+str(len(fundindInfoList))
        for i in fundindInfoList:
            fundcode=i['fundcode']
            industryName=i['industryName']
            ratio =i['ratio']
            reportdate =i['reportdate']
            now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
            #先删除再插入
            conn.execute("""
                delete from openfund_industryalloc where fundcode = %s and reportdate= %s and industryName= %s
            """, (fundcode,reportdate,industryName))
            conn.execute("""
                INSERT INTO openfund_industryalloc (fundcode, industryName, ratio, reportdate, updatetime) VALUES (%s, %s, %s, %s, %s)
            """, (fundcode, industryName, ratio, reportdate, now,))
    def saveTop10StockAlloc(self, conn, item):
        fundTop10stockList=item['fundTop10stock']
        print "fundTop10stockList's length is  "+str(len(fundTop10stockList))
        for i in fundTop10stockList:
            fundcode=i['fundcode']
            stockcode=i['stockcode']
            stockname=i['stockname']
            holdshares =i['holdshares']
            marketvalue=i['marketvalue']
            ratio=i['ratio']
            reportdate =i['reportdate']
            now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
            #先删除再插入
            conn.execute("""
                delete from openfund_top10stock where fundcode = %s and reportdate= %s and stockcode= %s
            """, (fundcode,reportdate,stockcode))
            conn.execute("""
                INSERT INTO openfund_top10stock (fundcode, stockcode,stockname,holdshares,ratio, marketvalue,reportdate, updatetime) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)
            """, (fundcode, stockcode,stockname,holdshares,ratio, marketvalue,reportdate, now   ,))
    def saveFundbaseinfo(self, conn, item):
        fundcode = item['fundcode']
        # 开始保存基金基础信息
        now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
        conn.execute("""
                select 1 from openfundinfo where fundcode = %s
        """, (fundcode,))
        ret = conn.fetchone()
        if ret:
            conn.execute("""
                update openfundinfo set  fundfullname = %s, fundmanager = %s, fundname = %s, fundtype = %s, fundassetvalue = %s,setupdate= %s,fundurl= %s, updatetime = %s, fundcompany= %s where fundcode = %s
            """, (item['fundfullname'],item['fundmanager'], item['fundname'], item['fundtype'], item['fundassetValue'], item['setupdate'],
                  item['fundurl'], now, item['fundcompany'], fundcode))
            print """
               update fundinfo of %s
            """, (fundcode)
        else:
            conn.execute("""
                INSERT INTO openfundinfo (fundfullname,fundcode, fundmanager, fundname, fundtype, fundassetValue, setupdate,fundurl,fundcompany,updatetime)
                values(%s,%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (item['fundfullname'],item['fundcode'], item['fundmanager'], item['fundname'], item['fundtype'], item['fundassetValue'],
                  item['setupdate'], item['fundurl'], item['fundcompany'], now))
            print """
               insert fundinfo of %s
            """, (fundcode)
    # #获取url的md5编码
    # def _get_linkmd5id(self, item):
    #     #url进行md5处理，为避免重复采集设计
    #     return md5(item['link']).hexdigest()
    #异常处理
    def _handle_error(self, failure, item, spider):
        log.err(failure)