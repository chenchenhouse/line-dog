import requests
from bs4 import BeautifulSoup 

def stock_id(message):
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(message)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
    soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
    mes = "成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤 : {} \n最高 : {} \n最低 : {}".format(soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7])
    return mes