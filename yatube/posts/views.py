from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Post, Group


def index(request):
    # template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    posts = Post.objects.order_by('-pub_date')[0:3]
    context = {
        'title': title,
        # 'text': 'Это главная страница проекта Yatube'
        'posts': posts
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    # template = 'posts/group_list.html'
    # desc = 'Здесь будет информация о группах проекта Yatube'
    # context = {'desc': desc}
    # return render(request, template, context)
    title = 'Лев Толстой - зеркало русской революции.'
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'title': title,
        'group': group,
        'posts': posts
    }
    return render(request, 'posts/group_list.html', context)


def group_detail(request, slug):
    return HttpResponse(f'Пост номер {slug}')
