import hashlib

import requests
import os

from urllib3.exceptions import InsecureRequestWarning


class Cache():
    base_dir = "/home/martin/Documents/Programming/statCollector/cacheEntries"

    def get(self, url):
        filename = os.path.join(self.base_dir, hashlib.sha512(url.encode('utf-16')).hexdigest())

        if not os.path.exists(filename):
            return None
        else:
            with open(filename, 'r') as on_disk:
                return on_disk.read()

    def fetch(self, url):

        cached = self.get(url=url)

        if cached:
            #print("[CACHE] Using cached version of {0}".format(url))

            return cached
        else:
            #print("[CACHE] Fetching remote version of {0}".format(url))

            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/39.0.2171.95 Safari/537.36'}

            # disable SSL checking
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

            fetched = requests.get(url, headers=headers, stream=True, verify=False)

            resp = bytes()

            for chunk in fetched.iter_content(chunk_size=512 * 1024):
                resp += chunk

            # set the filename to a unique UUID4 identifier with the passed file extension
            filename = hashlib.sha512(url.encode('utf-16')).hexdigest()

            with open(os.path.join(self.base_dir, filename), 'wb') as f:
                f.write(resp)

            return resp
