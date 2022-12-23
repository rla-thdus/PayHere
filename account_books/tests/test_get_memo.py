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
        self.headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        memo = self.client.post('/account_books/memos', self.data, **self.headers)
        self.memo_id = memo.data['id']

    def test_get_memo_should_success_with_authenticated_user_and_exists_memo(self):
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        response = self.client.get(f'/account_books/memos/{self.memo_id}', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spend_price'], self.data['spend_price'])
        self.assertEqual(response.data['content'], self.data['content'])

    def test_get_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.get(f'/account_books/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
