from django.urls import path
from .import views

app_name = 'crawler'

urlpatterns = [
    path('', views.status),
    path('get_log/<str:id>', views.get_log)
]