from spider import *
from config import *
from chaojiying import Chaojiying_Client
class get_td_spider(object):
    def __init__(self):
        self.beginTime = beginTime
        self.endTime = endTime
    def get_data(self, partner=None, headers=None, data_login=None, data_target=None, login_url=None, target_url=None):
        session = requests.Session()
        session.keep_alive = False
        if partner == 'jx':
            session.get(login_url,  headers=headers)
            code_img = session.get(img_url_jx,headers=headers).content
            verifyCode = chaojiying.PostPic(code_img,'1902')
            data_login['verifyCode'] = verifyCode
            login = session.post(login_url,headers=headers,data=data_login)
            return login.text

    def get_login_img_jx(self):
        page_text = self.get_data(partner='jx',headers=headers_jx,login_url=login_url_jx)

        return img_url

if __name__==  '__main__':
    pprint(get_td_spider().get_data(partner='jx',headers=headers_jx,login_url=login_url_jx,data_login=data_login_jx))
    # chaojiying = Chaojiying_Client('outianci', 'outianci520*', '910047')
    # ver = chaojiying.PostPic(im,'1902')
    # print(ver)