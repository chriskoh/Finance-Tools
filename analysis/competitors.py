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

def comp(ticker):

    tickers     = []
    compname    = []
    lastsale    = []
    netchange   = []
    volume      = []
    highlow     = []
    highlow2    = []
    peratio     = []
    cap         = []

    for var in ticker:  #loop for all tickers
        set_url     = 'http://www.nasdaq.com/symbol/'+var+'/competitors'
        resp        = requests.get(set_url)
        resp_data   = resp.text
        data        = BeautifulSoup(resp_data)
        div         = data.find('div', attrs={'class':'genTable thin'})
        tbody       = div.find('tbody')
        trs         = tbody.find_all('tr')
        
        for tr in trs:
            tds = tr.find_all('td')
            counter = 0
            tickers.append(str(var))

            for td in tds:
                value = td.getText()
                value.strip()
                if counter == 0:
                    compname.append(value)
                elif counter == 1:
                    lastsale.append(value)
                elif counter == 2:
                    netchange.append(value)
                elif counter == 3:
                    volume.append(value)
                elif counter == 4:
                    highlow.append(value)
                elif counter == 5:
                    highlow2.append(value)
                elif counter == 6:
                    peratio.append(value)
                elif counter == 7:
                    cap.append(value)

                counter += 1

    return tickers, compname, lastsale, netchange, volume, highlow, highlow2, peratio, cap

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
    det_tick, det_name, det_lsale, det_change, det_volume, det_highlow, det_highlow2, det_per, det_cap = comp(tickers)

    print('Result: The following information has been pulled from NASDAQ')


if __name__ == '__main__':
   main()       
