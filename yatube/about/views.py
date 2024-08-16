from django.shortcuts import render
from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Действия для контекста
        context['just_title'] = 'Очень простоя страница'
        context['just_text'] = 'На создание страницы у меня ушло пять минут! Ай да я.'
        return context


class AboutTechView(TemplateView):
    template_name = 'about/tech.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Действия для контекста
        context['just_title'] = 'Очень простоя страница'
        context['just_text'] = 'На создание страницы у меня ушло пять минут! Ай да я.'
        return context
