import sys
sys.path.append("website")
from website.models import Note, Work, User, Team
from test_base import BaseTest
from website.__init__ import db

class TestModels(BaseTest):
    def test_crud(self):
        with self.app_context():
            note = Note(data='test')
            
            db.session.query(Note).filter_by(data="test").first()
            db.session.add(note)
            db.session.commit()
            
            assert note in db.session
            
    def test_work(self):
        with self.app_context():
            work = Work(title='test')
            
            db.session.query(Work).filter_by(title='test').first()
            db.session.add(work)
            db.session.commit()
            
            assert work in db.session    
    def test_user(self):
        user = User(email='test@test.com')
        
        db.session.query(User).filter_by(email='test@test.com').first()
        db.session.add(user)
        db.session.commit()
            
        assert user in db.session    
    def test_team(self):
        team = Team(name='tester')
        
        db.session.query(Team).filter_by(name='tester').first()
        db.session.add(team)
        db.session.commit()
            
        assert team in db.session 