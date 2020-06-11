#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-06-09 上午11:23
'''
class Kline():
    def __init__(self,open,high,low,close,volume_base,volume_amount):
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume_base = volume_base
        self.volume_amount = volume_amount