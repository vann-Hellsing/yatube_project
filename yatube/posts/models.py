from django.contrib.auth import get_user_model
from django.db import models

from core.models import CreatedModel
from .validators import validate_not_empty

# создание таблицы юзеров из шаблона Django.
User = get_user_model()


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
    )

    class Meta:
        ordering = ('-pub_data',),
        verbose_name = 'Пост',
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.text


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
    text = models.TextField()
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )

    def __str__(self):
        return self.text
