# Create your views here.
from __future__ import unicode_literals

import os.path

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm

import boto3
import traceback


def index(request):
    return render(request, 'app/index.html', {})


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['uploadFile'])

    return HttpResponseRedirect('/index')


def handle_uploaded_file(f):
    bucket_name = os.environ["BUCKET_NAME"]
    try:
        s3 = boto3.resource('s3')
        bucket = s3.Bucket(bucket_name)
        if bucket not in s3.buckets.all():
            s3.create_bucket(Bucket=bucket_name)

        obj = bucket.Object(f.name)
        obj.upload_fileobj(f)
    except Exception as e:
        err = traceback.format_exc()
        print(str(err))
