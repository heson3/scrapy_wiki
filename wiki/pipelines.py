# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv

class WikiPipeline:
    def process_item(self, item, spider):

        f = open('data.csv','a+', newline='',encoding='utf-8')
        writer = csv.writer(f)
        writer.writerows([[item['title'],item['link']]])

        return item
