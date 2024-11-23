from typing import List
import time
from datetime import datetime, timezone
from model import Rating
from parser import CommentParser
from data_fetcher import DataFetcher
from writer import DataWriter

class RatingsScraper:
    """Main class to coordinate the ratings scraping process"""
    def __init__(self, data_fetcher: DataFetcher, data_writer: DataWriter):
        self.data_fetcher = data_fetcher
        self.data_writer = data_writer
        self.comment_parser = CommentParser()
    
    def scrape(self) -> List[Rating]:
        ratings: List[Rating] = []
        
        for type_value in range(1, 4):
            offset = 0
            limit = 25
            
            while True:
                print(f"Fetching data with type={type_value}, limit={limit}, offset={offset}...")
                data = self.data_fetcher.fetch(type_value, limit, offset)
                
                if not data or 'data' not in data or 'ratings' not in data['data'] \
                   or not data['data']['ratings']:
                    print(f"No ratings found for type={type_value}.")
                    break
                
                current_ratings = data['data']['ratings']
                for rating_data in current_ratings:
                    if comment := rating_data.get('comment'):
                        parsed = self.comment_parser.parse(comment)
                        ratings.append(Rating(
                            rating_star=rating_data.get('rating_star', 0),
                            quality=parsed['Quality'],
                            fragrance=parsed['Fragrance'],
                            performance=parsed['Performance'],
                            comment=parsed['Comment'],
                            submit_time=datetime.fromtimestamp(
                                rating_data.get('submit_time', 0), 
                                tz=timezone.utc
                            )
                        ))
                
                if len(current_ratings) < limit:
                    break
                    
                offset += limit
                time.sleep(1)  # Rate limiting
        
        return ratings