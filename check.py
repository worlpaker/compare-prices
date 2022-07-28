from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from cmprice.spiders.hepsiburada import hepsiburada
from cmprice.spiders.trendyol import trendyol
import numpy as np
import re
from datetime import datetime
import sys


def myscript():
    product_name = sys.argv[1]
    Runningtime = datetime.now()  # running timer

    Cleaned_hepsiburada_data = {"Name": [], "Price": []}
    Cleaned_trendyol_data = {"Name": [], "Price": []}

    # multiple spiders settings
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(hepsiburada)
        yield runner.crawl(trendyol)
        reactor.stop()

    crawl()

    reactor.run()

    # convert them one list.
    hepsiburada.Data["Name"] = [
        item for sublist in hepsiburada.Data["Name"] for item in sublist
    ]
    hepsiburada.Data["Price"] = [
        item for sublist in hepsiburada.Data["Price"] for item in sublist
    ]

    trendyol.Data["Name"] = [
        item for sublist in trendyol.Data["Name"] for item in sublist
    ]
    trendyol.Data["Price"] = [
        item for sublist in trendyol.Data["Price"] for item in sublist
    ]

    # Clean data, only exact words of products will contain.
    product = product_name.split()

    # hepsiburada
    # search exact words
    result_hepsi = [
        (x, y)
        for x, y in zip(hepsiburada.Data["Name"], hepsiburada.Data["Price"])
        if all(re.search("{}".format(w), x, re.IGNORECASE) for w in product)
    ]
    # add them to new data
    Add_hepsi = [
        (
            Cleaned_hepsiburada_data["Name"].append(i[0]),
            Cleaned_hepsiburada_data["Price"].append(i[1]),
        )
        for i in result_hepsi
    ]

    # trendyol
    # search exact words
    result_trendyol = [
        (x, y)
        for x, y in zip(trendyol.Data["Name"], trendyol.Data["Price"])
        if all(re.search("{}".format(w), x, re.IGNORECASE) for w in product)
    ]
    # add them to new data
    Add_trendyol = [
        (
            Cleaned_trendyol_data["Name"].append(i[0]),
            Cleaned_trendyol_data["Price"].append(i[1]),
        )
        for i in result_trendyol
    ]

    # best price

    # get minimum from hepsi
    best_price_hepsi, name_hepsi = (
        min(Cleaned_hepsiburada_data["Price"]),
        Cleaned_hepsiburada_data["Name"][np.argmin(Cleaned_hepsiburada_data["Price"])],
    )
    # get minimum from trendyol
    best_price_trendyol, name_trendyol = (
        min(Cleaned_trendyol_data["Price"]),
        Cleaned_trendyol_data["Name"][np.argmin(Cleaned_trendyol_data["Price"])],
    )
    print("Minimum Price-Hepsiburada.com:", best_price_hepsi, name_hepsi)
    print("Minimum Price-Trendyol.com:", best_price_trendyol, name_trendyol)

    # compare best price
    if best_price_hepsi < best_price_trendyol:
        print("BEST: Hepsiburada.com: ", best_price_hepsi, name_hepsi)
    else:
        print("BEST: Trendyol.com: ", best_price_trendyol, name_trendyol)
    return print("Running time:", datetime.now() - Runningtime)


if __name__ == "__main__":
    print("--STARTED--")
    myscript()
    print("--FINISHED--")
