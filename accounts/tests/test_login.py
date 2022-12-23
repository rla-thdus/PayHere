from rest_framework import status
from rest_framework.test import APITestCase


class LoginTest(APITestCase):
    def setUp(self):
        self.data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/accounts/registration', self.data)

    def test_login_should_success_with_registration_user(self):
        response = self.client.post('/accounts/login', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access_token' in response.data)
