# -*- coding: utf-8 -*-
import scrapy


class GetOneBookSpider(scrapy.Spider):
    name = 'get_one_book'
    allowed_domains = ['projekt-gutenberg.org']
    start_urls = ['https://www.projekt-gutenberg.org/meier/elend/chap001.html']

    custom_settings={'FEED_URI': "emerenz.json", 'FEED_FORMAT': 'jsonlines'}


    def extract_text(self, node):
        if not node:
            return ''
        _text = './/text()'
        extracted_list = [x.strip() for x in node.xpath(_text).extract() if len(x.strip()) > 0]
        if not extracted_list:
            return ''
        return ' '.join(extracted_list)

    def parse(self, response):
        author = response.css(".author::text").extract()
        title = response.css(".title::text").extract()
        text = self.extract_text(response.css("html body p"))
        #text = response.css("html body p::text").extract()
        #link = response.xpath("/html/body/a[2]/@href").extract()
        chapter_title = response.css("h3::text").extract()

        
        yield {
            'author': author,
            'title': title,
            'chapter_title': chapter_title,
            'text': text,
        }

        next_page = response.xpath('/html/body/a[3]/@href').get()

        if next_page is not None:
            next_page = "https://www.projekt-gutenberg.org/meier/elend/" + next_page
            #next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)