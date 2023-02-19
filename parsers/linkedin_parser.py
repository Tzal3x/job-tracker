"""
Scrap LinkedIn data with selenium and BeautifulSoup.
"""
import re
from time import sleep
from random import random
from typing import Set

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from helpers.logger import logger
from models.job_application import JobApplication
from exporters.csv_exporter import CSVExporter


class LinkedInParser:
    """
    Singleton object used to parse LinkedIn data of applied job applications. 
    """

    def __init__(self, credentials: dict, headless=True) -> None:
        options = Options()
        options.headless = headless
        self.driver = webdriver.Chrome(
            # TODO: I might need to download install Chrome and set
            # CHROMEDRIVER_PATH when (and if) I dockerize the app.
            # CHROMEDRIVER_PATH,
            options=options
        )

        self.username = credentials["LinkedIn"]["username"]
        self.password = credentials["LinkedIn"]["password"]

    def __del__(self) -> None:
        self.driver.close()

    def _login(self) -> None:
        """
        Driver logs in to the LinkedIn
        """
        logger.info("Logging in to LinkedIn ...")
        # Go to the home page
        self.driver.get("https://www.linkedin.com/home")

        # Fill username
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_key"))
        )
        self.driver.find_element(By.ID, "session_key").send_keys(self.username)
        self.driver.implicitly_wait(4)
        sleep(1 + random() * 5)

        # Fill password
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_password"))
        )
        self.driver.find_element(
            By.ID, "session_password").send_keys(self.password)
        self.driver.implicitly_wait(4)
        sleep(1 + random() * 2)

        # Click sign-in button
        self.driver.find_element(
            By.CSS_SELECTOR, "button.sign-in-form__submit-button").click()

        # TODO: - save cookies so that you don't need to login each time
        self.driver.implicitly_wait(1)
        logger.info("Login successful!")

    def run(self, from_page=0, until_page=None) -> None:
        """
        Iterate through LinkedIn pages of applied jobs.
        Scrap job application information such as url, company name, etc.
        Export/save the contents to an archive of your choice (e.g. csv, google_spreadsheets). 
        """
        self._login()

        logger.info("Parsing URLS of applied jobs ...")
        next_page_available = True
        page = from_page
        while next_page_available:
            # pylint: disable = line-too-long
            self._go_to_page(page_number=page)
            job_applications_of_current_page = self._parse_job_applications_of_current_page()

            was_export_interrupted = self._to_csv(job_applications_of_current_page)
            if was_export_interrupted:
                break

            final_page_reached = not job_applications_of_current_page
            if final_page_reached:
                logger.info("Final page reached! Parsing no further ...")
                next_page_available = False
            else:
                if until_page and until_page == page:
                    break
                page += 10  # go to next page ...

        logger.info("Job application parsing was complete.")

    def _go_to_page(self, page_number: int):
        """
        Move webdriver to specific page of applied jobs.
        
        The page number is actually the N-th most recent job application
        the user has done.
        Specifying page_number = 5, is like saying skip the first 5 job applications
        and get the following 10 most recent (i.e. from 6th to 10th).
        Since LinkedIn fetches job applications in batches of 10, specifying
        page_number as decades (i.e. 0, 10, 20, 30, ...) is like specifying a page number. 
        """
        logger.info("Going to page %s ...", page_number)
        # pylint: disable = line-too-long
        applied_jobs_url = f"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start={page_number}"
        self.driver.get(applied_jobs_url)
        self.driver.implicitly_wait(1)
        sleep(1 + random() * 4)

    def _parse_job_applications_of_current_page(self) -> Set[JobApplication]:
        """
        Parse the job application contents of a specific page. 
        Create JobApplication objects containing that information and accumulate
        them in a set to avoid duplicates.
        """
        _tag_of_boxes_containing_jobs_of_current_page = {
            "div": "entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light"
        }
        html_doc = self.driver.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        div_boxes = soup.find_all(_tag_of_boxes_containing_jobs_of_current_page)

        job_applications_set = set()  #This is the output
        for div_box in div_boxes:
            job_info = {
                "url": self._parse_job_post_url(div_box),
                "company_name": self._parse_company_name(div_box),
                "linkedin_status": self._parse_linkedin_status(div_box),
                "title": self._parse_title(div_box),
                "location": self._parse_location(div_box)
                }
            job_application = JobApplication(**job_info)
            if job_application.all_basic_fields_valid():
                job_applications_set.add(
                    job_application
                )
        return job_applications_set

    def _parse_job_post_url(self, div_box) -> str:
        """
        Given an html div_box, parse the job post url.
        """
        _html_box_containing_job_url = {"a": "app-aware-link "}
        job_post_url_found = div_box.find_all(_html_box_containing_job_url)
        job_post_url = job_post_url_found[0].attrs['href'] if job_post_url_found else ""
        url_pattern = re.compile(r"(https:\/\/www\.linkedin\.com\/jobs\/view\/\d+)(\/.+)")
        regex_result = url_pattern.search(job_post_url)
        job_post_final_url = regex_result.group(1) if regex_result else ""
        return job_post_final_url

    def _parse_company_name(self, div_box) -> str:
        """
        Given an html div_box, parse the job post company name.
        """
        company_found = div_box.find_all(
            'div', class_="entity-result__primary-subtitle t-14 t-black t-normal"
        )
        if company_found:
            company_name = self._extract_text_from_div(
                str(company_found[0]))
            return company_name
        return ""

    def _parse_linkedin_status(self, div_box) -> str:
        """
        Given an html div_box, parse the linkedin status.

        examples of linkein statuses: 
        - Application viewed 3d ago
        - Applied 5d ago
        - Applied 1w ago
        - Applied 1mo ago
        - Application viewed 2yr ago
        - Applied 3yr ago
        """
        linkedin_status_found = div_box.find_all(
            'span',
            class_="entity-result__simple-insight-text entity-result__simple-insight-text--small"
        )
        if linkedin_status_found:
            linkedin_status = self._extract_text_from_div(
                str(linkedin_status_found[0]))
            return linkedin_status
        return ""

    def _parse_title(self, div_box) -> str:
        """
        Given an html div_box, parse the job title.

        e.g. "Software Engineer"
        """
        _html_box_containing_job_url = {"a": "app-aware-link "}
        job_title_found = div_box.find_all(_html_box_containing_job_url)
        res = ""
        for elem in job_title_found:
            res = self._extract_text_from_div(str(elem))
        return res

    def _parse_location(self, div_box) -> str:
        """
        Given an html div_box, parse the job post company name.
        """
        subdivs = div_box.find_all(
            {'div': "entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light"}
        )
        location_and_policy_pattern = re.compile(r"\b\w+ \(([Hh]ybrid|[Rr]emote|[Oo]n-?site)\)")

        for subdiv in subdivs:
            locations = subdiv.find_all(text=location_and_policy_pattern);
            if len(locations) == 1:
                return locations[0]
        return ""

    def _extract_text_from_div(self, div: str) -> str:
        """
        Extracts the text from an html div.
        
        ---
        e.g.
        
        Input:
        '<div class="entity-result__primary-subtitle t-14 t-black t-normal">
        <!-- -->XYZ.Pub<!-- -->
        </div>'
        
        Output:
        'XYZ.Pub'
        """
        # Each parenthesi is a regex group
        text_inbetween_pattern = re.compile(r'(<!-- -->)(.+)(<!-- -->)')
        regex_result = text_inbetween_pattern.search(div)

        # Returning the second group, therefore the text that matches the middle parenthesi above
        return regex_result.group(2) if regex_result else ""

    def _to_csv(self, job_applications_of_current_page: Set[JobApplication]) -> int:
        """
        Export current page contents to csv.
        """
        input_not_empty = job_applications_of_current_page
        if input_not_empty:
            was_export_interrupted = CSVExporter.export(
                list(job_applications_of_current_page)
                )
            return was_export_interrupted
        return 1  # export was interrupted due to empty input
