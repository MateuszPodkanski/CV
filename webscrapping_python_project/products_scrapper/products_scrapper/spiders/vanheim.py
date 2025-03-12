import scrapy
import datetime  # Importujemy datetime

class VanheimSpider(scrapy.Spider):
    name = "vanaheim"
    allowed_domains = ["vanaheim.pl"]
    start_urls = ["https://vanaheim.pl/pl/7-warhammer-40000"]

    def parse(self, response):
        # Pobieranie linków i cen
        for product in response.css("h3 a"):
            product_url = response.urljoin(product.attrib['href'])
            price = product.xpath('./ancestor::div[contains(@class, "product-container")]//p[@class="pprice"]/span/text()').get()
            if price:
                price = price.strip()

            yield scrapy.Request(
                url=product_url,
                callback=self.parse_product,
                meta={
                    'shop': 'vanaheim',
                    'product_url': product_url,
                    'price': price if price else 'No data'
                }
            )

    def parse_product(self, response):
        # Pobieranie danych ze strony produktu
        ean = response.css("label[for='product_ean13'] + span::text").get()
        quantity = response.css('p#pQuantityAvailable span#quantityAvailable::text').get()
        title = response.css('h1.vh-product-title::text').get()
        image_url = response.css('img#bigpic::attr(src)').get()

        if quantity:
            quantity = quantity.replace('Dostępna ilość:', '').strip()

        yield {
            'product_url': response.meta['product_url'],
            'product_price': response.meta['price'],
            'shop': response.meta['shop'],
            'scraping_date': datetime.date.today().isoformat(),  # Bezpośrednio ustawiamy datę tutaj
            'product_title': title.strip() if title else 'No title',
            'ean': ean.strip() if ean else 'No data',
            'quantity_available': quantity if quantity else 'No data',
            'image_url': response.urljoin(image_url) if image_url else 'No image'
        }