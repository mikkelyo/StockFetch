import requests
import pandas as pd
import json
import plotly.express as px

class Stocks:
    ''' Class for fetching and processing stock data from NASDAQ and stuff '''
    
    def __init__(self):
        ''' Default Constructor '''
        self.symbol_list = []
        self.dataframe = []
        
    def symbol_init(self, input_list):
        ''' This method adds the given symbol string into list '''
        self.symbol_list = input_list.split()
    
    def symbol_show(self):
        ''' Prints symbol list '''
        print(self.symbol_list)

    def fetch_stock(self):
        ''' This method fetches stock '''

        url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self.symbol_list[0]}?region=US&interval=2m&range=1d'
        page = requests.get(url)
        data = page.text

        with open (f'{self.symbol_list[0]}.json', 'w') as f:
            f.write(data)

    def initialize_data(self):
        ''' This method initializes stock data into pandas dataframe'''
        with open(f'{self.symbol_list[0]}.json', 'r') as myfile:
            data = json.load(myfile)
        
        # Note timestamps are loaded in unix timestamp format
        timestamps = data['chart']['result'][0]['timestamp']
        stock_values = data['chart']['result'][0]['indicators']['quote'][0]
        stock_values['timestamp'] = timestamps
        self.dataframe = pd.DataFrame(stock_values)

    def visualize_data(self):
        ''' This method visualizes the data using plotly'''
        # Converting unix timestamp format using built in pandas function
        fig = px.line(self.dataframe, 
                      x=pd.to_datetime(self.dataframe['timestamp'], 
                      unit='s'), 
                      y=self.dataframe['close'],
                      hover_data=['open', 'high', 'low'],
                      title=f'Graph for {self.symbol_list[0]}',
                      labels={'x' : 'time'},
                      template='simple_white')
        fig.update_xaxes(rangeslider_visible=True)
        fig.update_layout(hovermode="x unified")
        fig.show()




if __name__ == '__main__':

    x = Stocks()

    x.symbol_init('AAPL')
    x.initialize_data()
    x.visualize_data()

