import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re

import json

class VandalSpider(CrawlSpider):
    name = "vandal"
    allowed_domains = ["vandal.elespanol.com"]
    start_urls = ["https://vandal.elespanol.com/noticias/videojuegos"]
    
    

    rules = (
        # Extract links matching 'category.php' (but not matching 'subsection.php')
        # and follow links from them (since no callback means follow=True by default).
        Rule(LinkExtractor(allow=('vandal\.elespanol\.com\/noticias\/videojuegos\/inicio\/[0-9]*.*', ))),

        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('vandal\.elespanol\.com\/noticia\/[0-9]*.*', )), callback='parseArticle'),
    )

    def parseArticle(self, response):
        jsonText = response.xpath('//div[contains(@id,"globalwrap")]/script/text()').get()

        jsonData = json.loads(jsonText, strict=False)
        
        yield {
                'description': jsonData["description"],
                'articleBody': jsonData["articleBody"],
                'title': jsonData["headline"],
                'author': jsonData["author"]["name"],
        }
