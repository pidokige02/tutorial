import logging
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from .models import SearchDomain
from .serializers import SearchDomainSerializer, CreateSearchDomainSerializer
from .pagination import CustomPagination

logger = logging.getLogger(__name__)
# search domain model Create(post), Read(get)
class SearchDomainListCreateAPIView(generics.ListCreateAPIView):
    queryset = SearchDomain.objects.all().order_by('-id')
    serializer_class = SearchDomainSerializer
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['domain_column']  # 검색 가능한 필드

    filterset_fields = ['created_at']  # 필터링 가능한 필드

    #기본 쿼리셋을 필터링하거나, 사용자 기반 데이터를 반환하도록 수정
    def get_queryset(self):
        # 예: 로그인한 사용자와 관련된 데이터만 반환
        user = self.request.user
        return SearchDomain.objects.filter(owner=user).order_by('-id')

    #새 객체를 생성할 때 추가 로직을 포함시킵니다.
    def perform_create(self, serializer):
        # 예: 생성된 객체에 현재 사용자 추가
        logger.info("Performing create for user: %s", self.request.user)
        serializer.save(owner=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateSearchDomainSerializer  # POST 요청 시 사용하는 시리얼라이저
        return SearchDomainSerializer  # GET 요청 시 사용하는 시리얼라이저

    def get(self, request, *args, **kwargs):
        logger.info("User %s accessed the search domain list.", request.user)
        response = super().get(request, *args, **kwargs)
        # 예: 추가 데이터 포함
        response.data['custom_message'] = "Hello, this is custom data!"
        return response

    def post(self, request, *args, **kwargs):
        logger.info("User %s created a new search domain with data: %s", request.user, request.data)
        return super().post(request, *args, **kwargs)