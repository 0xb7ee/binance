import datetime
import functools
import json
import logging
import threading
import time

import binance
import imgkit
import numpy as np
import pandas as pd
import requests
from requests_toolbelt import MultipartEncoder
from sqlalchemy import create_engine

engine = create_engine('mysql://root:eos@localhost/crypto?charset=utf8')

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
logger = logging.getLogger("【binance】")
keys = binance.prices().keys()


def computBoll(close_array):
    mean = close_array.mean()
    std = close_array.std()
    return (mean + 2 * std, mean, mean - 2 * std)


def sendMessageForUser(content):
    corpid = 'ww2a75e4df23d09862'
    agentid = '1000002'
    secret = 'tHR2nZrfDLG_6R2RU6edoXKRnakedyw7c63jFYDudB8'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
    getr = requests.get(url=url.format(corpid, secret))
    access_token = getr.json().get("access_token")
    data = {
        "touser": "ZhouJia",
        # "toparty" : "PartyID1|PartyID2",   # 向这些部门发送
        "msgtype": "text",
        "agentid": agentid,  # 应用的 id 号
        "text": {
            "content": content
        },
        "safe": 0
    }
    requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                  data=json.dumps(data))


def sendImgMessageForUser(imageid):
    corpid = 'ww2a75e4df23d09862'
    agentid = '1000002'
    secret = 'tHR2nZrfDLG_6R2RU6edoXKRnakedyw7c63jFYDudB8'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
    getr = requests.get(url=url.format(corpid, secret))
    access_token = getr.json().get("access_token")
    data = {
        "touser": "ZhouJia",
        "totag": "TagID1 | TagID2",
        "msgtype": "image",
        "agentid": agentid,
        "image": {
            "media_id": f"{imageid}"
        },
        "safe": 0,
        "enable_duplicate_check": 0,
        "duplicate_check_interval": 1800
    }
    requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                  data=json.dumps(data))


def uploadTmpFile(path):
    corpid = 'ww2a75e4df23d09862'
    secret = 'tHR2nZrfDLG_6R2RU6edoXKRnakedyw7c63jFYDudB8'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
    getr = requests.get(url=url.format(corpid, secret))
    access_token = getr.json().get("access_token")
    url = f"https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=image"
    multipart_encoder = MultipartEncoder(
        fields={
            'params': json.dumps(
                {"Content-Disposition": "form-data; name='media';filename='boll.jpg'; filelength=120032"}),
            'file': ('file', open(path, 'rb'), 'application/octet-stream')
        },

    )

    headers = {"Content-Type": multipart_encoder.content_type}
    r = requests.post(url, data=multipart_encoder, headers=headers)
    response = r.json()
    return response['media_id']


def isPositive(line):
    open = float(line['open'])
    close = float(line['close'])
    if close > open:
        return True
    elif close < open:
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


def is3std(lines, key):
    df = pd.DataFrame(lines[:-1])
    hight = df.high.astype(float)
    std = hight.std()
    mean = hight.mean()
    if float(df.iloc[-1, :].close) > mean + 3 * std:
        sendMessageForUser(key)


def computd_diff(boll):
    '''
    计算boll线指标的时间查
    :param boll:
    :return:
    '''
    boll_1 = boll[1:]
    boll = boll[:-1]
    days = []
    times = []
    for i in range(len(boll)):
        timedelta = boll_1[i][0] - boll[i][0]
        day = timedelta.days + timedelta.seconds / (14400 * 6)
        days.append(day)
        times.append(boll[i][0])
    return days, times


def isPositiveBoll(lines, key):
    result = None
    boll = []
    boll_data = []
    rdn_close = [float(i['close']) for i in lines]
    rate_dict = {}
    last_kline = ""
    info = None
    boll_data = {}
    close = rdn_close[-1]
    close = '{:.10f}'.format(close)
    for i in range(22, len(rdn_close)):
        rdn_class = lines[i]
        time = datetime.datetime.fromtimestamp(rdn_class['openTime'] / 1000)
        k3 = np.array(rdn_close[i - 20:i + 1])
        k2 = np.array(rdn_close[i - 21:i])
        k1 = np.array(rdn_close[i - 22:i - 1])
        # print(f"{time}\tk1从{i-23}到{i-4}\tk2从{i-22}到{i-3}\tk3从{i-21}到{i-2}")
        k3_upper, k3_middle, k3_lowwer = computBoll(k3)
        k2_upper, k2_middle, k2_lowwer = computBoll(k2)
        k1_upper, k1_middle, k1_lowwer = computBoll(k1)
        k3up = k3_upper / k2_upper
        k2up = k2_upper / k1_upper
        k3md = k3_middle / k2_middle
        k2md = k2_middle / k1_middle
        k3lw = k3_lowwer / k2_lowwer
        k2lw = k2_lowwer / k1_lowwer
        boll_data[time] = k3_upper, k3_middle, k3_lowwer, k2_upper, k2_middle, k2_lowwer, k1_upper, k1_middle, k1_lowwer
        rate = k2up * k3up * k2md * k3md * (1 / k2lw) * (1 / k3lw)
        if k2up > 1 and k3up > 1 and k2md > 1 and k3md > 1 and k2lw < 1 and k3lw < 1:
            boll.append([time, k3up, k2up, k3md, k2md, k3lw, k2lw])
            rate_dict[time] = rate
    if len(boll) >= 2:
        # print(f"【{key}】{str(boll[-1][0])} {boll[-1][1]} {boll[-1][2]} {boll[-1][3]} {boll[-1][4]} {boll[-1][5]} {boll[-1][6]}")
        latest = boll[-2:]
        timedelta = latest[1][0] - latest[0][0]
        last_kline = str(latest[0][0])
        hours = timedelta.days * 24 + timedelta.seconds / 60 / 60
        nowdelta = datetime.datetime.now() - latest[1][0]
        nowhours = nowdelta.days * 24 + nowdelta.seconds / 60 / 60
        if not (hours < 24 * 2 or nowhours > 24):
            logger.info(f"【交易对{key}\tprice:{close}\t@{boll[-1][0]}\trate: {round(rate_dict[boll[-1][0]], 5)}】")
            info = (key, str(boll[-1][0]), round(rate_dict[boll[-1][0]], 5), last_kline, boll_data[boll[-1][0]], close)
            result = info
    return result


def positive_boll(lines, key):
    boll = []
    rdn_close = [float(i['close']) for i in lines]
    boll_data = {}
    for i in range(22, len(rdn_close)):
        rdn_class = lines[i]
        close = rdn_close[i]
        time = datetime.datetime.fromtimestamp(rdn_class['openTime'] / 1000)
        k3 = np.array(rdn_close[i - 20:i + 1])
        k2 = np.array(rdn_close[i - 21:i])
        k1 = np.array(rdn_close[i - 22:i - 1])
        k3_upper, k3_middle, k3_lowwer = computBoll(k3)
        k2_upper, k2_middle, k2_lowwer = computBoll(k2)
        k1_upper, k1_middle, k1_lowwer = computBoll(k1)
        k3up = k3_upper / k2_upper
        k2up = k2_upper / k1_upper
        k3md = k3_middle / k2_middle
        k2md = k2_middle / k1_middle
        k3lw = k3_lowwer / k2_lowwer
        k2lw = k2_lowwer / k1_lowwer
        boll_data[time] = k3_upper, k3_middle, k3_lowwer, k2_upper, k2_middle, k2_lowwer, k1_upper, k1_middle, k1_lowwer
        rate = k2up * k3up * k2md * k3md * (1 / k2lw) * (1 / k3lw)
        if k2up > 1 and k3up > 1 and k2md > 1 and k3md > 1 and k2lw < 1 and k3lw < 1:
            boll.append([key, time, close, rate, k3up, k2up, k3md, k2md, k3lw, k2lw])
    return boll


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
        logger.error("Total week klines is less than 3 " + key + " in 1 week line")


def getNow():
    return str(datetime.datetime.now() + datetime.timedelta(hours=8))


def comput_vp(data, key):
    lines = []
    for i in data.iloc[84:]['openTime'].values:
        close = data[data['openTime'] == i]['close'].values[0]
        trank = vp_rank(data, i)
        if trank[0][0] >= 1.5 and trank[0][1] >= 1.5:
            lines.append([key, datetime.datetime.fromtimestamp(i / 1000), close, trank[0][0], trank[0][1], trank[1][0],
                          trank[1][1]])
    return lines


def index_value(data, time_end, end):
    end_data = data[data['openTime'] == end]
    t = data[(data['openTime'] >= time_end) & (data['openTime'] < end)]
    # t = t.sort_values('volume',ascending=False)
    # t = t.reset_index(drop=True)
    # volume_index = t[t['openTime']==end].index.values[0]+1
    volume_mean = t['volume'].mean()
    volume_std = t['volume'].std()
    v_index = (end_data['volume'].values[0] - volume_mean) / volume_std

    # t = t.sort_values('close',ascending=False)
    # t = t.reset_index(drop=True)
    # close_index = t[t['openTime']==end].index.values[0]+1
    close_mean = t['close'].mean()
    close_std = t['close'].std()
    c_index = (end_data['close'].values[0] - close_mean) / close_std
    return (v_index, c_index)


def vp_rank(data, end):
    one_week_end = end - 1000 * 60 * 60 * 24 * 7
    two_week_end = end - 1000 * 60 * 60 * 24 * 7 * 2
    # three_week_end = end-1000*60*60*24*7*3
    # four_week_end = end-1000*60*60*24*7*4
    # two_month_end = end-1000*60*60*24*7*8
    # three_month_end = end-1000*60*60*24*7*12
    # time_end = [one_week_end,two_week_end,three_week_end,four_week_end,two_month_end,three_month_end]
    time_end = [one_week_end, two_week_end]
    ret = []
    for i in time_end:
        index_v = index_value(data, i, end)
        ret.append([index_v[0], index_v[1]])
    return ret


def job1():
    logger.info(u"##############周线首次三连阳的BTC交易对##############")
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
            logger.error("Total week klines is less than 3 " + key + " in 1 week line")
    if len(ThreePositiveWeekKlinKEY) > 0:
        a = "\n".join(ThreePositiveWeekKlinKEY)
        b = getNow()
        MSG = u"##############最近一周周线三连阳的BTC交易对如下：\n" + a + u"\n发布时间:@%s" % b + u"##############"
        sendMessageForUser(MSG)
        logger.info(MSG + u" 发送到了Forrest")
    else:
        logger.info("暂无周线三连阳的BTC交易对")


def getLast30MinLine(kline):
    closeTime = kline[-1]['closeTime']
    now = time.time() * 1000
    if now < closeTime:
        return kline[:-1]
    else:
        return kline


def compute_30min_volume_rate(real_kline):
    # 获取最近三天的30分钟线中成交量最大的一次
    volumnList = [float(i['volume']) for i in real_kline[-145:-1]]
    max_volumn = max(volumnList)
    delta_3 = np.mean(volumnList) + 3 * np.std(volumnList, ddof=1)
    this_volumn = float(real_kline[-1]['volume'])
    rate = (this_volumn * 1.0 / max_volumn) * (this_volumn * 1.0 / delta_3)
    return rate


def job2():
    logger.info(u"##############30分钟线暴拉的BTC交易对##############")
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
                msg = key + u":" + kline[-1]['close']
                ThirtyMinutesBigVolumn.append(msg)
                logger.info(
                    u"##############[ BIG VOLUMNE ]" + key + u" with volumn:" + str(
                        volume) + u" ,volume rate is :" + str(rate) + u"##############")
            else:
                # logger.info(
                #     u"##############[ Normal VOLUMNE ]" + key + u" with volumn:" + str(volume) + u" ,volume rate is :" + str(rate)+u"##############")
                pass
        except Exception as e:
            logger.error(u"##############Total week klines is less than 3 " + key + u" in 1 week line##############")
            logger.error(e, exc_info=True)
    if len(ThirtyMinutesBigVolumn) > 0:
        MSG = u"30分钟成交巨量的BTC交易对如下：\n" + u"\n".join(ThirtyMinutesBigVolumn)
        sendMessageForUser(MSG)
        logger.info(u"##############" + MSG + u" 发送到了Forrest##############")
    else:
        logger.info(u"##############暂无30分钟暴拉的BTC交易对##############")


def convert2tds(posBollKlinKEY):
    ret = ""
    for i in posBollKlinKEY:
        tds = ""
        pair = i[0][:-3]
        time = i[1]
        rate = i[2]
        last_time = i[3]
        close = i[5]
        line = i[4]
        line = [k for k in map(format, line)]
        up = line[0]
        md = line[1]
        lw = line[2]
        up_1 = line[3]
        md_1 = line[4]
        lw_1 = line[5]
        up_2 = line[6]
        md_2 = line[7]
        lw_2 = line[8]
        for j in [pair, close, rate, time, last_time, up, md, lw, up_1, md_1, lw_1]:
            tds += f"<td>{j}</td>"
        ret += f"<tr>{tds}</tr>"
    return ret


def format(boll):
    return '{:.10f}'.format(boll)


def isbigline(kline):
    df = pd.DataFrame(kline)
    df['close'] = df['close'].astype(float)
    df['open'] = df['open'].astype(float)
    df['rate'] = df['close'] / df['open'] - 1


def comput_realtime_vp(data, key):
    '''
    计算实时量价关系
    :param data:
    :param key:
    :return:
    '''
    end = data.iloc[-1]['openTime'].values[0]
    close = data.iloc[-1]['close'].values[0]
    trank = vp_rank(data, end)
    lines = []
    if trank[0][0] >= 1.5 and trank[0][1] >= 1.5:
        lines.append([key, datetime.datetime.fromtimestamp(end / 1000), close, trank[0][0], trank[0][1], trank[1][0],
                      trank[1][1]])
    return lines


def comput_realtime_boll(lines, key):
    boll = []
    rdn_close = [float(i['close']) for i in lines]
    close = rdn_close[-1]
    boll_data = {}
    i = len(rdn_close)
    rdn_class = lines[i - 1]
    time = datetime.datetime.fromtimestamp(rdn_class['openTime'] / 1000)
    k3 = np.array(rdn_close[i - 20:i + 1])
    k2 = np.array(rdn_close[i - 21:i])
    k1 = np.array(rdn_close[i - 22:i - 1])
    k3_upper, k3_middle, k3_lowwer = computBoll(k3)
    k2_upper, k2_middle, k2_lowwer = computBoll(k2)
    k1_upper, k1_middle, k1_lowwer = computBoll(k1)
    k3up = k3_upper / k2_upper
    k2up = k2_upper / k1_upper
    k3md = k3_middle / k2_middle
    k2md = k2_middle / k1_middle
    k3lw = k3_lowwer / k2_lowwer
    k2lw = k2_lowwer / k1_lowwer
    boll_data[time] = k3_upper, k3_middle, k3_lowwer, k2_upper, k2_middle, k2_lowwer, k1_upper, k1_middle, k1_lowwer
    rate = k2up * k3up * k2md * k3md * (1 / k2lw) * (1 / k3lw)
    if k2up > 1 and k3up > 1 and k2md > 1 and k3md > 1 and k2lw < 1 and k3lw < 1:
        boll.append([key, time, close, rate, k3up, k2up, k3md, k2md, k3lw, k2lw])
    return boll


def job3():
    '''
    计算boll线向上
    :return:
    '''
    logger.info(f"EXEC_TIME:{str(datetime.datetime.now())}")
    posBollKlinKEY = []
    for key in keys:
        if key[-3:] == 'BTC':
            try:
                logger.info(f"计算 {key} 的历史量价")
                kline = binance.klines(key, '4h')
                data = pd.DataFrame(kline[:-1])
                data['quoteVolume'] = data['quoteVolume'].astype('float')
                data['volume'] = data['volume'].astype('float')
                data['close'] = data['close'].astype('float')
                vp = comput_vp(data, key)
                boll = positive_boll(kline[:-1], key)
                vp_df = pd.DataFrame(vp, columns=['key', 'time', 'close', 'vol_1w_std', 'prc_1w_std', 'vol_2w_std',
                                                  'prc_2w_std'])
                boll_df = pd.DataFrame(boll,
                                       columns=['key', 'time', 'close', 'rate', 'k3up', 'k2up', 'k3md', 'k2md', 'k3lw',
                                                'k2lw'])
                vp_df.to_sql('binance_vp', engine, index=False, if_exists='append')
                boll_df.to_sql('binance_boll', engine, index=False, if_exists='append')
                # ret = pd.merge(vp_df,boll_df,how='inner',left_on='time',right_on='time')
                # if ret is not None and len(ret) > 0:
                #     # logger.info(f"【{key}】{ret[0]}")
                #     posBollKlinKEY.append(ret)
            except Exception as e:
                logger.error(key)
                logger.error(e, exc_info=True)


def job3_send(posBollKlinKEY):
    key = functools.cmp_to_key(lambda a, b: cmp(a, b))
    posBollKlinKEY = sorted(posBollKlinKEY, key=key, reverse=True)
    if len(posBollKlinKEY) > 0:
        trs = convert2tds(posBollKlinKEY)
        html = '''
                <html>
                <head>
                    <style type="text/css">
                        table {
                            border-collapse: collapse;
                            border:1px solid #f4f4f4;;
                        }
                        thead th {
                            font-size: 20px;
                            text-align: left;
                            background: #20BAE6;
                            color: #fff;
                            font-weight: 100;
                            line-height: 30px;
                        }
                        tbody tr {
                            width: 400px;
                            height: 20px;
                        }
                        tbody td {
                            font-size: 9px;
                            color: #59004a;
                            line-height: 0px;
                            /*border:1px solid #dddddd;*/
                        }
                    </style>
                    <meta charset="UTF-8">
                </head>
                <body>
                <table>
                    <thead>
                    <th style="width: 40px">pair</th>
                    <th style="width: 100px">close</th>
                    <th style="width: 70px">rate</th>
                    <th style="width: 140px">now</th>
                    <th style="width: 140px">past</th>
                    <th style="width: 100px">upper</th>
                    <th style="width: 100px">middle</th>
                    <th style="width: 100px">lowwer</th>
                    <th style="width: 100px">upper_1</th>
                    <th style="width: 100px">middle_1</th>
                    <th style="width: 100px">lowwer_1</th>
                    </thead>
                    <tbody>
                    %s
                    </tbody>
                </table>
                </body>
                </html>''' % trs
        fit = open("tmp.html", 'w+')
        fit.write(html)
        fit.close()
        path = "out.png"
        with open("tmp.html") as f:
            imgkit.from_file(f, path)
        imgid = uploadTmpFile(path)
        sendImgMessageForUser(imgid)
        logger.info(imgid + u" 发送到了Forrest")
    else:
        logger.info("暂无4h Boll线向上的BTC交易对")


def cmp(x1, x2):
    if x1[1] > x2[1]:
        return 1
    elif x1[1] == x2[1]:
        if x1[2] >= x2[2]:
            return 0
        else:
            return -1
    else:
        return -1


def buyer_thread_job2():
    threading.Thread(job2()).start()


if __name__ == "__main__":
    # itchat.send("hello",NICKNAME_USERNAME['Forrest'])
    # job1()
    # job2()
    # schedule.every().monday.at("08:01").do(job1)
    # now = datetime.datetime.now()
    # while not (now.hour == 12 and now.minute == 0):
    #     time.sleep(5)
    #     now = datetime.datetime.now()
    # logger.info(u"##############BEGIN TO DO JOB2##############")
    # schedule.every(30).minutes.do(buyer_thread_job2)
    # job3()
    job3()
    # schedule.every().day.at("00:00").do(job3)
    # schedule.every().day.at("04:00").do(job3)
    # schedule.every().day.at("08:00").do(job3)
    # schedule.every().day.at("12:00").do(job3)
    # schedule.every().day.at("16:00").do(job3)
    # schedule.every().day.at("20:00").do(job3)
    # while True:
    #         schedule.run_pending()
    #         time.sleep(1)
