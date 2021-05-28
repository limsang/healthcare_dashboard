"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin #url, include # django 2.부터 url 대신 path사용한다고 함
from django.urls import include, re_path, path


from rest_framework import permissions
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # http://127.0.0.1:8000/apmall/item2vec/sample/test
    # 앞에 apmall을 붙이고 다음에 오는 애들을 붙이면 응답하겠다.
    re_path(r'^apmall/', include(('item2vec.urls', 'item2vector'), namespace='apmall_item2vec_api')),


    # path('test/', include('item2vec.urls'))
    # re_path(r'^apmall/', include(('personalize.urls', 'psnl'), namespace='apmall_personalize_api')),
]

# 의미없음
urlpatterns += staticfiles_urlpatterns()