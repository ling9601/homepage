from django.db import models
from users.models import User

from ckeditor.fields import RichTextField
from mptt.models import MPTTModel,TreeForeignKey

class Comment(MPTTModel):

    body = RichTextField()

    created_time = models.DateTimeField(auto_now_add=True)

    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE)

    author = models.ForeignKey(User,on_delete = models.CASCADE)

    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    # 新增，记录二级评论回复给谁, str
    reply_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers'
    )

    class MPTTMeta:
        order_insertion_by = ['created_time']

    def __str__(self):
        return self.body[:20]
