#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-06-10 上午9:20
'''
import datetime
def converTime(time:int)->str:
    '''
    如果time为毫秒则除以1000
    :param time:
    :return:
    '''
    time
import numpy as np

def computBoll(close_array:np.ndarray)->tuple:
    return (close_array.mean()+2*close_array.std(),close_array.mean(),close_array.mean()-2*close_array
            .std())

def computBollRate():


rdn = []
rdn_close = [float(i['close']) for i in rdn]
for i in range(23,len(rdn)):
    rdn_class = rdn[i]
    time = str(datetime.datetime.fromtimestamp(rdn_class['openTime']/1000))

    k3 = np.array(rdn_close[i-21:i-1])
    k2 = np.array(rdn_close[i-22:i-2])
    k1 = np.array(rdn_close[i-23:i-3])
    k3_upper,k3_middle,k3_lowwer = computBoll(k3)
    k2_upper,k2_middle,k2_lowwer = computBoll(k2)
    k1_upper,k1_middle,k1_lowwer = computBoll(k1)

