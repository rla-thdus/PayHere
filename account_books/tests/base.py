import json

from rest_framework.test import APITestCase


class BaseAPITest(APITestCase):
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
        self.update_data = {
            "spend_price": 18000,
        }
        self.data2 = {
            "spend_price": 1000,
            "content": 'buy snacks'
        }
        self.headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access']}"}
        memo = self.client.post('/account_books/memos', self.data, **self.headers)
        self.client.post('/account_books/memos', self.data2, **self.headers)
        self.memo_id = memo.data['id']
        share = self.client.post(f'/account_books/share/memos/{self.memo_id}', **self.headers)
        self.share_link = share.data['link']