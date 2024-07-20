from django.urls import path

from . import views


app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Список постов
    path('group_posts/<slug:slug>/', views.group_posts, name='group'),
    # Подробная информация по выбранному посту
#     path(
#         'group_posts/<slug:slug>/',
#         views.group_detail,
#     ),
]
