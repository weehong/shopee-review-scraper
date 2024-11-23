import os
from abc import ABC, abstractmethod
from typing import List
from pathlib import Path
from datetime import datetime
from openpyxl import Workbook
from model import Rating

# Define ROOT_DIR for project root directory
ROOT_DIR = str(Path(__file__).resolve().parent)

class DataWriter(ABC):
    """Abstract base class for data writers"""
    def __init__(self, base_dir: str = "exports"):
        """
        Initialize the writer with a base directory
        Args:
            base_dir (str): Base directory for storing files
        """
        # Use ROOT_DIR as the root path
        self.base_dir = Path(ROOT_DIR).parent / base_dir
        self._ensure_directory_exists()

    def _ensure_directory_exists(self) -> None:
        """Create the output directory if it doesn't exist"""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _generate_filename(self, base_filename: str) -> Path:
        """
        Generate a full path for the output file
        Args:
            base_filename (str): Base filename without directory
        Returns:
            Path: Full path including directory
        """
        return self.base_dir / base_filename

class ExcelWriter(DataWriter):
    """Concrete implementation of DataWriter for Excel format"""
    def write(self, ratings: List[Rating], filename: str) -> None:
        """
        Write ratings to an Excel file
        Args:
            ratings (List[Rating]): List of ratings to write
            filename (str): Base filename for the output file
        """
        # Add timestamp to filename to avoid overwrites
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_filename = self._generate_filename(f"{filename}_{timestamp}.xlsx")
        
        wb = Workbook()
        ws = wb.active
        ws.title = "Ratings"
        
        # Write headers
        headers = ["#", "Editable Date", "Rating Star", "Quality", 
                  "Fragrance", "Performance", "Comment"]
        ws.append(headers)
        
        # Write data
        for idx, rating in enumerate(ratings, start=1):
            if any([rating.rating_star, rating.comment, rating.quality, 
                   rating.fragrance, rating.performance]):
                ws.append([ 
                    idx,
                    rating.submit_time.strftime('%Y-%m-%d %H:%M:%S'),
                    rating.rating_star,
                    rating.quality,
                    rating.fragrance,
                    rating.performance,
                    rating.comment
                ])
        
        # Save the workbook
        wb.save(str(full_filename))
        print(f"Data saved to {full_filename}")
