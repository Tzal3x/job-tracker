"""
Export JobApplication(s) to csv files. 
"""
import csv
import os.path
from typing import List

from models.job_application import JobApplication
from helpers.logger import logger
from loaders.csv_loader import CSVLoader


class CSVExporter:
    """
    Singleton that exports JobApplications to csv files
    """
    filename = "my_job_applications.csv"
    delimiter = "@"
    existing_urls = CSVLoader.load_job_urls(filename)  # job urls already in the archive

    @staticmethod
    def export(job_applications: List[JobApplication]) -> int:
        """
        Export the job_applications to a csv file. 
        Each row contains the fields of a JobApplication object.

        Return 1 if export was interrupted early.
        Return 0 if all input was exported. 
        """
        file_exists = os.path.isfile(CSVExporter.filename)
        with open(CSVExporter.filename, 'a', newline='', encoding='utf-8') as csvfile:
            logger.info("Exporting files")
            if not job_applications:
                logger.warning("No job applications found. Nothing to export!")
                return 1
            fieldnames = list(job_applications[0].to_dict().keys())
            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames,
                                    delimiter=CSVExporter.delimiter)
            if not file_exists:
                writer.writeheader()
            for job_application in job_applications:
                already_in_csv = job_application.url in CSVExporter.existing_urls
                if already_in_csv:
                    logger.warning("Existing job url found! Stopping export.")
                    return 1
                row = {
                    key: CSVExporter.remove_delimiter(value)
                    for key, value in job_application.to_dict().items()
                    }
                writer.writerow(row)
            logger.info("Exported %s jobs", len(job_applications))
        return 0

    @staticmethod
    def remove_delimiter(job_application_field: str) -> str:
        """
        Remove occurances of delimiter because it breaks the data.
        """
        return job_application_field.replace(CSVExporter.delimiter, '')
    