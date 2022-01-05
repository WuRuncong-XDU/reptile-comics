# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from time import sleep
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class ComicsSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ComicsDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        pass
        # return None

    def process_response(self, request, response, spider):
        bro = spider.bro  # 获取了爬虫类中定义的浏览器对象

        # if request.url in spider.models_urls:
        if '?p=' in request.url:
            # 如果获取失败则重新连接
            while 1:
                try:
                    bro.get(request.url)  # 对应的url进行i请求
                    spider.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="manga"]')))
                    while 1:
                        src = bro.find_element(By.XPATH, '//*[@id="manga"]').get_attribute('src')
                        if 'blank.gif' in src:
                            sleep(1)
                        else:
                            break
                except TimeoutException:
                    # except:
                    print('recall0 : ' + request.url)
                else:
                    break
            page_text = bro.page_source  # 包含了动态加载的数据

            # 针对定位到的这些response进行篡改
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        elif '.html' in request.url:
            while 1:
                try:
                    bro.get(request.url)  # 对应的url进行i请求
                    # 显性等待
                    spider.wait.until(ec.presence_of_element_located((By.XPATH, '//*[@id="pageSelect"]')))
                except TimeoutException:
                    # except:
                    print('recall1 : ' + request.url)
                else:
                    break
            page_text = bro.page_source  # 包含了动态加载的数据

            # 针对定位到的这些response进行篡改
            new_response = HtmlResponse(url=request.url, body=page_text, encoding='utf-8', request=request)
            return new_response
        else:
            return response  # 其他请求对应的响应对象

    def process_exception(self, request, exception, spider):
        # Download image occur exception will be recall here.
        print('recall3 : ' + request.url)
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
