# -*- coding: utf-8 -*-
"""
Created on Wed Dec 07 05:28:06 2016
体验pandas相对于、pandas的对应操作
@author: Administrator
"""

import pandas as pd
import numpy as np
url = 'https://raw.github.com/pandas-dev/pandas/master/pandas/tests/data/tips.csv'
tips = pd.read_csv(url)
tips.head()
#==============================================================================
# SELECT total_bill, tip, smoker, time
# FROM tips
# LIMIT 5;
#==============================================================================
tips[['total_bill', 'tip', 'smoker', 'time']].head(5)
#==============================================================================
# SELECT *
# FROM tips
# WHERE time = 'Dinner'
# LIMIT 5;
#==============================================================================
tips[tips['time'] == 'Dinner'].head(5)
#去除某两列的重复值
tips.head(5).duplicated(['sex','size'])
tips.head(5).drop_duplicates(['sex','size'])
#==============================================================================
# SELECT *
# FROM tips
# WHERE time = 'Dinner' AND tip > 5.00;
#==============================================================================
tips[(tips['time'] == 'Dinner') & (tips['tip'] > 5.00)]
#==============================================================================
# SELECT *
# FROM tips
# WHERE size >= 5 OR total_bill > 45;
#==============================================================================
tips[(tips['size'] >= 5) | (tips['total_bill'] > 45.00)]
frame = pd.DataFrame({'col1': ['A', 'B', np.NaN, 'C', 'D'],'col2': ['F', np.NaN, 'G', 'H', 'I']})
#==============================================================================
# SELECT *
# FROM frame
# WHERE col1 IS NOT NULL;
# SELECT *
# FROM frame
# WHERE col1 IS  NULL;
#==============================================================================
frame[frame['col1'].notnull()]
frame[frame['col1'].isnull()]
#####################################group by#####################################
#==============================================================================
# SELECT sex, count(*)
# FROM tips
# GROUP BY sex;
#==============================================================================
groupedtips=tips.groupby('sex').size()

#==============================================================================
# SELECT day, AVG(tip), COUNT(*)
# FROM tips
# GROUP BY day;
#==============================================================================
groupedtips2=tips.groupby('day').agg({'tip': np.mean, 'day': np.size})
#==============================================================================
# 
# SELECT smoker, day, COUNT(*), AVG(tip)
# FROM tips
# GROUP BY smoker, day;
#==============================================================================
groupedtips3=tips.groupby(['smoker', 'day']).agg({'tip': [np.size, np.mean]})
#################################join#########################################
df1 = pd.DataFrame({'key': ['A', 'B', 'C', 'D'],'value': np.random.randn(4)})
df2 = pd.DataFrame({'key': ['B', 'D', 'D', 'E'],'value': np.random.randn(4)})
#innerjoin
pd.merge(df1, df2, on='key')
indexed_df2 = df2.set_index('key')




#接下来可以看看分析函数，窗口聚合函数等的操作