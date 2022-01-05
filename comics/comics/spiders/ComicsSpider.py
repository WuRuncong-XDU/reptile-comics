import scrapy
from scrapy import cmdline
from comics.items import ComicsItem
from selenium.webdriver import Edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.options import Options


class ComicsSpider(scrapy.Spider):
    name = 'ComicsSpider'

    def __init__(self):
        self.opt = Options()
        self.opt.add_argument("--headless")
        self.opt.add_argument("--disable-gpu")
        self.bro = Edge(options=self.opt)
        self.wait = WebDriverWait(self.bro, 5)

    start_urls = ['http://www.guomanba.cc/36350/']

    def parse(self, response):
        li_list = response.xpath('//*[@id="chpater-list-1"]/ul[1]/li')
        li_list += response.xpath('//*[@id="chpater-list-1"]/ul[2]/li')

        for i in li_list:
            item = ComicsItem()
            url = 'http://www.guomanba.cc' + i.xpath('./a/@href').extract_first()

            # Save parameters in item
            item['url'] = url
            item['title'] = i.xpath('./a/@title').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_model, meta={'item': item})
            # return

    # 解析每一个子页面中对应的url
    def parse_model(self, response):
        item = response.meta['item']
        page_num = len(response.xpath('//*[@id="pageSelect"]/option'))

        # 异步需要新建item0
        for i in range(1, page_num+1):
            sub_url = item['url'] + '?p=' + str(i)
            item0 = ComicsItem()
            item0['page'] = i
            item0['title'] = item['title']
            yield scrapy.Request(url=sub_url, callback=self.parse_detail, meta={'item': item0})

    def parse_detail(self, response):
        item0 = response.meta['item']
        item0['img_src'] = response.xpath('//*[@id="manga"]/@src').extract_first()
        yield item0

    def closed(self, spider):
        self.bro.quit()
        print('结束爬虫')


# Automatic run scripts
if __name__ == '__main__':
    cmdline.execute("scrapy crawl ComicsSpider".split())
