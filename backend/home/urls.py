from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add, name='add'),
    path('debug/', views.debug, name='debug'),
    path('run-sh/',views.run_sh,name='run_sh'),
]
