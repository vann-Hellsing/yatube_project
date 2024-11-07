from rest_framework import filters
from rest_framework.throttling import AnonRateThrottle, ScopedRateThrottle
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.permissions import AuthorOrReadOnly, ReadOnly
from api.serializer import PostSerializer, UserSerializer
from posts.models import Post, User
from api.pagination import CustomPagination
from api.throttling import WorkingHoursRateThrottle, LunchBreakThrottle


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all().order_by('-pub_date')
    serializer_class = PostSerializer
    permission_classes = (AuthorOrReadOnly,)
    throttle_classes = (AnonRateThrottle, WorkingHoursRateThrottle, LunchBreakThrottle, ScopedRateThrottle)
    # throttle_scope = 'low_request'
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    # filterset_fields = ('color', 'birth_year',)
    search_fields = ('$text', 'group__id')
    ordering_fields = ('text',)
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action == 'retrieve':
            return (ReadOnly(),)
        return super().get_permissions()


class UserViewSet(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer



# @api_view(['GET', 'POST'])
# def api_posts(request):
#     """Функция для получения и записи постов через API"""
#     if request.method == 'POST':
#         serializers = PostSerializer(data=request.data)
#         if serializers.is_valid():
#             serializers.save(author=request.user)
#             return Response(serializers.data, status=status.HTTP_201_CREATED)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#     posts = Post.objects.all().order_by('-pub_date')
#     serializers = PostSerializer(posts, many=True)
#     return Response(serializers.data, status=status.HTTP_200_OK)
#
#
# @api_view(['GET', 'PATCH', 'PUT', 'DELETE'])
# def api_post_detail(request, pk: int):
#     """Функция получения поста из БД с указанным индексом"""
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'GET':
#         post = get_object_or_404(Post, pk=pk)
#         serializers = PostSerializer(post)
#         return JsonResponse(serializers.data)
#     if request.user != post.author:
#         return Response(status=status.HTTP_403_FORBIDDEN)
#     if request.method == 'PATCH':
#         serializers = PostSerializer(post, data=request.data, partial=True)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#     if request.method == 'PUT':
#         serializers = PostSerializer(post, data=request.data,)
#         if serializers.is_valid():
#             serializers.save()
#             return Response(serializers.data, status=status.HTTP_200_OK)
#         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
#     # if request.method == 'DELETE':
#     if post:
#         post.delete()
#         return Response({"text": "Пост был удален"}, status=status.HTTP_204_NO_CONTENT)
#
# # class APIPost(APIView):
# #     def get(self, request):
# #         posts = Post.objects.all()
# #         serializers = PostSerializer(posts, many=True)
# #         return Response(serializers.data,)
# #
# #     def post(self, request):
# #         serializers = PostSerializer(data=request.data)
# #         if serializers.is_valid():
# #             serializers.save()
# #             return Response(serializers.data, status=status.HTTP_201_CREATED)
# #         return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #
# # class APIPostDetail(APIView):
# #     def get(self, request, pk: int):
# #         post = get_object_or_404(Post, pk=pk)
# #         serializer = PostSerializer(post)
# #         return Response(serializer.data, status=status.HTTP_200_OK)
# #
# #     def put(self, request, pk: int):
# #         post = get_object_or_404(Post, pk=pk)
# #         serializer = PostSerializer(post, data=request.data,)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def patch(self, request, pk: int):
# #         post = get_object_or_404(Post, pk=pk)
# #         serializer = PostSerializer(post, data=request.data, partial=True)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk: int):
# #         post = get_object_or_404(Post, pk=pk)
# #         if post:
# #             post.delete()
# #             return Response({"text": "Пост был удален"}, status=status.HTTP_202_ACCEPTED)
#
#
# # class APIPostList(generics.ListCreateAPIView):
# #     queryset = Post.objects.all().order_by('-pub_date')
# #     serializer_class = PostSerializer
# #
# #
# # class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Post.objects.all()
# #     serializer_class = PostSerializer
#
#
# class APIPostList(generics.ListCreateAPIView):
#     queryset = Post.objects.all().order_by('-pub_date')
#     serializer_class = PostSerializer
#     permission_classes = (AuthorOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user)
#
#
# class APIPostDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = (AuthorOrReadOnly,)