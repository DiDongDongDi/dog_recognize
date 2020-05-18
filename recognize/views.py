from django.shortcuts import render
from django.http import HttpResponse
import os
import json

from dog_recognize.settings import MAIN_MEDIA_ROOT
from . import recognize
from dog_recognize.urls import SITE_ROOT_URL

samples_dir = os.path.join(MAIN_MEDIA_ROOT, 'media/samples/')
classes = sorted(os.listdir(samples_dir))
upload_img_dir = os.path.join(MAIN_MEDIA_ROOT, 'media/upload_img/')

upload_img_url = '/' + SITE_ROOT_URL + 'recognize/upload_img/'
get_res_url = '/' + SITE_ROOT_URL + 'recognize/get_res/'

def main(request):
    context = {'upload_img_url': upload_img_url, 'get_res_url': get_res_url}
    return render(request, 'recognize/main.html', context)

def about(request):
    context = {'classes': classes}
    return render(request, 'recognize/about.html', context)

def upload_img(request):
    if request.method == "POST":
        img = request.FILES.get('input-1[]')
        if img is None:
            return HttpResponse(json.dumps({'error': '请先选择图片!'}), content_type="application/json")
        img_token = request.POST.get('img_token')
        img_ext_name = img.name
        img_dst = upload_img_dir + img_token + img_ext_name
        with open(img_dst, 'wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        return HttpResponse(json.dumps({}), content_type="application/json")
    return HttpResponse(json.dumps({'error': 'Unknow error!'}), content_type="application/json")

def get_res(request):
    if request.method == "GET":
        img_token = request.GET.get('img_token')
        img_ext_name = request.GET.get('img_ext_name')
        img_dst = upload_img_dir + img_token + img_ext_name

        pred_classes, pred_percents = recognize.recognize(img_dst)

        pred_classes_name = []
        for i in range(len(pred_classes)):
            pred_classes_name.append(classes[pred_classes[i]])

        pred_res = zip(pred_classes_name, pred_percents)
        your_img = img_token + img_ext_name
        context = {'pred_res': pred_res, 'your_img': your_img}

    return render(request, "recognize/result.html", context)
