import json

from rest_framework import status
from rest_framework.test import APITestCase


class LogoutTest(APITestCase):
    def setUp(self):
        data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/users/', data)
        self.login = self.client.post('/users/login', data)

    def test_logout_should_success_with_authenticated_user(self):
        headers = {'HTTP_AUTHORIZATION': f"Bearer {json.loads(self.login.content)['access']}"}
        response = self.client.delete('/users/logout', None, **headers)
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertEqual(response.data['message'], 'Logout success')

    def test_logout_should_fail_with_not_authenticated_user(self):
        response = self.client.delete('/users/logout')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
