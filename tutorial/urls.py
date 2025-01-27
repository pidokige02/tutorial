"""
URL configuration for tutorial project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.contrib.auth import views as auth_views
from blog.views import default_layout, signup, about


urlpatterns = [
    path('admin/', admin.site.urls),

    # # local app w/ template engine
    path('', default_layout, name='home'),  # 기본 URL
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup/', signup, name='signup'),
    path('about/', about, name='about'),  # About 페이지 경로 추가

    # # end point for JWT
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # djoser 엔드포인트 계정생성이나 회원관리용으로 사용함
    path('auth/', include('djoser.urls')),  # 기본 엔드포인트

    # end point for SNS auth, 등 다영한 auth 기능을 지원함
    path('accounts/', include('allauth.urls')),  # allauth URL 추가

    path('blog/', include('blog.urls')),

    path('api/', include('quickstart.urls')),
    path('api2/', include('genericapp.urls')),
]
