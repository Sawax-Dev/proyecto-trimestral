from flaskext.mysql import MySQL
import pymysql

try:
    mysql = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='proyecto_trimestral')
except:
    print("Database connection error: ERR_CONN_REFUSED")