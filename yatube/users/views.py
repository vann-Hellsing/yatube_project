# Импортируем CreateView, чтобы создать насленика
from django.core.mail import send_mail
from django.shortcuts import render
from django.views.generic import CreateView

# Импортируем функцию reverse_lazy, которая позволяет получить URL по функции path()
from django.urls import reverse_lazy

# Импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm
# from .models import Contact


class SignUp(CreateView):
    form_class = CreationForm
    # После регистрации перенаправляем на главную
    success_url = reverse_lazy('posts:index')
    template_name = 'users/signup.html'

    # send_mail(
    #     'Тема письма',
    #     'Текст письма',
    #     'from@example.com',
    #     ['to@example.com'],
    #     fail_silently=False,
    # )

# def user_contact(request):
#     # запрашиваем объект модели Contact
#     contact = Contact.objects.get(pk=3)
#
#     # Создаем объект формы и передаем в него объект модели с pk=3
#     form = ContactForm(isinstance=contact)
#
#     # Передаем форму в HTML-шаблон
#     return render(request, 'users/contact.html', {'form': form})
