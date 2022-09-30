import scrapy
import json

class VandalSpider(scrapy.Spider):
    name = "vandal"

    def start_requests(self):
        urls = [
            'https://vandal.elespanol.com/noticias/videojuegos',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        next_page = response.xpath('//div[contains(@class,"caja620")]/a/@href').getall()
        print("debugElement nextPage: ", next_page)
        yield from response.follow_all(next_page, self.parseArticle)

    def parseArticle(self, response):
        jsonText = response.xpath('//div[contains(@id,"globalwrap")]/script/text()').get()
        print("debugElementArticle ", jsonText)
        jsonData = json.loads(jsonText)
        
        yield {
                'description': jsonData["description"],
                'articleBody': jsonData["articleBody"],
                'title': jsonData["headline"],
                'author': jsonData["author"]["name"]
        }