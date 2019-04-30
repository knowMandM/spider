from sqlalchemy import Column,Integer,String #区分大小写
from mysql_mgr import mysqlMgr, base


# 表 brief_movie_info
class lianjia_info(base):
    __tablename__ = 'lianjia_info' #表名
    id = Column(Integer, primary_key=True)
    name        = Column(String(128))
    city        = Column(String(64))
    loupan_type = Column(String(32))
    sale_status = Column(String(32))
    address     = Column(String(512))
    price       = Column(Integer())
    units       = Column(String(32))
    crawl_time  = Column(String(64))

mysqlMgr.create_all_table() # 建表，定义都写在上面

