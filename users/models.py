from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    nickname = models.CharField(max_length=50, blank=True)
    # overwrite email of AbstractUser,make it unique in order to use it as authentication
    email = models.EmailField(unique=True)

    class Meta(AbstractUser.Meta):
        pass
    
    def __str__(self):
        return self.username
