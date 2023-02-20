"""
Creates user-friendly command-line interface.
"""
import argparse


def get_command_line_arguments():
    """
    Create the interface and parse the command line arguments.
    """
    parser = argparse.ArgumentParser(
                    prog = 'Job Tracker',
                    description = "A program that tracks applications by "
                                  "scrapping your personal data from popular job hiring "
                                  "platforms and exports them to a file of your choice.",
                    epilog = 'Example: TODO') # TODO example
    parser.add_argument("--from_platform",
                        choices=('LinkedIn',), 
                        help="The platform that is to be scrapped.",
                        required=True)
    parser.add_argument("--username",
                        help="Username to login to the corresponding platform.",
                        required=True)
    parser.add_argument("--export_type",
                        choices=('csv',),
                        required=True,
                        help="The file type that the results will be saved on.")
    args = parser.parse_args()
    return args
