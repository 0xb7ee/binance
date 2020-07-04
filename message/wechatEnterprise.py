#!/usr/bin/python
# -*- coding:utf-8 -*- 
'''
作者:jia.zhou@aliyun.com
创建时间:2020-06-08 下午3:08
'''
import json

import requests


def sendMessageForUser(content):
    corpid = 'ww2a75e4df23d09862'
    agentid = '1000002'
    secret = 'tHR2nZrfDLG_6R2RU6edoXKRnakedyw7c63jFYDudB8'
    url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={}&corpsecret={}'
    getr = requests.get(url=url.format(corpid,secret))
    access_token = getr.json().get("access_token")
    data = {
        "touser" : "ZhouJia",
        # "toparty" : "PartyID1|PartyID2",   # 向这些部门发送
        "msgtype" : "text",
        "agentid" : agentid,                       # 应用的 id 号
        "text" : {
            "content" : content
        },
        "safe":0
    }
    requests.post(url="https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={}".format(access_token),
                      data=json.dumps(data))