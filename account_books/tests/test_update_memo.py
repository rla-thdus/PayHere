import json

from rest_framework import status

from account_books.tests.base import BaseAPITest


class MemoUpdateAPITest(BaseAPITest):
    def test_update_memo_should_success_with_valid_data_and_user(self):
        response = self.client.patch(f'/account_books/memos/{self.memo_id}', self.update_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['spend_price'], self.update_data['spend_price'])

    def test_update_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.patch(f'/account_books/memos/{self.memo_id}', self.update_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_memo_should_fail_with_not_exists_memo(self):
        response = self.client.patch(f'/account_books/memos/{self.memo_id + 100}', self.update_data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Invalid memo id')

    def test_update_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.patch(f'/account_books/memos/{self.memo_id}', self.update_data, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
