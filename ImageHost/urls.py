from django.urls import path
from . import views

app_name='ImageHost'

urlpatterns=[
    path('',views.ImageList.as_view(),name='ImageList'),
    path('upload/',views.upload.as_view(),name='upload'),
    path('delete/<int:pk>/',views.delete,name='delete'),
]
