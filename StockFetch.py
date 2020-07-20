class Stocks:
    ''' Class for fetching and processing stock data from NASDAQ and stuff '''
    
    def __init__(self):
        ''' Default Constructor '''
        self.symbol_list = []
        
    def symbol_init(self, input_list):
        ''' This method adds the given symbol string into list '''
        self.symbol_list = input_list.split()
    
    def symbol_show(self):
        ''' Prints symbol list '''
        print(self.symbol_list)    
    