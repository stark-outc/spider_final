# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:05:12 2020

@author: 徐钦华
"""

import requests
from pprint import pprint
import json
from datetime import datetime, timedelta
import pandas as pd
from lxml import etree
import re
from chaojiying import Chaojiying_Client
# delta = 1095
# today = datetime.today()+timedelta(days=delta)
today = datetime.today()
today_strf = today.strftime('%Y-%m-%d')
gap = 15
beginTime = (today - timedelta(days=gap)).strftime('%Y-%m-%d')
endTime = (today - timedelta(days=1)).strftime('%Y-%m-%d')
limit = 300
bank = '恒丰银行'
bank_map = {'恒丰银行': '87'}
userName_wc = "hengpujinke@wacai.com"
password_wc = "MB8wHZpUikCulI2Ak+Nl/ChHjdz6fLFkyr/yQPhMAqnH+/hbi4srFGpAGpWfksdEAf6lhZAo6tmgmo+q5C8dodmTVIR43/S56sT4Zy0oCpSz01RWJ76MRsjRY7slo0KbVAGs4IVKv8/yaStpBllK/cGvJGTl7jE8wC2GLu7lx9Q="
data_login_wc = {"userName": userName_wc, "password": password_wc}
data_target_wc = {"beginTime": beginTime, "endTime": endTime, "name": bank, "limit": str(limit), "pageNum": "1",
                  "type": "card"}
login_url_wc = 'https://dianshi.wacai.com/ssp/api/ad-merchant/api/v1/user/login'
target_url_wc = 'https://dianshi.wacai.com/ssp/api/ad-merchant/api/v1/user/settlement-data'
headers_wc = {'Accept': 'application/json, text/plain, */*',
              'Accept-Encoding': 'gzip, deflate, br',
              'Accept-Language': 'zh-CN,zh;q=0.9',
              'Connection': 'close',
              'Content-Type': 'application/json;charset=UTF-8',
              'Host': 'dianshi.wacai.com',
              'Origin': 'https://dianshi.wacai.com',
              'Referer': 'https://dianshi.wacai.com/ssp/user/login',
              'Sec-Fetch-Dest': 'empty',
              'Sec-Fetch-Mode': 'cors',
              'Sec-Fetch-Site': 'same-origin',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                            '(KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
              'x-requested-with': 'XMLHttpRequest'}

key_list_wc = ['visitNum', 'entryNum', 'oneEntryNum', 'validEntryNum', 'firstCheckNum', 'oneFirstCheckNum',
               'effectiveFirstCheckNum',
               'middleFirstCheckNum', 'highFirstCheckNum', 'awardCardNum', 'commonCardNum', 'uncommonCardNum',
               'goldCardNum', 'newUserNum', 'activationNum', 'firstBrushNum',
               'finalCheckNum', 'highQualityCustomerANum', 'highQualityCustomerBNum']
key_list_hsl = ['time', 'url_code', 'bank_name', 'company_name', 'submit', 'valid_submit', 'first_trial', 'check',
                'new_check', 'activate', 'first_brush', 'artificial', 'refused']
login_url_hsl = "http://ccard.yingbei365.com/index.php/Login/getLogin"
target_url_hsl = "http://ccard.yingbei365.com/index.php/Settlement/day_list"
data_login_hsl = {'u': 'cunying', 'p': 'hslzsjj25'}
data_target_hsl = {'bank_id': bank_map['恒丰银行'], 'page': '1', 'datemin': beginTime, 'datemax': endTime, type: 0}
headers_hsl = {'Host': 'ccard.yingbei365.com',
               'Connection': 'close',
               'Accept': 'application/json, text/plain, */*',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Origin': 'http://ccard.yingbei365.com',
               'Referer': 'http://ccard.yingbei365.com/web/',
               'Accept-Encoding': 'gzip, deflate',
               'Accept-Language': 'zh-CN,zh;q=0.9'}

save_path = 'D://银行日报相关//'

# 恒智后台
login_url_hz = 'http://console.hzphfin.com/login/ldap/login'
target_url_hz_send = 'http://console.hzphfin.com/api/marketing/task/query/list'
target_url_hz_uv = 'http://console.hzphfin.com/api/marketing/monitor/gather'

headers_hz = {'Host': 'console.hzphfin.com',
'Connection': 'close',
'Accept': 'application/json, text/plain, */*',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
'Content-Type': 'application/json',
'Origin': 'http://console.hzphfin.com',
'Referer': 'http://console.hzphfin.com/',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9'}
access_token_hz = 'eyJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJzb21lIElkIiwiaWF0IjoxNjA1NjYzNjYzLCJzdWIiOiJ7XCJyZXNDb2RlXCI6MCxcImVycm9yTXNnXCI6XCJPS1wiLFwiZGF0YVwiOm51bGx9IiwiZXhwIjoxNjA1Njk5NjYzfQ.tYA8ArsWn09oQORFaGAc-uG9USkytFjTz_Tp7UHZB6M'
data_target_hz = {"limit":1000,"page":1,"send_begin_time":beginTime,"send_end_time":today_strf}
data_target_hz_send = {"limit":1000,"page":1,"send_begin_time":today_strf,"send_end_time":today_strf}
data_target_hz_uv = {"limit":5000,"page":1,"gather_begin_time":today_strf,"gather_end_time":today_strf,"gather_type":"0"}
data_login_hz = {"name":"outc","password":"RnQrjjZIw5ps8xIWwTbppcD2SoWtwfsLBFhAy6404Ksm13UOkM8QfNvsBnxeokcznwFrcfH5xc6niXSzMPyeBV8aYV5J9duQaL/OhQ6hoe4bHp6PSU3Nq+GSZuImJFukFLNQLRW8mZ9r9/KS4xqA5cJ0bkbqOry7NjhLGk6G8o27wAFyQ0TZtmA6SOG0gUnG1rv5lDy0Me8m31lhJzdpV72+qhsXkd3Xklx/1jMSVbKtRW7Qm5/PEExB5i+KvX72w1CQ9TM7VT7XIy9pGb1hv0yffV3ISzRjUzSUljlfaiBrONMbO4J3beV+swt46unhou9XtQH2GnLoZt9NFFKzig==","verification":"avt8","ladpLoginOnly":"false"}

chaojiying = Chaojiying_Client('outianci', 'outianci520*', '910047')
# 京迅后台
headers_jx = {
'Host': '61.129.57.157:8888',
'Connection': 'keep-alive',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Referer': 'http://61.129.57.157:8888/corp/main.jsp',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9',
}
login_url_jx = 'http://61.129.57.157:8888/index.jsp'
img_url_jx = 'http://61.129.57.157:8888/verifycode.do'
# target_url_jx =
data_login_jx = {'corpCode': '400042','username': 'admin','verifyCode': 'c5s9','password': '8ba4c333c1e6f7e0b4abaa5c4cdc049d'}



