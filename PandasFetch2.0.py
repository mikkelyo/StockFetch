import requests
import pandas as pd
import arrow
import datetime
import matplotlib.pyplot as plt
import numpy as np

def get_stock_data(symbol='DIS', data_range='1d', data_interval='1m'):

    res = requests.get('https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?range={data_range}&interval={data_interval}'.format(**locals()))
    data = res.json()
    try:
        body = data['chart']['result'][0]
        dt = datetime.datetime
        dt = pd.Series(map(lambda x: arrow.get(x).to('CET').datetime.replace(tzinfo=None), body['timestamp']), name='Datetime')
        df = pd.DataFrame(body['indicators']['quote'][0], index=dt)
        dg = pd.DataFrame(body['timestamp'])

    except (UnboundLocalError, TypeError):
        print('Seems like you are calling a symbol that is not listed on YAHOO finance.')
        return 

    return df.loc[:, ('open', 'high', 'low', 'close', 'volume')].dropna() #remove NaN rows in the end


def visualize_include_closing_times(data,shortw=20,longw=100,symbol='stock'):
    # Calculate the 20 and 100 days moving averages of the closing prices
#    short_rolling_OPEN = data.rolling(window=shortw).mean()
#    long_rolling_OPEN = data.rolling(window=longw).mean()
    
    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16*0.7,9*0.7))
    
    ax.plot(data.index, data, label=symbol)
#    ax.plot(short_rolling_OPEN.index, short_rolling_OPEN, label='20 days rolling')
#    ax.plot(long_rolling_OPEN.index, long_rolling_OPEN, label='100 days rolling')
    
    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
#    ax.set_xticks(rotation='vertical')
    ax.legend()
    plt.grid()
    plt.show()

def visualize(data, label = 'Undefined' , xticks = 11, window=20 , mean=False):
    plt.figure(1,figsize=[12,3])
    plt.plot(data.reset_index().Datetime.index,data, alpha = 0.9, linewidth = 2 , label=label)
   
    ticks = list(np.arange(0,len(data),len(data)/xticks))
    ticks.append(len(data)-1)
    ticks = [int(round(i)) for i in ticks] #kinda silly way to make ticks include first and last tick - also is this precise enough?
    labels = data.index[ticks]
    plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')
    
    if mean:
        rolling_mean = data.rolling(window=window).mean()
        plt.plot(data.reset_index().Datetime.index, rolling_mean, label=str(window)+' days rolling mean')
    
    plt.ylabel('Stock Value [$]')
    plt.xlabel('Timestamp')
    plt.legend()
    plt.grid(which='both',linestyle='--')
#    plt.show()
    
if __name__ == '__main__':
    
#    data = get_stock_data('DIS', '7d', '1m') #Cannot request 1m data longer than 1w into the past.
#    visualize(data['open'] , label='Open' , xticks = 22, mean=True, window = 100)
    
    
    
    #%%
# =============================================================================
#     LOOP TO COLLECT DATA FOR RANGE OF SYMBOLS
# =============================================================================
    
    symbols = ('VXUS ISRG AAXN VTI ATVI ADBE GOOGL AMZN AMGN AAPL BIIB CSCO EA EBAY SYMC FB INTC MAR MNST NFLX NVDA PYPL PEP SBUX SYMC TSLA TXN MMM AXP T BAC KO GE IBM MRK PFE PG WMT DIS VZ ACN CAT C XOM DE GD GS IBM INTC KHC NKE ORCL V').split()
#    symbols = ('CPH:NOVO-B').split()
    data={}
    
    for symbol in symbols:
        try:
            data[str(symbol)]=get_stock_data(str(symbol), '1y', '1h')
        except KeyError:
            print('One or more symbols are non-existant')
            pass
        
    #%%   
# =============================================================================
#     DELETION OF NON-EXISTANT DATA
# =============================================================================
    for number in range(len(list(data.keys()))):
        
        try:
            if type(data[(list(data.keys())[number])]) is type(None):
                
                print('***', (list(data.keys())[number]),'*** has no data. Entry deleted.')
                del data[(list(data.keys())[number])]
                
        except IndexError:
            pass
        
    #%%
# =============================================================================
#     LOOP FOR PLOTTING DATA
# =============================================================================
    for key in data:
        plt.figure(key,figsize=[12,3])
        plt.plot(data[key].reset_index().Datetime.index,data[key]['open'], alpha = 0.9, linewidth = 2 , label=key)
        plt.title(key)
        plt.grid(which='both')
        plt.ylabel('Stock price [$]')
        plt.xlabel('Date')
        ticks = list(np.arange(0,len(data[key]),len(data[key])/15))
        ticks.append(len(data[key])-1)
        ticks = [int(round(i)) for i in ticks] #kinda silly way to make ticks include first and last tick - also is this precise enough?
        labels = data[key].index[ticks]
        plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')

    
    
  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# =============================================================================
#     Future improvements
# =============================================================================
    #lav evt ticks på skift i dage.

    #lav compatible med at åbne og gemme data for mange stocks
    
    #ML predictive models




















#%%
#### Rolling averages
#short_rolling_OPEN = OPEN.rolling(window=20).mean()
#long_rolling_OPEN = OPEN.rolling(window=100).mean()
#plt.plot(OPEN.reset_index().Datetime.index, short_rolling_OPEN, label='20 days rolling')
#plt.plot(OPEN.reset_index().Datetime.index, long_rolling_OPEN, label='100 days rolling')
####
#%% #to csv
#import os
#data.to_csv(r'DIS_hourly.csv', index = True)
