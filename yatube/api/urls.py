from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'posts', views.PostViewSet)
router.register(r'users', views.UserViewSet)

app_name = 'api'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
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
