from django.contrib import admin
from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # Перечисление данных, которые должны отображаться в админке
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    list_editable = ('group',)
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('pub_date',)
    # Это свойство сработает для всех пустых колонок: где пусто - там будет эта строка
    empty_value_display = '-пусто-'


# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('pk', 'title', 'description', 'slug')
#     search_fields = ('title',)
#     # Это свойство сработает для всех пустых колонок: где пусто - там будет эта строка
#     empty_value_display = '-пусто-'
#     # Свойство автозаполнения колонок
#     prepopulated_fields = {'slug': ('title',)}


admin.site.register(Post, PostAdmin,)
admin.site.register(Group,)


