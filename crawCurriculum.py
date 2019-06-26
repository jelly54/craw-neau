import requests
from lxml import etree

from crawNEAU.Login import info_headers, login


# 从教务处获取个人课表


def get_class(date):
    #    info_headers['Referer'] = 'http://202.118.167.86:9001/menu/menu.jsp'
    #    url = 'http://202.118.167.86:9001/xkAction.do?actionType=6'
    info_headers['Referer'] = 'http://202.118.167.86:9001/lnkbcxAction.do'
    url = 'http://202.118.167.86:9001/lnkbcxAction.do'
    data = 'zxjxjhh=' + date
    resp = requests.post(url, headers=info_headers, data=data)
    # print(resp.text)
    selector = etree.HTML(resp.text)
    for i in range(2, 8):
        week = selector.xpath('//*[@id="user"]/thead/tr[1]/td[' + str(1 + i) + ']/div/text()')[0].strip()
        th1 = selector.xpath('//*[@id="user"]/thead/tr[3]/td[2]/text()')[0].strip()
        cla1 = selector.xpath('//*[@id="user"]/thead/tr[3]/td[' + str(1 + i) + ']/text()')[0].strip()
        th2 = selector.xpath('//*[@id="user"]/thead/tr[5]/td[1]/text()')[0].strip()
        cla2 = selector.xpath('//*[@id="user"]/thead/tr[5]/td[' + str(i) + ']/text()')[0].strip()

        th3 = selector.xpath('//*[@id="user"]/thead/tr[8]/td[2]/text()')[0].strip()
        cla3 = selector.xpath('//*[@id="user"]/thead/tr[8]/td[' + str(1 + i) + ']/text()')[0].strip()
        th4 = selector.xpath('//*[@id="user"]/thead/tr[10]/td[1]/text()')[0].strip()
        cla4 = selector.xpath('//*[@id="user"]/thead/tr[10]/td[' + str(i) + ']/text()')[0].strip()

        th5 = selector.xpath('//*[@id="user"]/thead/tr[13]/td[2]/text()')[0].strip()
        cla5 = selector.xpath('//*[@id="user"]/thead/tr[13]/td[' + str(1 + i) + ']/text()')[0].strip()
        # //*[@id="user"]/thead/tr[15]/td[1]
        th6 = selector.xpath('//*[@id="user"]/thead/tr[15]/td[1]/text()')[0].strip()
        cla6 = selector.xpath('//*[@id="user"]/thead/tr[15]/td[' + str(i) + ']/text()')[0].strip()
        print('%s \n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n%s\t%s\n' % (
            week, th1, cla1, th2, cla2, th3, cla3, th4, cla4, th5, cla5, th6, cla6))


if __name__ == '__main__':
    # if login('A1 ','xxx'):
    if login('A19', 'A19'):
        # 获取课表 zxjxjhh=2017-2018-1-1  秋 zxjxjhh=2017-2018-2-1  春
        date = '2018-2019-2-1'
        get_class(date)
