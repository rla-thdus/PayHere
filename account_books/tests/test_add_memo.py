from rest_framework import status

from account_books.tests.base import BaseAPITest


class MemoAddAPITest(BaseAPITest):
    def test_add_memo_should_success_with_valid_data_and_user(self):
        response = self.client.post('/account-books/memos', self.data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_memo_should_fail_with_not_authenticated_user(self):
        response = self.client.post('/account-books/memos', self.data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_add_memo_should_fail_with_invalid_data(self):
        self.data['spend_price'] = ''
        response = self.client.post('/account-books/memos', self.data, **self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
