from django.urls import path
from . import views

app_name='imagehost'

urlpatterns=[
    path('',views.ImageList.as_view(),name='ImageList'),
    path('upload/',views.ImageCreate.as_view(),name='upload'),
    path('delete/<int:pk>/',views.delete,name='delete'),
]
