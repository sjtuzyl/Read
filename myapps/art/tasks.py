from Read.celery import app
import time
from redis_ import rd

@app.task
def qdTask(uid, aid):
    '''
    异步执行抢读功能
    :param uid: 用户id
    :param aid: 文章id
    :return:
    '''
    if rd.hlen('qdArticl') == 5:
        return '抢读失败'
    # 将用户uid和文章aid存入到hash中
    # qdArticl
    rd.hset('qdArticl',uid,aid)

    return '抢读成功!'
