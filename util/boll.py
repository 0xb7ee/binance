#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-06-09 上午11:21
'''
import numpy as np
import datetime

def computBoll(close_array:np.ndarray)->tuple:
    mean = close_array.mean()
    std = close_array.std()
    return (mean+2*std,mean,mean-2*std)


'''
boll = []
kline = []
rdn_close = [float(i['close']) for i in kline]

for i in range(23,len(rdn_close)):
    rdn_class = kline[i]
    time = str(datetime.datetime.fromtimestamp(rdn_class['openTime']/1000))
    k3 = np.array(rdn_close[i-21:i-1])
    k2 = np.array(rdn_close[i-22:i-2])
    k1 = np.array(rdn_close[i-23:i-3])
    # print(f"{time}\tk1从{i-23}到{i-4}\tk2从{i-22}到{i-3}\tk3从{i-21}到{i-2}")
    k3_upper,k3_middle,k3_lowwer = computBoll(k3)
    k2_upper,k2_middle,k2_lowwer = computBoll(k2)
    k1_upper,k1_middle,k1_lowwer = computBoll(k1)
    k3up = k3_upper/k2_upper
    k2up = k2_upper/k1_upper
    k3md = k3_middle/k2_middle
    k2md = k2_middle/k1_middle
    k3lw = k3_lowwer/k2_lowwer
    k2lw = k2_lowwer/k1_lowwer
    if k2up>1 and k3up>1 and k2md>1 and k3md>1 and k2lw<1 and k3lw<1:
        print(time,k3up/k2up,k3md/k2md,k3lw/k2lw)
    boll.append([time,k2up,k2md,k2lw,k3up,k3md,k3lw])
'''


