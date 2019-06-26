#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql


def connect():
    try:
        conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='nongda', charset='utf8')
        return conn
    except Exception as e:
        print("Mysql 连接失败！！{}",e)
        return None


def select_info(sql):
    with connect() as cur:
        cur.execute(sql)
        db_stu_infos = cur.fetchall()
    return db_stu_infos


def update_info(sql):
    flg = 0
    try:
        with connect() as cur:
            flg = cur.execute(sql)
            cur.close()
    except Exception as e:
        print(e)
        print('更新失败！！')
    if flg >= 1:
        print('更新成功')


if __name__ == '__main__':
    # 测试
    sql = "select s_no from student limit 0, 8"
    res = select_info(sql)
    for r in res:
        print(str(r)[2:11])
