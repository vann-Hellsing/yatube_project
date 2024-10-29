from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import TestCase, Client
from django.urls import reverse

from ..models import Group, Post

User = get_user_model()


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем тестовую запись в БД для проверки group_posts/<slug:slug>/
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug',
            description='Тестовое описание',)
        cls.author = User.objects.create_user(username='TestUserAuthor')
        cls.no_author = User.objects.create_user(username='TestUserNoAuthor')
        cls.post = Post.objects.create(
            text='Тестовая запись!',
            author=cls.author,
            group=cls.group,
        )
        cls.templates_url_names_public = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': reverse(
                'posts:group',
                kwargs={'slug': cls.group.slug}
            ),
            # 'posts/profile.html': reverse(
            #     'posts:profile',
            #     kwargs={'username': cls.author.username}
            # ),
            'posts/post_detail.html': reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}
            )
        }
        cls.templates_url_names_private = {
            'posts/create_post.html': reverse('posts:post_create'),
            'posts/create_detail.html': reverse('posts:post_edit', kwargs={'post_id': cls.post.id}),
            'posts/profile.html': reverse(
                'posts:profile',
                kwargs={'username': cls.author.username}
            ),
        }
        cls.templates_url_names = {
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
            'posts/post_detail.html': reverse(
                'posts:post_detail',
                kwargs={'post_id': cls.post.id}
            )
        }
        cls.url_unexisting_page = '/unexisting_page/'

    def setUp(self):
        cache.clear()
        # Создадим неавторизованный клиент
        self.guest_client = Client()

        # Создадим авторизованный клиент автора
        self.author_client = Client()
        # Авторизуем пользователя
        self.author_client.force_login(self.author)
        # Создадим авторизованный клиент не автора
        self.no_author_client = Client()
        # Авторизуем пользователя
        self.no_author_client.force_login(self.no_author)

    def test_url_guest_user_private(self):
        """Проверка на доступность ссылок гостевому пользователю и редирект
        недоступных страниц"""
        for templates, reverse_name in self.templates_url_names_private.items():
            with self.subTest():
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.FOUND)
        response = self.guest_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_url_guest_user_public(self):
        """Проверка на доступность ссылок гостевому пользователю и редирект
        доступных страниц"""
        for templates, reverse_name in self.templates_url_names_public.items():
            with self.subTest():
                response = self.guest_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_author_user(self):
        """Проверка доступности ссылок авторизованному пользователю - автору поста."""
        for templates, reverse_name in self.templates_url_names.items():
            with self.subTest():
                response = self.author_client.get(reverse_name)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_url_no_author_user(self):
        """Проверка доступности ссылок авторизованному пользователю - не автору поста."""
        response = self.no_author_client.get(
            reverse(
                'posts:post_edit',
                kwargs={'post_id': self.post.id}
            )
        )
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_page_not_found(self):
        """Страница не найдена"""
        response = self.client.get(self.url_unexisting_page)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_urls_user_correct_templates(self):
        """Проверка, что URL использует правильный шаблон"""
        for template, reverse_name in self.templates_url_names.items():
            with self.subTest():
                response = self.author_client.get(reverse_name)
                self.assertTemplateUsed(response, template)



    # def test_home_url_exists_at_desired_location(self):
    #     """Страница / доступна любому пользователю."""
    #     response = self.guest_client.get('/')
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #
    # def test_group_detail_url_exists_at_desired_location_authorized(self):
    #     """Страница /group_posts/test-slug/ доступна авторизованному пользователю."""
    #     response = self.authorized_user.get('/group_posts/test-slug/')
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #
    # # def test_profile_url_exists_at_desired_location_authorised(self):
    # #     """Страница profile/username/ доступна авторизованному пользователю."""
    # #     response = self.authorized_user.get('profile/username/')
    # #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #
    # def test_create_url_exists_at_desired_authorized(self):
    #     """Страница create/ доступна только авторизованному пользователю."""
    #     response = self.authorized_user.get('/create/')
    #     self.assertEqual(response.status_code, HTTPStatus.OK)
    #
    # def test_group_detail_url_redirect_anonymous(self):
    #     """Страница /group_posts/test-slug/ перенаправит анонимного пользователя на страницу авторизации."""
    #     response = self.client.get('/group_posts/test-slug/', follow=True)
    #     self.assertRedirects(response, '/auth/login/')
    #
    # def test_urls_uses_correct_template(self):
    #     """URL-адрес использует соответствующий шаблон."""
    #     templates_url_names = {
    #         'posts/index.html': '/',
    #         'posts/group_list.html': '/group_posts/test-slug/',
    #         'posts/create_post.html': '/create/',
    #     }
    #     for template, address in templates_url_names.items():
    #         with self.subTest(address=address):
    #             response = self.authorized_user.get(address)
    #             self.assertTemplateUsed(response, template)
