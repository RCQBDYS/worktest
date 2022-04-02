import pymysql


# mysql的方法类
class Mysql(object):
    # mysql 端口号,注意：必须是int类型
    def __init__(self, host, user, passwd, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.port = port
        # self.db_name = db_name

    def select(self, sql):
        """
        执行sql命令
        :param sql: sql语句
        :return: 元祖
        """
        try:
            conn = pymysql.connect(
                host=self.host,
                user=self.user,
                passwd=self.passwd,
                port=self.port,
                # database=self.db_name,
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()  # 创建游标
            # conn.cursor()

            cur.execute(sql)  # 执行sql命令
            res = cur.fetchall()  # 获取执行的返回结果
            cur.close()
            conn.close()
            return res
        except Exception as e:
            print(e)
            return False

    def get_all_db(self):
        """
        获取所有数据库名
        :return: list
        """
        # 排除自带的数据库
        exclude_list = ["sys", "information_schema", "mysql", "performance_schema"]
        sql = "show databases"  # 显示所有数据库
        res = self.select(sql)
        # print(res)
        if not res:  # 判断结果非空
            return False

        db_list = []  # 数据库列表
        for i in res:
            db_name = i['Database']
            # db_list.append(db_name)
            # 判断不在排除列表时
            if db_name not in exclude_list:
                db_list.append(db_name)

        if not db_list:
            return False

        return db_list

    def get_all_table(self):
        """
        获取所有数据库表
        :return: list
        """
        sql = "show tables"  # 显示所有数据库表
        res = self.select(sql)
        # print(res)
        if not res:  # 判断结果非空
            return False
        dbtable_list = []  # 数据库表列表
        for i in res:
            dbtable_name = i['Tables_in_' + self.db_name]
            dbtable_list.append(dbtable_name)

        if not dbtable_list:
            return False

        return dbtable_list

    def get_all_field(self):
        """
        获取所有表字段数据
        :return: list
        """
        sql = "SELECT COLUMN_NAME as 'fieldname',COLUMN_COMMENT as 'Fieldnotes',DATA_TYPE as 'fieldtype',COLUMN_TYPE as 'Fieldtypelength' FROM information_schema.columns where TABLE_NAME =" + "'" + self.db_table + "'" + "and `TABLE_SCHEMA`=" + "'" + self.db_name + "'"
        # print(sql)
        res = self.select(sql)
        if not res:  # 判断结果非空
            return False
        dbtables_list = []  # 表字段列表
        if not res:  # 判断结果非空
            return False
        for i in res:
            dbtables_list.append(i)
        return dbtables_list

    # def add_all_dbdata(self, field, fieldlist):
    #     """
    #     将字段数据写入数据库中
    #     :return: list
    #     """
    #     conn = pymysql.connect(
    #             host=self.host,
    #             user=self.user,
    #             passwd=self.passwd,
    #             port=self.port,
    #             database=self.db_name,
    #             charset='utf8',
    #             cursorclass=pymysql.cursors.DictCursor
    #            )
    #     cur = conn.cursor()  #创建游标
    #     tup2 = []
    #     for k in range(len(field)):
    #         tup2.append('%s')
    #         #print(tup2)
    #     y = ",".join([str(s) for s in field])
    #     j = ','.join([str(s) for s in tup2])
    #     #print(j)
    #     sql = "insert into "+self.db_table + "(" + y + ") " + "values(" + j + ")"
    #     args = fieldlist
    #     try:
    #         cur.executemany(sql, args)
    #         return ('Successful')
    #     except Exception as e:
    #         return ("执行MySQL: % s时出错： % s" % (sql, e))
    #     finally:
    #         cur.close()
    #         conn.commit()
    #         conn.close()


if __name__ == '__main__':
    host = "172.28.5.153"
    user = "root"
    passwd = "root"
    port = 3306
    db_name = "pms"
    obj = Mysql(host, user, passwd, port, db_name)
    sql = "SELECT * FROM pms.users where username ='admin'"  # 显示所有数据库
    res = obj.select(sql)
    print(res)
    for i in res:
        db_name = i['id']
        print(db_name)
        # db_list.append(db_name)
        # 判断不在排除列表时
