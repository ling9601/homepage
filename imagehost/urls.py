from django.urls import path
from . import views

app_name = 'imagehost'

urlpatterns = [
    path('', views.ImageListView.as_view(), name='index'),
    path('upload/', views.ImageCreateView.as_view(), name='upload'),
    path('image/<int:pk>', views.ImageDetailView.as_view(), name='detail'),
    path('delete/<int:pk>', views.ImageDeleteView.as_view(), name='delete'),
    path('test/',views.test,name='test'),

    # simple query
    path('tag/<int:pk>',views.TagView.as_view(),name='tag'),
    path('category/<int:pk>',views.CategoryView.as_view(),name='category'),
    path('uploader/<int:pk>',views.UploaderView.as_view(),name='uploader'),
]
