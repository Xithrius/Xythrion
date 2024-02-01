import re
from enum import Enum
from urllib.parse import urlparse

VALID_XPATH_PATTERN = re.compile(r"(/(?:[\w-]+|[*])(?:\[\d+\])?)+")


class DestinationType(Enum):
    XPATH = 1
    URL = 2


def validate_destination(destination: str) -> DestinationType:
    if re.fullmatch(VALID_XPATH_PATTERN, destination):
        return DestinationType.XPATH

    parsed_url = urlparse(destination)
    if parsed_url.scheme and parsed_url.netloc:
        return DestinationType.URL

    raise ValueError("Input string is neither a valid XPath nor a valid URL.")
