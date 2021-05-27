from main import app
from website.views import *
import sys
sys.path.append("test/test_base/")
from test_base import BaseTest

class testViews(BaseTest):
    def test_home_note_flash_correct(self):
        with self.app:
            response = home(data='test note')
            result = db.session.query(Note).filter_by(data='test note').first()
            self.assertIsNone(result)
            
            db.session.add(response)
            db.session.commit()
            
            result = db.session.query(Note).filter_by(data="test").first()
            self.assertIsNotNone(result)
    
    def test_home_without_logged_in(self):
        with app.test_client() as client:
            response =  client.get('/')
            self.assertEqual(response.status_code, 302)
    
    def test_home_while_logged_in(self):
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
            
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
        
    def test_note_connect(self):
        with app.test_client() as client:
            
            response = client.get('/delete-note')
            self.assertEqual(response.status_code, 405)