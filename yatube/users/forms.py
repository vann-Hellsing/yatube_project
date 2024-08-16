from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# from .models import Contact

User = get_user_model()


# создадим класс для формы регистрации
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        # Указываем модель, с которой связана форма
        model = User
        # Необходимые поля и их порядок
        fields = ('first_name', 'last_name', 'username', 'email')


# class ContactForm(forms):
#     class Meta:
#         # Но основе какой модели создается форма
#         model = Contact
#         # Указываем какие поля будут в форме
#         fields = ['name', 'email', 'subject', 'body']
#
#         # Метод валидатор для поля subject
#         def clean_subject(self):
#             data = self.cleaned_data['subject']
#
#             # Если пользователь не поблагодарит - считаем это ошибкой
#             if 'спасибо' not in data.lower():
#                 raise forms.ValidationError('Вы обязательно должны нас поблагодарить!')
#
#             # Валидатор обязательно должен вернуть очищенные данные, даже если не изменил их
#             return data
