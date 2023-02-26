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
        print(f"Enter your credentials to login to {args.from_platform} ...")
        credentials["username"] = args.username
        credentials["password"] = getpass()
    elif args.credentials_file:
        credentials = load_credentials(args.credentials_file)[args.from_platform]
    else:
        raise ImportError("No credentials found!")
    linkedin_parser = LinkedInParser(
        credentials=credentials,
    )

    linkedin_parser.run()


if __name__ == "__main__":
    main()
