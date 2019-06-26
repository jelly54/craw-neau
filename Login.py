#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from shutil import copyfile

import requests
from PIL import Image
import pytesseract
from lxml import etree

# 登录教务处

# 头部信息
info_headers = {
    'Accept': 'text/html,application/xhtml+xml,image/jxr,*/*',
    'Host': "202.118.167.86:9001",
    'Accept-Language': "zh-CN",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/x-www-form-urlencoded",
    'Connection': "Keep-Alive",
    'Cookie': '',
    'Referer': '',
    'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)"
}
login_headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': "202.118.167.86:9001",
    'Accept-Language': "zh-CN,zh,q=0.8",
    'Accept-Encoding': "gzip, deflate",
    'Content-Type': "application/x-www-form-urlencoded",
    'Connection': "Keep-Alive",
    'Content-Length': '44',
    'Cache-Control': 'max - age = 0',
    'Origin': 'http://202.118.167.86:9001',
    'Upgrade-Insecure-Requests': '1',
    'Cookie': '',
    'Referer': "http://202.118.167.86:9001/",
    'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 10.0; WOW64; Trident/7.0)"
}

def init_table(threshold=125):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    return table


def get_url_code(username, password):
    im = Image.open('checkcode.jpg')
    im = im.convert('L')
    binaryImage = im.point(init_table(), '1')
    # binaryImage.show()
    code = pytesseract.image_to_string(binaryImage, config='--psm 7')
    pattern = re.compile(u'[a-zA-Z0-9]{4}')
    match = pattern.match(code)
    if match:
        print("验证码解析为四位", end='； ')
        return code
    else:
        print("验证码=", code, "将重新生成", end='； ')
        return "1"


def refresh_code(session, username, password, is_one):
    code_url = 'http://202.118.167.86:9001/validateCodeAction.do?random=0.8875258917591355'
    code_resp = session.get(code_url)
    if is_one:
        cookies = code_resp.headers['Set-Cookie']
        cookies = cookies.strip(';path=/')
        info_headers['Cookie'] = cookies
        login_headers['Cookie'] = cookies
    check_code = session.get(code_url, timeout=60 * 4)
    with open('checkcode.jpg', 'wb') as f:
        f.write(check_code.content)
    # 复制生成的验证码
    # copyfile('./checkcode.jpg', 'D:/Documents_Pychar/num-font/code/code-'+str(i)+".jpg")
    init_table()
    var_code = get_url_code(username, password).replace(' ', '')  # 自动识别验证码
    return var_code


def login(username, password):
    mysession = requests.session()
    var_code = refresh_code(mysession, username, password, True)
    while var_code == "1":
       var_code = refresh_code(mysession, username, password, False)
    login_url = 'http://202.118.167.86:9001/loginAction.do'
    login_data = {
        'zjh1': '',
        'tips': '',
        'lx': '',
        'evalue': '',
        'eflag': '',
        'fs': '',
        'dzslh': '',
        'zjh': username,
        'mm': password,
        'v_yzm': var_code
    }
    #  将账号，密码，验证码和表头Post上去
    #  wo们可以用过BeautifulSoup或者正则表达式，抓取d.text有用的信息，判断是否登录成功
    resp = mysession.post(url=login_url, headers=login_headers, data=login_data)
    # print resp.text
    error = etree.HTML(resp.text).xpath('//td[@class="errorTop"]')
    if len(error) == 0:
        print('\n', username, '登录成功')
        return True
    else:
        print('\n', username, '登录失败')
        return False


if __name__ == '__main__':
    if login('A19', 'A19'):
        print("111")
