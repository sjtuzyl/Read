from redis import Redis

rd = Redis('127.0.0.1', db=12)  # 创建redis对象


def incrTopRank(id):
    # 自增id的阅读排行
    rd.zincrby('ReadTopRank', id)


def getReadTopRank(top):
    # 获取排名前top的文章
    topRanks = rd.zrevrange('ReadTopRank', 0, top - 1, withscores=True)

    try:
        from art.models import Articl
        # topArticls = Articl.objects.in_bulk([int(id.decode()) for id,_ in topRanks])
        return [(Articl.objects.get(pk=int(id.decode())), int(score)) for id, score in topRanks]
    except:
        pass
