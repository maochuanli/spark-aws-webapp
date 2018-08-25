# Create your views here.
from __future__ import unicode_literals

import os.path

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import boto3
import traceback


def index(request):
    file_obj_list = []
    bucket_name = os.environ["BUCKET_NAME"]
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        for s3_file in bucket.objects.all():
            file_obj_list.append(s3_file)
    except Exception:
        err = traceback.format_exc()
        print(str(err))
    return render(request, 'app/index.html', {'bucket_name': bucket_name, 'file_obj_list': file_obj_list})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['uploadFile'])

    return HttpResponseRedirect('/index')


def handle_uploaded_file(f):
    if not f:
        return
    if f.size > 5 * 1024 * 1024:
        print('File size capped by 5 MB, file size: {} too big!'.format(f.size))
        return
    bucket_name = os.environ["BUCKET_NAME"]
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)

        if bucket not in s3.buckets.all():
            s3.create_bucket(Bucket=bucket_name)

        obj_list = bucket.objects.all()
        if len(obj_list) > 20:
            print("Limit 20 objects in the bucket is hit! ")
            return

        obj = bucket.Object(f.name)
        obj.upload_fileobj(f)
    except Exception:
        err = traceback.format_exc()
        print(str(err))
