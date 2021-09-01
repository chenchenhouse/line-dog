from abc import ABC, abstractmethod
import pandas as pd
import requests

#股票抽象類別
class all_stock(ABC):
    def _init_(self,s_id):
        self.s_id = s_id
    def scrape(self):
        pass
    
#股票資訊
class stock(all_stock):
    def scrape(self):
        stock_id_listed = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
        stock_id_otc = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
        data_listed = requests.get(stock_id_listed)
        data_listed = pd.read_html(data_listed.text)[0]
        data_listed.columns = data_listed.iloc[0]
        data_listed = data_listed[1:]
        data_listed = data_listed.loc[:,"有價證券代號":"產業別"]
        data_otc = requests.get(stock_id_otc)
        data_otc = pd.read_html(data_otc.text)[0]
        data_otc.columns = data_otc.iloc[0]
        data_otc = data_otc[1:]
        data_otc = data_otc.loc[:,"有價證券代號":"產業別"]
        stock_id = pd.concat([data_listed,data_otc],axis = 0)
        stock = stock_id[stock_id["有價證券代號"] == self.s_id]
        content =print(f"股票代號 : {stock.values[0,0]} \n股票名稱 :{stock.values[0,1]} \n市場別 : {stock.values[0,2]} \n有價證券別 : {stock.values[0,3]} \n產業別 :{stock.values[0,4]}")
        return content