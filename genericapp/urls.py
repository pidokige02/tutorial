from django.urls import path

from genericapp.views import SearchDomainListCreateAPIView


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', SearchDomainListCreateAPIView.as_view(),
         name='search-domain-list-createAPI')
]
