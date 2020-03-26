from django.db import models

class StoreItem_dj(models.Model):
    store_name = models.CharField(max_length=100)
    store_id = models.IntegerField()
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    item_id = models.IntegerField()
    hole_num = models.IntegerField()
    hole_1 = models.CharField(max_length=100)
    hole_2 = models.CharField(max_length=100)
    hole_3 = models.CharField(max_length=100)
    hole_4 = models.CharField(max_length=100)
    level = models.IntegerField()
    price = models.IntegerField()
    num = models.IntegerField()
    time = models.DateTimeField()