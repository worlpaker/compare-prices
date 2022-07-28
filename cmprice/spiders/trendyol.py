import sys
import scrapy

product_name = sys.argv[1]


class trendyol(scrapy.Spider):
    name = "trendyol"
    start_urls = [
        f"https://www.trendyol.com/sr?q={product_name}",
    ]
    Data = {"Name": [], "Price": []}
    page_number = 1

    def parse(self, response):
        for quote in response.xpath('//div[@class="prdct-cntnr-wrppr"]'):
            Prd_Name = quote.xpath(
                './/span[@class="prdct-desc-cntnr-name hasRatings"]/text()'
            ).extract()
            if not Prd_Name:
                Prd_Name = quote.xpath(
                    './/span[@class="prdct-desc-cntnr-name"]/text()'
                ).extract()
            Prd_Price = quote.xpath('.//div[@class="prc-box-dscntd"]/text()').extract()
            trendyol.Data["Name"].append(Prd_Name)
            trendyol.Data["Price"].append(Prd_Price)
        if trendyol.page_number != 6:  # until page 5
            trendyol.page_number += 1
            yield scrapy.Request(
                response.urljoin(f"sr?q={product_name}" + f"&pi={trendyol.page_number}")
            )  # next url link
