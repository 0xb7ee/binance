#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-07-15 下午4:17
'''
import seaborn as sns

sns.boxplot()

import zlib
import json
import websocket
import threading
import logging

logging.basicConfig(level = logging.INFO,format = '%(asctime)s [%(process)d:%(threadName)s:%(thread)d] [%(name)s:%(lineno)d] [%(levelname)s]- %(message)s')
logger =logging.getLogger(" BINANCE ")

class binance_websocket():
    def __init__(self):
        self.ws = None

    def on_message(self, message):
        logger.info(f"message:{message}")

    def on_error(self, error):
        logger.info(error)

    def on_close(self):
        logger.info("### closed ###")

    def on_open(self):
        params = {
            "method": "SUBSCRIBE",
            "params":
                [
                    "linkbtc@trade",
                ],
            "id": 1
        }
        paras = json.dumps(params)
        logger.info(f"send: {params}")
        self.ws.send(paras)

    def run(self):
        t = threading.Thread(target=self._run,args=())
        t.run()

    def _run(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp("wss://stream.binance.com:9443/ws/linkbtc@trade",
                                         on_message = self.on_message,
                                         on_error = self.on_error,
                                         on_close = self.on_close,
                                         on_open= self.on_open)
        self.ws.run_forever()

    def inflate(self,data):
        decompress = zlib.decompressobj(
            -zlib.MAX_WBITS
        )
        inflated = decompress.decompress(data)
        inflated += decompress.flush()
        return inflated


if __name__ == "__main__":
    binance = binance_websocket()
    binance.run()
