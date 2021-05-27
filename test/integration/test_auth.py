from test_base import BaseTest
import sys
sys.path.append("website\__init__")
from website.__init__ import db
from website.models import User
from flask_login import current_user
from flask import request


class TestSignUp(BaseTest):
    def test_sign_up_post_success(self):
        with self.app:
             response = self.app.post('/sign-up', data=dict(email='tests@gmail.com', firstName='qwerty', password1= '1234567', password2= '1234567'), follow_redirects=True)
             user = db.session.query(User).filter_by(email='tests@gmail.com').first()
             self.assertTrue(user)
             self.assertIn(b'Account created', response.data)
             self.assertEqual(current_user.get_id(), '1')
             self.assertIn(b'Notes', response.data)
             
             
    def test_sign_up_post_user_exists(self):
        with self.app:
            # create user in db - can use post req
            response = self.app.post('/sign-up', data=dict(email='bob@gmail.com', firstName='steve', password1= '01234567', password2= '01234567'), follow_redirects=True)
            # assert that user exists in db
            user = db.session.query(User).filter_by(email='bob@gmail.com').first()
            self.assertTrue(user)
            # create post req with same email (repeat)
            response = self.app.post('/sign-up', data=dict(email='bob@gmail.com', firstName='qwerty', password1= '1234567', password2= '1234567'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='bob@gmail.com').first()
            self.assertTrue(user)
            
            # assert that email already in use flash message appears
            self.assertIn(b'Email already in use', response.data)
            
            
            # self.assertNotEqual(current_user.get_id(), '1')
            # self.assertIn(b'Notes', response.data)
class TestLogin(BaseTest):
    def test_login_post_success(self):
        with self.app:
            response = self.app.post('/sign-up', data=dict(email='jeff@gmail.com', firstName='steve', password1= '01234567', password2= '01234567'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='jeff@gmail.com').first()
            self.assertTrue(user)
            
            response = self.app.post('/log-in', data=dict(email='jeff@gmail.com', password='01234567'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='jeff@gmail.com').first()
            self.assertTrue(user)
            self.assertIn(b'Logged in successfully', response.data)
            
            
            # self.assertIn(b'Notes', response.data)
    
    def test_login_invalid_user(self):
        with self.app:
            response = self.app.post('/log-in', data=dict(email='jefff@gmail.com', password='01234567'), follow_redirects=True)
            # user = db.session.query(User).filter_by(email='jefff@gmail.com').first()
            # self.assertTrue(user)
            self.assertIn(b'Email does not exist', response.data)
            
    def test_login_wrong_password(self):
        with self.app:
            response = self.app.post('/sign-up', data=dict(email='jeffs@gmail.com', firstName='steves', password1= '1234567', password2= '1234567'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='jeffs@gmail.com').first()
            self.assertTrue(user)
            
            
            response = self.app.post('/log-in', data=dict(email='jeffs@gmail.com', password='0123456'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='jeffs@gmail.com').first()
            self.assertTrue(user)
            self.assertIn(b'Incorrect password, try again.', response.data)
    
    
class TestLogout(BaseTest):
    
    def test_logout_route_while_logged_in(self):
        with self.app:
            # sign up
            response = self.app.post('/sign-up', data=dict(email='solo@gmail.com', firstName='han', password1= 'qwerty123', password2= 'qwerty123'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='solo@gmail.com').first()
            self.assertTrue(user)
            # log in
            response = self.app.post('/log-in', data=dict(email='solo@gmail.com', password='qwerty123'), follow_redirects=True)
            user = db.session.query(User).filter_by(email='solo@gmail.com').first()
            self.assertTrue(user)
            
            response = self.app.get('/log-out', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
    
    

            self.assertIn('/log-in', request.url)
            # after log out test current user is none
            self.assertFalse(current_user.is_active)