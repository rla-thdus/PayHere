import json

from rest_framework import status

from account_books.tests.base import BaseAPITest


class MemoDuplicateAPITest(BaseAPITest):
    def test_duplicate_memo_should_success_with_valid_data_and_user(self):
        response = self.client.post(f'/account_books/memos/{self.memo_id}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_duplicate_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.post(f'/account_books/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_duplicate_memo_should_fail_with_not_exists_memo(self):
        response = self.client.post(f'/account_books/memos/{self.memo_id + 100}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], 'Invalid memo id')

    def test_duplicate_memo_should_fail_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.post(f'/account_books/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
