import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.urls import reverse
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from ..models import Post, Group

# Создание временной папки для медиа-файлов;
# на момент теста папка будет переопределена
TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)

User = get_user_model()


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.authorized_client = Client()
        self.authorized_client.force_login(user=self.author)
        self.guest_client = Client()

    def test_posts_forms_create_post(self):
        """Проверка создает ли форма пост в БД"""
        post_count = Post.objects.count()
        # Для тестирования загрузки изображений
        # берем байт-последовательность картинки,
        # состоящей из двух пикселей: белого и черного
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        uploaded = SimpleUploadedFile(
            name='small.gif',
            content=small_gif,
            content_type='image/gif'
        )
        form_data = {
            'text': 'Тестовый пост формы для прохождения теста',
            # 'author': self.author,
            'group': self.group.id,
            'image': uploaded,
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
            image='posts/small.gif'
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
