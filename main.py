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

    linkedin_parser.run()


if __name__ == "__main__":
    main()
