"""
Load information of job application csv files.
"""
import csv
from typing import List
from helpers.logger import logger


class CSVLoader:
    """
    Load the files (if exist) of past job application scrapping. 
    """
    delimiter = '@'
    @staticmethod
    def load_job_urls(filename) -> List[str]:
        """
        Load the job application urls.
        """
        urls = []
        try:
            with open(filename, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=CSVLoader.delimiter)
                for row in reader:
                    urls.append(row[0])
        except FileNotFoundError:
            logger.warning("No past job application archive! Returning empty url list")
        return urls
        