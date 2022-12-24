import json

from rest_framework.test import APITestCase


class BaseAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        cls.new_user_data = {
            "email": "test1@test.com",
            "password": "test1234",
        }
        cls.data = {
            "spend_price": 10000,
            "content": 'buy snacks'
        }
        cls.update_data = {
            "spend_price": 18000,
        }
        cls.data2 = {
            "spend_price": 1000,
            "content": 'buy snacks'
        }

    def setUp(self):
        self.client.post('/users/', self.user_data)
        self.client.post('/users/', self.new_user_data)
        self.login = self.client.post('/users/login', self.user_data)
        self.new_login = self.client.post('/users/login', self.new_user_data)
        self.headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access']}"}
        memo = self.client.post('/account-books/memos', self.data, **self.headers)
        self.client.post('/account-books/memos', self.data2, **self.headers)
        self.memo_id = memo.data['id']
        share = self.client.post(f'/account-books/share/memos/{self.memo_id}', **self.headers)
        self.share_link = share.data['link']