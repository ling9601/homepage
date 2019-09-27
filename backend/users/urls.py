from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('', views.index, name='index'),

    path('ajax/validate_username/',
         views.validate_username, name='validate_username')
]
