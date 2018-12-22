import re
from urllib.parse import urlparse, urljoin
import requests
from parsel import Selector
from boltons.urlutils import find_all_links
from flask import request, redirect, url_for


def links(res: requests.models.Response, search: str=None, pattern: str=None) -> list:
    """Get the links of the page.

    Args:
        res (requests.models.Response): The response of the page.
        search (str, optional): Defaults to None. Search the links you want.
        pattern (str, optional): Defaults to None. Search the links use a regex pattern.

    Returns:
        list: The links you want.
    """
    absolute_hrefs = [link.to_text() for link in find_all_links(res.text)]
    relative_hrefs = Selector(text=res.text).css('a::attr(href)').extract()
    relative_hrefs = [rehref for rehref in relative_hrefs if not rehref.startswith('http')]
    domain = f'https://{urlparse(res.url).netloc}'
    hrefs = [*absolute_hrefs, *[urljoin(domain, rehref) for rehref in relative_hrefs]]
    if search:
        hrefs = [href for href in hrefs if search in href]
    if pattern:
        hrefs = [href for href in hrefs if re.findall(pattern, href)]
    return list(set(hrefs))
