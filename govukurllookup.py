# coding: utf-8

import re, requests
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup

class govukurls(object):
    """
    Clean and handle GOV.UK urls.
    """

    def __init__(self, urls):
        """
        Check that x is a pd series.
        """

        self.urls = urls
        assert isinstance(self.urls, pd.core.series.Series)
        
        self.dedupurls = self.urls.drop_duplicates().dropna()


    def lookup(self):
        """
        Look up urls on GOV.UK content API
        """

        self.urldicts = self.dedupurls.apply(api_lookup)

        return self.urldicts

def api_lookup(x):
    
    '''
    Simple function to lookup a url on the GOV.UK content API
    Takes as an input the dictionary output by clean_url()
    '''

    url = "https://www.gov.uk/api/content" + x
    
    try:
       
        # read JSON result into r
        r = requests.get(url)
        results = r.json()

    except Exception as e:
        print(e)
        print('Error looking up ' + url)
        print('Returning url dict without api lookup')
    
    return results

def extract_text(self, list_of_dict):
    """loop through list and for each dictionary extract the url and all contnet items. Concatenate content items and clean. Give back a url, text list"""
    urltext = []
    for page in list_of_dict:
        page_path = json_dict['base_path']
        page_title = json_dict['title']
        page_desc = json_dict['description']
        page_body = json_dict['details']['Body'] 

        soup = BeautifulSoup(page_body,'html.parser') #parse html using bs4
            # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
            # extract all text from html 
        txt = " ".join(page_title, page_desc, soup.getText())
            # format string by replacing tabs, new lines and commas
        txt = txt.strip().replace("\t", " ").replace("\r", " ").replace('\n', ' ').replace(',', ' ')
            # remove remaining excess whitespace
        txt = " ".join(txt.encode('utf-8').split())
        urltext.append(page_path,txt)
    
    return(urltext)

def import_urls(self, fname):
    """#import the csv as a dataframe but extract the first column as a panda series so it is typed correctly for govukurls class"""
    self.trunc_urls = pd.read_csv(fname).iloc[:,0] 

def wtf(oname):
"""write data structure to (a .csv) file."""
    f = open(oname,'w')
    f.write('url,text\n')
    for row in urltext:
        f.write(row.url+','+row.text+'\n')
    f.close()
    return(0)




