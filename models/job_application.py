"""
Structures to describe job application data.
"""

class JobApplication:
    """
    Objects of this class contain information about the job application.  
    """

    def __init__(self,
                 url: str,
                 company_name: str,
                 linkedin_status: str,
                 title: str) -> None:
        self.url = url
        self.company_name = company_name
        self.linkedin_status = linkedin_status
        self.title = title

    def to_dict(self) -> dict:
        """
        Return the fields of the JobApplication in a dictionary.
        Useful when exporting the data to files.
        """
        return vars(self)

    def __str__(self) -> str:
        pattern = "{}, {} - {}"
        return pattern.format(
            self.title,
            self.company_name,
            self.linkedin_status
        )

    def all_basic_fields_valid(self) -> bool:
        """
        Check if all basic fields are valid. 
        
        For example the string "ayayaya" is not a valid url. 
        An empty company name is not considered valid. 
        Same with the linkedin status.
        """
        all_valid = self._is_valid_url() and \
            self._is_valid_company_name() and \
            self._is_valid_linkedin_status()
        return all_valid

    def _is_valid_url(self) -> bool:
        return self.url != ''

    def _is_valid_company_name(self) -> bool:
        is_empty = bool(self.company_name)
        return is_empty

    def _is_valid_linkedin_status(self) -> bool:
        is_empty = bool(self.linkedin_status)
        return is_empty

    def __hash__(self) -> int:
        return hash(self.url)

    def __eq__(self, other):
        return isinstance(other, JobApplication) and self.url == other.url
