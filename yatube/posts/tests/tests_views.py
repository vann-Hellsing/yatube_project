from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from django import forms

from ..models import Group, Post

User = get_user_model()


class PostPagesTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестовую запись в БД
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',)
        cls.author = User.objects.create_user(username='TestUserAuthor')

        cls.post = Post.objects.create(
            text='Тестовая запись!',
            author=cls.author,
            group=cls.group
        )

        cls.templates_page_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group',
                kwargs={'slug': cls.group.slug}
            ),
            'posts/profile.html': reverse(
                'posts:profile',
                kwargs={'username': cls.author.username}
            ),
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/create_post.html': reverse('posts:post_edit',
                                              kwargs={'post_id': cls.post.id}),
            'posts/post_detail.html': reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}
            ),

        }

    def setUp(self):
        # Создадим авторизованный клиент

        self.authorised_client = Client()
        self.authorised_client.force_login(user=self.author)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL использует соответствующий шаблон."""
        # Собираем словарь пары шаблон: reverse(name)

        for template, reverse_name in self.templates_page_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorised_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_create_show_context_correct(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = self.authorised_client.get(reverse('posts:post_create',))
        # Создаем словарь с ожидаемым типом полей формы:
        # указываем, объектами какого класса должны быть поля формы
        form_fields = {
            'text': forms.fields.CharField,
            # При создании формы поля модели типа TextField
            # преобразуются в CharField с виджетом forms.Textarea
            # 'author': forms.fields.ChoiceField,
            'group': forms.fields.ChoiceField
        }
        # Проверяем, что типы полей формы в словаре context соответствуют ожидаемым
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context['form'].fields[value]
                # Проверяем, что поле является экземпляром класса
                self.assertIsInstance(form_field, expected)

    def posts_check_all_fields(self, post):
        """Метод проверяющий поля поста"""
        with self.subTest(post=post):
            self.assertEqual(post.text, self.post.text)
            self.assertEqual(post.author, self.post.author)
            self.assertEqual(post.group.id, self.post.id)

    def test_posts_context_index_template(self):
        """
        Проверка, сформирован ли шаблон group_list с правильным контекстом.

        Появляется ли пост, при создании на главной странице.
        """
        response = self.authorised_client.get(reverse('posts:index'))
        self.posts_check_all_fields(response.context['page_obj'][0])
        last_post = response.context['page_obj'][0]
        self.assertEqual(last_post, self.post)


class PostsPaginatorTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='TestUser')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(user=cls.user)
        for _ in range(13):
            cls.post = Post.objects.create(
                text=f'Тестовая запись поста номер {_}!',
                author=cls.user
            )

    def test_first_page_contains_ten_records(self):
        response = self.authorized_client.get(reverse('posts:index'))
        # Проверка: количество постов на 1 странице равно 10
        self.assertEqual(len(response.context.get('page_obj').object_list), 10)

    def test_second_page_contains_three_records(self):
        response = self.authorized_client.get(
            reverse('posts:index') + '?page=2'
        )
        self.assertEqual(len(response.context.get('page_obj').object_list), 3)
