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
        credentials=load_credentials(r".env.yaml"),
        headless=True
    )

    linkedin_parser.parse_all_applied_jobs(until_page=10)


if __name__ == "__main__":
    main()
