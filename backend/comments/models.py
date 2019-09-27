from django.db import models
from users.models import User

class Comment(models.Model):

    body = models.TextField()

    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    author = models.ForeignKey(User,on_delete = models.CASCADE)

    def __str__(self):
        return self.body[:20]
