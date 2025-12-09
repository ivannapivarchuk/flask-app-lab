import unittest
from app import create_app, db
from app.users.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_auth_pages_load(self):
        """1. Перевірка, що сторінки входу та реєстрації відкриваються (200 OK)"""
        response = self.client.get('/users/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'register', response.data.lower())  # Перевіряємо, що це саме реєстрація

        response = self.client.get('/users/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'login', response.data.lower())

    def test_register_user(self):
        """2. Тестування збереження користувача у БД при реєстрації"""
        response = self.client.post('/users/register', data={
            'username': 'TestUser',
            'email': 'test@test.com',
            'password': 'password123',
            'confirm_password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        user = db.session.scalar(db.select(User).where(User.username == 'TestUser'))
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@test.com')
        self.assertNotEqual(user.password, 'password123')

    def test_login_and_logout(self):
        """3. Тестування входу і виходу користувача"""
        user = User(username='LoginUser', email='login@test.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()


        response = self.client.post('/users/login', data={
            'email': 'login@test.com',
            'password': 'password123'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/users/logout', response.data)
        response = self.client.get('/users/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'/users/login', response.data)