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

def analyst_rating(ticker):
    tickers = []
    date    = []
    firm    = []
    action  = []
    current = []
    pt      = []

    for var in ticker:  #loop for all tickers
        set_url     = 'http://www.benzinga.com/stock/'+var+'/ratings'
        resp        = requests.get(set_url)
        resp_data   = resp.text
        data        = BeautifulSoup(resp_data)
        table       = data.find('table', attrs={'class':'sortable stock-ratings-calendar stock-calendar-table-data sticky-enabled'})
        body        = table.find('tbody')
        trs         = body.find_all('tr')


        for tr in trs:
            tds = tr.find_all('td')
            detail = ''
            counter = 0
            tickers.append(str(var))
#            print(str(var))
            for td in tds:
                # return in table format
                value = td.getText()
                value.strip()
                if counter == 0:
                    date.append(str(value))
#                    print('0: date = ' + str(value))
                elif counter == 1:
                    firm.append(str(value))
#                    print('1: Research Firm = ' + str(value))
                elif counter == 2:
                    action.append(str(value))
#                    print('2: Action = ' + str(value))
                elif counter == 3:
                    current.append(str(value))
#                    print('3: Current = ' + str(value))
                elif counter == 4:
                    pt.append(str(value))
#                    print('4: PT = ' + str(value))

                #save detail as long string
                #detail += '(' + str(counter) + ') ' + str(value) + ' | '

                counter += 1
            #print(detail)
#        print('-----------------------')

    return tickers, date, firm, action, current, pt

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
    det_tick, det_date, det_firm, det_action, det_current, det_pt = analyst_rating(tickers)
    print('Result: The following information has been pulled from NASDAQ')

    for earn_tick, earn_time in zip(tickers, time):
        print(earn_tick + ' --- ' + earn_time)
        print('Date | Research Firm | Action | Current | PT')
        for detail_tick, detail_date, detail_firm, detail_action, detail_current, detail_pt in zip(det_tick, det_date, det_firm, det_action, det_current, det_pt):
            if(earn_tick == detail_tick):
                print(detail_date + ' | ' + detail_firm + ' | ' + detail_action + ' | ' + detail_current + ' | ' + detail_pt)
        print('--------------------')


if __name__ == '__main__':
   main()       
