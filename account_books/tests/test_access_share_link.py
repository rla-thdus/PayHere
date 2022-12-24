import json

from rest_framework import status
from rest_framework.test import APITestCase


class GenerateMemoShareLinkAPITest(APITestCase):
    def setUp(self):
        user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/accounts/registration', user_data)
        login = self.client.post('/accounts/login', user_data)
        data = {
            "spend_price": 10000,
            "content": 'buy snacks'
        }
        self.headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(login.content)['access']}"}
        memo = self.client.post('/account_books/memos', data, **self.headers)
        memo_id = memo.data['id']
        share = self.client.post(f'/account_books/share/memos/{memo_id}', **self.headers)
        self.share_link = share.data['link']


    def test_access_share_link_should_success_with_does_not_expire_link(self):
        response = self.client.get(f'/account_books/{self.share_link}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
