import sys
sys.path.append("website/__init__")
from unittest import TestCase
from flask_login import current_user, AnonymousUserMixin
from website.models import User
from main import app
from flask import request
from website.__init__ import db

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
    
    #test sign up response code
    def test_sign_up(self):
        with app.test_client() as client:
            response = client.get('/sign-up')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'/sign-up', response.get_data())
    
    #test sign up with short email
    def test_sign_up_post_short_email(self):
        with app.test_client() as client:
            response = client.post('/sign-up',
                           data=dict(email='meh', firstName='NormalName', password1='pass1234', password2='pass1234'),
                           follow_redirects=True)
            self.assertIn(b'Email must be greater than 3 characters', response.data)
            self.assertEqual(response.status_code, 200)
            user = db.session.query(User).filter_by(email='meh').first()
            self.assertFalse(user)
            self.assertIsNone(current_user.get_id())

    #test if password is incorrect
    def test_sign_up_post_passwords_mismatched(self):
        with app.test_client() as client:
            response = client.post('/sign-up', 
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass6789'),
                                    follow_redirects=True)
            self.assertIn(b'Passwords don&#39;t match', response.data)
            self.assertEqual(response.status_code, 200)
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertFalse(user)
            self.assertIsNone(current_user.get_id())
    
    def test_logged_in(self):
        with app.test_client() as client:
            response = client.post('/sign-up', 
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass1234'),
                                    follow_redirects=True)
            
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            
            response = client.post('/log-in', data=dict(email='email@gmail.com',password='pass1234'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            self.assertIn(b'Logged in successfully', response.data)
            self.assertEqual(response.status_code, 200)            
    
    def test_log_out(self):
         with app.test_client() as client:
            response = client.post('/log-out', 
                                    data=dict(email='email@gmail.com', password1='pass1234'),
                                    follow_redirects=True)
            
            self.assertEqual(response.status_code, 405)
   