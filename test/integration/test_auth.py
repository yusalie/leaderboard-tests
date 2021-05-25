from flask.wrappers import Response
from werkzeug.wrappers import response
import sys
sys.path.append("/test/test_base")
from test.test_base import BaseTest, db
from website.models import User
from flask_login import current_user

class TestSignUp(BaseTest):

    # test signing up user successfully 
    def test_sign_up_post_success(self):
        with self.app:
            # create a post req with valid data
            response = self.app.post('/sign-up',
                                    data=dict(email='email@gmail.com', firstName='Namey', password1='pass1234', password2='pass1234'),
                                    follow_redirects=True)
            # assert that new user is created in db
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            # assert that flash message is shown
            self.assertIn(b'Account created', response.data)
            # assert that user is logged in 
            self.assertEqual(current_user.get_id(), '1')
            # assert that page is redirected
            self.assertIn(b'Notes', response.data)
    
    def test_sign_up_post_error(self):
        with self.app:
            response = self.app.post('/sign-up', data=dict(email='em', firstName='Name', password1='pass12345', password2='passs12345'))
            user = db.session.query(User).filter_by(email='em').first()
            self.assertFalse(user)
            self.assertIn(b'Email must be greater than 3 characters', response.data)
    
    def test_log_in_existing_user(self):
        with self.app:
            response = self.app.post('/log-in', data=dict(email='email@gmail.com', password1='pass1234'))
            
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            self.assert(b'Logged in successfully', response.data)
    
    def test_log_in_valid_user_invalid_password(self):
        with self.app:
            response = self.app.post('/log-in', data=dict(email='email@gmail.com', password1='pass'))
            
            user = db.session.query(User).filter_by(email='email@gmail.com').first()
            self.assertTrue(user)
            self.assert(b'incorrect password try again', response.data)
                                
                                    
            
            