#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-07-16 下午5:11
'''

import requests
import datetime
Base_url = "https://api.binance.com"
r_url = Base_url+"/api/v3/aggTrades?symbol=ALGOBTC&fromId=4565000"
r = requests.get(r_url)
ret = r.json()
print(len(ret))
print(ret[0])
datetime.datetime.fromtimestamp(ret[0]['T']/1000)+datetime.timedelta(hours=7)

import requests
Base_url = "https://api.binance.com"
r_url = Base_url+"/api/v3/historicalTrades?symbol=ALGOBTC&fromId=4640000&limit=1000"
r = requests.get(r_url)
ret = r.json()
print(len(ret))

import pandas as pd

kline = ""
data = pd.DataFrame(kline[:-1])
def comput_vp(data,key):
    # data['time'] = data['openTime'].apply(lambda x:datetime.datetime.fromtimestamp(x / 1000))
    data['quoteVolume'] = data['quoteVolume'].astype('float')
    data['volume'] = data['volume'].astype('float')
    data['close'] = data['close'].astype('float')
    # end = data['openTime'].values[-1]
    lines = []
    for i in data.iloc[84:]['openTime'].values:
        trank = vp_rank(data,i,key)
        if trank[0][0]>=1.5 and trank[0][1]>=1.5:
            lines.append([key,datetime.datetime.fromtimestamp(i/1000),trank[0][0],trank[0][1],trank[1][0],trank[1][1]])
    return lines

def vp_rank(data,end,key):

    def index_value(data,time_end):
        t = data[(data['openTime']>=time_end)&(data['openTime']<=end)]
        t = t.sort_values('volume',ascending=False)
        t = t.reset_index(drop=True)
        # volume_index = t[t['openTime']==end].index.values[0]+1
        volume_mean = t['volume'].mean()
        volume_std = t['volume'].std()
        v_index = (t[t['openTime']==end]['volume'].values[0]-volume_mean)/volume_std

        t = t.sort_values('close',ascending=False)
        t = t.reset_index(drop=True)
        # close_index = t[t['openTime']==end].index.values[0]+1
        close_mean = t['close'].mean()
        close_std = t['close'].std()
        c_index = (t[t['openTime']==end]['close'].values[0]-close_mean)/close_std
        return (v_index,c_index)

    one_week_end = end-1000*60*60*24*7
    two_week_end = end-1000*60*60*24*7*2
    three_week_end = end-1000*60*60*24*7*3
    four_week_end = end-1000*60*60*24*7*4
    two_month_end = end-1000*60*60*24*7*8
    three_month_end = end-1000*60*60*24*7*12
    time_end = [one_week_end,two_week_end,three_week_end,four_week_end,two_month_end,three_month_end]
    ret = []
    for i in time_end:
        index_v = index_value(data,i)
        ret.append([index_v[0],index_v[1]])
    return ret

df.columns = ['key','time','vol_1w_std','prc_1w_std','vol_2w_std','prc_2w_std']
