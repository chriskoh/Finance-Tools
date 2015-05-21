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
#                    print('Name: ' + value)                   
                elif counter == 1:
                    lastsale.append(value)
#                    print('LastSale: ' + value)
                elif counter == 2:
                    netchange.append(value)
#                    print('NetChange: ' + value)
                elif counter == 3:
                    volume.append(value)
#                    print('Volume: ' + value)
                elif counter == 4:
                    highlow.append(value)
#                    print('Todays High / Low: ' + value)
                elif counter == 5:
                    highlow2.append(value)
#                    print('52 Week High / Low: ' + value)
                elif counter == 6:
                    peratio.append(value)
#                    print('P/E Ratio: ' + value)
                elif counter == 7:
                    cap.append(value)
#                    print('Market Cap: ' + value)

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

    for earn_tick, earn_time in zip(tickers, time):
        print(earn_tick + ' --- ' + earn_time)
        print('Company Name | Last Sale | Net Change | Volume | Today"s high / low | 52 Week high / low | P/E Ratio | Market Cap')
        for detail_tick, detail_name, detail_lsale, detail_change, detail_volume, detail_highlow, detail_highlow2, detail_per, detail_cap in zip(det_tick, det_name, det_lsale, det_change, det_volume, det_highlow, det_highlow2, det_per, det_cap):
            if(earn_tick == detail_tick):
                print(detail_name + ' | ' + detail_lsale + ' | ' +  detail_change + ' | ' + detail_volume + ' | ' + detail_highlow + ' | ' + detail_highlow2 + ' | ' + detail_per + ' | ' + detail_cap)
        print('--------------------')


if __name__ == '__main__':
   main()       
