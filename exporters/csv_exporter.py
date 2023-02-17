"""
Export JobApplication(s) to csv files. 
"""
import csv
from typing import List
from models.job_application import JobApplication


class CSVExporter:
    """
    Singleton that exports JobApplications to csv files
    """

    @staticmethod
    def export(path_filename: str, job_applications: List[JobApplication]) -> None:
        #TODO: verify that it checks if file already exists. If yes, updates the values (append).
         
        #TODO: loop by parsing a page, then export it. Then moving on to the next one.
        # This way we can stop parsing when we find an entry (url) that already exists in the archive.
        """
        Export the job_applications to a csv file. 

        Each row contains the fields of a JobApplication object.
        """
        with open(path_filename, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = list(job_applications[0].to_dict().keys())
            writer = csv.DictWriter(csvfile,
                                    fieldnames=fieldnames)
            writer.writeheader()
            for job_application in job_applications:
                writer.writerow(job_application.to_dict())
