from http import HTTPStatus
from django.test import TestCase, Client


class StaticURLTests(TestCase):
    def setUp(self):
        # Создаем неавторизованный клиент
        self.guest_client = Client()

    def test_about_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/author"""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_about_url_uses_correct_template(self):
        """Проверка шаблона для адреса /about/author"""
        response = self.guest_client.get('/about/author/')
        self.assertTemplateUsed(response, 'about/about.html')

    def test_tech_url_exists_at_desired_location(self):
        """Проверка доступности адреса /about/tech"""
        response = self.guest_client.get('http://127.0.0.1:8000/about/tech/')
        self.assertEqual(response.status_code, 200)

    def test_tech_url_uses_correct_template(self):
        """Проверка шаблона для адреса /about/tech"""
        response = self.guest_client.get('http://127.0.0.1:8000/about/tech/')
        self.assertTemplateUsed(response, 'about/tech.html')
