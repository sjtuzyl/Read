import os
import uuid

from django.contrib.auth.hashers import check_password
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render,redirect
import json

from django.views.decorators.csrf import csrf_exempt

from Read import settings
from user import helper
from user.forms import UserForm
# Create your views here.
from user.models import UserProfile


def regist(request):
    if request.method == 'POST':

        userForm = UserForm(request.POST)
        if userForm.is_valid():
            user = userForm.save()
            helper.addLoginSession(request,user)

            return redirect('/')
        errors = json.loads(userForm.errors.as_json())
        print(errors)
    return render(request,'user/regist.html',locals())

@csrf_exempt
def uploadPhoto(request):
    # 上传文件-> request.FILES字典中 {'字段名': InMemoryUploadedFile}
    if request.method == 'POST':
        uploadFile:InMemoryUploadedFile = request.FILES.get('photoImg')

        # 生成新的文件名
        newFileName = str(uuid.uuid4()).replace('-','')+'.'+ uploadFile.name.split('.')[-1]

        # 确定生成新的文件的目录
        dirPath = os.path.join(settings.BASE_DIR,'static/user/photo/')
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        with open(os.path.join(dirPath,newFileName),'wb') as f:
            for chunk in uploadFile.chunks():
                f.write(chunk)

        return JsonResponse({
                'status': 200,
                'path': '/static/users/photo/1.png'
        })
    return JsonResponse({
            'status': 200,
            'msg': '上传失败,目前请求只支持POST'
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        errors = {}
        if not username or len(username.strip()) < 8:
            errors['username'] = [{'message': '用户名不能为空或不能低于八位字符'}]

        if not password or len(password.strip()) <8:
            errors['password'] = [{'message': '密码不能为空或不能低于8位'}]

        if not errors:

            qs = UserProfile.objects.filter(username=username)
            if not qs.exists():
                errors['username'] = [{'message': '此用户不存在!'}]
            else:
                user = qs.first()
                if not check_password(password,user.password):
                    errors['password'] = [{'message': '密码错误'}]
                else:
                    helper.addLoginSession(request,user)
                    return redirect('/')
    return render(request,'user/login.html',locals())

def logout(request):
    login_user = helper.getLoginInfo(request)
    if login_user:
        del request.session['login_user']
        return redirect('/')

def userInfo(request):
    login_user = helper.getLoginInfo(request)
    if request.method == 'POST':
        pass
    return render(request,'user/userInfo.html',locals())