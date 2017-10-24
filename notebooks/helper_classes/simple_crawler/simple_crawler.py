import os, sys
import requests
import logging
import json
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
import io
import os.path
from multiprocessing.dummy import Pool as ThreadPool 
import requests
from urllib.parse import urljoin, urlunsplit, urlparse
import hashlib
import copy
from lxml.html.clean import clean_html
from itertools import tee, islice
from lxml import etree
from lxml import html as lxml_html
from io import StringIO
import re


class Crawler():

    def __init__(self, threads):
        self.pool = ThreadPool(threads) 
        pass

    def get_websites(self, urls):
        results = self.pool.map(self.get_url, urls)
        return results

    # called by each thread
    def get_url(self, url):
        urlo = urlparse(url)
        netloc = urlo.netloc
        fingerprint = self.get_fingerprint(url)
        filename = "./crawlcache/{}/{}".format(netloc, fingerprint)
        crawl = True
        if os.path.isfile(filename):
            #logging.info("File Exists {}".format(filename))
            with open(filename) as data_file:
                try:
                    data = json.load(data_file)
                    crawl = False
                except:
                    crawl = True
                    pass
        if crawl is True:
            if not os.path.exists(os.path.dirname(filename)):
                try:
                    os.makedirs(os.path.dirname(filename))
                except:
                    pass
            with open(filename, 'w') as outfile:
                try:
                    response = requests.get(url)
                    content = ''
                    try:
                        lxml = self.get_lxml_from_html(response.text)
                        content = self.get_text_from_lxml(lxml)
                        res = lxml.xpath('//title/text()')
                        if len(res) > 0:
                            title = res[0]
                        else:
                            title = ''
                    except:
                        pass
                    data = {'url': url,
                            'title': title,
                            'response_content': content,
                            'response_status': response.status_code} 
                except:
                    data = {'url': url, 
                            'title': '',
                            'response_content': '',
                            'response_status': 0}
                    pass
                json.dump(data, outfile)
        return data
    
    def get_fingerprint(self, string):
        hash_object = hashlib.md5(string.encode("utf-8"))
        return hash_object.hexdigest()
    def get_lxml_from_html(self, html):
        if isinstance(html, bytes):
            html = html.decode("utf-8")
        parser = etree.HTMLParser()
        lxml_tree = etree.parse(StringIO(html), parser)
        return lxml_tree

    def get_text_from_lxml(self, lxml_tree):
        try:
            lxml_tree_content = copy.deepcopy(lxml_tree)
            etree.strip_elements(lxml_tree_content, "style", "script", "head", "iframe", etree.Comment)
            ret_document = self.remove_whitespaces(lxml_html.tostring(lxml_tree_content, method="text", encoding='unicode'))
        except Exception as e:
            logging.error("problems getting content from lxml: {}".format(e))
            ret_document = ''

        return ret_document
    
    def remove_whitespaces(self, content):
        Newlines = re.compile(r'[\r\n]\s+')
        return Newlines.sub('\n', content)
    
    
    