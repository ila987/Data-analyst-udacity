#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 19:20:28 2017

@author: Ilaria
"""

import pandas as pd
import numpy as np

a = pd.read_csv("airports_code.csv",index_col=False)
a.drop(['Airport ID','ICAO','Latitude','Longitude','Altitude','Timezone','DST','Type','Source'], axis = 1, inplace = True, errors = 'ignore')

b = pd.read_csv("2008.csv")
c=pd.merge(a,b,left_on='IATA', right_on = 'Dest', how='right')
#print c
d = pd.merge(a,c,left_on='IATA', right_on = 'Origin', how='right')
#lst=[]
#for i in c.index:
#    if(c.iloc[i]['result_x']!=''):
#         lst.append(c.iloc[i]['result_x'])
#    else:
#         lst.append(c.iloc[i]['result_y'])
#c['result']=pd.Series(lst)
#del c['result_x']
#del c['result_y']

d.to_csv('result.csv')