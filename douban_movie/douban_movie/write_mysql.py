import  sqlalchemy
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String #区分大小写

mysql_user = "root"
mysql_passwd = "123456"
mysql_dbname = "mydb"
#创建连接
engine=create_engine("mysql+pymysql://{}:{}@localhost/{}".format(mysql_user, mysql_passwd, mysql_dbname),encoding='utf-8',echo=True)
#生成orm基类
base=declarative_base()
class douban_movie(base):
    __tablename__ = 'douban_movie' #表名
    id = Column(Integer, primary_key=True)
    name = Column(String(128))
    descripe = Column(String(2048))
    image = Column(String(512))
    director = Column(String(128))
    actors = Column(String(1024))

headers = []

def collect_fields(classname):
    for attr in classname.__dict__.keys():
        if type(getattr(classname, attr)) == sqlalchemy.orm.attributes.InstrumentedAttribute:
            headers.append(attr)
    print(headers)

collect_fields(douban_movie)

def createTable():
    base.metadata.create_all(engine)

# 对外接口 批量
def insertValues(jonlist):
    Session_class=sessionmaker(bind=engine)
    session=Session_class()

    for jobinfo in jonlist:
        douban_movie_obj = douban_movie()
        for field in headers:
            if field in jobinfo:
                setattr(douban_movie_obj, field, jobinfo[field])
        session.add(douban_movie_obj)

    session.commit()
    session.close()

# 对外接口 单个
def insertValue(item):
    Session_class=sessionmaker(bind=engine)
    session=Session_class()

    douban_movie_obj = douban_movie()
    for field in headers:
        if field in item:
            setattr(douban_movie_obj, field, item[field])
    session.add(douban_movie_obj)

    session.commit()
    session.close()

createTable()