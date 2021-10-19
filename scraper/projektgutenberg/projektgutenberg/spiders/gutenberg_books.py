# -*- coding: utf-8 -*-
import scrapy
import requests
from bs4 import BeautifulSoup
import re

class GutenbergBooksSpider(scrapy.Spider):
    name = 'gutenberg_books'
    allowed_domains = ['projekt-gutenberg.org']

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
    start_urls = start_urls[:5]
    print(start_urls)
    custom_settings={'FEED_URI': "fulltext.json", 'FEED_FORMAT': 'json'}

    def extract_text(self, node):
        if not node:
            return ''
        _text = './/text()'
        extracted_list = [x.strip() for x in node.xpath(_text).extract() if len(x.strip()) > 0]
        if not extracted_list:
            return ''
        return ' '.join(extracted_list)

    def parse(self, response):
        #author = response.css(".author::text").extract()
        #title = response.css(".title::text").extract()
        id = re.search(r"(?<=org\/)\w+\/\w+", response.request.url).group(0)
        id = re.sub("/", "_", id)
        text = self.extract_text(response.css("html body p"))
        chapter_title = response.css("h3::text").extract()

        
        yield {
            #'author': author,
            #'title': title,
            'id': id,
            'chapter_title': chapter_title,
            'text': text,
        }

        next_page = response.xpath('/html/body/a[3]/@href').get()

        if next_page is not None:
            next_page = re.sub(r"\w+.html$", "", response.request.url) + next_page
            yield scrapy.Request(next_page, callback=self.parse)