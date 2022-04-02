# coding: utf-8
from sql_model import Mysql
import pandas as pd
from openpyxl import load_workbook
import time

class sql_method(object):  # 底层数据库
    host = "172.28.5.153"
    user = "root"
    passwd = "root"
    port = 3306
    # db_name = "pms"
    obj = Mysql(host, user, passwd, port)

    def sql_1(self, sql_statements):  # 业务sql语句、功能点、sql逻辑详情
        sql_results = self.obj.select(sql_statements)  # sql结果
        return sql_results

    # def sql_2(self, starttime, endtime):
    #     sql = "SELECT * FROM pms.dbdata WHERE create_time>"+"'"+starttime+"'"+"and create_time<"+"'"+endtime+"'"  # 显示所有数据库
    #     res2 = self.obj.select(sql)
    #     return res2


class sql_method1(object):  # 结果表数据库
    host = "172.28.5.157"
    user = "root"
    passwd = "123456"
    port = 3307
    # db_name = "pms"
    obj = Mysql(host, user, passwd, port)

    def sql_1(self, sql_statements):  # 业务sql语句、功能点、sql逻辑详情
        sql_results = self.obj.select(sql_statements)  # sql结果
        return sql_results

    # def sql_2(self, starttime, endtime):
    #     sql = "SELECT * FROM pms.dbdata WHERE create_time>"+"'"+starttime+"'"+"and create_time<"+"'"+endtime+"'"  # 显示所有数据库
    #     res2 = self.obj.select(sql)
    #     return res2


class other_method(object):
    def transform_array(self, l, length):  # 实现把一维列表转换成二维列表
        r = []
        m = []
        for i in range(len(l)):
            m.append(l[i])
            if len(m) == length:
                r.append(m)
                m = []
        return r

    def function(self, a, b):  # 判断数据是否相等，主要用于判断底层表查询结果与结果表查询结果是否相等
        if a == b:
            return 'PASS'
        else:
            return 'FAIL'

    def sql_successful(self, val):
        '''
        对列不相等失败高亮（红色）处理
        '''
        if val == 'FAIL':  # 表格标红
            color = 'red'
            return 'background-color: %s' % color
        # color = 'red' if val == 'FAIL' else 'black'     #字体标红
        # return f"color:{color}"


if __name__ == '__main__':
    dic1 = {}
    list_dic1 = []
    list1 = []
    i = time.strftime("%Y-%m-%d %H-%M-%S", time.localtime())
    filepath = 'F:\\PycharmProjects\\worktest\\check.xlsx'
    filepath1 = 'F:\\PycharmProjects\\worktest\\check1.xlsx'
    df = pd.read_excel(filepath1, sheet_name="Sheet1")  # header=2从第3行开始读数据
    dfs = pd.read_excel(filepath1, sheet_name="Sheet1", header=2)  # header=2从第3行开始读数据
    # print(df.head(2))
    sql_perform1 = sql_method()
    sql_perform2 = sql_method1()
    sql_perform3 = other_method()
    # sql_res = sql_perform.sql_2('2021-03-03 17:00:00', '2021-05-03 17:00:00')
    # print(sql_res)

    for row in dfs.itertuples():
        # print(row)
        # dic1["sql_function"] = row.功能点
        # dic1["sql_logic"] = row.业务逻辑详情
        # dic1["sql_statements"] = row.底层业务sql
        if row.校验方式 == "校验方式1（两sql对比）":
            sql_res1 = sql_perform1.sql_1(row.底层业务sql)
            sql_res2 = sql_perform2.sql_1(row.结果表业务sql或绝对值)
            sql_results = sql_perform3.function(sql_res1, sql_res2)
            list1.append(row.功能点)
            list1.append(row.业务逻辑详情)
            list1.append(row.底层业务sql)
            list1.append(sql_res1)
            list1.append(row.结果表业务sql或绝对值)
            list1.append(sql_res2)
            list1.append(row.校验方式)
            list1.append(sql_results)
        elif row.校验方式 == "校验方式2（绝对值对比）":
            sql_res1 = sql_perform1.sql_1(row.底层业务sql)
            sql_res2 = row.结果表业务sql或绝对值
            sql_results = sql_perform3.function(sql_res1, sql_res2)
            # dic1["sql_results1"] = sql_res1
            # dic1["sql_results2"] = sql_res2
            # dic1["sql_results"] = sql_results
            # list_dic1.append(dic1)
            list1.append(row.功能点)
            list1.append(row.业务逻辑详情)
            list1.append(row.底层业务sql)
            list1.append(sql_res1)
            list1.append(row.结果表业务sql或绝对值)
            list1.append(sql_res2)
            list1.append(row.校验方式)
            list1.append(sql_results)
    dataAll = sql_perform3.transform_array(list1, 8)

    writer = pd.ExcelWriter(filepath)
    book = load_workbook(filepath1)
    writer.book = book
    dfs1 = pd.DataFrame(dataAll, columns=['功能点', '业务逻辑详情', '底层业务sql', '查询结果1', '结果表业务sql或绝对值', '查询结果2', '校验方式', '对比结果'])
    dfs1 = dfs1.style.applymap(sql_perform3.sql_successful, subset=['对比结果'])  # 调用excel颜色样式，subset为具体哪列需要颜色设置
    dfs2 = df.head(2)
    dfs2.to_excel(writer, index=False, sheet_name=str(i))
    dfs1.to_excel(writer, index=False, sheet_name=str(i), startrow=2)  # startrow实现从第二行开始写数据
    writer.save()  # 保存
