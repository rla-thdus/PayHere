from rest_framework import status
from rest_framework.test import APITestCase


class UserRegisterTest(APITestCase):

    def test_registration_should_success_with_valid_data(self):
        data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_registration_should_fail_when_data_not_enough(self):
        data = {
            "email": "",
            "password": "test1234"
        }
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_should_fail_with_already_exists_email(self):
        data = {
            "email": "test@test.com",
            "password": "test1234",
        }
        self.client.post('/users/', data)
        response = self.client.post('/users/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
