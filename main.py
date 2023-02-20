"""
The main script. All starts from here.
"""
from getpass import getpass

from helpers.credential_loaders import load_credentials
from helpers.argument_parser import get_command_line_arguments
from parsers.linkedin_parser import LinkedInParser


def main():
    """
    The main flow of the program is included here.
    """
    args = get_command_line_arguments()

    credentials = {}
    if args.username:
        credentials["username"] = args.username
        credentials["password"] = getpass()
    else:
        credentials = load_credentials(r".env.yaml")

    linkedin_parser = LinkedInParser(
        credentials=credentials,
        headless=True
    )

    linkedin_parser.run()


if __name__ == "__main__":
    main()
