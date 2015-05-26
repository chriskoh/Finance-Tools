#!/usr/bin/env python2

import re
import time
import requests
import os
from pylab import *
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup, NavigableString
from datetime import date, datetime
from matplotlib.dates import DateFormatter, WeekdayLocator, HourLocator, DayLocator, MONDAY
from matplotlib.finance import candlestick, plot_day_summary, candlestick2
import matplotlib.mlab as mlab
import plotly.plotly as py
import unicodedata

def stock_report():
    titles = []
    valsopen = []
    valshigh = []
    valslow = []
    valsclose = []

    parsnum = 1

    x = 0
    start_date = date(2015, 1, 1)
    end_date   = date.today()
    diff = end_date - start_date

    while x < diff.days:
            
        set_url = 'http://www.finance.yahoo.com/q/hp?s=aapl&a=00&b=1&c=2012&d=04&e=14&f=2015&g=d&z=66&y=' + str(x)
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
                        histopen = total
                    elif tdcounter == 2:
                        histhigh = total
                    elif tdcounter == 3:
                        histlow = total
                    elif tdcounter == 4:
                        histclose = total
                    tdcounter += 1

                if histdate != 'N/A':
                    if histopen != 'N/A':
                        titles.append(histdate)
                        valsopen.append(histopen)
                        valshigh.append(histhigh)
                        valslow.append(histlow)
                        valsclose.append(histclose)

        except:
            pass

        x += 66
    parsnum += 1

    return titles, valsopen, valshigh, valslow, valsclose


def main():
    os.system('clear')

    print('Program Start')
    print('Scraping: NASDAQ for AAPL')
    
    det_titles, det_open, det_high, det_low, det_close = stock_report()
    print('Result: The following information has been pulled from NASDAQ')
    prices = []

    for detail_title, detail_open, detail_high, detail_low, detail_close in zip(det_titles, det_open, det_high, det_low, det_close):
        date1 = detail_title
        date1 = date2num(datetime.strptime(date1, '%b %d, %Y'))
        tup = (date1, float(detail_open), float(detail_close), float(detail_high), float(detail_low))
        prices.append(tup)
        
    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()
    weekFormatter = DateFormatter('%b %d')
    dayFormatter = ('%d')
    
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    ax.xaxis.set_major_locator(mondays)
    ax.xaxis.set_minor_locator(alldays)
    ax.xaxis.set_major_formatter(weekFormatter)
    candlestick(ax, prices, width=0.6)

    ax.xaxis_date()
#    ax.autoscale_view()
    plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

    plt.show()

    py.sign_in('chriskoh', 'yyy0hoavmt')

    plot_url = py.plot_mpl(fig)

if __name__ == '__main__':
   main()       
