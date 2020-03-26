import scrapy
from app.utils.cookies import get_cookies
from app.items import BaseItem,BaseItemLoader

from crawler.models import BaseItem_dj

class DatabaseSpider(scrapy.Spider):
    name = "base"

    def start_requests(self):
        
        # clean BaseItem_dj
        BaseItem_dj.objects.all().delete()

        username = '2064162186'
        password = 'king88628'
        cookies = get_cookies(username, password)
        base_url = 'https://odinro.online/item/?&equip_loc=-1/&p={}'
        for page in range(1,205):
            yield scrapy.Request(url=base_url.format(page), callback=self.parse, cookies=cookies)

    def parse(self, response):
        
        raw_items = response.css('table[id=item-table] tbody tr') 
        for raw_item in raw_items:
            l = BaseItemLoader(item=BaseItem(), selector=raw_item)
            if raw_item.css('td:nth-child(2) img::attr(src)').get():
                # item with image_link
                l.add_css('item_id', 'td:nth-child(1) a::text')
                l.add_css('image_link', 'td:nth-child(2) img::attr(src)')
                l.add_css('name', 'td:nth_child(3)::text')
                l.add_css('genre', 'td:nth_child(4)::text')
                l.add_css('equipment_location', 'td:nth_child(5) span::text')
                l.add_css('buy_price', 'td:nth_child(6)::text')
                l.add_css('sell_price', 'td:nth_child(7)::text')
                l.add_css('weight', 'td:nth_child(8)::text')
                l.add_css('atk', 'td:nth_child(9)::text')
                l.add_css('matk', 'td:nth_child(10)::text')
                l.add_css('defense', 'td:nth_child(11)::text')
                l.add_css('attack_distance', 'td:nth_child(12)::text')
                l.add_css('hole_num', 'td:nth_child(13)::text')
                l.add_css('refinable', 'td:nth_child(14) span::text')

            else:
                # item without image_link
                l.add_css('item_id', 'td:nth-child(1) a::text')
                l.add_css('name', 'td:nth_child(2)::text')
                l.add_css('genre', 'td:nth_child(3)::text')
                l.add_css('equipment_location', 'td:nth_child(4) span::text')
                l.add_css('buy_price', 'td:nth_child(5)::text')
                l.add_css('sell_price', 'td:nth_child(6)::text')
                l.add_css('weight', 'td:nth_child(7)::text')
                l.add_css('atk', 'td:nth_child(8)::text')
                l.add_css('matk', 'td:nth_child(9)::text')
                l.add_css('defense', 'td:nth_child(10)::text')
                l.add_css('attack_distance', 'td:nth_child(11)::text')
                l.add_css('hole_num', 'td:nth_child(12)::text')
                l.add_css('refinable', 'td:nth_child(13) span::text')

            item = l.load_item()
            yield item