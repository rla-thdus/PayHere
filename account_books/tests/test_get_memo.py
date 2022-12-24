import json

from rest_framework import status
from rest_framework.test import APITestCase


class MemoGetAPITest(APITestCase):
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
        self.data2 = {
            "spend_price": 1000,
            "content": 'buy snacks'
        }
        self.headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access_token']}"}
        memo = self.client.post('/account_books/memos', self.data, **self.headers)
        self.client.post('/account_books/memos', self.data2, **self.headers)
        self.memo_id = memo.data['id']

    def test_get_memo_should_success_with_authenticated_user_and_exists_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spend_price'], self.data['spend_price'])
        self.assertEqual(response.data['content'], self.data['content'])

    def test_get_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.get(f'/account_books/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_memo_should_fail_with_not_exists_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos/{self.memo_id + 10}', **headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Invalid memo id')

    def test_get_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_memos_should_success_with_authenticated_user(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_all_memos_should_success_with_order_by_spend_price(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos?order_by=spend_price', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['spend_price'] < response.data['results'][1]['spend_price'])

    def test_get_all_memos_should_fail_with_not_authenticated_user(self):
        response = self.client.get(f'/account_books/memos')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_memos_should_return_empty_array_when_does_not_have_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access_token']}"}
        response = self.client.get(f'/account_books/memos', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
