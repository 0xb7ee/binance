#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-06-10 上午9:20
'''
import datetime
def converTime(time:int)->str:
    '''
    默认为秒
    如果time为毫秒则除以1000
    :param time:
    :return:
    '''
    return datetime.datetime.fromtimestamp(time)

