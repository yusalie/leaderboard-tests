from unittest import TestCase
from main import app

class TestAuth(TestCase):
    def test_log_in(self):
        with app.test_client() as client:
            response = client.get('/log-in')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'/log-in', response.get_data())
    
    def test_log_out(self):
        with app.test_client() as client:
            response = client.get('/log-out')
            self.assertEqual(response.status_code, 302)
            
    def test_sign_up(self):
        with app.test_client() as client:
            response = client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'/sign-up', response.get_data())