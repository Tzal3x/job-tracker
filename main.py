"""
The main script. All starts from here.
"""
from helpers.credential_loaders import load_credentials
from parsers.linkedin_parser import LinkedInParser


def main():
    """
    The main flow of the program is included here.
    """
    linkedin_parser = LinkedInParser(
        credentials=load_credentials(r".env.yaml"),  #TODO: create OS env vars instead
        headless=False
    )
    linkedin_parser.login()
    linkedin_parser.get_job_urls()


if __name__ == "__main__":
    main()
