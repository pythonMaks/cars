from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import CarBrand, CustomUser

 
# Create your tests here.
class UserSystemTestCase(APITestCase):
    def setUp(self):
        self.editor = CustomUser.objects.create_user(username='editor', password='password123', is_editor=True)
        self.non_editor = CustomUser.objects.create_user(username='non_editor', password='password456', is_editor=False)
        self.car_brand_data = {
            'name': 'Toyota',
            'country': 'Japa',
            'info': 'Toyota Motor Corporation is a Japanese multinational automotive manufacturer.'
        }

        
    def test_editor_can_create_car_brand(self):
        self.client.force_authenticate(user=self.editor)
        url = reverse('carbrand-list')
        response = self.client.post(url, self.car_brand_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(dir(status))  
        print(CarBrand.objects.get().name)      
        self.assertEqual(CarBrand.objects.count(), 1)
        self.assertEqual(CarBrand.objects.get().name, 'Toyota')        
        url = '/1/'
        data = {'name': 'Лада Прада'}
        response = self.client.patch(url, data)
        print(CarBrand.objects.get().name)      
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CarBrand.objects.get().name, 'Лада Прада')
        
    def test_editor_cannot_change_car_brand(self):
        self.client.force_authenticate(user=self.non_editor)
        url = reverse('carbrand-list')
        response = self.client.post(url, self.car_brand_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)             
        self.assertEqual(CarBrand.objects.count(), 1)
        self.assertEqual(CarBrand.objects.get().name, 'Toyota')  
              
        url = '/1/'
        data = {'name': 'Лада Прада'}
        response = self.client.patch(url, data)
        print(CarBrand.objects.get().name)      
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(CarBrand.objects.get().name, 'Toyota')
    
   
        