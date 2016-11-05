import requests
from bs4 import BeautifulSoup

def get_hero_response_links():
    r = requests.get("http://overwatch.gamepedia.com/Category:Quotations")
    soup = BeautifulSoup(r.text, 'html.parser')
    # get all the links with Quotes in it
    unparsed_links = []
    for link in soup.find_all('a'):
        if 'Quotes' in str(link.get('href')):
            unparsed_links.append(link.get('href'))
    # now we return that array
    return unparsed_links

def main():
    print(get_hero_response_links())

if __name__ == '__main__':
    main()
