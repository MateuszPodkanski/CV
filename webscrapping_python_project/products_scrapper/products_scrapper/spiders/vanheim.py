import scrapy
import datetime  

class VanheimSpider(scrapy.Spider):
    name = "vanaheim"
    allowed_domains = ["vanaheim.pl"]
    start_urls = ["https://vanaheim.pl/pl/7-warhammer-40000"]

    custom_settings = {
    'ROBOTSTXT_OBEY': True,
    'DOWNLOAD_DELAY': 2,  
    }

    def parse(self, response):
        for product in response.css("h3 a"):
            product_url = response.urljoin(product.attrib['href'])

            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={
                'product_url': product_url
                }
            )

    def parse_product(self, response):
        ean = response.css("label[for='product_ean13'] + span::text").get()
        quantity = response.css('p#pQuantityAvailable span#quantityAvailable::text').get()
        title = response.css('h1.vh-product-title::text').get()
        image_url = response.css('img#bigpic::attr(src)').get()
        price = response.css('span#our_price_display::text').get()

        if price:
            price = price.replace('zł', '')
            price = price.strip()

        if quantity:
            quantity = quantity.replace('Dostępna ilość:', '').strip()

        yield {
            'product_title': title.strip() if title else 'No title',
            'product_url': response.meta['product_url'],
            'product_price': price.strip() if price else 'No data',
            'shop': 'vanaheim',
            'scraping_date': datetime.date.today().isoformat(),
            'ean': ean.strip() if ean else 'No data',
            'quantity_available': quantity if quantity else 'No data',
            'image_url': response.urljoin(image_url) if image_url else 'No image'
        }