#!/usr/bin/env python2

import re
import time
import requests
import os
import plotly.plotly as py
from plotly.graph_objs import *
from bs4 import BeautifulSoup, NavigableString
from datetime import date

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
    parsnum = 1
    for var in ticker:  #loop for all tickers
        print('Parsing(' + str(parsnum) +'): ' + var)
        x = 0
        start_date = date(2012, 1, 1)
        end_date   = date.today()
        diff = end_date - start_date

        while x < diff.days:
            
            set_url = 'http://www.finance.yahoo.com/q/hp?s=' + str(var) + '&a=00&b=1&c=2012&d=04&e=14&f=2015&g=d&z=66&y=' + str(x)
            resp = requests.get(set_url)
            resp_data = resp.text
            data = BeautifulSoup(resp_data)
            table = data.find('table', attrs={'class':'yfnc_datamodoutline1'})
            try:
                nestedtable = table.find('table')
                trs = nestedtable.find_all('tr')
                for tr in trs:
                    tds = tr.find_all('td', attrs={'class':'yfnc_tabledata1', 'align':'right'})
                    tdcounter = 0
                    histdate = 'N/A'
                    histamt = 'N/A'
                    for td in tds:
                        total = td.getText()
                        total.strip()
                        if tdcounter == 0:
                            histdate = total
                        elif tdcounter == 1:
                            histamt = total
                        tdcounter += 1
                    if histdate != 'N/A':
                        if histamt != 'N/A':
                            tickers.append(str(var))
                            titles.append(histdate)
                            values.append(histamt)
            except:
                pass

            x += 66
        parsnum += 1

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
    
    print('Scraping: Yahoo for historical detail of ' + str(len(tickers)) + ' stocks.')
    det_tickers, det_titles, det_values = stock_report(tickers)
    print('Result: The following information has been pulled from NASDAQ')

    for earn_tick, earn_time in zip(tickers, time):
        values = []
        pos = []
        for detail_tick, detail_title, detail_value in zip(det_tickers, det_titles, det_values):
            if(earn_tick == detail_tick):
                #print(detail_tick + ': ' + detail_title + ' = ' + detail_value)
                values.append(detail_value)
                pos.append(detail_title)
        xvals = list(reversed(pos))
        yvals = list(reversed(values))
        trace = Scatter(
            x = xvals,
            y = yvals)

        data = Data([trace])
        u_url = py.plot(data, filename = str(earn_tick))

        print('--------------------')


if __name__ == '__main__':
   main()       
