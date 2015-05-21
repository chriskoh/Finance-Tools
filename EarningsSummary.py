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

def get_detail(ticker):     # Get NASDAQ information based on array of tickers

    tickers = []
    titles = []
    values = []

    for var in ticker:
        set_url     = 'http://www.nasdaq.com/symbol/'+var
        resp        = requests.get(set_url)
        resp_data   = resp.text
        data        = BeautifulSoup(resp_data)
        div         = data.find('div', attrs={'class':'genTable thin'})
        trs         = div.find_all('tr')

        for tr in trs:
            tds = tr.find_all('td')
            try:   # If title has link
                a = tr.find('a', attrs={'class':'tt show-link'})
                for child in a.children:
                    if isinstance(child, NavigableString):
                        title = str(child).strip()
                        if title != '':
                            linktitle = title
                            titlecheck = title
                        else:
                            title = title
                for child in tds[1].children:

                    if titlecheck == 'Share Volume': #Find share volume label
                        label = tds[1].find('label')
                        for kids in label.children:
                            if isinstance(kids, NavigableString):
                                linkvalue = str(kids).strip()
                    elif titlecheck == "Today's High /Low":
                        labels = tds[1].find_all('label')
                        linkvalue = labels[0].getText() + ' / ' + labels[1].getText()
                    else:
                        if isinstance(child,NavigableString):
                            linkvalue = child.strip()
                tickers.append(str(var))
                titles.append(linktitle)
                values.append(linkvalue)

            except: # If title doesnt have link
                for child in tds[0].children:
                    if isinstance(child, NavigableString):
                        title = str(child).strip()
                for child in tds[1].children:
                    if isinstance(child, NavigableString):
                        value = child.strip()
                tickers.append(str(var))
                titles.append(title)
                values.append(value)

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
    det_tickers, det_titles, det_values = get_detail(tickers)
    print('Result: The following information has been pulled from NASDAQ')

    for earn_tick, earn_time in zip(tickers, time):
        print(earn_tick + ' --- ' + earn_time)
        for detail_tick, detail_title, detail_value in zip(det_tickers, det_titles, det_values):
            if(earn_tick == detail_tick):
                print(detail_title + ': ' + detail_value)
        print('--------------------')


if __name__ == '__main__':
   main()       
