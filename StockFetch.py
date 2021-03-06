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
        self.strat1_symbols = {}
        self.strat2_symbols = {}
        
    def symbol_init(self, input_list):
        '''Input desired symbols as a string and with a space separating them'''
        
        self.symbol_list = input_list.split()
        self.process(self.symbol_list)
        return self.symbol_list
    
    def symbol_show(self):
        '''Shows all desired symbols'''
        
        print(self.symbol_list)
        
    def get_dataframe(self,strat1=False,strat2=False):
        '''Outputs the dataframe with all data to a variable
        strat1 = True will output a dataframe with the stocks fulfiilling strat1
        '''
        if strat1 == True:
            df = self.strat1_symbols
        if strat2 == True:
            df = self.strat1_symbols
        else:    
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
            print(symbol,'is not listed on YAHOO-finance')
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
                print(symbol,'has no data')
                pass
            
    def visualize_all(self, strat1=False):
        '''Plots all current symbols'''
        if strat1 == True:
            try:
                for key in self.strat1_symbols:
                    
                    plt.figure(key,figsize=[12,3])
                    plt.plot(self.strat1_symbols[key].reset_index().Datetime.index,self.strat1_symbols[key]['open'], alpha = 0.9, linewidth = 2 , label=key)
                    plt.title(key)
                    plt.grid(which='both')
                    plt.ylabel('Stock price [$]')
                    plt.xlabel('Date')
                    ticks = list(np.arange(0,len(self.strat1_symbols[key])-1,len(self.strat1_symbols[key])/15)) #if i dont subtract 1 from the length of arange, it can assume a length too long
                    ticks.append(len(self.strat1_symbols[key])-1)
                    ticks = [int(round(i)) for i in ticks]                          #kinda silly way to make ticks include first and last tick - also is this precise enough?
                    labels = self.strat1_symbols[key].index[ticks]
                    plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')
                    plt.show()
            
            except AttributeError:
                print(key,'was not plotted due to data missing - check if symbol exists')
            
        
        else:
            try:
                for key in self.processed_data:
                    
                    plt.figure(key,figsize=[12,3])
                    plt.plot(self.processed_data[key].reset_index().Datetime.index,self.processed_data[key]['open'], alpha = 0.9, linewidth = 2 , label=key)
                    plt.title(key)
                    plt.grid(which='both')
                    plt.ylabel('Stock price [$]')
                    plt.xlabel('Date')
                    ticks = list(np.arange(0,len(self.processed_data[key])-1,len(self.processed_data[key])/15)) #if i dont subtract 1 from the length of arange, it can assume a length too long
                    ticks.append(len(self.processed_data[key])-1)
                    ticks = [int(round(i)) for i in ticks]                          #kinda silly way to make ticks include first and last tick - also is this precise enough?
                    labels = self.processed_data[key].index[ticks]
                    plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')
                    plt.show()
            
            except AttributeError:
                print(key,'was not plotted due to data missing - check if symbol exists')
             
    def strat1(self):
        '''Executes a strategy to check which stocks are doing really bad but could be interesting to invest in'''
        
        
        for key in self.processed_data:
            try:
                mean_tot = self.processed_data[key]['open'].mean()
                mean_60 = self.processed_data[key]['open'][420:].mean() #past 60 days, find a better way to do this, perhaps use timestamps?
                mean_10 = self.processed_data[key]['open'][70:].mean()  #past 10 days
                max_tot = self.processed_data[key]['open'].max()    
                price_now = self.processed_data[key]['open'][-1]
                price_1day = self.processed_data[key]['open'][-8] #indices in the shape of hours - meaning 8 will go back to the previous business day
                price_2days = self.processed_data[key]['open'][-16] #similar here will go back 2 days
    
                
                if price_now <= mean_tot and price_now <= mean_60 and price_now <= mean_10 and price_now <= max_tot and price_1day <= price_2days and price_now <= price_1day and price_now <= max_tot*0.7:
                    self.strat1_symbols[key] = self.processed_data[key]
                
                    
                else:
#                    print(key,'does not fulfill Mortens criteria') #all this is used only for testing function
                    pass
                
                    
            except TypeError:
#                print(key,'is empty and was skipped')
                pass    
        print(list(self.strat1_symbols.keys()),'fulfill strategy 1s criteria')


    def strat2(self):
        '''Executes a strategy to check which stocks are escalating'''
        for key in self.processed_data:
            try:
                volume = self.processed_data[key]['volume']
#                print(volume)
                
                volume_mean = volume.mean()
                volume_mean_5 = volume[-40]
                
                price_now = self.processed_data[key]['close'][-1]
                price_max = self.processed_data[key]['close'].max()
                            
                price_3days = self.processed_data[key]['close'][-24]
                
                if volume_mean_5 >= volume_mean*2.5 and price_now >= price_max*0.93 and price_now >= price_3days*0.9:
#                    print(key,'is escalating')
                    self.strat2_symbols[key] = self.processed_data[key]
                
                    
                else:
                    pass
                
                    
            except (TypeError,IndexError):
                print(key,'is empty or not enough data - skipped (strat2)')
                pass    
        print(list(self.strat2_symbols.keys()),'fulfill strategy 2s criteria')

            
    def visualize(self,symbol):
        '''Plots a symbol'''
        
        try:
            
            plt.figure(symbol,figsize=[12,3])
            plt.plot(self.processed_data[symbol].reset_index().Datetime.index,self.processed_data[symbol]['open'], alpha = 0.9, linewidth = 2 , label=symbol)
            plt.title(symbol)
            plt.grid(which='both')
            plt.ylabel('Stock price [$]')
            plt.xlabel('Date')
            ticks = list(np.arange(0,len(self.processed_data[symbol])-1,len(self.processed_data[symbol])/15)) #if i dont subtract 1 from the length of arange, it can assume a length too long
            ticks.append(len(self.processed_data[symbol])-1)
            ticks = [int(round(i)) for i in ticks]                          #kinda silly way to make ticks include first and last tick - also is this precise enough?
            labels = self.processed_data[symbol].index[ticks]
            plt.xticks( ticks=ticks , labels=labels , rotation = 'vertical')
            plt.show()
        
        except AttributeError:
            print(symbol,'was not plotted due to data missing - check if symbol exists')
   #%%         
if __name__ == '__main__':
    #adasdasd
    x = Stocks()
    x.symbol_init('DIS AAPL maersk-b.co INTC L RL CCL FOXA HST LYV COLO-B.CO CARL-B.CO AEP QCOM LUN.CO NZYM-B.CO NOVO-B.CO MAERSK-B.CO')
#    x.symbol_init('MC F FTNT FTV FBHS FOXA FOX BEN FCX GPS GRMN IT GD GE GIS GM GPC GILD GL GPN GS GWW HRB HAL HBI HIG HAS HCA PEAK HSIC HSY HES HPE HLT HFC HOLX HD HON HRL HST HWM HPQ HUM HBAN HII IEX IDXX INFO ITW ILMN INCY IR INTC ICE IBM IP IPG IFF INTU ISRG IVZ IPGP IQV IRM JKHY J JBHT SJM JNJ JCI JPM JNPR KSU K KEY KEYS KMB KIM KMI KLAC KSS KHC KR LB LHX LH LRCX LW LVS LEG LDOS LEN LLY LNC LIN LYV LKQ LMT L LOW LYB MTB MRO MPC MKTX MAR MMC MLM MAS MA MKC MXIM MCD MCK MDT MRK MET MTD MGM MCHP MU MSFT MAA MHK TAP MDLZ MNST MCO MS MOS MSI MSCI MYL NDAQ NOV NTAP NFLX NWL NEM NWSA NWS NEE NLSN NKE NI NBL NSC NTRS NOC NLOK NCLH NRG NUE NVDA NVR ORLY OXY ODFL OMC OKE ORCL OTIS PCAR PKG PH PAYX PAYC PYPL PNR PBCT PEP PKI PRGO PFE PM PSX PNW PXD PNC PPG PPL PFG PG PGR PLD PRU PEG PSA PHM PVH QRVO PWR DGX RL RJF RTX O REG REGN RF RSG RMD RHI ROK ROL ROP ROST RCL SPGI CRM SBAC SLB STX SEE SRE NOW SHW SPG SWKS SLG SNA SO LUV SWK SBUX STT STE SYK SIVB SYF SNPS SYY TMUS TROW TTWO TPR TGT TEL FTI TDY TFX TXN TXT TMO TIF TJX TSCO T TDG TRV TFC TWTR TYL TSN UDR ULTA USB UAA UA UNP UAL UNH UPS URI UHS UNM VFC VLO VAR VTR VRSN VRSK VZ VRTX VIAC V VNO VMC WRB WAB WMT WBA DIS WM WAT WEC WFC WELL WST WDC WU WRK WY WHR WMB WLTW WYNN XEL XRX XLNX XYL YUM ZBRA ZBH ZION ZTS MMM ABT ABBV ABMD ACN ATVI ADBE AMD AAP AES AFL A APD AKAM ALK ALB ARE ALXN ALGN ALLE LNT ALL GOOG MO AMZN AMCR AEE AAL AEP AXP AIG AMT AWK AMP ABC AME AMGN APH ADI ANSS ANTM AON AOS APA AIV AAPL AMAT APTV ADM ANET AJG AIZ T ATO ADSK ADP AZO AVB AVY BKR BLL BAC BK BAX BDX BBY BIO BIIB BLK BA BKNG BWA BXP BSX BMY AVGO BR B CHRW COG CDNS CPB COF CAH KMX CCL CARR CAT CBOE CBRE CDW CE CNC CNP CTL CERN CF SCHW CHTR CVX CMG CB CHD CI CINF CTAS CSCO C CFG CTXS CLX CME CMS KO CTSH CL CMCSA CMA CAG CXO COP ED STZ COO CPRT GLW CTVA COST COTY CCI CSX CMI CVS DHI DHR DRI DVA DE DAL XRAY DVN DXCM FANG DLR DFS DISCA DISCK DISH DG DLTR D DPZ DOV DOW DTE DUK DRE DD DXC ETFC EMN ETN EBAY ECL EIX EW EA EMR ETR EOG EFX EQIX EQR ESS EL EVRG ES RE EXC EXPE EXPD EXR XOM FFIV FB FAST FRT FDX FIS FITB FE FRC FISV FLT FLIR FLS ATVI ADBE amd  alxn algn goog GOOGL AMZN AMGN adi anss AAPL amat asml adsk adp bidu biib bmrn bkng avgo cdns cdw cern chtr ctas CSCO ctxs ctsh cmcsa cprt cost csx dxcm docu dltr EA EBAY exc expe FB fast fisv fox foxa gild idxx ilmn incy INTC intu isrg jd klac lrcx lbtya lbtyk lulu mar mxim meli mchp mu msft mrna mdlz MNST ntap ntes NFLX NVDA nxpi orly pcar payx pypl pep qcom regn rost sgen siri swks splk sbux snps tmus ttwo tsla txn khc tcom ulta vrsn vrsk vrtx wba wdc wday xel xlnx zm AC.PA F7TB.MU MAERSK-B.CO ULVR.L AZN.L RDSA.L RDSB.L BHP.L RIO.L GSK.L HSBA.L DGE.L BATS.L BP.L RB.L NG.L REL.L VOD.L LSE.L PRU.L AAL.L EXPN.L GLEN.L CRH.L TSCO.L LLOY.L CPG.L FLTR.L BARC.L OCDO.L BA.L FERG.L ABF.L SSE.L SN.L SMT.L LGEN.L STAN.L IMB.L SGRO.L AHT.L AV.L ANTO.L RTO.L SDR.L BT-A.L FRES.L ITRK.L III.L HL.L HLMA.L SGE.L PSN.L BNZL.L CRDA.L NXT.L CCH.L WPP.L ADM.L DCC.L MNDI.L PHNX.L IHG.L SKG.L UU.L SVT.L SLA.L INF.L BKG.L CCL.L SMIN.L BDEV.L AUTO.L KGF.L BRBY.L STJ.L HIK.L RMV.L RSA.L MRW.L WTB.L JMAT.L RR.L LAND.L TW.L MRO.L EVR.L DLG.L SBRY.L PSON.L SMDS.L BLND.L IAG.L CNA.L HSX.L EZJ.L ITV.L MKS.L TUI.L MCRO.L ROCK-A.CO ROCK-B.CO ORSTED.CO ASTGRP.CO BAVA.CO CARL-B.CO COLO-B.CO DNORD.CO DANSKE.CO DSV.CO FLS.CO LUN.CO MAERSK-A.CO NKT.CO NDA-DK.CO NOVO-B.CO NZYM-B.CO SYDB.CO TOP.CO TRYG.CO VWS.CO')
    
    x.process(data_range='9mo',data_interval='1h')
    
    #%%
#    x.visualize(symbol='MAERSK-B.CO')
#    c=x.get_dataframe()
    x.strat1()
#    x.strat2()
#    data = x.get_dataframe(strat1=True)
    

#    x.visualize_all(strat1=True)
    
    
#%%
    #homemade shit to test if there are duplicates XD
#    test = 'FMC F FTNT FTV FBHS FOXA FOX BEN FCX GPS GRMN IT GD GE GIS GM GPC GILD GL GPN GS GWW HRB HAL HBI HIG HAS HCA PEAK HSIC HSY HES HPE HLT HFC HOLX HD HON HRL HST HWM HPQ HUM HBAN HII IEX IDXX INFO ITW ILMN INCY IR INTC ICE IBM IP IPG IFF INTU ISRG IVZ IPGP IQV IRM JKHY J JBHT SJM JNJ JCI JPM JNPR KSU K KEY KEYS KMB KIM KMI KLAC KSS KHC KR LB LHX LH LRCX LW LVS LEG LDOS LEN LLY LNC LIN LYV LKQ LMT L LOW LYB MTB MRO MPC MKTX MAR MMC MLM MAS MA MKC MXIM MCD MCK MDT MRK MET MTD MGM MCHP MU MSFT MAA MHK TAP MDLZ MNST MCO MS MOS MSI MSCI MYL NDAQ NOV NTAP NFLX NWL NEM NWSA NWS NEE NLSN NKE NI NBL NSC NTRS NOC NLOK NCLH NRG NUE NVDA NVR ORLY OXY ODFL OMC OKE ORCL OTIS PCAR PKG PH PAYX PAYC PYPL PNR PBCT PEP PKI PRGO PFE PM PSX PNW PXD PNC PPG PPL PFG PG PGR PLD PRU PEG PSA PHM PVH QRVO PWR QCOM DGX RL RJF RTX O REG REGN RF RSG RMD RHI ROK ROL ROP ROST RCL SPGI CRM SBAC SLB STX SEE SRE NOW SHW SPG SWKS SLG SNA SO LUV SWK SBUX STT STE SYK SIVB SYF SNPS SYY TMUS TROW TTWO TPR TGT TEL FTI TDY TFX TXN TXT TMO TIF TJX TSCO T TDG TRV TFC TWTR TYL TSN UDR ULTA USB UAA UA UNP UAL UNH UPS URI UHS UNM VFC VLO VAR VTR VRSN VRSK VZ VRTX VIAC V VNO VMC WRB WAB WMT WBA DIS WM WAT WEC WFC WELL WST WDC WU WRK WY WHR WMB WLTW WYNN XEL XRX XLNX XYL YUM ZBRA ZBH ZION ZTS MMM ABT ABBV ABMD ACN ATVI ADBE AMD AAP AES AFL A APD AKAM ALK ALB ARE ALXN ALGN ALLE LNT ALL GOOG MO AMZN AMCR AEE AAL AEP AXP AIG AMT AWK AMP ABC AME AMGN APH ADI ANSS ANTM AON AOS APA AIV AAPL AMAT APTV ADM ANET AJG AIZ T ATO ADSK ADP AZO AVB AVY BKR BLL BAC BK BAX BDX BBY BIO BIIB BLK BA BKNG BWA BXP BSX BMY AVGO BR B CHRW COG CDNS CPB COF CAH KMX CCL CARR CAT CBOE CBRE CDW CE CNC CNP CTL CERN CF SCHW CHTR CVX CMG CB CHD CI CINF CTAS CSCO C CFG CTXS CLX CME CMS KO CTSH CL CMCSA CMA CAG CXO COP ED STZ COO CPRT GLW CTVA COST COTY CCI CSX CMI CVS DHI DHR DRI DVA DE DAL XRAY DVN DXCM FANG DLR DFS DISCA DISCK DISH DG DLTR D DPZ DOV DOW DTE DUK DRE DD DXC ETFC EMN ETN EBAY ECL EIX EW EA EMR ETR EOG EFX EQIX EQR ESS EL EVRG ES RE EXC EXPE EXPD EXR XOM FFIV FB FAST FRT FDX FIS FITB FE FRC FISV FLT FLIR FLS ATVI ADBE amd  alxn algn goog GOOGL AMZN AMGN adi anss AAPL amat asml adsk adp bidu biib bmrn bkng avgo cdns cdw cern chtr ctas CSCO ctxs ctsh cmcsa cprt cost csx dxcm docu dltr EA EBAY exc expe FB fast fisv fox foxa gild idxx ilmn incy INTC intu isrg jd klac lrcx lbtya lbtyk lulu mar mxim meli mchp mu msft mrna mdlz MNST ntap ntes NFLX NVDA nxpi orly pcar payx pypl pep qcom regn rost sgen siri swks splk sbux snps tmus ttwo tsla txn khc tcom ulta vrsn vrsk vrtx wba wdc wday xel xlnx zm'
#    test = test.split()
#    
#    test = list(dict.fromkeys(test))
#    len(test) != len(set(test))
    
    
    
    
    
    
    
    
    