#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-07-09 上午11:21
'''

import MySQLdb

con = MySQLdb.connect("")

a = [{'openTime': 1587153600000,
      'open': '0.00000113',
      'high': '0.00000118',
      'low': '0.00000113',
      'close': '0.00000117',
      'volume': '3476654.00000000',
      'closeTime': 1587167999999,
      'quoteVolume': '4.00558695',
      'numTrades': 318},
     {'openTime': 1587168000000,
      'open': '0.00000117',
      'high': '0.00000121',
      'low': '0.00000114',
      'close': '0.00000115',
      'volume': '28949761.00000000',
      'closeTime': 1587182399999,
      'quoteVolume': '34.30391769',
      'numTrades': 1182},
     {'openTime': 1587182400000,
      'open': '0.00000115',
      'high': '0.00000116',
      'low': '0.00000111',
      'close': '0.00000113',
      'volume': '3616833.00000000',
      'closeTime': 1587196799999,
      'quoteVolume': '4.10774812',
      'numTrades': 362}]