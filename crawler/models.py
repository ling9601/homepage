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

class BaseItem_dj(models.Model):
    item_id = models.IntegerField(primary_key=True)
    image_link = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    genre = models.CharField(max_length=30)
    equipment_location = models.CharField(max_length=30)
    buy_price = models.IntegerField(null=True)
    sell_price = models.IntegerField(null=True)
    weight = models.FloatField(null=True)
    atk = models.IntegerField(null=True)
    matk = models.IntegerField(null=True)
    defense = models.IntegerField(null=True)
    attack_distance = models.IntegerField(null=True)
    hole_num = models.IntegerField()
    refinable = models.BooleanField(null=True)

class ScrapyItem(models.Model):
    start_time = models.DateTimeField(primary_key=True)
    end_time = models.DateTimeField()
    item_num = models.IntegerField()
    time_cost = models.FloatField()
