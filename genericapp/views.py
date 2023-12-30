from rest_framework import generics
from .models import SearchDomain
from .serializers import SearchDomainSerializer

# search domain model Create(post), Read(get)
class SearchDomainListCreateAPIView(generics.ListCreateAPIView):
    queryset = SearchDomain.objects.all().order_by('-id')
    serializer_class = SearchDomainSerializer
