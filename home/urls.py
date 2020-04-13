from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('debug/', views.debug, name='debug'),
    path('get_token/<code>', views.get_token, name='get_token'),
]
