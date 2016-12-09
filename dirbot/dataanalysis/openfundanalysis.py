#encoding:utf8
'''
    20161206 根据腾讯基金网抓取的数据分析相关基金配置情况
'''
__author__ = 'xuyuming'
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import sqlalchemy as sa
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
engine = create_engine('mysql://fundbi:fundbi@127.0.0.1/python?charset=utf8')
def generalAnalysis():
    '''
    提供一般性分析，包括：
    1，股票型基金
    :return:
    '''
    with engine.connect() as conn, conn.begin():
        #df_fundinfo = pd.read_sql_table('openfundinfo', conn)    #基金基本信息
        #行业信息
        #df_fundind = pd.read_sql(sa.text('SELECT * FROM openfund_industryalloc where reportdate >=:col1'), engine, params={'col1': '2016-01-30'})
        #10大股票持仓配置信息
        #df_fundstock = pd.read_sql(sa.text('SELECT * FROM openfund_top10stock where reportdate >=:col1'), engine, params={'col1': '2016-01-30'})
        #股票基本信息
        #df_stockinfo = pd.read_sql_table('stock_basics', conn)   
    
        df_fundcount=pd.read_sql(sa.text('SELECT case fundcompany when \'\' then \'unkown\' else fundcompany end fundcompany, count(DISTINCT fundfullname) AS fundcount FROM openfundinfo t \
        GROUP BY t.fundcompany'),engine)
    plt.style.use("ggplot")
    #plt.figure(figsize=(16,12), dpi=200)
    df_fundcount=df_fundcount.set_index('fundcompany')
    #plt.title(u'显示中文')
    df_fundcount.sort('fundcount',ascending=False).head(10).\
    plot(kind='barh',title=u'')
    
    #plt.subplot(1,1,1)
    #基金资产配置信息
    #df_fundasset=pd.read_sql()

#==============================================================================
# 
# from matplotlib import pyplot as plt
# plt.title(u'显示中文')
# plt.xticks((0,1,2,3,4,5),(u'男',u'女'),fontproperties='SimHei')
# plt.xlabel(u'显示中文',fontproperties='SimHei')
# plt.show()
#==============================================================================

generalAnalysis()