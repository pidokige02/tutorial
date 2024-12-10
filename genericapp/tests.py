from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from .models import SearchDomain

class SearchDomainListCreateViewTest(APITestCase):
    def setUp(self):
        # 테스트 사용자 생성 및 로그인
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        # 테스트 데이터 생성
        SearchDomain.objects.create(domain_column='Search 1', value='value 1', owner=self.user)
        SearchDomain.objects.create(domain_column='Search 2', value='value 2', owner=self.user)


    def test_list_SearchDomain(self):
        response = self.client.get('/api2/search/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are 2 items in the database

    def test_create_SearchDomain(self):
        data = {'domain_column': 'New Search', 'value': 'New value'}
        response = self.client.post('/api2/search/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SearchDomain.objects.count(), 3)  # Assuming there were initially 2 items

    def test_perform_create(self):
        # POST 요청
        response = self.client.post('/api2/search/', {
            'domain_column': 'example.com',
            'value': 'Test value'
        })

        # 응답 상태 확인
        self.assertEqual(response.status_code, 201)

        # 생성된 객체 확인
        search_domain = SearchDomain.objects.get(domain_column='example.com')
        self.assertEqual(search_domain.owner, self.user)