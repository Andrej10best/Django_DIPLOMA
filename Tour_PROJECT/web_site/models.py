from PIL import Image as PILImage

from django.db import models
from django.db.models import Model, CharField, IntegerField, ForeignKey, TextField, DateField, DecimalField
from django.forms import ValidationError


def validate_square_and_size(image):
    """
    Проверяет, что изображение квадратное и его размер не превышает 1000x1000 пикселей.
    Параметры:
    ---
    image : File
        Изображение, которое проверяется.

    Исключения:
    ---
    ValidationError
        Выбрасывается, если изображение не квадратное или его размер превышает 1000x1000 пикселей.
    """
    img = PILImage.open(image)
    if img.width != img.height:
        raise ValidationError(('Изображение должно быть квадратным.'))
    if img.width > 1000 or img.height > 1000:
        raise ValidationError(
            ('Разрешение изображения должно быть не больше 1000x1000 пикселей.'))


class Tour(Model):
    """
    Модель для представления тура.
    Атрибуты:
    ----------
    title : CharField
        Заголовок тура (не более 17 символов).

    description : TextField
        Описание тура (не более 1100 символов).

    place : CharField
        Локация тура (не более 27 символов).

    start_date_tour : DateField
        Дата начала тура.

    duration : IntegerField
        Длительность тура (в днях).

    max_people : IntegerField
        Максимальное количество мест.

    available_places : IntegerField
        Свободные места.

    occupied_places : IntegerField
        Занятые места.

    price_per_person : DecimalField
        Цена за одного человека (в формате 0000.00).

    image : ImageField
        Загружаемое квадратное изображение размером не более 1000x1000 пикселей.
    """

    title = CharField(max_length=17, help_text=(
        'Заголовок тура (не более 17 символов)'))

    description = TextField(max_length=1100, help_text=(
        'Описание тура (не более 1100 символов)'))

    place = CharField(max_length=27, help_text=(
        'Локация тура (не более 27 символов)'))

    start_date_tour = DateField(help_text=('Дата начала тура'))
    duration = IntegerField(help_text=('Длительность тура (в днях)'))
    max_people = IntegerField(help_text=('Максимальное количество мест'))
    available_places = IntegerField(help_text=('Свободные места'))
    occupied_places = IntegerField(help_text=('Занятые места'))
    price_per_person = DecimalField(max_digits=10, decimal_places=2, help_text=(
        'Цена за одного человека (в формате 0000.00)'))

    image = models.ImageField(
        upload_to='static/image/img_tour',
        validators=[validate_square_and_size],
        help_text=(
            'Загрузите квадратное изображение размером не более 1000x1000 пикселей.'))

    def __str__(self):
        """
        Возвращает строковое представление объекта тура.
        Возвращает:
        ---
        str
            Заголовок тура.
        """
        return self.title

    class Meta:
        """
        Класс Meta для модели Tour.
        Атрибуты:
        ---
        verbose_name_plural : str
            Человеко-читаемое имя во множественном числе для модели Tour.
        """
        verbose_name_plural = 'Tours'


class User(Model):
    """
    Модель для представления пользователя.
    Атрибуты:
    ---
    name : CharField
        Имя пользователя.

    email : CharField
        Email пользователя.

    phone : CharField
        Номер телефона пользователя.

    number_of_people : IntegerField
        Количество людей в группе.

    tour : ForeignKey
        Связь с моделью Tour (Несколько пользователей могут быть связаны с одним туром).
    """

    name = CharField(max_length=30)
    email = CharField(max_length=200)
    phone = CharField(max_length=30)
    number_of_people = IntegerField(help_text=('Количество людей в группе'))
    tour = ForeignKey(Tour, on_delete=models.CASCADE, related_name='users')

    def __str__(self):
        """
        Возвращает строковое представление объекта пользователя.
        Возвращает:
        ---
        str
            Имя пользователя.
        """
        return self.name

    class Meta:
        """
        Класс Meta для модели User.
        Атрибуты:
        ---
        verbose_name_plural : str
            Человеко-читаемое имя во множественном числе для модели User.
        """
        verbose_name_plural = 'Users'
