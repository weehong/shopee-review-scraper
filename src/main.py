import os

from pathlib import Path
from parser import URLParser
from data_fetcher import DataFetcher
from writer import ExcelWriter
from scraper import RatingsScraper

def main() -> None:
    print("You can find the item URL from: https://shopee.sg/api/v4/pdp/get_pc")
    print("Example URL: https://shopee.sg/api/v4/pdp/get_pc?item_id=25809034146&shop_id=1028479860")
    
    url = input("Please enter the URL containing the item_id and shop_id: ")
    itemid, shopid = URLParser.extract_ids(url)
    
    if not itemid or not shopid:
        print("Exiting script. Could not extract valid item_id and shop_id.")
        return
    
    data_fetcher = DataFetcher(itemid, shopid)
    data_writer = ExcelWriter()  # It will use the default 'exports' directory
    scraper = RatingsScraper(data_fetcher, data_writer)
    
    ratings = scraper.scrape()
    data_writer.write(ratings, f"ratings_{shopid}_{itemid}")

if __name__ == "__main__":
    main()