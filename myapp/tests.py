from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from .models import MenuItem
from .serializers import MenuItemSerializer, UserSerializer


class MenuItemViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.menu_item = MenuItem.objects.create(
            first_name='Test Item',
            reservation_data='2023-06-09',
            reservation_slot='Slot 1'
        )
        self.menu_item_serializer = MenuItemSerializer(instance=self.menu_item)

    def test_get_menu_items(self):
        url = reverse('menu-items')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [self.menu_item_serializer.data])

    def test_create_menu_item(self):
        url = reverse('menu-items')
        data = {
            'first_name': 'New Item',
            'reservation_data': '2023-06-10',
            'reservation_slot': 'Slot 2'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], 'New Item')
        self.assertEqual(response.data['reservation_data'], '2023-06-10')
        self.assertEqual(response.data['reservation_slot'], 'Slot 2')

    def test_get_single_menu_item(self):
        url = reverse('single-item', args=[self.menu_item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.menu_item_serializer.data)


class UserSignupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_signup(self):
        url = reverse('user-signup')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('user' in response.data)
        self.assertTrue('token' in response.data)

    def test_user_signup_with_existing_username(self):
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='password123'
        )
        url = reverse('user-signup')
        data = {
            'username': 'existinguser',
            'email': 'new@example.com',
            'password': 'password123',
            'password2': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'Username is already taken.')

    # Add more test cases for UserSignupView if needed


class UserLoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password123'
        )

    def test_user_login(self):
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'password123'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('user' in response.data)
        self.assertTrue('token' in response.data)

    def test_user_login_with_invalid_credentials(self):
        url = reverse('user-login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['error'], 'Invalid credentials.')

    # Add more test cases for UserLoginView if needed


class UserListViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123'
        )
        self.user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123'
        )

    def test_get_all_users(self):
        url = reverse('user-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['username'], 'user1')
        self.assertEqual(response.data[1]['username'], 'user2')

    # Add more test cases for UserListView if needed


class MenuItemModelTest(TestCase):
    def test_string_representation(self):
        menu_item = MenuItem(
            first_name='Test Item',
            reservation_data='2023-06-09',
            reservation_slot='Slot 1'
        )
        self.assertEqual(str(menu_item), 'Test Item')

    # Add more test cases for MenuItem model if needed


class MenuItemSerializerTest(TestCase):
    def test_serializer_data(self):
        menu_item = MenuItem.objects.create(
            first_name='Test Item',
            reservation_data='2023-06-09',
            reservation_slot='Slot 1'
        )
        serializer = MenuItemSerializer(instance=menu_item)
        expected_data = {
            'id': menu_item.id,
            'first_name': 'Test Item',
            'reservation_data': '2023-06-09',
            'reservation_slot': 'Slot 1'
        }
        self.assertEqual(serializer.data, expected_data)

    # Add more test cases for MenuItemSerializer if needed


class UserSerializerTest(TestCase):
    def test_password_validation(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'password2': 'wrongpassword'
        }
        serializer = UserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(
            serializer.errors['non_field_errors'][0],
            "Passwords do not match."
        )

    # Add more test cases for UserSerializer if needed
