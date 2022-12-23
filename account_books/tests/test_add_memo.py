import json

from rest_framework import status
from rest_framework.test import APITestCase


class MemoAddAPITest(APITestCase):
    def setUp(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/accounts/registration', user_data)
        self.login = self.client.post('/accounts/login', user_data)
        self.data = {
            "spend_price": 10000,
            "content": 'buy snacks'
        }

    def test_add_memo_should_success_with_valid_data_and_user(self):
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        response = self.client.post('/account_books/memos', self.data, **headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.post('/account_books/memos', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_memo_should_fail_with_invalid_data(self):
        self.data['spend_price'] = ''
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        response = self.client.post('/account_books/memos', self.data, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
