from linebot.models import *
import pandas as pd
import requests

def stock_id():
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
    stock_ = input("請輸入股票代號: ")
    stock = stock_id[stock_id["有價證券代號"] == stock_]
    print("股票代號 : ",stock.values[0,0])
    print("股票名稱 : ",stock.values[0,1])
    print("市場別 : ",stock.values[0,2])
    print("有價證券別: ",stock.values[0,3])
    print("產業別: ",stock.values[0,4])