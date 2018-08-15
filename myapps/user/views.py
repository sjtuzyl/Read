import os
import uuid

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import JsonResponse
from django.shortcuts import render,redirect
import json
from user.forms import UserForm
# Create your views here.

def regist(request):
    if request.method == 'POST':
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            userForm.save()
            return redirect('/')
        errors = json.loads(userForm.errors.as_json())
    return render(request,'user/regist.html',locals())

def uploadPhoto(request):
    # 上传文件-> request.FILES字典中 {'字段名': InMemoryUploadedFile}
    if request.method == 'POST':
        uploadFile:InMemoryUploadedFile = request.FILES.get('photoImg')

        # 生成新的文件名
        newFileName = str(uuid.uuid4()).replace('-','')+'.'+ uploadFile.name.split('.')[-1]

        # 确定生成新的文件的目录
        dirPath = os.path
        return JsonResponse({
                'status': 200,
                'path': '/static/users/photo/1.png'
        })
    return JsonResponse({
            'status': 200,
            'msg': '上传失败,目前请求只支持POST'
    })