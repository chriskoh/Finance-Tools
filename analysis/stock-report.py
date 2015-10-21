#!/usr/bin/env python2

import re
import time
import requests
import os
from bs4 import BeautifulSoup, NavigableString

def scrape(website): # Get web page data
    set_url     = website
    cal_resp    = requests.get(set_url)
    cal_data    = cal_resp.text
    data        = BeautifulSoup(cal_data)

    return data


def get_data(parsed_html, returntype):
    soup    = parsed_html
    values  = []

    casts   = soup.find_all('a', attrs={'class':'cast'})
    for cast in casts:
        childnum = 0
        for span in cast.find_all('span'):
            for child in span.children:
                if isinstance(child, NavigableString):
                    if returntype == 'tickers':
                        if childnum == 0:
                            values.append(str(child).strip())
                    elif returntype == 'time':
                        if childnum == 2:
                            values.append(str(child).strip())
                    childnum = childnum+1

    return values

def stock_report(ticker):
    tickers = []
    titles = []
    values = []

    for var in ticker:  #loop for all tickers
        set_url     = 'http://www.nasdaq.com/symbol/'+var+'/stock-report'
        resp        = requests.get(set_url)
        resp_data   = resp.text
        data        = BeautifulSoup(resp_data)
        div         = data.find('div', attrs={'class':'genTable'})
        trs         = div.find_all('tr')
 
#        print(var)       
        for tr in trs:  # for each row in all rows
            a = tr.find('a', attrs={'class':'tt show-link'})
            ths = tr.find_all('th')
            tds = tr.find_all('td')
            for child in a.children:    # for each <a> tag grab the text
                if isinstance(child, NavigableString):
                    title = str(child).strip()
                    if title != '': # if title is first child do not replace with an empty string
                        linktitle = title
                        titlecheck = title
                    else:
                        title = title
            if linktitle == 'Dividend Yield':   # grab information for divident yield (Speical case, odd format)
                for child in ths[1].children:
                    if isinstance(child, NavigableString):
                        DYlinktitle = str(child).strip()
                for kids in tds[1].children:
                    if isinstance(kids, NavigableString):
                        DYlinkvalue = kids.strip()
#                print(DYlinktitle)
#                print(DYlinkvalue)
                tickers.append(str(var))
                titles.append(DYlinktitle)
                values.append(DYlinkvalue)
            elif linktitle == 'P/E Ratio':      # grab information for P/E Ratio (Special, case, odd format)
                for child in ths[1].children:
                    if isinstance(child, NavigableString):
                        PElinktitle = str(child).strip()
                for kids in tds[1].children:
                    if isinstance(kids, NavigableString):
                        PElinkvalue = kids.strip()
#                print(PElinktitle)
#                print(PElinkvalue)
                tickers.append(str(var))
                titles.append(PElinktitle)
                values.append(PElinkvalue)
            for kids in tds[0].children:
                if isinstance(kids, NavigableString):
                    linkvalue = kids.strip()
#            print(linktitle)
#            print(linkvalue)
            if linktitle == 'Exchange':
                pause = 1
            elif linktitle == '52 Week High':
                pause = 1
            else:
                tickers.append(str(var))
                titles.append(linktitle)
                values.append(linkvalue)

    return tickers, titles, values

def save_html(parsed_html): # Save HTML for easy viewing
    with open('html.txt', 'w') as text_file:
        text_file.write(str(parsed_html))

def main():
    os.system('clear')

    print('Program Start')
    print('Scraping: Earnings Calendar')
    data    = scrape('http://earningscast.com/calendar/daily')

    tickers = get_data(data, 'tickers')
    time    = get_data(data, 'time')
    print('Result: Found ' + str(len(tickers)) + ' companies on earnings calendar.')
    
    print('Scraping: NASDAQ for detail of ' + str(len(tickers)) + ' stocks.')
    det_tickers, det_titles, det_values = stock_report(tickers)
    print('Result: The following information has been pulled from NASDAQ')

    for earn_tick, earn_time in zip(tickers, time):
        print(earn_tick + ' --- ' + earn_time)
        for detail_tick, detail_title, detail_value in zip(det_tickers, det_titles, det_values):
            if(earn_tick == detail_tick):
                print(detail_title + ': ' + detail_value)
        print('--------------------')


if __name__ == '__main__':
   main()       
