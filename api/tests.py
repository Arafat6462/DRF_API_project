from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Project

class AuthTests(APITestCase):
    def test_register(self):
        """
        Ensure we can create a new user.
        """
        url = reverse('auth_register')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_login(self):
        """
        Ensure we can log in and get a token.
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

class ProjectTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.project = Project.objects.create(owner=self.user, name='Test Project', description='A test project')
        
        # Authenticate user
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)


    def test_get_projects(self):
        """
        Ensure we can get a list of projects.
        """
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Project')

    def test_create_project(self):
        """
        Ensure we can create a new project.
        """
        url = reverse('project-list')
        data = {'name': 'New Project', 'description': 'A new test project'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.get(id=response.data['id']).name, 'New Project')

    def test_unauthenticated_user_cannot_create_project(self):
        """
        Ensure an unauthenticated user cannot create a project.
        """
        self.client.credentials() # Unset credentials
        url = reverse('project-list')
        data = {'name': 'New Project', 'description': 'A new test project'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_can_only_see_their_own_projects(self):
        """
        Ensure a user can only see their own projects.
        """
        other_user = User.objects.create_user(username='otheruser', password='otherpassword')
        Project.objects.create(owner=other_user, name='Other Project', description='Another test project')
        url = reverse('project-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Project')