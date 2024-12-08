from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel
from .validators import validate_not_empty

# создание таблицы юзеров из шаблона Django.
User = get_user_model()


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


# Создание экземпляра постов
class Group(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, db_index=True)
    description = models.TextField()

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField(validators=[validate_not_empty],
                            verbose_name='Текст поста',
                            help_text='Введите текст поста')

    pub_date = models.DateTimeField(auto_now_add=True,
                                    verbose_name='Дата публикации',)
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               verbose_name='Автор',
                               related_name='posts')
    group = models.ForeignKey(Group,
                              blank=True,
                              null=True,
                              on_delete=models.SET_NULL,
                              related_name='posts',
                              verbose_name='Группа',
                              help_text='Выберите группу')
    # Поле для картинки (необязательное)
    image = models.ImageField(
        'картинка',
        upload_to='posts/',
        blank=True,
        null=True,
    )
    tag = models.ManyToManyField(Tag, through='TagPost')

    class Meta:
        ordering = ('-pub_data',),
        verbose_name = 'Пост',
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


class TagPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.post}'


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментарий',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва'
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.text


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Укажите подписчика',
        related_name='follower',
        help_text='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Укажите на кого подписываемся',
        related_name='following',
        help_text='Автор поста'
    )

    class Meta:
        ordering = ('-user',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'author'),
                name='unique_follows',
            ),
        )

    def __str__(self) -> str:
        return f'{self.user.username} подписан на {self.author.username}'
