from django.conf.urls import url
from django.urls import path,include
from . import views

# for url reverse
app_name = 'blog'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>', views.ArchivesView.as_view(), name='archives'),
    path('category/<int:pk>', views.CategoryView.as_view(), name='category'),
    path('author/<int:pk>', views.AuthorView.as_view(), name='author'),
    path('tag/<int:pk>',views.TagView.as_view(),name='tag'),
    path('search/',include('haystack.urls')),
]
