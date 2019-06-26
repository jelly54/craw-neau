#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
from lxml import etree
from crawNEAU.Login import info_headers, login


# 获取个人历史成绩


def get_grades():
    info_headers['Referer'] = 'http://202.118.167.86:9001/gradeLnAllAction.do?type=ln&oper=qb'
    url = 'http://202.118.167.86:9001/gradeLnAllAction.do?type=ln&oper=qbinfo&lnxndm=2017-2018å­¦å¹´æ¥(ä¸¤å­¦æ)'
    resp = requests.get(url, headers=info_headers)
    # print resp.text
    selector = etree.HTML(resp.text)
    # 根据 a标签 分学期
    for i in range(0, len(selector.xpath('body/a'))):
        # 哪个学期
        title = selector.xpath('//*[@id="tblHead"]')[i].xpath('tr/td[1]/table/tr/td[2]/b/text()')[0]
        print(title)
        # 标题
        head_1 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[1]/text()')[0].strip()
        head_2 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[2]/text()')[0].strip()
        head_3 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[3]/text()')[0].strip()
        head_4 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[4]/text()')[0].strip()
        head_5 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[5]/text()')[0].strip()
        head_6 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[6]/text()')[0].strip()
        head_7 = selector.xpath('//table[@id="user"]')[i].xpath('thead/tr/th[7]/text()')[0].strip()
        print(head_1, head_2, head_3, head_4, head_5, head_6, head_7)
        # 课程信息,xpath获取list后从 0 开始计数
        trs = selector.xpath('//table[@id="user"]')[i].xpath('child::tr')
        print(len(trs))
        for tr in trs:
            class_no = tr.xpath('td[1]/text()')[0].strip()
            class_num = tr.xpath('td[2]/text()')[0].strip()
            class_name = tr.xpath('td[3]/text()')[0].strip()
            class_ename = tr.xpath('td[4]/text()')[0].strip()
            class_core = tr.xpath('td[5]/text()')[0].strip()
            class_attr = tr.xpath('td[6]/text()')[0].strip()
            class_grade = tr.xpath('td[7]/p/text()')[0].strip()
            print(class_no, class_num, class_name, class_ename, class_core, class_attr, class_grade)
        zongjie = selector.xpath('//table[@id="user"]')[i].xpath('following::table[1]/tr/td/text()')[0].strip()
        print(zongjie)
        zongjie2 = ''


if __name__ == '__main__':
    # if login('A111','111111'):
    if login('A19 ', 'A19 '):
        get_grades()
