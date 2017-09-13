from urllib.parse import urlparse
from uuid import uuid4

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning

from shared.cache import Cache

cache = Cache()


def get_soup(soup_object, field_name, default=None):
    """ Parses a soup object and returns field_name if found, otherwise default

    :param soup_object: the BeautifulSoup object to parse
    :param field_name: the name of the field to look for
    :param default: the default to return if it isn't found
    :return: a default value to return if the soup_object is None
    """
    if soup_object:
        return soup_object.get(field_name, None)
    else:
        return default


def parse_url(url):
    """ Parses a URL into a well-formed and navigable format

    :param url: the URL to parse
    :return: the formatted URL
    """
    return '{uri.scheme}://{uri.netloc}/'.format(uri=urlparse(url))


def fetch_page(url):
    """ Fetches a remote page and returns a BeautifulSoup object

    :param url: the URL to fetch
    :return: a BeautifulSoup object
    """
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    resp = cache.fetch(url=url)
    return BeautifulSoup(resp, 'lxml-xml')


def get_pdf_url(soup_object):
    """
    Returns the value of the meta tag where the name attribute is citation_pdf_url from a BeautifulSoup object of a
    page.

    :param soup_object: a BeautifulSoup object of a page
    :return: a string of the PDF URL
    """
    pdf = get_soup(soup_object.find('meta', attrs={'name': 'citation_pdf_url'}), 'content')

    if pdf:
        pdf = pdf.replace('article/view/', 'article/viewFile/')

    return pdf


