from bs4 import BeautifulSoup
from requests import get
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = "https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/lodz/"

r = get(url)
soup = BeautifulSoup(r.content, 'html.parser')

def parse_link(link):
    if link[0] == "/":
        link = 'https://www.olx.pl' + link
    return link



for offer in soup.find_all('div', class_="css-1apmciz"):
    link = parse_link(offer.find('a')['href'])
    title = offer.find('h6', class_="css-1wxaaza").get_text()
    prise = float(offer.find('p', class_="css-13afqrm").get_text().split('zł')[0].replace(" ", "").replace(',', '.'))
    location = offer.find('p', class_="css-1mwdrlh").get_text().split(' ')[1]
    area = float(offer.find('span', class_="css-643j0o").get_text().split(' ')[0].replace(',', '.'))

    r=get(f'{link}')
    soup = BeautifulSoup(r.content, 'html.parser')
    
    if 'olx' in f'{link}':
        detail = soup.find_all('p')
        level = detail[2].get_text().split(' ')[1]
        market = detail[4].get_text().split(' ')[1]
        development = detail[5].get_text().split(': ')[1]
        num_of_rooms = detail[7].get_text().split(': ')
        print(num_of_rooms)


