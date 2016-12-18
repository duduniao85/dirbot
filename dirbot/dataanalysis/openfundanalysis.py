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

with engine.connect() as conn, conn.begin():
    #df_fundinfo = pd.read_sql_table('openfundinfo', conn)    #基金基本信息
    #行业信息
    #df_fundind = pd.read_sql(sa.text('SELECT * FROM openfund_industryalloc where reportdate >=:col1'), engine, params={'col1': '2016-01-30'})
    #10大股票持仓配置信息
    #df_fundstock = pd.read_sql(sa.text('SELECT * FROM openfund_top10stock where reportdate >=:col1'), engine, params={'col1': '2016-01-30'})
    #股票基本信息
    df_stockinfo = pd.read_sql_table('stock_basics', conn)   

    df_fundcount=pd.read_sql(sa.text('SELECT case fundcompany when \'\' then \'unkown\' else fundcompany end fundcompany, count(DISTINCT fundfullname) AS fundcount,sum(fundassetvalue)/count(DISTINCT fundfullname) as avgasset FROM openfundinfo t \
    GROUP BY t.fundcompany'),engine)
    #分析行业持仓
    df_industry=pd.read_sql(sa.text('select t2.industryName as industryName,sum(t.fundassetValue*t2.ratio) as value from openfundinfo t,openfund_industryalloc t2  where t.fundcode=t2.fundcode and t2.reportdate=\'2016-09-30\' \
    group by t2.industryName'),engine)
    #分析重仓股票
    df_stock=pd.read_sql(sa.text('select t3.timetomarket,t2.fundfullname,t3.name,t2.fundcompany,t3.area,t3.industry,t1.marketvalue,t1.holdshares,t3.outstanding from openfund_top10stock t1,openfundinfo t2,stock_basics t3 \
    where t1.fundcode=t2.fundcode and t1.reportdate=\'2016-09-30\' and t1.stockcode=t3.code'),engine)
plt.style.use("ggplot")
#plt.figure(figsize=(16,12), dpi=200)
df_fundcount=df_fundcount.set_index('fundcompany')
df_industry=df_industry.set_index('industryName')
#==============================================================================
# df_fundcount.sort('avgasset',ascending=False).head(50).\
# plot(kind='barh',title=u'公募基金非公募产品',figsize=(32,24),fontsize=25)
#==============================================================================
#==============================================================================
# df_holdfundcount=df_stock.groupby('name').fundfullname.nunique()
# df_holdfundcount=df_holdfundcount.sort_values(ascending=False)
# df_holdfundcount.head(30).plot(kind='barh',figsize=(24,16),fontsize=25)
# plt.show()
#==============================================================================
#公募持仓最多的前50股票排名
#==============================================================================
# df_stock[['marketvalue','holdshares']]=df_stock[['marketvalue','holdshares']].astype(float)
# 
#==============================================================================
#公募基金持仓分析
#==============================================================================
# df_holdstkvalue=df_stock.groupby('name')
# df_holdstkvalue=df_holdstkvalue['marketvalue'].agg([np.sum]).sort_values('sum',ascending=False).head(50)
# df_holdstkvalue.head(30).plot(kind='barh',figsize=(24,16),fontsize=25)
# plt.show()
#==============================================================================



#公募基金控盘度分析 totalshares/outstanding  总股本持有 除上 流通股票 的 比例
df_holdstkshares=df_stock.groupby(['name','outstanding'],as_index=False)
df_holdstkshares=df_holdstkshares['holdshares'].agg(np.sum)
df_holdstkshares['ratio']=df_holdstkshares['holdshares']/df_holdstkshares['outstanding']/1000000
df_holdstkshares.sort_values('ratio',ascending=False).tail(30).plot(x='name',y='ratio',kind='barh',figsize=(24,16),fontsize=18)
#公募基金重仓股上市年份统计直方图分布
#assign是基于现有列增加新列非常有用的方法
df_stock=df_stock.assign(yeartomarket = (df_stock['timetomarket'] /10000).astype(int))
df_stock['yeartomarket'].plot(kind='hist',figsize=(24,16),fontsize=25)


#公募10大股票重仓所属20细分行业

df_industry=df_stock.groupby('industry').fundfullname.nunique()
df_industry=df_industry.sort_values(ascending=False)
df_industry.head(30).plot(kind='barh',figsize=(40,40),fontsize=30)
plt.show()

# 最不看好的30的细分行业
df_industry=df_stock.groupby('industry').fundfullname.nunique()
df_industry=df_industry.sort_values(ascending=False)
df_industry.tail(30).plot(kind='barh',figsize=(40,40),fontsize=30)
plt.show()

# 最喜欢的股票
#==============================================================================
# 
# df_fundcount.sort('holdfundcount',ascending=False).head(50).\
# plot(kind='barh',title=u'公募基金最喜欢的股票',figsize=(24,16),fontsize=25)
# 
# 
#==============================================================================

#==============================================================================
# df_industry.sort('value',ascending=False).head(20).\
# plot(kind='barh',title=u'行业配置情况',figsize=(18,18),fontsize=20)
# df_industry.plot(kind='pie',y='value',figsize=(9,9),fontsize=20)
#==============================================================================

