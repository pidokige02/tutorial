from django.urls import path

from .views import SearchDomainListCreateAPIView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('search/', SearchDomainListCreateAPIView.as_view(),
         name='search-domain-list-createAPI')
]
