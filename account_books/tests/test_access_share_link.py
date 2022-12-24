from rest_framework import status

from account_books.tests.base import BaseAPITest


class GenerateMemoShareLinkAPITest(BaseAPITest):
    def test_access_share_link_should_success_with_does_not_expire_link(self):
        response = self.client.get(f'/account_books/{self.share_link}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
