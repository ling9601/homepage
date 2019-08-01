from django.urls import path
from . import views

app_name = 'imagehost'

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('upload/', views.ImageCreateView.as_view(), name='upload'),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name='detail'),
    path('delete/<int:pk>/', views.delete, name='delete'),
    path('test/',views.test,name='test'),
]
