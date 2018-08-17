from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.cache import cache_page

from art import tasks
from art.models import Articl
# Create your views here.
from user import helper
import redis_
from redis_ import rd

@cache_page(30)
def show(request,id):
    login_user = helper.getLoginInfo(request)
    articl = Articl.objects.filter(pk=id).first()

    # 阅读排行
    redis_.incrTopRank(id)

    readTopRank = redis_.getReadTopRank(5)
    return render(request,'articl/show.html',locals())


def qdArticl(request,id):
    # 获取当前登录的用户信息
    login_user = helper.getLoginInfo(request)
    if not login_user:
        return JsonResponse({
            'msg': '请先登录',
            'code': 101
        })
    tasks.qdTask.delay(login_user.get(id),id) #延迟异步执行

    return JsonResponse({
        'msg':'正在抢读',
        'code': 201
    })

def queryQDState(request,id):
    login_user = helper.getLoginInfo(request)
    if not login_user:
        return JsonResponse({
            'msg': '请先登录',
            'code': 101
        })

    uid = login_user.get('id')
    if rd.hexists('qdArticl',uid):
        # 一个用户抢两本书，查询最新的id的抢读状态
        qdId = rd.hget('qdArticl',uid)
        articl = Articl.objects.get(pk=id)
        return JsonResponse({
            'msg': '抢读成功',
            'code': 200,
            'articl':{
                'title': articl.title,
                'author': articl.author,
            }
        })
    if rd.hlen('qdArticl') <5:
        return JsonResponse({
            'msg': '再试一次',
            'code': 201
        })
    else:
        return JsonResponse({
            'msg': '抢读失败',
            'code': 300
        })