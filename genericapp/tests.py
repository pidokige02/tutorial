from rest_framework.test import APITestCase
from rest_framework import status

from .models import SearchDomain

class SearchDomainListCreateViewTest(APITestCase):
    def setUp(self):
        SearchDomain.objects.create(domain_column='Search 1', value='value 1')
        SearchDomain.objects.create(domain_column='Search 2', value='value 2')

    def test_list_SearchDomain(self):
        response = self.client.get('/api2/search/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # Assuming there are 2 items in the database

    def test_create_SearchDomain(self):
        data = {'domain_column': 'New Search', 'value': 'New value'}
        response = self.client.post('/api2/search/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(SearchDomain.objects.count(), 3)  # Assuming there were initially 2 items