from bs4            import BeautifulSoup
from csv            import writer
from requests       import get
from yahoo_finance  import Share

'''
Scrapes current SP500 list from Wikipedia.

Stores list as 'sp_list.txt'
'''
if __name__ == '__main__':
    response = get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup     = BeautifulSoup(response.text, "html.parser")
    table    = soup.find('table', {'class': 'wikitable sortable'})

    sp_symbols = []

    for row in table.findAll('tr'):
        col = row.findAll('td')
        if col:
            symbol  = col[0].string.replace('.','') 
            name    = col[1].string
            sector  = col[3].string

            sp_symbols.append((symbol, name, sector))

    with open('sp-list.txt', 'w') as csv_file:

        w = writer(csv_file)

        for security in sorted(sp_symbols):
            w.writerow(security)
