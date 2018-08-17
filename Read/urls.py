"""Read URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import json

from django.conf.urls import url,include
from django.core.paginator import Paginator
from django.shortcuts import render
from art.models import Tag,Articl
import xadmin as admin
from user import helper


def toIndex(request):
    # 加载所有分类
    tags = Tag.objects.all()
    # locals()将当前函数的局部变量转变为字典的k-v

    # 读取分类id
    tag_id = request.GET.get('tag')
    if tag_id:
        tag_id = int(tag_id)
        articls = Articl.objects.filter(tag_id=tag_id)
    else:
        tag_id = 0
        articls = Articl.objects.all()
    #将文章分页
    paginator = Paginator(articls,10)
    page = int(request.GET.get('page',1))
    pager = paginator.page(page)

    # 获取登录用户信息
    login_user = helper.getLoginInfo(request)
    return render(request,'index.html',locals())

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^articl/',include('art.urls')),
    url(r'^$',toIndex),


]
