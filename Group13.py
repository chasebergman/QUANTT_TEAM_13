import clr
import decimal
clr.AddReference("System")
clr.AddReference("QuantConnect.Algorithm")
clr.AddReference("QuantConnect.Indicators") 
clr.AddReference("QuantConnect.Common")

from System import *
from QuantConnect import *
from QuantConnect.Algorithm import *
from datetime import datetime, timedelta

class Group13(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetCash(100000000)  # Set Strategy Cash
        self.BBands = []
        self.stocks = ['AAPL', 'MSFT', 'GOOGL', 'FB', 'NVDA', 'TSLA', 'CRM', 'ADBE', 'INTC', 'QCOM', 'AMZN', 'SHOP', 'NFLX', 'TXN', 'AMD', 'ORCL', 'APPN', 'CMG', 'PFE', 'TWTR', 'COST'] 
        for i in range(0,len(self.stocks)):
            self.AddEquity(self.stocks[i], Resolution.Daily)
            self.BBands.append(self.BB(self.stocks[i], 30, 2, MovingAverageType.Simple, Resolution.Daily))
            self.SetWarmup(30)
     
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        
        
        for i in range(0, len(self.stocks)):
            if not(data.ContainsKey(self.stocks[i]) or self.BBands[i].IsReady):
                break
            self.StockHoldings = self.Portfolio[self.stocks[i]].Quantity
            self.CurrentPrice = self.Securities[self.stocks[i]].Price
            if (self.StockHoldings<=0):
                if self.CurrentPrice < self.BBands[i].LowerBand.Current.Value:
                    self.SetHoldings(self.stocks[i], 0.2)
                    
            elif(self.StockHoldings>0):
                if self.CurrentPrice < self.BBands[i].LowerBand.Current.Value:
                    self.SetHoldings(self.stocks[i], 0.2)
                elif self.CurrentPrice > self.BBands[i].UpperBand.Current.Value:
                    self.Liquidate()
            
            self.Plot(self.stocks[i], "MiddleBand", self.BBands[i].MiddleBand.Current.Value)
            self.Plot(self.stocks[i], "UpperBand", self.BBands[i].UpperBand.Current.Value)
            self.Plot(self.stocks[i], "LowerBand", self.BBands[i].LowerBand.Current.Value)
            self.Plot(self.stocks[i], "Price", self.Securities[self.stocks[i]].Price)
            self.Plot("Stocks", "Quantity of %s" %self.stocks[i], self.Portfolio[self.stocks[i]].Quantity)
        
        return
                
            

        