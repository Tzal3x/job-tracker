"""
Creates user-friendly command-line interface.
"""
import argparse


def get_command_line_arguments():
    """
    Create the interface and parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
                    prog = 'main.py',
                    description = "A program that tracks applications by "
                                  "scrapping your personal data from popular job hiring "
                                  "platforms and exports them to a file of your choice.",
                    epilog = 'Example: python main.py -p LinkedIn -c .env.yaml')
    parser.add_argument("-p", "--from_platform",
                        choices=('LinkedIn',),
                        help="The platform that is to be scrapped.",
                        default='LinkedIn')
    parser.add_argument("-e", "--export_type",
                        choices=('csv',),
                        default='csv',
                        help="The file type that the results will be saved on.")

    # Either login with username password by passing them in cmd
    # or parse the credentials through a YAML file:
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-u", "--username",
                        help="Username to login to the corresponding platform.")
    group.add_argument("-c", "--credentials_file",
                       help="The name of the YAML file that contains the credentials"
                       "to log in to the corresponding platform.",
                       type=str)

    return parser.parse_args()
