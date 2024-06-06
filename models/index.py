import sys
import pymysql
from pymysql.err import MySQLError

def connect_to_database():
    """連接至 MySQL 數據庫並返回連接對象"""
    try:
        # 建立連接
        connection = pymysql.connect(
            host='127.0.0.1',  # 數據庫服務器地址
            user='root',       # 數據庫登錄使用者名
            password='0000',   # 數據庫登錄密碼
            database='speekproject',   # 要連接的數據庫名
            port=3307,         # 數據庫端口號，MySQL預設為3306，根據實際情況進行修改
            charset='utf8mb4'  # 字符集
        )
        print("成功連接至 MySQL 數據庫")
        return connection
    except MySQLError as e:
        print(f"數據庫連接失敗：{e}")
        #sys.exit()
        return None

# 使用連接進行操作的示例
def get_student(connection):
    if connection is None:
        return {}
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:  # 使用DictCursor
            # 確保此處的查詢是按照您的表結構來的
            sql = "SELECT StudentID, Name FROM test;"
            cursor.execute(sql)
            results = cursor.fetchall()
            return {str(result['StudentID']): result['Name'] for result in results}
    except pymysql.MySQLError as e:
        print(f"查詢失敗：{e}")
        return {}


