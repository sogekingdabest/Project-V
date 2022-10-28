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
        consoles_script = response.xpath('//*[@id="globalwrap"]/div[1]/script/text()').get()

        regex_oas_query = re.compile('.*OAS_query=\"(.*)\".*')
        regex_console = re.compile('consola=(.*)')
        #"\nOAS_query=\"consola=pc&consola=iphone&consola=android\";\n"
        console_list = []
        if consoles_script is not None:
            consoles_str = regex_oas_query.match(consoles_script.strip()).group(1)
            for console_str in consoles_str.split('&'):
                console_name = regex_console.match(console_str).group(1)
                console_list.append(console_name)

        # print("debugElementArticle ", jsonText)
        jsonData = json.loads(jsonText, strict=False)
        
        yield {
                'description': jsonData["description"],
                'articleBody': jsonData["articleBody"],
                'title': jsonData["headline"],
                'author': jsonData["author"]["name"],
                'consoles': console_list
        }


    # def parse(self, response):
    #     news = response.xpath('//div[contains(@class,"caja620")]/a/@href').getall()
    #     # print("debugElement news: ", news)
    #     filename = f' {0} vandal.html'
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)

    #     next_page = response.xpath('//div[contains(@class,"tn14b")]/a/@href').getall()
        
    #     f = open("logs.txt", 'a')

    #     for i in range(0, len(next_page)):
    #         next_page[i] = 'https://vandal.elespanol.com'+next_page[i]
    #         f.write(next_page[i] + "\n")

    #     # print("soy nextpage: ", next_page)
    #     yield from response.follow_all(next_page,  callback=self.parse)
    #     yield from response.follow_all(news, self.parseArticle)

    