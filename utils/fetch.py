from argparse       import ArgumentParser
from csv            import reader, writer
from re             import search
from time           import strftime
from yahoo_finance  import Share


'''
Reads and "sp_list.txt" and returns a sorted list of SP 500 Companies in the form:

    [SYMBOL, NAME, SECTOR]
'''
def sp_symbols():
    with open('sp_list.txt') as f: return list(reader(f))


'''
Takes in a security symbol, ex: 'FDX'

Returns a dictionary of financial attributes.
'''
def symbol_data(symbol):
    yfd = None
    # Call until Yahoo answers
    while not yfd:
        try:
            yfd = Share(symbol)
        except:
            pass

    return yfd.data_set


'''
Takes in a dictionary of security financial data.

Converts every attribute to numeric representation and introduces some new attributes.

Returns a sorted list of financial attribute tuples, or an empty list if data missing.
'''
def clean_data(d, sector):
    exchanges   = {'NMS': 0, 'NYQ': 1}
    lets     = {'B': 10 ** 9, 'M': 10 ** 6, 'T': 10 ** 12}

    sectors = { 'Consumer Discretionary':0,
                'Consumer Staples':0,
                'Energy':0,
                'Financials':0,
                'Health Care':0,
                'Industrials':0,
                'Information Technology':0,
                'Materials':0,
                'Real Estate':0,
                'Telecommunication Services':0,
                'Utilities':0}

    sectors[sector] = 1

    dy = 'DividendYield'
    ec = 'EPSEstimateCurrentYear'
    en = 'EPSEstimateNextYear'
    op = 'Open'
    pb = 'PriceBook'
    pc = 'PreviousClose'
    pe = 'PriceEPSEstimateCurrentYear'
    pn = 'PriceEPSEstimateNextYear'
    pr = 'PERatio'
    #se = 'StockExchange'
    tp = 'OneyrTargetPrice'

    pa = ['PercentChangeFromFiftydayMovingAverage',
          'PercentChangeFromTwoHundreddayMovingAverage',
          'PercentChangeFromYearHigh',
          'PercentChangeFromYearLow' ]
    
    let_conv = lambda d,a: int(float(d[a][:-1]) * lets[d[a][-1]]) if search('[A-Z]',d[a]) else d[a] 
    per_conv = lambda d,a: float(d[a].strip('%')) / 100

    # Letter to Numerals Conversion
    for a in ['EBITDA', 'MarketCapitalization']: d[a] = let_conv(d,a)

    # Renaming Attributes
    d['EPS']                        = d.pop('EarningsShare')
    d['PercentChangeFromYearHigh']  = d.pop('PercebtChangeFromYearHigh')
    d['DaysVolume']                 = d.pop('Volume')
    d['.Symbol']                    = d.pop('symbol')
    d['.Name']                      = d.pop('Name')

    # Creating New Attributes
    
    dr = d['DaysRange'].split('-')
    d['DaysRange'] = (float(dr[1]) - float(dr[0])) / float(d[pc])

    d['EPSYearGrowthEstimate'] = (float(d[en]) / float(d['EPS'])) - 1 if d[en] else 0

    d['OneyrTargetChange']          = float(d[tp]) / float(d[pc]) - 1 if d[tp] else 0
    d['PercentChangeAfterHours']    = float(d[op]) / float(d[pc]) - 1 if d[op] else 0
    
    # Percent to Decimal Convertion
    for a in pa: d[a] = per_conv(d,a)

    # Numeric No Dividend Attribute
    d[dy] = d[dy] if d[dy] else 0

    # Binary Exchanges
    #d[se] = exchanges[d[se]] 

    # Remove Securities with common missing data
    if not all(d[a] for a in [pb, pe, pn, en, pr]): return []

    # Filter Attributes
    for a in [l.rstrip('\n') for l in open('attributes.txt') if '#' not in l]: del d[a]

    # Add Sector Dummy Variables
    if sector:
        for s in sectors.keys(): d['Sector-' + s] = sectors[s]

    # Energy Arbitrarily Chosen as Reference Category
    d.pop('Sector-Energy')

    return sorted(list(d.items()))


'''
Writes the cleaned current financial attributes of all SP 500 companies to {TODAY}.csv
'''
def write_current_data():
    with open('../data/' + strftime('%m-%d-%Y') + '.csv', 'w') as csv_file:

        form = lambda symdata, sector: list(zip(*clean_data(symdata, sector)))

        w = writer(csv_file)
        w.writerow(form(symbol_data('FDX'), 'Industrials')[0])

        for security in sp_symbols():
            print(security[0])
            row = form(symbol_data(security[0]), security[2])
            if row: w.writerow(row[1])


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-d', '--data', action='store_true', help='save current S&P data to {TODAY}.csv')
    parser.add_argument('-l', '--list', action='store_true', help='list S&P Companies with sectors')
    parser.add_argument('-s', '--sym', type=str, help='print all data for symbol "SYM"')
    parser.add_argument('-S', '--SYM', type=str, help='print filtered data for symbol "SYM"')
    args = parser.parse_args()

    if args.data: write_current_data()
    if args.list: print(*sp_symbols(), sep='\n')
    if args.sym : print(*sorted(symbol_data(args.sym).items()), sep='\n')
    if args.SYM : print(*clean_data(symbol_data(args.SYM), None), sep='\n')
