import scrapy
import json
class VandalSpider(scrapy.Spider):
    name = "vandal"
    num = 0

    def start_requests(self):
        urls = [
            'https://vandal.elespanol.com/noticias/videojuegos',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        news = response.xpath('//div[contains(@class,"caja620")]/a/@href').getall()
        # print("debugElement news: ", news)
        filename = f' {self.num} vandal.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

        next_page = response.xpath('//div[contains(@class,"tn14b")]/a/@href').getall()
        
        f = open("logs.txt", 'a')

        for i in range(0, len(next_page)):
            next_page[i] = 'https://vandal.elespanol.com'+next_page[i]
            f.write(next_page[i], "\n")

        # print("soy nextpage: ", next_page)
        yield from response.follow_all(next_page, callback=self.parse)
        yield from response.follow_all(news, self.parseArticle)

    def parseArticle(self, response):
        jsonText = response.xpath('//div[contains(@id,"globalwrap")]/script/text()').get()
        # print("debugElementArticle ", jsonText)
        jsonData = json.loads(jsonText, strict=False)
        
        yield {
                'description': jsonData["description"],
                'articleBody': jsonData["articleBody"],
                'title': jsonData["headline"],
                'author': jsonData["author"]["name"]
        }