from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Post, Group

User = get_user_model()


class PostFormTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.author = User.objects.create_user(username='TestUser')
        cls.group = Group.objects.create(
            title='Тестовое название группы',
            slug='test-slug',
            description='Тестовое описание группы',
        )
        cls.post = Post.objects.create(
            text='Тест пост',
            author=cls.author,
            group=cls.group,
        )

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(user=self.author)
        self.guest_client = Client()

    def test_posts_forms_create_post(self):
        """Проверка создает ли форма пост в БД"""
        post_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый пост формы для прохождения теста',
            # 'author': self.author,
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse('posts:profile',
                                                kwargs={'username': self.author}))

        self.assertEqual(Post.objects.count(), post_count+1)
        self.assertTrue(Post.objects.filter(
            text='Тестовый пост формы для прохождения теста',
            group=self.group.id,
        ).exists())

    def test_posts_form_edit_form(self):
        """Проверка редактирования поста"""
        form_data = {
            'text': 'Новый текст поста для прохождения теста',
            'group': self.group.id,
        }
        self.authorized_client.post(
            reverse('posts:post_edit',
                    kwargs={'post_id': self.post.id},),
            data=form_data
        )
        response = self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': self.post.id})
        )
        self.assertEqual(response.context['post'].text, 'Новый текст поста для прохождения теста')
        self.assertTrue(Post.objects.filter(
            text='Новый текст поста для прохождения теста',
            group=self.group.id
        ).exists())
