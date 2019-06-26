import time
from shutil import copyfile

import requests
from lxml import etree
from crawNEAU.Login import info_headers, login
from crawNEAU.MysqlTools import update_info, select_info


# 抓取教务处学籍信息，存入数据库


def get_header(s_no, s_name):
    update_header_sql = "UPDATE " + table + " SET s_header_uri= 1 WHERE s_no='" + s_no + "';"
    header_url = "http://202.118.167.86:9001/xjInfoAction.do?oper=img"
    check_code = requests.get(header_url, headers=info_headers, timeout=60 * 4)
    with open('header.jpg', 'wb') as f:
        f.write(check_code.content)
    # 复制生成的验证码
    copyfile('./header.jpg', 'D:/Documents_vm/neau/' + table + '/' + s_no + s_name + ".jpg")
    update_info(update_header_sql)
    print("抓取", s_name, "头像成功", end='  ')


def get_info():
    info_headers['Referer'] = 'http://202.118.167.86:9001/menu/menu.jsp'
    info_headers['Accept'] = 'text/html, application/xhtml+xml, image/jxr, */*'
    url = 'http://202.118.167.86:9001/xjInfoAction.do?oper=xjxx'
    resp = requests.get(url, headers=info_headers)
    resp.encoding = 'gbk'
    # print resp.text
    selector = etree.HTML(resp.text)
    student = {}  # 定义学生对象
    student.setdefault("s_no", selector.xpath('//*[@id="tblView"]/tr[1]/td[2]/text()')[0].strip())  # 学号
    student.setdefault("s_name", selector.xpath('//*[@id="tblView"]/tr[1]/td[4]/text()')[0].strip())  # 姓名
    student.setdefault("s_sex", selector.xpath('//*[@id="tblView"]/tr[4]/td[2]/text()')[0].strip())  # 性别
    student.setdefault("s_nationality", selector.xpath('//*[@id="tblView"]/tr[6]/td[4]/text()')[0].strip())  # 民族
    student.setdefault("s_id_card", selector.xpath('//*[@id="tblView"]/tr[3]/td[4]/text()')[0].strip())  # 身份证号
    student.setdefault("s_political_status", selector.xpath('//*[@id="tblView"]/tr[8]/td[2]/text()')[0].strip())  # 政治面貌
    student.setdefault("s_high_school", selector.xpath('//*[@id="tblView"]/tr[9]/td[2]/text()')[0].strip())  # 高中毕业学校
    student.setdefault("s_addr", selector.xpath('//*[@id="tblView"]/tr[11]/td[4]/text()')[0].strip())  # 通讯地址
    student.setdefault("s_in_date", selector.xpath('//*[@id="tblView"]/tr[13]/td[2]/text()')[0].strip())  # 入学日期
    student.setdefault("s_college", selector.xpath('//*[@id="tblView"]/tr[13]/td[4]/text()')[0].strip())  # 所在系
    student.setdefault("s_profession", selector.xpath('//*[@id="tblView"]/tr[14]/td[2]/text()')[0].strip())  # 专业
    stu_ProfessionDir = selector.xpath('//*[@id="tblView"]/tr[14]/td[4]/text()')[0].strip()  # 专业方向
    stu_Grade = selector.xpath('//*[@id="tblView"]/tr[15]/td[2]/text()')[0].strip()  # 年级
    student.setdefault("s_class", selector.xpath('//*[@id="tblView"]/tr[15]/td[4]/text()')[0].strip())  # 班级
    student.setdefault("s_dormitory", selector.xpath('//*[@id="tblView"]/tr[18]/td[4]/text()')[0].strip())  # 宿舍
    get_header(student['s_no'], student['s_name'])
    # 避免未知原因，查询完退出登录
    requests.post("http://202.118.167.86:9001/logout.do", headers=info_headers)
    return student


table = "s2017"


if __name__ == '__main__':
    sql = "select s_no from " + table + " where s_weak_pass = 1 order by id desc;"
    # sql = "select s_no from " + table + " where s_weak_pass = 1 AND s_header_uri is null;"
    db_nos = select_info(sql)
    count = db_nos.__len__()
    success = 0
    for i, db_no in enumerate(db_nos):
        print("\n\n抓取第 " + str(i + 1) + " 个， 剩余" + str(count - 1 - i) + "个， 成功 " + str(success))
        # 尝试登录三次
        login_flg = False
        for try_num in range(0, 4):
            print("尝试登录 第", try_num + 1, "次", end='  ')
            if login(str(db_no)[2:11], str(db_no)[2:11]):
                login_flg = True
                break

        if login_flg:
            success += 1
            student = get_info()
            update_info_sql = "UPDATE " + table + " SET s_name='" + student["s_name"] + "', s_sex='" + student[
                "s_sex"] + "', s_nationality='" + \
                         student["s_nationality"] + "', s_id_card='" + student[
                             "s_id_card"] + "', s_political_status='" + \
                         student["s_political_status"] + "', s_high_school='" + student[
                             "s_high_school"] + "', s_addr='" + \
                         student["s_addr"] + "', s_in_date='" + student["s_in_date"] + "', s_college='" + student[
                             "s_college"] + "', s_profession='" + \
                         student["s_profession"] + "', s_class='" + student["s_class"] + "',s_dormitory='" + student[
                             "s_dormitory"] + "', s_weak_pass= 1" \
                                              " WHERE s_no='" + student["s_no"] + "';"

            update_info(update_info_sql)
            time.sleep(0.5)
    if count == 0:
        print("\n数据库中数据为", count, "请调整查询 sql")
    else:
        print("\n抓取完成。尝试抓取", count, "条数据，成功", success, ", 成功率 ", success / count)
