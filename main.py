from linkedin_parser import LinkedInParser
import yaml


def main():
    # TODO move creds to the yml file
    linkedin_parser = LinkedInParser(
        credentials=load_credentials(r".env.yaml"),  # TODO: create OS env vars instead
        headless=False
    )
    linkedin_parser.login()
    linkedin_parser.get_job_urls()


def load_credentials(path) -> dict:
    with open(path, "r") as stream:
        try:
            output = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Unable to parse credentials yaml file! {exc}")
            raise exc
    return output


if __name__ == "__main__":
    main()
