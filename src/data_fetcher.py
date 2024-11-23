from typing import Optional, Dict, Any
import requests

class DataFetcher:
    """Responsible for fetching data from Shopee API"""
    def __init__(self, itemid: str, shopid: str):
        self.itemid = itemid
        self.shopid = shopid
        self.base_url = "https://shopee.sg/api/v2/item/get_ratings"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

    def fetch(self, type_value: int, limit: int, offset: int) -> Optional[Dict[str, Any]]:
        """Fetch ratings data from API"""
        params = {
            'exclude_filter': 1,
            'filter': 0,
            'filter_size': 0,
            'flag': 1,
            'fold_filter': 0,
            'itemid': self.itemid,
            'limit': limit,
            'offset': offset,
            'relevant_reviews': False,
            'request_source': 2,
            'shopid': self.shopid,
            'tag_filter': '',
            'type': type_value,
            'variation_filters': ''
        }
        
        try:
            response = requests.get(self.base_url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")
            return None