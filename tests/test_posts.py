import unittest
from app import create_app, db
from app.posts.models import Post, PostCategory
from app.users.models import User


class PostsCRUDTestCase(unittest.TestCase):
    def setUp(self):

        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        self.user = User(username="TestAuthor", email="author@test.com", password="password")
        db.session.add(self.user)
        db.session.commit()
        self.user_id = self.user.id


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_create_new_post(self):
        """Тест на створення нового поста (US01)"""
        response = self.client.post('/post/create', data={
            'title': 'Test Post Title',
            'content': 'Some content for TDD test',
            'category': 'news',
            'user_id': self.user_id,
            'publish_date': '2025-01-01T12:00'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        # Перевіряємо базу
        post = db.session.scalar(db.select(Post).where(Post.title == "Test Post Title"))
        self.assertIsNotNone(post)
        self.assertEqual(post.user_id, self.user_id)  # Перевіряємо, що автор прив'язався

    def test_list_posts(self):
        """Тест на перегляд списку постів (US02)"""
        # Створюємо пости, прив'язані до нашого юзера
        p1 = Post(title="Post 1", content="Content 1", category=PostCategory.news, user_id=self.user_id)
        p2 = Post(title="Post 2", content="Content 2", category=PostCategory.tech, user_id=self.user_id)
        db.session.add_all([p1, p2])
        db.session.commit()

        response = self.client.get('/post/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Post 1', response.data)
        self.assertIn(b'Post 2', response.data)

    def test_view_post_detail(self):
        """Тест на перегляд одного поста (US03)"""
        p = Post(title="Detail Post", content="Full content here", category=PostCategory.other, user_id=self.user_id)
        db.session.add(p)
        db.session.commit()

        response = self.client.get(f'/post/{p.id}')

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Detail Post', response.data)
        self.assertIn(b'Full content here', response.data)

    def test_update_post(self):
        """Тест на редагування поста (US04)"""
        p = Post(title="Old Title", content="Old Content", category=PostCategory.news, user_id=self.user_id)
        db.session.add(p)
        db.session.commit()

        response = self.client.post(f'/post/{p.id}/update', data={
            'title': 'New Title',
            'content': 'Updated Content',
            'category': 'tech',
            'publish_date': '2025-01-01T12:00',
            'user_id': self.user_id,
            'is_active': 'y'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        updated_post = db.session.get(Post, p.id)
        self.assertEqual(updated_post.title, 'New Title')

    def test_delete_post(self):
        """Тест на видалення поста (US05)"""
        p = Post(title="To Delete", content="Bye bye", category=PostCategory.other, user_id=self.user_id)
        db.session.add(p)
        db.session.commit()
        post_id = p.id

        response = self.client.post(f'/post/{post_id}/delete', follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        deleted_post = db.session.get(Post, post_id)
        self.assertIsNone(deleted_post)