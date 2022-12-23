import json

from rest_framework import status
from rest_framework.test import APITestCase


class MemoAddAPITest(APITestCase):
    def setUp(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        new_user_data = {
            "email": "test1@test.com",
            "password": "test1234",
        }
        self.client.post('/accounts/registration', user_data)
        self.client.post('/accounts/registration', new_user_data)
        self.login = self.client.post('/accounts/login', user_data)
        self.new_login = self.client.post('/accounts/login', new_user_data)
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

    def test_get_memo_should_fail_with_not_exists_memo(self):
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        response = self.client.get(f'/account_books/memos/{self.memo_id + 1}', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'invalid memo id')

    def test_get_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.new_login.content)['access_token']}
        response = self.client.get(f'/account_books/memos/{self.memo_id}', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

