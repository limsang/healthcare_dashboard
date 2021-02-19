# from django.conf.urls import url
from django.urls import path, include
from . import views

"""
  # ex: /5/comment/
  path('<int:question_id>/comment/', views.comment, name='comment'),
   # ex: /5/
    # path('<int:question_id>/', views.detail, name='detail'),
      path('tt', views.nginx_test.as_view()),
"""

urlpatterns = [
    # path('item2vec/<str:cemprdcd>', views.item2item.as_view()),
    # test/<int:question_id>/'
    # path('', views.nginx_test.as_view()),

    path('create_index/<str:index_nm>', views.create_index.as_view()),
    path('update_index/<str:index_nm>', views.update_index.as_view()),
    path('delete_index/<str:index_nm>', views.delete_index.as_view()),
    path('', views.react_test.as_view()),

    # path('hello', views.detail.as_view()),
    # question_id라는 이름의 파라미터로 들어가야함
    path('<int:question_id>/<int:second_key>', views.detail.as_view()),
    path('postman_test', views.postman_test.as_view())
]

