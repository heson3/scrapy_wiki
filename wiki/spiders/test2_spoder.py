import scrapy
from ..items import WikiItem

class WikiSpider(scrapy.Spider):
    name = "test2_spider"
    #"""亚洲"""
    #start_urls = ["https://zh.wikipedia.org/wiki/Category:%E4%BA%9A%E6%B4%B2"]
    """非洲"""
    start_urls = ["https://zh.wikipedia.org/wiki/Category:%E9%9D%9E%E6%B4%B2"]
    
    def parse(self,response):
        
        #subclass_list = response.xpath('//ol//li[position()<11]//div[@class="hd"]/a/@href').getall()
        #"""亚洲子类:亚洲文化 !!!"""
        """非洲子类:非洲文化"""
        subclass_list = response.xpath( \
            '//div[@class="mw-category-group"][position()<2]/ul//li[position()<2]//div[@class="CategoryTreeItem"]/a/@href' \
        #    '//div[@class="mw-category-group"][position()<2]/ul//li//div[@class="CategoryTreeItem"]/a/@href' \
                ).getall()
        
        for subclass in subclass_list:
            subclass = "https://zh.wikipedia.org"+subclass
            #print("亚洲子类：亚洲文化，",subclass)
            yield scrapy.Request(url=subclass,callback=self.parse2)

    def parse2(self,response):
        #"""亚洲文化：全部"""
        """非洲文化：全部"""
        subclass_list2 = response.xpath( \
            '//div[@class="mw-category-group"]/ul//li//div[@class="CategoryTreeItem"]/a/@href' \
                ).getall()
        if subclass_list2:
            #print("亚洲文化子类",subclass_list2)
            for subclass2 in subclass_list2:
                subclass2 = "https://zh.wikipedia.org"+subclass2
                #print("亚洲文化子类",subclass2)
                # subclass2 = "https://zh.wikipedia.org"+subclass2
                yield scrapy.Request(url=subclass2,callback=self.parse2)

        else:
            subclass_list3 = response.xpath( \
            '//div[@class="mw-category-group"]/ul//li/a/@href' \
                ).getall()
            for subclass3 in subclass_list3:
                
                subclass3 = "https://zh.wikipedia.org"+subclass3
                #print("最小分类 ",subclass3)
                yield scrapy.Request(url=subclass3,callback=self.parse3)

    def parse3(self,response):
        """跳过‘模板’页"""
        mb = response.xpath('//h1[@class="firstHeading mw-first-heading"]/span[@class="mw-page-title-namespace"]').get()
        if mb:
            pass
        else:    
            item = WikiItem()
            """两种标题格式"""
            tt = response.xpath('//span[@class="mw-page-title-main"]/text()').get()
            if tt:
                item['title'] = tt
            else:
                item['title'] =response.xpath('//h1[@class="firstHeading mw-first-heading"]/span/text()').get()
            item["link"] = response.url
            yield item