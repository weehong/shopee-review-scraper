from dataclasses import dataclass
from datetime import datetime

@dataclass
class Rating:
    """Data class to store rating information"""
    rating_star: int
    quality: str
    fragrance: str
    performance: str
    comment: str
    submit_time: datetime