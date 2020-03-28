from django.urls import path
from .import views

app_name = 'crawler'

urlpatterns = [
    path('status/', views.status),
    path('get_log/<str:id>', views.get_log),
    path('', views.WantedItemIndexVIew.as_view(), name='index'),
    path('create/', views.WantedItemCreateView.as_view(), name='create'),
    path('delete/<int:pk>', views.WantedItemDeleteView.as_view(), name='delete'),
]