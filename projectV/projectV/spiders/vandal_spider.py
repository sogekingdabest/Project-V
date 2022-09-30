import scrapy
import json

class VandalSpider(scrapy.Spider):
    name = "vandal"

    def start_requests(self):
        urls = [
            'https://vandal.elespanol.com/noticia/1350756965/pokemon-escarlata-y-purpura-tendran-una-cancion-compuesta-por-ed-sheeran/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        jsonText = response.xpath('//div[contains(@id,"globalwrap")]/script/text()').get()
        print("debugElement ", jsonText)


        jsonData = json.loads(jsonText)
        yield {
                'description': jsonData["description"],
                'articleBody': jsonData["articleBody"],
                'title': jsonData["headline"],
                'author': jsonData["author"]["name"]
        }