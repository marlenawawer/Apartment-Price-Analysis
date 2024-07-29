from bs4 import BeautifulSoup
from requests import get
import sys
import sqlite3
from sys import argv

def parse_link(link):
    if link[0] == "/":
        link = 'https://www.olx.pl' + link
    return link

def parse_page():
    r = get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    for offer in soup.find_all('div', class_="css-1apmciz"):
        link = parse_link(offer.find('a')['href'])
        if 'olx' in f'{link}':
            title = offer.find('h6', class_="css-1wxaaza").get_text()
            prise = float(offer.find('p', class_="css-13afqrm").get_text().split('zł')[0].replace(" ", "").replace(',', '.'))
            location = offer.find('p', class_="css-1mwdrlh").get_text().split(' ')[1]
            area = float(offer.find('span', class_="css-643j0o").get_text().split(' ')[0].replace(',', '.'))

            r=get(f'{link}')
            soup = BeautifulSoup(r.content, 'html.parser')
            
            detail = soup.find_all('p')

            for var_name, index, split_char, split_index in variables:
                try:
                    if len(detail) > split_index:
                        results[var_name] = detail[index].get_text().split(split_char)[split_index]
                    else:
                        results[var_name] = None
                except:
                    results[var_name] = None
                    
            level = results['level']
            market = results['market']
            building = results['building']
            num_of_rooms = results['num_of_rooms']

            c.execute('''INSERT INTO apartments VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (title, prise, location, area, level, market, building, num_of_rooms))
    conn.commit()


sys.stdout.reconfigure(encoding='utf-8')
conn = sqlite3.connect('database.db')
c = conn.cursor()
i=1
url = f"https://www.olx.pl/nieruchomosci/mieszkania/sprzedaz/lodz/?page={i}"
variables = [
    ('level', 2, ': ', 1),
    ('market', 4, ' ', 1),
    ('building', 5, ': ', 1),
    ('num_of_rooms', 7, ': ', 1)
]
results = {}

if len(argv)>1 and argv[1] == 'database':
    c.execute('''CREATE TABLE apartments
          (title text, prise number, location text, area number, level text, market text, building text, num_of_rooms text)''')

for i in range(1,25):
     parse_page()


conn.close()

