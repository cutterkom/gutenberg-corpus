# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
import re

class GetBookFromOverviewSpider(scrapy.Spider):
    name = 'get_book_from_overview'
    allowed_domains = ['projekt-gutenberg.org']
    custom_settings={'FEED_URI': "meta.json", 'FEED_FORMAT': 'json'}

    def extract_text(self, node):
        if not node:
            return ''
        _text = './/text()'
        extracted_list = [x.strip() for x in node.xpath(_text).extract() if len(x.strip()) > 0]
        if not extracted_list:
            return ''
        return ' '.join(extracted_list)

    def get_fulltext_links():
        full_text_links = []
        url = "https://www.projekt-gutenberg.org/info/texte/allworka.html"
        
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        dl = soup.find("dl")
        links = dl.findAll('a')

        for link in links:
            link = link.get("href").replace("../../", "")
            link = "https://www.projekt-gutenberg.org/" + link
            full_text_links.append(link)
        return(full_text_links)


    start_urls = get_fulltext_links()


    def parse(self, response):
        id = re.search(r"(?<=org\/)\w+\/\w+", response.request.url).group(0)
        id = re.sub("/", "_", id)
        author = response.css(".author::text").extract()
        title = self.extract_text(response.css(".title::text"))

        
        yield {
            'id': id,
            'author': author,
            'title': title,
            'link': link
        }
        
        #next_page = response.css("html body ul li a::attr(href)").get()

        # if next_page is not None:
        #     next_page = response.urljoin(full_text)
        #     print(full_text)
        #     yield scrapy.Request(next_page, callback=self.parse)
