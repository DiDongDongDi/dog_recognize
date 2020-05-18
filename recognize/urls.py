from django.urls import path
from django.conf.urls.static import static
from dog_recognize.settings import MAIN_MEDIA_ROOT

from . import views

app_name = 'recognize'

urlpatterns = [
    path('main/', views.main, name='main'),
    path('about/', views.about, name='about'),
    path('upload_img/', views.upload_img, name='upload_img'),
    path('get_res/', views.get_res, name='get_res'),
]
urlpatterns += static('/main/', document_root=MAIN_MEDIA_ROOT)
