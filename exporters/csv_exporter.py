"""
Export JobApplication(s) to csv files. 
"""
import csv
import os.path
from typing import List
from models.job_application import JobApplication
from helpers.logger import logger


class CSVExporter:
    """
    Singleton that exports JobApplications to csv files
    """
    export_filename = "my_job_applications.csv" 

    @staticmethod
    def export(job_applications: List[JobApplication]) -> None:
        #TODO: verify that it checks if file already exists. If yes, updates the values (append).

        #TODO: loop by parsing a page, then export it. Then moving on
        # to the next one.
        # This way we can stop parsing when we find an entry (url) that already
        # exists in the archive.
        """
        Export the job_applications to a csv file. 

        Each row contains the fields of a JobApplication object.
        """
        with open('a', newline='', encoding='utf-8') as csvfile:
            logger.info("Exporting files")
            if not job_applications:
                logger.warning("No job applications found. Nothing to export!")
                return
            fieldnames = list(job_applications[0].to_dict().keys())
            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames)
            if not os.path.isfile(CSVExporter.export_filename): 
                writer.writeheader()
            for job_application in job_applications:
                writer.writerow(job_application.to_dict())
            logger.info("Exported %s jobs", len(job_applications))