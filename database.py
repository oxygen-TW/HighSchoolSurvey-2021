import pymysql
from config import DatabaseConfig as dbc
class Database():
    def __init__(self, tableName):
        self.tableName = tableName

        #Connect to Mysql
        self.conn = pymysql.connect(host=dbc["host"],
                       user=dbc["user"],
                       passwd=dbc["passwd"],
                       db=dbc["db"],
                       port=dbc["port"])

    def insertDict(self, dataDict):
        placeholders = ', '.join(['%s']* len(dataDict))  ##按照dict长度返回如：%s, %s 的占位符
        columns = ', '.join(dataDict.keys())    ##按照dict返回列名，如：age, name
        insert_sql =  "INSERT INTO %s ( %s ) VALUES ( %s )" % (self.tableName, columns, placeholders) #INSERT INTO mytable ( age, name ) VALUES ( %s, %s )

        cursor = self.conn.cursor()
        cursor.execute(insert_sql, tuple(dataDict.values()))  ##执行SQL,绑定dict对应的参数
        self.conn.commit()

    def checkStuId(self, stuId, school):
        #防止SQL injection
        cmd = "SELECT COUNT(`id`) FROM `Main` WHERE `school` = %s AND `stuId` = %s"
        cursor = self.conn.cursor()
        cursor.execute(cmd, (school, stuId))
        res = cursor.fetchall()[0]
        return bool(res[0])

    def closeDB(self):
        self.conn.close()
    
if __name__ == "__main__":
    d = Database("Main")
    print(d.checkStuId("12345", "僑泰中學"))