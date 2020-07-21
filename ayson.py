#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-07-15 下午6:55
'''
import asyncio
import websockets

async def hello():
    uri = "wss://stream.binance.com:9443/ws/linkbtc@trade"
    async with websockets.connect(uri) as websocket:
        # params = {
        #     "method": "SUBSCRIBE",
        #     "params":
        #         [
        #             # "linkbtc@trade",
        #             "troybtc@kline_1h"
        #         ],
        #     "id": 1
        # }
        # await websocket.send(json.dumps(params))
        message = await websocket.recv()
        print(message)
        while True:
            message = await websocket.recv()
            print(message)
asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()


import MySQLdb
from MySQLdb.cursors import DictCursor
import pandas as pd
con = MySQLdb.connect(host="localhost",user="root",passwd="eos",db="crypto",charset='utf8')
cursor = con.cursor(DictCursor)
sql = '''
select a.`key`,a.`time`,a.`close`,a.`vol_1w_std`,a.`prc_1w_std`,b.`rate` from (select * from binance_vp where `key`='{key}') a inner join (select * from binance_boll where `key` = '{key}') b on a.`key` = b.`key` and a.`time` = b.`time` order by a.`time` desc;
'''.format(key='SYSBTC')
cursor.execute(sql)
key_times = cursor.fetchall()
df = pd.DataFrame(key_times)
df['close'] = df['close'].apply(lambda x:'{:.10f}'.format(x))
df.head(20)