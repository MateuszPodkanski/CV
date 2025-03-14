import scrapy
import datetime
from products_scrapper.items import ProductItem 
class AgtomSpider(scrapy.Spider):
    name = "agtom"
    allowed_domains = ["agtom.eu"]
    start_urls = ["https://agtom.eu/51-warhammer-40000"]

    custom_settings = { 
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 2,   
    }

    def parse(self, response):
        for product in response.css("div.h5 a.product-name"):
            product_url = product.attrib['href']
            print(product_url)
            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={'product_url': product_url}
            )

    def parse_product(self, response):
        title = response.css("h1.product-name::text").get()
        title = title.replace(",", " ") if title else 'No title'
        price = response.css("span#our_price_display::attr(content)").get()
        price = float(price) if price else None
        image_url = response.css('img#bigpic::attr(src)').get()
        ean = response.css("label:contains('EAN') + span::text").get()
        quantity = response.css('span#quantityAvailable::text').get()
        if quantity:
            quantity = quantity.replace('Dostępna ilość:', '').strip()
        description = response.css("p.page-product-heading + div.rte ::text").getall()
        description = " ".join(description).strip()
        description = description.replace(",", " ")

        product_item = ProductItem(
            product_title=title,
            product_url=response.meta['product_url'],
            product_price=price if price else 'No data',
            product_description=description if description else 'No data',
            shop='agtom',
            scraping_date=datetime.date.today().isoformat(),
            ean=ean.strip() if ean else 'No data',
            quantity_available=quantity if quantity else 'No data',
            image_url=response.urljoin(image_url) if image_url else 'No data'
        )

        yield product_item