"""
URL configuration for Tour_PROJECT project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from web_site.views import welcome_page, tours_page, book_tour_page, success_book_page

#  Пути:
#   страница администратора;
#   страница приветствия;
#   страница со всеми турами;
#   страница выбраного тура с формой броинрования для пользователя;
#   страница после успешного броинрования тура.

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', welcome_page, name='welcome_page'),
    path('tours/', tours_page, name='tours_page'),
    path('tours/book/<int:tour_id>/', book_tour_page, name='book_tour_page'),
    path('success_book/', success_book_page, name='success_book_page'),
]
