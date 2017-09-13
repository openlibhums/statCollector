import re

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
from urllib.parse import urlparse
import shared.shared_funcs


def import_oai(soup):
    """ Initiate an OAI import on a Ubiquity Press journal.
        :param soup: the BeautifulSoup object of the OAI feed
        
        :return: None
        """
    identifiers = soup.findAll('identifier')

    ret = []

    for identifier in identifiers:
        # rewrite the phrase /jms in Ubiquity Press OAI feeds to get version with
        # full and proper email metadata
        identifier.contents[0] = identifier.contents[0].replace('/jms', '')
        if identifier.contents[0].startswith('http'):
            #print('Parsing {0}'.format(identifier.contents[0]))

            res = import_article(identifier.contents[0])

            #if res > 0:
            ret.append(res)

    return ret


def import_article(url):
    """ Import a Ubiquity Press article.

    :param url: the URL of the article to import
    :return: None
    """

    # retrieve the remote page and establish if it has a DOI
    soup_object = shared.shared_funcs.fetch_page(url)

    pattern = re.compile(r'<div class="stat-number">(\d+)</div>')
    xml = str(soup_object)
    match = re.findall(pattern, xml)

    if len(match) > 0:
        #print(match[0])
        return int(match[0])
    else:
        # it's low. Assume zero.
        return 0



def parse_OAI(url, resume=None):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    if resume:
        verb = '?verb=ListRecords&resumptionToken={0}'.format(resume)
    else:
        verb = '?verb=ListRecords&metadataPrefix=oai_dc'

    print("Handling OAI URL: " + url + verb)
    journal_type = "UP"

    # note: we're not caching OAI pages as they update regularly
    page = requests.get(url + verb, verify=False)
    soup = BeautifulSoup(page.text, "lxml-xml")

    ret = []

    if journal_type == "UP":
        #print("Detected journal type as UP. Processing.")
        ret = import_oai(soup)
    else:
        #print("Journal type currently unsupported")
        return

    # see if there is a resumption token
    resume = soup.find('resumptionToken')

    if resume:
        resume = resume.getText()

    if resume and resume != '':
        #print('Executing resumeToken')
        for it in parse_OAI(url, resume=resume):
            ret.append(it)

    return ret
