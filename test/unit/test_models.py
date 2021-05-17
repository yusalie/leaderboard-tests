import sys
sys.path.append("website\models")
from unittest import TestCase
from website.models import Note, Work, User, Team

class TestModels(TestCase):
  def test_note(self):
    note = Note(data='test', date=17/5/2021, user_id=1)
    
    self.assertEqual(note.data, 'test', "this is a test")
    self.assertEqual(note.date, 17/5/2021, "testing date")
    self.assertEqual(note.user_id, 1, "test user id")
  
  def test_work(self):
    work = Work(title='test', description='working', date=17/5/2021, user_id=2, status='online', points=100)
    
    self.assertEqual(work.title, 'test', "this is a test")
    self.assertEqual(work.description, 'working', "testing date")
    self.assertEqual(work.date, 17/5/2021, "test user id")
    self.assertEqual(work.user_id, 2, 'user id')
    self.assertEqual(work.status, 'online', 'status')
    self.assertEqual(work.points, 100, 'points')
    
  def test_user(self):
    user = User(email='test@test.com', password='test', first_name='tester', team_id=3, team_leader=True, points=100)
    
    self.assertEqual(user.email, 'test@test.com', 'test email')
    self.assertEqual(user.password, 'test', 'test password')
    self.assertEqual(user.first_name, 'tester')
    self.assertIsNotNone(user.notes)
    self.assertEqual(user.team_id, 3, 'test team id')
    self.assertEqual(user.team_leader, True, 'test leader boolean data')
    self.assertIsNotNone(user.work)
    self.assertEqual(user.points, 100, 'test points')
    
  def test_team(self):
    team = Team(name='tester')
    
    self.assertEqual(team.name, 'tester')
    self.assertIsNotNone(team.users)