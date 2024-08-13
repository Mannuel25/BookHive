from django.contrib.auth import get_user_model
from bookhiveConfig.utils import AuthSetupTestCase

User = get_user_model()


class UserTests(AuthSetupTestCase):
    """
    A test case class for handling user-related API tests.

    This class inherits from AuthSetupTestCase. It includes various test cases for CRUD operations on the BookHive Users API.
    """

    def setUp(self):
        self.authenticate()
        self.data = {
            "email": "tester@gmaail.com",
            "first_name": "tester",
            "last_name": "tester",
            "password": "Tester12$%^&%",
        }
        self.app_user_id = User.objects.create(**self.data).id

    def test_user_list(self):
        response = self.client.get('/api/user_mgt/users')
        self.assertEqual(response.status_code, 200)

    def test_user_post(self):
        response = self.client.post('/api/user_mgt/signup', data={
            "email": "tester22@gmail.com",
            "first_name": "tester1",
            "last_name": "tester11",
            "password": "xQ092#$^11o",
            "user_type": "user",
        }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_user_get(self):
        url = f'/api/user_mgt/users/{self.app_user_id}'
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_patch(self):
        url = f'/api/user_mgt/users/{self.app_user_id}'
        response = self.client.patch(url, data={
            "first_name": "tester12",
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_put(self):
        response = self.client.post('/api/user_mgt/signup', data={
            "email": "update_me@gmail.com",
            "first_name": "Initial",
            "last_name": "User",
            "password": "InitialPassword123",
            "user_type": "user",
        }, format='json')
        user_id = response.json().get('data').get('id')
        response = self.client.put(f'/api/user_mgt/users/{user_id}', data={
            "email": "updated_email@gmail.com",
            "first_name": "Updated",
            "last_name": "Name",
            "user_type": "admin",
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_user_delete(self):
        url = f'/api/user_mgt/users/{self.app_user_id}'
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)

