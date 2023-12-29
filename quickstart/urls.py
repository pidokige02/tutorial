from django.urls import include, path

from rest_framework import routers

from quickstart import views

# DRF Router config
router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'persons',views.PersonViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)), # add for API-ROOT test
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]