from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup 
from logger import logger
import re
from time import sleep
from random import random

class LinkedInParser:
    _html_boxes_containing_current_jobs = {
        "div": "entity-result__content entity-result__divider pt3 pb3 t-12 t-black--light"
        }

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
    
    def __delattr__(self) -> None:
        self.driver.close()

    def login(self) -> None:
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
        sleep(1 + random() * 2)

        # Fill password
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "session_password"))
        )
        self.driver.find_element(By.ID, "session_password").send_keys(self.password)
        self.driver.implicitly_wait(4)
        sleep(1 + random() * 2)

        
        # Click sign-in button 
        self.driver.find_element(By.CSS_SELECTOR, "button.sign-in-form__submit-button").click()
        
        # TODO - save cookies so that you don't need to login each time
        self.driver.implicitly_wait(1)
        logger.info("Login successful!")
        
    def get_job_urls(self):
        """
        Iterate through all the pages of applied jobs and 
        return a set that contains tuples of brief info about them.
        Useful while running the program for the first time.

        TODO: parse job title/role
        TODO: Make an object JobApplication. 
         This job application will have a Brief and a Detailed version.
        """
        logger.info("Parsing URLS of applied jobs ...")
        
        next_page_available = True
        job_application_briefs = set()
        
        page = 0
        while next_page_available:
            logger.info(f"Scanning page {page} ...")
            applied_jobs_url = f"https://www.linkedin.com/my-items/saved-jobs/?cardType=APPLIED&start={page}"            
            self.driver.get(applied_jobs_url)
            self.driver.implicitly_wait(1)  # TODO: add random number to not get detected
            sleep(2 + random() * 2)
            
            html_doc = self.driver.page_source
            soup = BeautifulSoup(html_doc, 'html.parser')
            div_boxes = soup.find_all(self._html_boxes_containing_current_jobs)
            job_application_briefs_of_current_page = set()
            for div_box in div_boxes: 
                job_post_url = self._parse_job_post_url(div_box)
                company_name = self._parse_company_name(div_box)
                linkedin_status = self._parse_linkedin_status(div_box)
                if job_post_url and company_name and linkedin_status:
                    job_application_briefs_of_current_page.add(
                            (
                            job_post_url,
                            company_name,
                            linkedin_status
                            )  
                        )
            final_page_reached = not job_application_briefs_of_current_page
            if final_page_reached:
                logger.info(f"Final page reached! Parsing no further ...")
                next_page_available = False
            else:  
                job_application_briefs.update(job_application_briefs_of_current_page)
                page += 10

        logger.info("Number of jobs parsed: {len(job_application_briefs)}")
        return job_application_briefs

    def _parse_job_post_url(self, div_box) -> str:
        _html_box_containing_job_url = {"a": "app-aware-link "}
        job_post_url_found = div_box.find_all(_html_box_containing_job_url)
        if job_post_url_found:
            job_post_url = job_post_url_found[0].attrs['href']
            job_post_url_is_valid = "flagship3_job_home_appliedjobs" in job_post_url
            return job_post_url if job_post_url_is_valid else ""
        else:
            ""

    def _parse_company_name(self, div_box) -> str:
        company_found = div_box.find_all(
            'div', class_="entity-result__primary-subtitle t-14 t-black t-normal"
            )
        if company_found:
            company_name = self._extract_text_from_div(company_found[0].__str__())
            return company_name
        else:
            return ""
    
    def _parse_linkedin_status(self, div_box) -> str:
        linkedin_status_found = div_box.find_all(
            'span', 
            class_="entity-result__simple-insight-text entity-result__simple-insight-text--small"
            )
        if linkedin_status_found:
            linkedin_status = self._extract_text_from_div(linkedin_status_found[0].__str__())
            return linkedin_status
        else:
            return ""

    def _extract_text_from_div(self, div: str) -> str:
        """
        Extracts the text from an html div.

        e.g.

        """
        text_inbetween_pattern = re.compile(r'(<!-- -->)(.+)(<!-- -->)')
        regex_result = text_inbetween_pattern.search(div)
        
        return regex_result.group(2) if regex_result else ""
