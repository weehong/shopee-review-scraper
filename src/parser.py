import re
from typing import Optional, Dict

class URLParser:
    """Responsible for parsing Shopee URLs"""
    @staticmethod
    def extract_ids(url: str) -> tuple[Optional[str], Optional[str]]:
        """Extract item_id and shop_id from URL"""
        item_id_match = re.search(r'item_id=(\d+)', url)
        shop_id_match = re.search(r'shop_id=(\d+)', url)
        
        return (
            item_id_match.group(1) if item_id_match else None,
            shop_id_match.group(1) if shop_id_match else None
        )

class CommentParser:
    """Responsible for parsing rating comments"""
    @staticmethod
    def parse(comment: str) -> Dict[str, str]:
        """Parse comment to extract quality, fragrance, performance and additional comment"""
        patterns = {
            'Quality': r'Quality:(\w+)',
            'Fragrance': r'Fragrance:(\w+)',
            'Performance': r'Performance:(\w+)'
        }
        
        result = {key: '' for key in patterns}
        
        for key, pattern in patterns.items():
            if match := re.search(pattern, comment):
                result[key] = match.group(1)
        
        result['Comment'] = re.split(r'\n\n', comment)[-1]
        return result
