import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re


def stock_id(message):
    if not re.match(r'[+-]?\d+$', message):
        try:
            url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
            df = pd.read_html(requests.get(url).text)[0]
            df = df.iloc[:,2:7]
            df.columns = df.iloc[0,:]
            df = df[1:]
            url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
            df2 = pd.read_html(requests.get(url2).text)[0]
            df2 = df2.iloc[:,2:7]
            df2.columns = df2.iloc[0,:]
            df2 = df2[1:]
            df3 = pd.concat([df,df2])
            df4 = df3[df3["有價證券名稱"] == message]
            message = df4.values[0,0]
        except:
            return("錯誤")
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(message)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
    soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
    soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
    soup4 = soup3.find("a").text.split("\xa0")
    mes = "股票代號 :{} \n股票名稱 : {} \n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤 : {} \n最高 : {} \n最低 : {}".format(soup4[0],soup4[1],soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7])
    return mes
    

