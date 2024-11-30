import logging

from django.contrib import admin

from .models import User, Tour


logger = logging.getLogger('web_site')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления пользователями.
    Атрибуты:
    ---
    list_display : tuple
        Определяет, какие поля будут отображаться в списке пользователей в админ-панели.
    """

    list_display = ('name', 'email', 'phone')

    def save_model(self, request, obj, form, change):
        """
        Переопределяет метод сохранения модели пользователя.
        Параметры:
        ---
        request : HttpRequest
            Объект запроса, содержащий информацию о текущем запросе.
        obj : User
            Объект пользователя, который сохраняется.
        form : User(Model)
            Форма, связанная с объектом пользователя.
        change : bool
            Указывает, изменяется ли существующий объект (True) или создается новый (False).

        Логирование:
        ---
        Записывает информацию о добавлении или обновлении пользователя в базе данных.
        """
        if change:
            logger.info(f'Пользователь обновлен: {obj.name}, {obj.email}')
        else:
            logger.info(f'Новый пользователь добавлен: '
                        f'{obj.name}, {obj.email}')
        super().save_model(request, obj, form, change)


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    """
    Админ-класс для управления турами.
    Атрибуты:
    ---
    list_display : tuple
        Определяет, какие поля будут отображаться в списке туров в админ-панели.
    """
    list_display = ('title', 'place', 'price_per_person')

    def save_model(self, request, obj, form, change):
        """
        Переопределяет метод сохранения модели тура.
        Параметры:
        ---
        request : HttpRequest
            Объект запроса, содержащий информацию о текущем запросе.
        obj : Tour
            Объект тура, который сохраняется.
        form : Tour(Model)
            Форма, связанная с объектом тура.
        change : bool
            Указывает, изменяется ли существующий объект (True) или создается новый (False).

        Логирование:
        ---
        Записывает информацию о добавлении или обновлении тура в базе данных.
        """
        if change:
            logger.info(f'Тур обновлен: {obj.title}, {obj.place}')
        else:
            logger.info(f'Новый тур добавлен: {obj.title}, {obj.place}')
        super().save_model(request, obj, form, change)
