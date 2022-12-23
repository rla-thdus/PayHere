import json

from rest_framework import status
from rest_framework.test import APITestCase


class LogoutTest(APITestCase):
    def setUp(self):
        data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/accounts/registration', data)
        self.login = self.client.post('/accounts/login', data)

    def test_logout_should_success_with_authenticated_user(self):
        headers = {'HTTP_AUTHORIZATION': "Bearer " + json.loads(self.login.content)['access_token']}
        response = self.client.delete('/accounts/logout', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['message'], 'Logout success')

    def test_logout_should_fail_with_not_authenticated_user(self):
        response = self.client.delete('/accounts/logout')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
