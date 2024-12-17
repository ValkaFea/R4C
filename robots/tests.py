import datetime
import io
from django.test import TestCase
from django.urls import reverse
import json
from django.utils import timezone
from openpyxl import load_workbook
from .models import Robot


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
        }
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



import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from openpyxl import load_workbook
from .models import Robot


class GenerateExcelTest(TestCase):
    def setUp(self):
        now = timezone.now()

        Robot.objects.create(model='X5', version='LT', created=now - datetime.timedelta(days=2))
        Robot.objects.create(model='X5', version='LT', created=now - datetime.timedelta(days=3))
        Robot.objects.create(model='X7', version='LT', created=now - datetime.timedelta(days=1))
        Robot.objects.create(model='X7', version='Ly', created=now - datetime.timedelta(days=1))
        Robot.objects.create(model='X8', version='gf', created=now - datetime.timedelta(days=4))

    def test_generate_excel(self):
        response = self.client.get(reverse('generate_excel'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response['Content-Type'],
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )

        file_stream = response.content
        workbook = load_workbook(filename=io.BytesIO(file_stream))

        expected_sheets = {'Model_X5', 'Model_X7', 'Model_X8'}
        actual_sheets = set(workbook.sheetnames)
        self.assertSetEqual(expected_sheets, actual_sheets)

        sheet_x5 = workbook['Model_X5']
        self.assertEqual(sheet_x5.cell(row=1, column=1).value, 'Model')
        self.assertEqual(sheet_x5.cell(row=2, column=2).value, 'LT')
        self.assertEqual(sheet_x5.cell(row=2, column=3).value, 2)

        sheet_x7 = workbook['Model_X7']
        self.assertEqual(sheet_x7.cell(row=1, column=1).value, 'Model')
        self.assertEqual(sheet_x7.cell(row=2, column=2).value, 'LT')
        self.assertEqual(sheet_x7.cell(row=3, column=2).value, 'Ly')

        sheet_x8 = workbook['Model_X8']
        self.assertEqual(sheet_x8.cell(row=2, column=2).value, 'gf')
        self.assertEqual(sheet_x8.cell(row=2, column=3).value, 1)
