import sqlite3


class ConnSqlite3():
    def __init__(self, path):
        self.path = path
        self.cur = None
        self.con = None
        try:
            self.con = sqlite3.connect(path)
            self.cur = self.con.cursor()
        except:
            raise RuntimeError("DataBase connect error,please check the db config.")

    def close(self):
        '''结束查询和关闭连接'''
        self.cur.close()
        self.con.close()

    def query(self, sql_str):
        '''查询数据并返回
             cursor 为连接光标
             sql_str为查询语句
        '''
        try:

            self.cur.execute(sql_str)
            rows = self.cur.fetchall()
            return rows
        except:
            return False

    def execute_update_insert(self, sql):
        '''
        插入或更新记录 成功返回最后的id
        '''
        self.cur.execute(sql)
        self.con.commit()
        return self.cur.lastrowid


if __name__ == '__main__':
    conn = ConnSqlite3("./data/user.db")
    # conn.execute_update_insert("insert into user (userid,viptype,phone) values (1,'KK01','15717929717')")
    # conn.execute_update_insert("update user set viptype='KK02' where userid=1")
    sql = "select * from user where viptype in {} and phone_pro='{}'".format(('KK01', 'KK02'),'江西')
    print(sql)
    res = conn.query(sql)
    print(res)
    conn.close()
