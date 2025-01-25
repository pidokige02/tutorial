from django.urls import path
from . import views

urlpatterns = [
    path('', views.posts, name='posts'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('posts_json/', views.posts_json, name='posts_json'),

    # for REST API
    path('api/', views.posts_api, name='posts_api'),
    path('api/<int:id>/', views.post_detail_api, name='post_detail_api'),
    path('api/create/', views.post_create_api, name='post_create_api'),
    path('api/update/<int:id>/', views.post_update_api, name='post_update_api'),
    path('api/delete/<int:id>/', views.post_delete_api, name='post_delete_api'),
]