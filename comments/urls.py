from django.urls import path

from . import views

app_name = 'comments'

urlpatterns = [
    path('<int:post_pk>/', views.post_comment, name='post_comment'),
    path('<int:post_pk>/<int:parent_comment_id>',views.post_comment,name='comment_reply')
]
