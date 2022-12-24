import json

from rest_framework import status
from rest_framework.test import APITestCase


class MemoDeleteAPITest(APITestCase):
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
        self.headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access']}"}
        memo = self.client.post('/account_books/memos', self.data, **self.headers)
        self.memo_id = memo.data['id']

    def test_delete_memo_should_success_with_valid_data_and_user(self):
        response = self.client.delete(f'/account_books/memos/{self.memo_id}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

    def test_delete_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.delete(f'/account_books/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_memo_should_fail_with_not_exists_memo(self):
        response = self.client.delete(f'/account_books/memos/{self.memo_id + 1}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Invalid memo id')

    def test_delete_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.delete(f'/account_books/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
