import json

from rest_framework import status

from account_books.tests.base import BaseAPITest


class GenerateMemoShareLinkAPITest(BaseAPITest):
    def test_generate_memo_share_link_should_success_with_authenticated_user(self):
        response = self.client.post(f'/account_books/share/memos/{self.memo_id}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('link' in response.data)

    def test_generate_memo_share_link_should_fail_with_unauthorized_user(self):
        response = self.client.post(f'/account_books/share/memos/{self.memo_id}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_generate_memo_share_link_should_fail_with_not_own_memo(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.new_login.content)['access']}"}
        response = self.client.post(f'/account_books/share/memos/{self.memo_id}', **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_generate_memo_share_link_should_fail_with_does_not_exist_memo(self):
        response = self.client.post(f'/account_books/share/memos/{self.memo_id + 100}', **self.headers)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
