import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base

#--mysql 连接配置
mysql_user = "root"
mysql_passwd = "123456"
mysql_dbname = "mydb"

# 公共部分
engine = sqlalchemy.create_engine("mysql+pymysql://{}:{}@localhost/{}".format(mysql_user, mysql_passwd, mysql_dbname),encoding='utf-8',echo=True)
base=declarative_base()

#-- mysql 管理类
class MysqlMgr():
    session = None

    def __init__(self):
        Session_class=sessionmaker(bind=engine)
        self.session=Session_class()

    def insertValue(self, ormItem):
        try:
            self.session.add(ormItem)
            self.session.commit()
        except:
            Session_class=sessionmaker(bind=engine)
            self.session=Session_class()

    def insertValues(self, ormItemList):
        try:
            [self.session.add(item) for item in ormItemList]
            self.session.commit()
        except:
            Session_class=sessionmaker(bind=engine)
            self.session=Session_class()

    def create_all_table(self):
        base.metadata.create_all(engine)

    def selectAll(self, ormClass):
        return self.session.query(ormClass).all()

    def __del__(self):
        self.session.close()

mysqlMgr = MysqlMgr()