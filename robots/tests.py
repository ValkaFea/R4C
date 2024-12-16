from django.test import TestCase
from django.urls import reverse
import json

class RobotAPITest(TestCase):
    def test_add_robot_success(self):
        url = reverse('add_robot')
        data = {
            'model': 'R2',
            'version': 'D2',
            'created': '2022-12-31 23:59:59'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Robot created successfully', response.json()['message'])

    def test_add_robot_missing_fields(self):
        url = reverse('add_robot')
        data = {
            'model': 'R2',
            'created': '2022-12-31 23:59:59'
        }  # Нет поля version
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Missing required fields', response.json()['error'])

    def test_add_robot_invalid_date(self):
        url = reverse('add_robot')
        data = {
            'model': 'R2',
            'version': 'D2',
            'created': 'invalid-date'
        }
        response = self.client.post(url, json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid date format', response.json()['error'])
