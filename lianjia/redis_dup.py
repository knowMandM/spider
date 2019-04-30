import redis 
'''
使用redis查重,去除重复数据
'''

# 连接redis
def connect_redis():
    conn = None
    try:
        conn = redis.StrictRedis.from_url('redis://@localhost:6379/0')
        print('redis connect successfully!')
    except Exception as e:
        print(e)
    return conn
    
conn = connect_redis()

# 判断数据是否重复
def isExist(key, value):
    return conn.sadd(key, value) == 0

# 重置数据
def resetKeys(key):
    return conn.delete(key)

if __name__ == "__main__":
    pass