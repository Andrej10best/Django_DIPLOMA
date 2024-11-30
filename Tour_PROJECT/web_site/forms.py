import logging
import re

from django.core.exceptions import ValidationError
from django import forms

from .models import User


logger = logging.getLogger('web_site')


class UserForm(forms.ModelForm):
    """
    Форма для создания и редактирования пользователей.
    Атрибуты:
    ---
    Meta : class
        Внутренний класс, который определяет модель и поля, используемые в форме.
    """
    class Meta:
        model = User
        fields = ['name', 'email', 'phone', 'number_of_people']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Введите ваш email'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Введите ваш телефон'}),
            'number_of_people': forms.NumberInput(attrs={'placeholder': 'Количество людей'}),
        }

    def clean_phone(self):
        """
        Проверяет корректность номера телефона.
        Возвращает:
        ---
        str
            Проверенный номер телефона.

        Исключения:
        ---
        ValidationError
            Выбрасывается, если номер телефона некорректен.
        """
        phone = self.cleaned_data.get('phone')

        if phone and not phone.startswith('+7'):
            logger.warning(f'Некорректный номер телефона: {phone}')
            raise ValidationError('Номер телефона должен начинаться с +7.')

        if phone and not re.match(r'^\+7\d{10}$', phone):
            logger.warning(f'Некорректный формат телефона: {phone}')
            raise ValidationError(
                'Номер телефона должен быть в формате +7XXXXXXXXXX, где X - цифры.')

        return phone

    def clean_number_of_people(self):
        """
        Проверяет корректность количества людей.
        Возвращает:
        ---
        int
            Проверенное количество людей.

        Исключения:
        ---
        ValidationError
            Выбрасывается, если количество людей некорректно.
        """
        number_of_people = self.cleaned_data.get('number_of_people')

        if number_of_people is not None and number_of_people <= 0:
            logger.warning(f'Некорректное количество людей: '
                           f'{number_of_people}')
            raise ValidationError('Количество людей должно быть больше 0.')

        return number_of_people
