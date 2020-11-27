# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:08:54 2020

@author: 徐钦华
"""
import requests
from pprint import pprint
import json
from datetime import datetime,timedelta
import pandas as pd
from config import *
from OP_Method import DingDingRobotService
class get_table_spider(object):
    def __init__(self):
        self.beginTime = beginTime
        self.endTime = endTime
    def get_data(self, partner=None, headers=None, data_login=None, data_target=None, login_url=None, target_url=None):
        session = requests.Session()
        session.keep_alive = False
        if partner == 'wc':
            res0 = session.post(login_url, data=json.dumps(data_login), headers=headers)
            token = res0.json().get('tokenId')
            session.headers.update({'token': token})
            res = session.post(target_url, data=json.dumps(data_target), headers=headers)
            return res.json()
        elif partner == 'hsl':
            res0 = session.post(login_url, data=data_login, headers=headers)
            res0.encoding = res0.apparent_encoding
            session3rd = res0.json().get('data')['session3rd']
            data_target['session3rd'] = session3rd
            res = session.post(target_url, data=data_target, headers=headers)
            res.encoding = res.apparent_encoding
            num = res.json().get('data')['count']
            page_num = int(num) // 10 + 1
            lst = []
            for n in range(1, page_num + 1):
                data_target['page'] = n
                res1 = session.post(target_url, data=data_target, headers=headers)
                res1.encoding = res.apparent_encoding
                lst.append(res1.json())
            return lst

        elif partner == 'hz':
            res0 = session.post(login_url, data=json.dumps(data_login), headers=headers)
            res0.encoding = res0.apparent_encoding
            session.headers.update({'access-token':res0.headers['Access-Token']})
            res = session.post(target_url,data=json.dumps(data_target),headers=headers)
            return res.json()
    def parse_data_wc(self):
        data = self.get_data(partner='wc', headers=headers_wc, data_login=data_login_wc, data_target=data_target_wc,
                             login_url=login_url_wc, target_url=target_url_wc)
        card = data.get('objects')
        lst = []
        for i in card:
            dic = dict()
            dic['stat_date'] = i['settlementDate']
            dic['bank'] = i['financeOrg']['shortName']
            dic['channelCode'] = i['channelCode']
            for j in key_list_wc:
                dic[j] = i[j]
            lst.append(dic)
        final_data = pd.DataFrame(lst)
        final_data['stat_date'] = final_data['stat_date'].map(lambda x: str(x)[:10])
        return final_data

    def parse_data_hsl(self):
        data = self.get_data(partner='hsl', headers=headers_hsl, data_login=data_login_hsl, data_target=data_target_hsl,
                             login_url=login_url_hsl, target_url=target_url_hsl)
        group_lst = list()
        for i in data:
            lst = list()
            card = i.get('data')['list']
            for j in card:
                dic = dict()
                for q in key_list_hsl:
                    dic[q] = j[q]
                lst.append(dic)
            group_lst.extend(lst)
        final_data = pd.DataFrame(group_lst)
        # final_data['time'] = final_data['time'].map(lambda x: str(x)[:10])
        return final_data

    def parse_data_hz_url(self):
        data = self.get_data(partner='hz',headers=headers_hz,data_login=data_login_hz,data_target=data_target_hz,login_url=login_url_hz,target_url=target_url_hz_send)
        target_url = data.get('data')['list']
        url_lst = list()
        for i in target_url:
            url_lst.append(i['target_url'])
        url_lst = set(url_lst)
        return url_lst
    def parse_data_hz_uv(self):

        uv_data_hz = self.get_data(partner='hz',headers=headers_hz,data_login=data_login_hz,data_target=data_target_hz_uv,login_url=login_url_hz,target_url=target_url_hz_uv)
        uv_data = uv_data_hz.get('data')['list']
        uv_lst = list()
        for j in uv_data:
            uv_dic = dict()
            uv_dic['batch_no'] = j['batch_no']
            uv_dic['ip_distinct_count'] = j['ip_distinct_count']
            uv_dic['send_time'] = j['send_time']
            uv_lst.append(uv_dic)
        uv_dataframe = pd.DataFrame(uv_lst)
        return uv_dataframe

    def parse_data_hz_send(self):
        save_data_hz = self.get_data(partner='hz', headers=headers_hz, data_login=data_login_hz,
                                                   data_target=data_target_hz_send, login_url=login_url_hz,
                                                   target_url=target_url_hz_send)
        send_data = save_data_hz.get('data')['list']
        send_lst = list()
        for i in send_data:
            send_dic = dict()
            send_dic['batch_no'] = i['batch_no']
            send_dic['commit_status'] = i['commit_status']
            send_dic['send_time'] = i['send_time'][:10]
            send_lst.append(send_dic)
        send_dataframe = pd.DataFrame(send_lst)
        send_dataframe = send_dataframe[send_dataframe['commit_status'] == '发送成功']
        uv_dataframe = self.parse_data_hz_uv()
        today_send_uv = pd.merge(send_dataframe,uv_dataframe,how='left',on='batch_no')
        not_send_batch = today_send_uv[today_send_uv['ip_distinct_count']<150]
        not_send_batch_lst = not_send_batch['batch_no'].to_list()
        if len(not_send_batch_lst)>0:
            return not_send_batch_lst
        else:
            return None


def save_data(save_data=None, save_partner=None):
    re_date = today.strftime('%m%d')
    save_data.to_csv(save_path + f'{save_partner}_form' + re_date + '.csv', encoding='utf_8_sig', index=False,
                     line_terminator="\n")
    return print(f'{save_partner}_form{re_date}.csv 成功写入')
def dingding_service(url,title,data_list):
    dd_server = DingDingRobotService(url=url,message_type=1)
    if data_list:
        for i in data_list:
            text = f'发送监控：\n该发送批次可能仍未下发,请及时确认：\n{i}\n'
            dd_server.dingding(title,text,file_url=None)
    else:
        return None


if __name__=='__main__':
    url = ''
    title = '发送监控'
    data_list = get_table_spider().parse_data_hz_send()
    # dingding_service(url,title,data_list)