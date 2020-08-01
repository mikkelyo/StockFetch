import StockFetch_Daniel as sf

if __name__ == '__main__':

    x = sf.Stocks()
    # x.symbol_init('AAPL DIS TSLA AMD')
    # x.symbol_show()

    x.fetch_stock()