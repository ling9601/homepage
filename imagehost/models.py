from django.db import models
from homepage.settings import THUMB_SIZE
from users.models import User

import PIL.Image,PIL.ImageOps
from io import BytesIO
import os.path
from django.core.files.base import ContentFile

class Tag(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Image(models.Model):
    #根据settings中的MEDIA_ROOT来存放
    picture=models.ImageField(upload_to='pictures')

    title=models.CharField(max_length=100,blank=True)

    uploaded_time=models.DateField(auto_now_add=True)

    tags=models.ManyToManyField(Tag,blank=True)

    # blank,null同时设置为True，否则使用createform时会出现NOT NULL constraint failed error
    category=models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)

    views=models.PositiveIntegerField(default=0)

    favorites=models.PositiveIntegerField(default=0)

    thumbnail=models.ImageField(upload_to='thumbs',editable=False)

    uploader=models.ForeignKey(User,on_delete=models.CASCADE)

    
    def save(self,*args,**kwargs):

        if not self.make_thumbnail():
            # set to a default thumbnail
            raise Exception('Could not create thumbnail - is the file type valid?')

        super(Image, self).save(*args, **kwargs)
    
    def make_thumbnail(self):

        image = PIL.Image.open(self.picture)

        image=PIL.ImageOps.fit(image,THUMB_SIZE,PIL.Image.ANTIALIAS)

        thumb_name, thumb_extension = os.path.splitext(self.picture.name)
        thumb_extension = thumb_extension.lower()

        thumb_filename = thumb_name + '_thumb' + thumb_extension

        if thumb_extension in ['.jpg', '.jpeg']:
            FTYPE = 'JPEG'
        elif thumb_extension == '.gif':
            FTYPE = 'GIF'
        elif thumb_extension == '.png':
            FTYPE = 'PNG'
        else:
            return False    # Unrecognized file type

        # Save thumbnail to in-memory file as StringIO
        temp_thumb = BytesIO()
        image.save(temp_thumb, FTYPE)
        temp_thumb.seek(0)

        # set save=False, otherwise it will run in an infinite loop
        self.thumbnail.save(thumb_filename, ContentFile(temp_thumb.read()), save=False)
        temp_thumb.close()

        return True

    def delete(self, *args,**kwargs):
        self.picture.delete()
        self.thumb.delete()
        super().delete(*args,**kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

