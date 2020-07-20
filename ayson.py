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