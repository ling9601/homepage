import scrapy
from scrapy import signals

from app.items import StoreItem, StoreItemLoader
from app.utils.cookies import get_cookies
import datetime
import re
import pytz
import time

from django.db.models import Avg, Max, Min, Count

from crawler.models import *

class StoreSpider(scrapy.Spider):
    name = 'store'

    def start_requests(self):
        username = '2064162186'
        password = 'king88628'
        self.cookies = get_cookies(username, password)
        self.base_url = 'https://odinro.online/vending/?s=/vending/&p={}'
        self.vender_url = 'https://odinro.online/vending/viewshop/?id={}'

        self.start_time = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
        self.scrapy_item = ScrapyItem(start_time=self.start_time)
        # save it at first for the foreign key in StoreItem
        self.scrapy_item.save()
        
        yield scrapy.Request(url=self.base_url.format(1), callback=self.parse_page_num, cookies=self.cookies)
        # yield scrapy.Request(url='https://odinro.online/vending/viewshop/?id=134', callback=self.parse, cookies=self.cookies, meta={'store_id':134})
    
    def parse_page_num(self, response):
        page_num_string = response.css('#ranking-page p::text') .get()
        num = int(re.findall(r'\d+', page_num_string)[1])

        for i in range(num):
            yield scrapy.Request(url=self.base_url.format(i+1), callback=self.parse_store_id, cookies=self.cookies, dont_filter=True)

    def parse_store_id(self, response):
        raw_items = response.css('table[class=table] tbody tr')

        for raw_item in raw_items:
            store_id = int(raw_item.css('td:first-child a::text').get())
            yield scrapy.Request(url=self.vender_url.format(store_id), callback=self.parse, cookies=self.cookies, meta={'store_id':store_id})
    
    def parse(self, response):
        raw_items = response.css('table[class*=db-table] tbody tr') 

        store_name = response.css('#page-content h3::text').get()
        store_id = str(response.meta['store_id'])
        position = response.css('#page-content h4::text').get()

        for raw_item in raw_items:
            l = StoreItemLoader(item=StoreItem(), selector=raw_item)
            l.add_css('item_id','td:first-child a::text')
            l.add_css('hole_1', 'td:nth-child(5) * ::text')
            l.add_css('hole_2', 'td:nth-child(6) * ::text')
            l.add_css('hole_3', 'td:nth-child(7) * ::text')
            l.add_css('hole_4', 'td:nth-child(8) * ::text')
            l.add_css('price', 'td:nth-child(9)::text')
            l.add_css('num', 'td:nth-child(10)::text')
            
            level = raw_item.css('td:nth-child(3) strong::text').get()
            level = level if level else '0'
            hole_num = raw_item.css('td:nth-child(4)::text').get().strip()
            hole_num = hole_num if hole_num else '0'
            name = raw_item.css('td:nth-child(2) a::text').get()
            name = name if name else 'No Name'

            l.add_value('name', name)
            l.add_value('store_name', store_name)
            l.add_value('store_id', store_id)
            l.add_value('position', position)
            l.add_value('level', level)
            l.add_value('hole_num', hole_num)        

            item = l.load_item()
            yield item

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(StoreSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
        return spider
    def spider_closed(self, spider):
        
        # save scrapy_item
        self.scrapy_item.end_time = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
        stats = spider.crawler.stats.get_stats()
        self.scrapy_item.item_num = stats['item_scraped_count']
        self.scrapy_item.time_cost = stats['elapsed_time_seconds']
        self.scrapy_item.save()

        # check for wanted_items
        start_time = time.time()
        wanted_items = WantedItem.objects.all()

        spider.logger.info('WantedItem({})'.format(len(wanted_items)))
        catch_count = 0
        for wanted_item in wanted_items:
            # delete all previous cathed_item
            wanted_item.catcheditem_set.all().delete()
            
            # do some statistics
            items = self.scrapy_item.storeitem_dj_set.filter(
                item_id = wanted_item.base_item.pk,
                level = wanted_item.level
            )

            # attach 'sum_price'
            for item in items:
                item.sum_price = item.price*item.num

            wanted_item.num = sum([item.num for item in items])
            wanted_item.highest_price = items.aggregate(Max('price'))['price__max']
            wanted_item.lowest_price = items.aggregate(Min('price'))['price__min']
            wanted_item.avg_price = sum([item.sum_price for item in items])/wanted_item.num if wanted_item.num else None
            wanted_item.save()
            
            # catched item
            q = self.scrapy_item.storeitem_dj_set.filter(
                item_id = wanted_item.base_item.pk,
                price__lte = wanted_item.upper_price,
                level__gte = wanted_item.level
            )
            for store_item in q:
                CatchedItem(
                    wanted_item = wanted_item,
                    store_item = store_item
                ).save()

                catch_count += 1

        spider.logger.info('CatchedItem({})'.format(catch_count))
        spider.logger.info('Time cost({:.2f})'.format(time.time()-start_time))

