# from django.conf.urls import url
from django.urls import path, include
from . import views

urlpatterns = [
    # path('item2vec/<str:cemprdcd>', views.item2item.as_view()),
    path('item2vec/sample/test', views.nginx_test.as_view()),

    path('item2vec/post/test', views.post_test.as_view()),
    # path('item2vec/status/ht', include('health_check.urls')),
]

