import re
from ic1.items import Product
from scrapy.spiders import CrawlSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class MySpider_1(CrawlSpider):
    name = 'spider_1'
    allowed_domains = ['sp-computer.ru']
    start_urls = ['https://www.sp-computer.ru/catalog/noutbuki/']
    hurl = "https://www.sp-computer.ru/"
    default_headers ={}
    def parse(self, response):
        nout_card = "//div[@class='col-xs-12']//div[@class='product-item-title']//a/@href"
        for card in response.xpath(nout_card):
            yield response.follow(card, callback=self.parse_nouts)
        next_page_css = '.bx-pag-next a ::attr(href)'
        for nextpage_link in response.css(next_page_css):
            yield response.follow(url=nextpage_link, callback=self.parse)

    def parse_nouts(self, response):
        item = Product()
        freq_core = 1.0
        proc_core = response.xpath("//div[.='Характеристики процессора']/following-sibling::div/text()").get().strip()
        proc = re.findall(r'(\d+[\.]?[\d+]?) ?[\D]+(\d?)', proc_core)
        price = response.xpath("//td[@class='price']/span/text()").get().strip()
        if proc[0][1]:
            freq_core=float(proc[0][1])

        item['name']=re.sub(r'Ноутбук?','',response.xpath("//div[@class='head_title pad_mobi']/h1/text()").get().split(',')[0]).strip()
        item['core'] = freq_core
        item['ram'] = response.xpath("//div[.='Оперативная память']/following-sibling::div/text()").get().strip().split(" ")[0]
        item['screen'] = response.xpath("//div[.='Диагональ экрана в дюймах']/following-sibling::div/text()").get().strip()
        item['price'] = int(re.sub(r'\D?', '', price))
        item['url'] = response.url
        return item
 
    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
                url, callback=self.parse, headers=self.default_headers
                )

class MySpider_2(CrawlSpider):
    name = 'spider_2'
    allowed_domains = ['notik.ru']
    start_urls = ['https://www.notik.ru/index/notebooks.htm?srch=true&full=&f117=5650']
    default_headers ={}
    def parse(self, response):
        for card in response.xpath("//tr[@class='hide-mob']//a/@href"):
            yield response.follow(card, callback=self.parse_nouts)
        for page in response.xpath("//div[@class='paginator align-left']//a/@href"):
            yield response.follow(page, callback=self.parse)

    def parse_nouts(self, response):
        item = Product()
        column1=response.xpath("//table[@class='parametersInCard column']")[0]
        column2=response.xpath("//table[@class='parametersInCard column']")[1]
        price = column2.xpath("//*[.='Цена:']/parent::td/following::td[1]")
        price = price.xpath("//span[@itemprop='price']/text()").get().split()

        item['name']=re.sub(r'Ноутбук','',response.xpath("//h1[@class='goodtitlemain']/text()").get()).strip()
        item['core'] = int(column1.xpath("//*[.='Количество ядер:']/parent::td/following::td[1]/text()").get().strip())
        item['ram'] = int(column1.xpath("//*[.='Оперативная память:']/parent::td/following::td[1]/text()").get().split(' ')[0])
        item['screen'] = float(column1.xpath("//*[.='Экран:']/parent::td/following::td[1]/text()").get().split('"')[0])
        item['price'] = int("".join(price))
        item['url'] = response.url

        return item

    def parse_start_url(self, response, **kwargs):
        url = self.start_urls[0]
        return response.follow(
                url, callback=self.parse, headers=self.default_headers
                )

process = CrawlerProcess(get_project_settings())
process.crawl(MySpider_1)
process.crawl(MySpider_2)
process.start()