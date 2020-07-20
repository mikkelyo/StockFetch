#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 20 14:25:15 2020

@author: MI
"""

import requests
import pandas as pd
import arrow
import datetime
import matplotlib.pyplot as plt
import numpy as np

class Stocks:
    ''' Class for fetching and processing stock data from NASDAQ '''
    
    def __init__(self):
        self.symbol_list = []
        
    def symbol_init(self, input_list):
        self.symbol_list = input_list.split()
    
    def symbol_show(self):
        print(self.symbol_list)
    
#    def fetch(self, symbol=None, data_range='1d', data_interval='1m'):
#        ''' Forklar hvilke værdier data range og data interval kan være '''
#        res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
#        data = res.json()
#        try:
#            body = data['chart']['result'][0]
#            dt = datetime.datetime
#            dt = pd.Series(map(lambda x: arrow.get(x).to('CET').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
#            df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
#            dg = pd.DataFrame(body['timestamp'])
#    
#        except (UnboundLocalError, TypeError):
#            print('Seems like you are calling a symbol that is not listed on YAHOO-finance.')
#            return 
#    
#        output_data = df.loc[:, ('open', 'high', 'low', 'close', 'volume')].dropna() 
#        
#        
#        #This loop is in place to delete any nonetype-data, does this need to be here?
#        for number in range(len(list(output_data.keys()))):
#        
#            try:
#                if type(output_data[(list(output_data.keys())[number])]) is type(None):
#                    
#                    print('***', (list(output_data.keys())[number]),'*** has no data. Entry deleted.')
#                    del output_data[(list(output_data.keys())[number])]
#                    
#            except IndexError:
#                pass
#    
#        return output_data 
     
        
    
    
    
if __name__ == '__main__':
    
#    stocks = Stocks().fetch('DIS','7d','1h')
#    x= Stocks()
#    x = Stocks().symbol_init('AAPL')
    x=Stocks()
    x.symbol_init('AAPL DIS TSLA AMD')
    x.symbol_show()
    