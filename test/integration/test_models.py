import sys
sys.path.append("website\__init__")
from website.models import Note, Work, User, Team
from test.test_base import BaseTest
from website.__init__ import db


class TestModels(BaseTest):
    def test_crud(self):
        with self.app_context():
            note = Note(data='test', date=17 / 5 / 2021, user_id=1)
            
            db.session.query(Note).filter_by(data="test").first()

    def test_work(self):
        with self.app_context():
            work = Work(title='test', description='working', date=17/5/2021, user_id=2, status='online', points=100)
            
            db.session.query(Work).filter_by(title='test').first()
    
    def test_user(self):
        user = User(email='test@test.com', password='test', first_name='tester', team_id=3, team_leader=True, points=100)
        
        db.session.query(User).filter_by(email='test@test.com').first()
    
    def test_team(self):
        team = Team(name='tester')
        
        db.session.query(Team).filter_by(name='tester').first()