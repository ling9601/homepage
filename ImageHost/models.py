from django.db import models
from django.conf import settings

import os

class Image(models.Model):
    #根据settings中的MEDIA_ROOT来存放
    picture=models.ImageField(upload_to='pictures')
    title=models.CharField(max_length=100,blank=True)
    uploaded_time=models.DateField(auto_now_add=True)

    def delete(self, *args,**kwargs):
        self.picture.delete()
        super().delete(*args,**kwargs)

    def get_picture_absolute_url(self):
        print(settings.DOMAIN_NAME+self.picture.url)
        return settings.DOMAIN_NAME+self.picture.url
