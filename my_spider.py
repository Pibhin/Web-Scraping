import scrapy
import logging

class MySpider(scrapy.Spider):
    name = 'my_spider'

    def __init__(self, url='', *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.logger.info(f"Spider initialized with start URL: {url}")

    def start_requests(self):
        """Generate initial requests for the spider."""
        for url in self.start_urls:
            self.logger.debug(f"Starting request for URL: {url}")
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        """Parse the response and extract data."""
        self.logger.info(f"Received response for URL: {response.url}")
        
        try:
            # Example: Scraping the title from the webpage
            title = response.xpath('//title/text()').get()
            if title:
                self.logger.info(f"Page title extracted: {title}")
            else:
                self.logger.warning(f"No title found for URL: {response.url}")
            yield {'title': title}
        except Exception as e:
            self.logger.error(f"An error occurred while parsing {response.url}: {e}")
