from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
# from rest_framework.routers import SimpleRouter

from . import views

# router = SimpleRouter()
# router.register('posts', views.PostViewSet)

app_name = 'posts'

urlpatterns = [
    # Главная страница
    path('', views.index, name='index'),
    # Список постов
    path('group_posts/<slug:slug>/', views.group_posts, name='group'),
    # Подробная информация по выбранному посту
    path(
        'profile/<str:username>/',
        views.profile,
        name='profile'
    ),
    path(
        'posts/<int:post_id>/',
        views.post_detail,
        name='post_detail'
    ),
    path(
        'posts/<int:post_id>/edit/',
        views.post_edit,
        name='post_edit'
    ),
    path(
        'create/',
        views.post_create,
        name='post_create'
    ),
    path(
        'posts/<int:post_id>/comment/',
        views.add_comment,
        name='add_comment'
    ),
    path(
        'follow/',
        views.follow_index,
        name='follow_index'
    ),
    path(
        'profile/<str:username>/follow/',
        views.profile_follow,
        name='profile_follow'
    ),
    path(
        'profile/<str:username>/unfollow/',
        views.profile_unfollow,
        name='profile_unfollow'
    ),
    # path(
    #     'api/v1/', include(router.urls)
    # ),
    # path(
    #     'api/v1/api-token-auth/',
    #     obtain_auth_token,
    # ),
    # path(
    #     'api/v1/posts/<int:pk>/',
    #     views.api_post_detail,
    #     name='api_post_detail'
    # ),
    # path(
    #     'api/v1/posts/',
    #     views.api_posts,
    #     name='api_posts'
    # )
    # path(
    #     'api/v1/posts/',
    #     views.APIPostList.as_view()
    # ),
    # path(
    #     'api/v1/posts/<int:pk>/',
    #     views.APIPostDetail.as_view()
    # ),
]
