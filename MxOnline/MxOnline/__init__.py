# 因为python3.6不支持mysqldb，所以在__init__文件中导入pymysql包
# 否则无法操作数据库
import pymysql
pymysql.install_as_MySQLdb()