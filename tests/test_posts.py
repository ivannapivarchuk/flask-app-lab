import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory


class PostsCRUDTestCase(unittest.TestCase):
    def setUp(self):
        # Використовуємо конфігурацію для тестів
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_new_post(self):
        """Тест на створення нового поста (US01)"""
        # Емулюємо відправку форми.
        # ВАЖЛИВО: Передаємо category, бо форма цього вимагає!
        response = self.client.post('/post/create', data={
            'title': 'Test Post Title',
            'content': 'Some content for TDD test',
            'category': 'news'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Перевіряємо базу
        stmt = db.select(Post).where(Post.title == "Test Post Title")
        post = db.session.scalar(stmt)

        self.assertIsNotNone(post)
        self.assertEqual(post.content, 'Some content for TDD test')

    def test_list_posts(self):
        """Тест на перегляд списку постів (US02)"""
        with self.app.app_context():
            p1 = Post(title="Post 1", content="Content 1", category=PostCategory.news)
            p2 = Post(title="Post 2", content="Content 2", category=PostCategory.tech)
            db.session.add_all([p1, p2])
            db.session.commit()

        response = self.client.get('/post/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)

    def test_view_post_detail(self):
        """Тест на перегляд одного поста (US03)"""
        with self.app.app_context():
            p = Post(title="Detail Post", content="Full content here", category=PostCategory.other)
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.get(f'/post/{post_id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Post', response.data)
        self.assertIn(b'Full content here', response.data)

    def test_update_post(self):
        """Тест на редагування поста (US04)"""
        with self.app.app_context():
            p = Post(title="Old Title", content="Old Content", category=PostCategory.news)
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        # Передаємо category і publish_date (З ЛІТЕРОЮ T!)
        response = self.client.post(f'/post/{post_id}/update', data={
            'title': 'New Title',
            'content': 'Updated Content',
            'category': 'tech',
            # БУЛО: '2025-01-01 12:00'
            'publish_date': '2025-01-01T12:00',
            'is_active': 'y'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            updated_post = db.session.get(Post, post_id)
            self.assertEqual(updated_post.title, 'New Title')

    def test_delete_post(self):
        """Тест на видалення поста (US05)"""
        with self.app.app_context():
            p = Post(title="To Delete", content="Bye bye", category=PostCategory.other)
            db.session.add(p)
            db.session.commit()
            post_id = p.id

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            deleted_post = db.session.get(Post, post_id)
            self.assertIsNone(deleted_post)