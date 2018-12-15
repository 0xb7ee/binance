#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2018-10-11 下午5:24
'''
'''

'''
import datetime
import logging
import time

import binance
import itchat
import numpy as np

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
keys = binance.prices().keys()
itchat.auto_login(hotReload=True, enableCmdQR=2)
friends = itchat.get_friends
NICKNAME_USERNAME = {}
for friend in friends:
    NICKNAME_USERNAME[friend['NickName']] = friend['UserName']
'''
kline = 
{'close': u'0.00001842',
 'closeTime': 1539250199999,
 'high': u'0.00001960',
 'low': u'0.00001831',
 'numTrades': 1762,
 'open': u'0.00001869',
 'openTime': 1539248400000,
 'quoteVolume': u'66.55352920',
 'volume': u'3471331.00000000'}

'''
def isPositive(line):
    open = float(line['open'])
    close = float(line['close'])
    if close>open:
        return True
    elif close<open:
        return False
    else:
        return None

def is3Positive(lines):
    if isPositive(lines[-2]) and isPositive(lines[-3]) and isPositive(lines[-4]):
        return True
    elif not (isPositive(lines[-2]) or isPositive(lines[-3]) or isPositive(lines[-4])):
        return False
    else:
        return None


def get24hourVolume(ThreePositiveWeekKlin):
    for key in ThreePositiveWeekKlin:
        hkline1h = binance.klines(key, '1h')
        for line in hkline1h[-24:]:
            line['volume']
    try:
        kline = binance.klines(key, '1w')
        ret = is3Positive(kline)
        if not ret is None and ret == True and not isPositive(kline[-5]):
            ThreePositiveWeekKlin.append(key)
    except Exception:
        logging.error("Total week klines is less than 3 " + key + " in 1 week line")


def getNow():
    return str(datetime.datetime.now() + datetime.timedelta(hours=8))


def job1():
    logging.info("周线首次三连阳的BTC交易对")
    ThreePositiveWeekKlinKEY = []
    for key in keys:
        if key[-3:] != 'BTC':
            continue
        try:
            kline = binance.klines(key, '1w')
            ret = is3Positive(kline)
            if not ret is None and ret == True and not isPositive(kline[-5]):
                ThreePositiveWeekKlinKEY.append(key)
        except Exception:
            logging.error("Total week klines is less than 3 " + key + " in 1 week line")
    if len(ThreePositiveWeekKlinKEY > 0):
        MSG = "最近周线三连阳的BTC交易对如下：\n" + "\n".join(ThreePositiveWeekKlinKEY + "\n+@%s|n" % getNow())
        itchat.send(MSG, NICKNAME_USERNAME['Forrest'])
        logging.info(MSG + " 发送到了Forrest")
    else:
        logging.info("暂无周线三连阳的BTC交易对")


def getLast30MinLine(kline):
    closeTime = kline[-1]['closeTime']
    now = time.time() * 1000
    if now < closeTime:
        return kline[:-1]
    else:
        return kline


def compute_30min_volume_rate(real_kline):
    # 获取最近三天的30分钟线中成交量最大的一次
    volumnList = [float(i['volume']) for i in real_kline[143:-1]]
    max_volumn = max(volumnList)
    delta_3 = np.mean(volumnList) + 3 * np.std(volumnList, ddof=1)
    this_volumn = float(real_kline[-1]['volume'])
    rate = (this_volumn * 1.0 / max_volumn) * (this_volumn * 1.0 / delta_3)
    return rate


def job2():
    logging.info("30分钟线暴拉的BTC交易对")
    ThirtyMinutesBigVolumn = []
    for key in keys:
        if key[-3:] != 'BTC':
            continue
        try:
            kline = binance.klines(key, '30m')
            real_kline = getLast30MinLine(kline)
            if not isPositive(real_kline[-1]):
                continue
            volume = real_kline[-1]['volume']
            rate = compute_30min_volume_rate(real_kline)
            if rate > 1:
                ThirtyMinutesBigVolumn.append(key)
                logging.info("[ BIG VOLUMNE ]" + key + " with volumn:" + str(volume) + " ,volume rate is :" + str(rate))
        except Exception:
            logging.error("Total week klines is less than 3 " + key + " in 1 week line")
            logging.error(exc_info=True)
    if len(ThirtyMinutesBigVolumn > 0):
        MSG = "30分钟成交巨量的BTC交易对如下：\n" + "\n".join(ThirtyMinutesBigVolumn)
        itchat.send(MSG, NICKNAME_USERNAME['Forrest'])
        logging.info(MSG + " 发送到了Forrest")
    else:
        logging.info("暂无周线三连阳的BTC交易对")


if __name__ == "__main__":
    # itchat.send("hello",NICKNAME_USERNAME['Forrest'])
    job1()
    job2()
    # schedule.every().monday.at("08:01").do(job1)
    # schedule.every(30).minute.do(job2)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
