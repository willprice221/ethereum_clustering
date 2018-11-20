import requests
from bs4 import BeautifulSoup

def find_tag(address):
    url = 'https://etherscan.io/address/{}'.format(address)
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('font', title='NameTag')
    if type(tag) == type(None):
        return 'unknown'
    return tag.decode_contents()

def find_cat(address):
    url = 'https://etherscan.io/address/{}'.format(address)
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find('a', href="/accounts?l=Exchange")
    if type(tag) == type(None):
        return 'unknown'
    return tag.decode_contents()