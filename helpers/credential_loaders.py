"""
Credential loaders  
"""
import yaml


def load_credentials(path) -> dict:
    """
    Loads the credentials for logins.
    """
    with open(path, "r", encoding="utf-8") as stream:
        try:
            output = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(f"Unable to parse credentials yaml file! {exc}")
            raise exc
    return output
