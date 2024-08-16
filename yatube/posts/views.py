import datetime

from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator

from .forms import PostForm
# from django.contrib.auth.decorators import login_required

from .models import Post, Group, User


# def index(request):
#     # template = 'posts/index.html'
#     author = User.objects.get(username='leo')
#     start_date = datetime.date(1854, 7, 7)
#     end_date = datetime.date(1854, 7, 21)
#     keyword = 'утро'
#     title = 'Последние обновления на сайте'
#     # posts = Post.objects.order_by('-pub_date')[0:3]
#     posts = Post.objects.filter(text__contains=keyword).filter(author=author.id).filter(pub_date__range=(start_date, end_date))
#     context = {
#         'title': title,
#         # 'text': 'Это главная страница проекта Yatube'
#         'posts': posts
#     }
#     return render(request, 'posts/index.html', context)
# def index(request):
#     keyword = request.GET.get('q', None)
#     if keyword:
#         posts = Post.objects.filter(text__contains=keyword).select_related('author').select_related('group')
#     else:
#         posts = None
#     return render(request, 'posts/index.html', {'posts': posts})
def authorized_only(func):
    def check_user(request, *args, **kwargs):
        if request.user.is_authenticated:
            return func(request, *args, **kwargs)
        return redirect('/auth/login')
    return check_user


# @login_required
def index(request):
    # Создаем список постов
    post_list = Post.objects.all().order_by('-pub_date')
    # Создаем пагинатор для отображения 10 страниц
    paginator = Paginator(post_list, 10)
    # Из URL извлекаем номер страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,


    }
    return render(request, 'posts/index.html', context)


@authorized_only
def group_posts(request, slug):
    # template = 'posts/group_list.html'
    # desc = 'Здесь будет информация о группах проекта Yatube'
    # context = {'desc': desc}
    # return render(request, template, context)
    # title = 'Лев Толстой - зеркало русской революции.'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')
    title = group.title
    # Создаем пагинатор для отображения 10 страниц
    paginator = Paginator(posts, 10)
    # Из URL извлекаем номер страницы - это значение параметра page
    page_number = request.GET.get('page')
    # Получаем набор записей для страницы
    page_obj = paginator.get_page(page_number)
    context = {
        'title': title,
        'group': group,
        'page_obj': page_obj
    }
    return render(request, 'posts/group_list.html', context)


@authorized_only
def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author_id=user.id).order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    title = user.get_full_name
    quantity_posts = user.posts.count()

    context = {
        'title': title,
        'page_obj': page_obj,
        'user': user,
        'quantity_posts': quantity_posts
    }
    return render(request, 'posts/profile.html', context)


@authorized_only
def post_detail(request, post_id):

    post = get_object_or_404(Post, pk=post_id)
    title = post.text[:30]
    quantity_posts = post.author.posts.count()
    context = {
        'title': title,
        'post': post,
        'quantity_posts': quantity_posts,
    }
    return render(request, 'posts/post_detail.html', context)


@authorized_only
def post_create(request):

    if request.method == 'POST':
        # Создаем объект формы PostForm
        # И передаем в него полученные данные
        form = PostForm(request.POST or None)

        # Если данные валидны - работаем с "очищенными" данными
        if form.is_valid():
            text = form.cleaned_data['text']
            group = form.cleaned_data['group']

            instance = form.save(commit=False)
            instance.author_id = request.user.id
            instance.save()
            user_name = request.user.username

            # Перенаправляем на другую страницу, чтобы защититься от повторного заполнения
            return redirect('posts:profile', user_name)

        return render(request, 'posts/create_post.html', {'form': form})

    # Если пришел не пост запрос - передаем пустую форму
    form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})


def post_edit(request, post_id):
    """Функция редактирования поста"""

    # Находим необходимый пост
    post = get_object_or_404(Post, pk=post_id)

    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post.pk)

    if request.method == 'POST':

        form = PostForm(request.POST or None, instance=post)

        # Если данные валидны - работаем с "очищенными" данными
        if form.is_valid():
            # text = form.cleaned_data['text']
            # group = form.cleaned_data['group']
            #
            # instance = form.save(commit=False)
            # instance.author_id = request.user.id
            # instance.save()
            form.save()
            user_name = request.user.username

            # Сохраняем данные

            # Перенаправляем на другую страницу, чтобы защититься от повторного заполнения
            return redirect('posts:profile', user_name)

        return render(request, 'posts/create_post.html', {'form': form})

        # Если пришел не пост запрос - передаем пустую форму
    form = PostForm(instance=post)
    context = {'form': form,
               'is_edit': True}
    return render(request, 'posts/create_post.html', context)

