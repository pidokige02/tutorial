from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    page_size = 2  # 페이지당 5개 항목
    page_size_query_param = 'page_size'  # 클라이언트가 페이지 크기를 조정 가능
    max_page_size = 50
