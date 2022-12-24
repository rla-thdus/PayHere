import json

from rest_framework import status

from account_books.tests.base import BaseAPITest


class MemoGetAPITest(BaseAPITest):
    def test_get_memo_should_success_with_authenticated_user_and_exists_memo(self):
        response = self.client.get(f'/account-books/memos/{self.memo_id}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spend_price'], self.data['spend_price'])
        self.assertEqual(response.data['content'], self.data['content'])

    def test_get_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.get(f'/account-books/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_memo_should_fail_with_not_exists_memo(self):
        response = self.client.get(f'/account-books/memos/{self.memo_id + 10}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Invalid memo id')

    def test_get_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.get(f'/account-books/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_memos_should_success_with_authenticated_user(self):
        response = self.client.get(f'/account-books/memos', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_get_all_memos_should_success_with_order_by_spend_price(self):
        response = self.client.get(f'/account-books/memos?order_by=spend_price', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['results'][0]['spend_price'] < response.data['results'][1]['spend_price'])

    def test_get_all_memos_should_fail_with_not_authenticated_user(self):
        response = self.client.get(f'/account-books/memos')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_all_memos_should_return_empty_array_when_does_not_have_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.get(f'/account-books/memos', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])

    def test_get_all_memos_should_fail_with_invalid_order_option(self):
        response = self.client.get(f'/account-books/memos?order_by=wrong_option', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Invalid ordering option')
