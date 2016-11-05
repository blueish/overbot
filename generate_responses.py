import requests
from bs4 import BeautifulSoup

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
    generate_pickles(urls)

def generate_pickles(urls):
    for link in urls:
        # generate soup
        r = requests.get(link)
        soup = BeautifulSoup(r.text, 'html.parser')

        # parse soup for audio files
        responses = []
        for element in soup.find_all('audio'):
            responses.append(element.get('src'))



if __name__ == '__main__':
    main()
