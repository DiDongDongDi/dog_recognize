# 定时任务

import os
from . import views

def clear_upload_imgs():
    os.removedirs(views.upload_img_dir)
    os.mkdir(views.upload_img_dir)
