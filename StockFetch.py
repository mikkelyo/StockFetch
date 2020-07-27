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
        self.processed_data = {}
        
    def symbol_init(self, input_list):
        '''Input desired symbols as a string and with a space separating them'''
        
        self.symbol_list = input_list.split()
        self.process(self.symbol_list)
        return self.symbol_list
    
    def symbol_show(self):
        '''Shows all desired symbols'''
        
        print(self.symbol_list)
        
    def get_dataframe(self):
        '''Outputs the dataframe with all data to a variable'''
        
        df = self.processed_data
        return df
    

    def fetch(self, symbol=None, data_range='1d', data_interval='1m'):
        ''' Forklar hvilke værdier data range og data interval kan være '''
            
        res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
        data = res.json()
        try:
            body = data['chart']['result'][0]
            dt = datetime.datetime
            dt = pd.Series(map(lambda x: arrow.get(x).to('CET').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
            df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
            dg = pd.DataFrame(body['timestamp'])
    
        except (UnboundLocalError, TypeError):
            print('Seems like you are calling a symbol that is not listed on YAHOO-finance.')
            return 
    
        output_data = df.loc[:, ('open', 'high', 'low', 'close', 'volume')].dropna() 
        
        
        #This loop is in place to delete any nonetype-data, does this need to be here?
        for number in range(len(list(output_data.keys()))):
        
            try:
                if type(output_data[(list(output_data.keys())[number])]) is type(None):
                    
                    print('***', (list(output_data.keys())[number]),'*** has no data. Entry deleted.')
                    del output_data[(list(output_data.keys())[number])]
                    
            except IndexError:
                pass
        return output_data 
        
    def process(self,data_range='1d', data_interval='1m'):
        '''Processes all data from symbols in symbol_list'''
        
        for symbol in self.symbol_list:
            try:
                self.processed_data[str(symbol)]=self.fetch(str(symbol),
                                   data_range=data_range, data_interval=data_interval)
            except KeyError:
                print('One or more symbols are non-existant')
                pass
            
    def visualize_all(self):
        '''Plots all current symbols - individual plotter to be added'''
        
        try:
            for key in self.processed_data:
                
                plt.figure(key,figsize=[12,3])
                plt.plot(self.processed_data[key].reset_index().Datetime.index,self.processed_data[key]['open'], alpha = 0.9, linewidth = 2 , label=key)
                plt.title(key)
                plt.grid(which='both')
                plt.ylabel('Stock price [$]')
                plt.xlabel('Date')
                ticks = list(np.arange(0,len(self.processed_data[key]),len(self.processed_data[key])/15))
                ticks.append(len(self.processed_data[key])-1)
                ticks = [int(round(i)) for i in ticks] #kinda silly way to make ticks include first and last tick - also is this precise enough?
                labels = self.processed_data[key].index[ticks]
                plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')
        
        except AttributeError:
            print(key,'was not plotted due to data missing - check if symbol exists')
            
    
    
if __name__ == '__main__':
    
    x = Stocks()
#    x.symbol_init('DIS')
    x.symbol_init('DIS AAPL AMD GOOGL SYMC')
    x.process(data_range='1mo',data_interval='1h')
    x.visualize_all()
    
#    data = x.get_dataframe()

    
    
    
    
    
    
    
    
    
    
    
    
    