from django.db import models

class ScrapyItem(models.Model):
    class Meta:
        ordering = ['start_time']

    start_time = models.DateTimeField(primary_key=True)
    end_time = models.DateTimeField(null=True)
    item_num = models.IntegerField(null=True)
    time_cost = models.FloatField(null=True)
    fail_num = models.IntegerField(default=0)

    def __str__(self):
        return str(self.start_time.date())

class BaseItem_dj(models.Model):
    # Database item
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

    def __str__(self):
        return "{} ({})".format(self.name, self.item_id)

class StoreItem_dj(models.Model):
    # Store item
    base_item = models.ForeignKey(
        BaseItem_dj,
        on_delete=models.CASCADE,
    )
    store_name = models.CharField(max_length=100)
    store_id = models.IntegerField()
    position = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    hole_num = models.IntegerField()
    hole_1 = models.CharField(max_length=100)
    hole_2 = models.CharField(max_length=100)
    hole_3 = models.CharField(max_length=100)
    hole_4 = models.CharField(max_length=100)
    level = models.IntegerField()
    price = models.IntegerField()
    num = models.IntegerField()

    scrapy_item = models.ForeignKey(
        ScrapyItem,
        models.CASCADE,
    )
    def __str__(self):
        return self.base_item.__str__()

class WantedItem(models.Model):
    base_item = models.ForeignKey(
        BaseItem_dj,
        on_delete=models.CASCADE,
    )
    upper_price = models.IntegerField()
    level = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now=True)
    # string compose of hole-name seperate by comma used for query
    ### hole_string query to be finish ###
    hole_string = models.CharField(max_length=400, blank=True)
    highest_price = models.IntegerField(null=True, blank=True)
    lowest_price = models.IntegerField(null=True, blank=True)
    avg_price = models.FloatField(null=True, blank=True)
    num = models.IntegerField(null=True, blank=True)
    store_items = models.ManyToManyField(
        StoreItem_dj,
    )

    def __str__(self):
        return self.base_item.__str__()