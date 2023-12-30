from rest_framework import generics
from genericapp.models import SearchDomain
from genericapp.serializers import SearchDomainSerializer

# search domain model Create(post), Read(get)
class SearchDomainListCreateAPIView(generics.ListCreateAPIView):
    queryset = SearchDomain.objects.all().order_by('-id')
    serializer_class = SearchDomainSerializer
