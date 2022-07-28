import sys
import scrapy

product_name = sys.argv[1]


class hepsiburada(scrapy.Spider):
    name = "hepsiburada"
    start_urls = [
        f"https://www.hepsiburada.com/ara?q={product_name}",
    ]
    Data = {"Name": [], "Price": []}
    page_number = 1

    def parse(self, response):
        for quote in response.xpath('//li[@class="productListContent-item"]'):
            Prd_Name = (
                quote.xpath(
                    './/h3[@data-test-id="product-card-name"]/text()'
                ).extract_first(),
            )
            Prd_Price = quote.xpath(
                './/div[@data-test-id="price-current-price"]/text()'
            ).extract()
            hepsiburada.Data["Name"].append(Prd_Name)
            hepsiburada.Data["Price"].append(Prd_Price)
        if hepsiburada.page_number != 6:  # until page 5
            hepsiburada.page_number += 1
            yield scrapy.Request(
                response.urljoin(
                    f"ara?q={product_name}" + f"&sayfa={hepsiburada.page_number}"
                )
            )  # next url link
