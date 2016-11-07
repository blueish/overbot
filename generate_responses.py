import requests
import bs4
from bs4 import BeautifulSoup
import pymongo

# CONSTANTS
BASE_URL = 'http://overwatch.gamepedia.com'

def get_hero_response_links():
    r = requests.get("http://overwatch.gamepedia.com/Category:Quotations")
    soup = BeautifulSoup(r.text, 'html.parser')
    # get all the links with Quotes in it
    unparsed_links = []
    for link in soup.find_all('a'):
        if 'Quotes' in str(link.get('href')):
            # We cast it to a string to make it easier for us later
            unparsed_links.append(str(link.get('href')))
    return unparsed_links

def main():
    url_stubs = get_hero_response_links()
    # Map the urls to the base, and write them each to their own file
    urls = map(lambda u: BASE_URL + u, url_stubs)
    generate_all_responses(urls)

def generate_all_responses(urls):
    responses = {}
    for link in urls:
        # generate soup
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')

        # parse soup for audio files
        # since we need the hero name, the line, and the link
        # this is a dict of strings that leads to a tuple of (character, href)

        # we need to restrict it to finding the table:
        table = soup.find('table')
        # since it's the only table on page, just get it at 0th index
        for element in table.children:
            # we need to get the child tds that have the lines, which are the last two:
            if type(element) == bs4.element.Tag:
                for tr in element.children:
                    if type(tr) == bs4.element.Tag:
                        if tr.find_all('audio'):
                            src = tr.find('audio').get('src')
                            # insert into the array
                            # key is lastNode, character is parsed out from the link,
                            # and the href is simply the src
                            name = src.split('/')[-1].split('-')[0]
                            name = name.replace('_', '').replace('\n', '')
                            charRef = (name, src)
                            responses[lastNode] = charRef
                        else:
                            # we keep track of the last one, next one might be audio
                            lastNode = tr.text.replace('\n', '')

if __name__ == '__main__':
    main()
