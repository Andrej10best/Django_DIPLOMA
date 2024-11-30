import logging

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from .models import Tour
from .forms import UserForm

from Tour_PROJECT.settings import DEFAULT_FROM_EMAIL


logger = logging.getLogger('web_site')


def send_book_email(user_email, tour_title, tour_start_date_tour, tour_duration, number_of_people, price_per_person):
    """
    Отправляет электронное письмо пользователю с информацией о забронированном туре.
    Параметры:
    ---
    user_email : str
        Электронная почта пользователя, который забронировал тур.
    tour_title : str
        Название забронированного тура.
    tour_start_date_tour : str
        Дата начала тура.
    tour_duration : int
        Длительность тура в днях.
    number_of_people : int
        Количество людей, бронирующих тур.
    price_per_person : float
        Стоимость тура за одного человека.
    """

    subject = 'Tours for the soul. Добро пожаловать!'
    message = (
        f'\nБлагодарим Вас за бронирование тура!\n'
        f'Вами был выбран тур: {tour_title}\n'
        f'Дата старта тура: {tour_start_date_tour}\n'
        f'Длительность тура: {tour_duration} дн.\n'
        f'Количество людей: {number_of_people}\n'
        f'Стоимость за человека: {price_per_person} руб.\n'
        f'В течении 24 часов с Вами свяжется наш менеджер для уточнения дополнительных деталей и информировании о предстоящем туре. Пожалуйста ожидайте звонка!'
    )

    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user_email]
    send_mail(subject, message, from_email, recipient_list)


def welcome_page(request):
    """
    Отображает страницу приветствия.
    Параметры:
    ---
    request : HttpRequest
        Объект запроса.

    Возвращает:
    ---
    HttpResponse
        Отрендеренная страница приветствия.
    """
    logger.debug('Страница приветствия загружена')
    return render(request, 'base_page.html')


def tours_page(request):
    """
    Отображает страницу со списком туров.
    Параметры:
    ---
    request : HttpRequest
        Объект запроса.

    Возвращает:
    ---
    HttpResponse
        Отрендеренная страница со списком туров или страница с ошибкой,
        если туры отсутствуют.
    """

    logger.debug('Страница туров загружена')
    tours = Tour.objects.all()
    if not tours:
        logger.warning(
            'Страница с турами пуста (туры не загружены в базу данных)')
        return render(request, 'errors/empty_list_tours_page.html')
    context = {
        'tours': tours,
    }
    logger.info(f'Туры: {len(tours)} шт. загружены на странице')
    return render(request, 'list_tours_page.html', context)


def book_tour_page(request, tour_id):
    """
    Отображает страницу бронирования тура.
    Параметры:
    ---
    request : HttpRequest
        Объект запроса.
    tour_id : int
        Идентификатор тура, который нужно забронировать.

    Возвращает:
    ---
    HttpResponse
        Отрендеренная страница бронирования тура или страница с ошибкой,
        если тур не найден.
    """

    logger.debug(f'Страница тура под id: {tour_id} загружена')

    #  Проверка на получение определенного тура
    try:
        tour = Tour.objects.get(id=tour_id)
    except Tour.DoesNotExist:
        logger.error(f'Страница тура под id: '
                     f'{tour_id} недоступна. Возможно тура с данным id не существует')
        return render(request, 'errors/error_page.html')

    #  Проверка на тип запроса.
    if request.method == "POST":
        form = UserForm(request.POST)
        #  Проверка, является ли форма, отправленная пользователем, корректной
        if form.is_valid():
            user = form.save(commit=False)
            number_of_people = user.number_of_people
            user_email = user.email
            #  Провекрка на корректность вводимого значения для количества людей
            if number_of_people > tour.available_places:
                logger.warning(f'Недостаточно мест для бронирования. Запрошено: '
                               f'{number_of_people}, доступно: {tour.available_places}')
                form.add_error('number_of_people',
                               'Недостаточно свободных мест для бронирования.')
            else:
                tour.available_places -= number_of_people
                tour.occupied_places += number_of_people
                tour.save()

                user.tour = tour
                user.save()
                logger.info(f'Тур успешно забронирован с помощью {user_email}. Тур: '
                            f'{tour.title}, Количество человек: {number_of_people}')
                send_book_email(user_email, tour.title, tour.start_date_tour,
                                tour.duration, number_of_people, tour.price_per_person)
                return redirect('success_book_page')
    else:
        form = UserForm()

    context = {
        'tour': tour,
        'form': form,
    }
    return render(request, 'book_tour_page.html', context)


def success_book_page(request):
    """
    Отображает страницу успешного бронирования.
    Параметры:
    ---
    request : HttpRequest
        Объект запроса.

    Возвращает:
    ---
    HttpResponse
        Отрендеренная страница успешного бронирования.
    """

    logger.debug('Страница отображения успешного бронирования загружена')
    return render(request, 'success_book_page.html')
