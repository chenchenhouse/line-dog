import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from linebot.models import *

def stock_change(message):
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
        return(message)
    except:
        return("請輸入正確的股票名稱")

def stock_id(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    if message == "請輸入正確的股票名稱":
        return("是我錯了")
    try:
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
        soup_1 = soup.find("table",{"class":"b1 p4_4 r10"})
        soup_2 = soup_1.find_all("td",{"bgcolor":"white"})
        mes = "股票代號 :{} \n股票名稱 : {} \n產業別 : {} \n市場 : {}\n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {}  \n資本額 : {} \n市值 : {}".format(soup4[0],soup4[1],soup_2[1].text,soup_2[2].text,soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7],soup_2[4].text,soup_2[5].text)
        return mes
    except:
        return("請輸入正確的股票代號")
    
def compare_one(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    if message == "請輸入正確的股票名稱":
        return("是我錯了")
    url = "https://tw.stock.yahoo.com/quote/" +str(message)+"/compare"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    while soup.text =="\n\n\n\n\n":
        res = requests.get(url,headers= headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("a",{"class":"D(ib) Fz(14px) Lh(20px) C($c-button) Mb(20px) Mb(16px)--mobile C($c-active-text):h Td(n)"}).text
    soup2 = soup.find_all("span",{"class":"C(#000) Fz(24px) Fw(600)"})
    message = "{} \n近一年漲跌幅 : 第{}名 \n近一年每股盈餘 : 第{}名 \n近一年殖利率 : 第{}名".format(soup1,soup2[0].text,soup2[1].text,soup2[2].text)
    return message


def compare_other(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    if message == "請輸入正確的股票名稱":
        return("是我錯了")
    url = "https://tw.stock.yahoo.com/quote/" +str(message)+"/compare"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    while soup.text =="\n\n\n\n\n":
        res = requests.get(url,headers= headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
    compare = "股票代號\t股票名稱\t近一月漲跌幅 \n"
    stock_id = soup.find_all("span",{"class":"Fz(14px) C(#979ba7) Ell"})
    stock_name = soup.find_all("div",{"class":"Lh(20px) Fw(600) Fz(16px) Ell"})
    stock_quote = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(100px) Bgc(t)"})
    stock_ud = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(100px) Bgc(t)"})[:-1]
    for i in range(len(stock_id)):
        try:
            stock_mark = stock_ud[i].find("span",{"class":"Mend(4px) Bds(s)"}).get("style")
            if "#ff333a" in  stock_mark:
                ud = "+"
            else:
                ud = "-"
        except:
            ud = " "
        compare += "{}\t{}\t {}\t{} \n".format(stock_id[i].text,stock_name[i].text,ud,stock_quote[i].text)
    return(compare)


def stock_message(message):
    if not re.match(r"[+-]?\d+$", message):
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
            df4 = df3[df3["有價證券代號"] == message]
            message = df4.values[0,1]
        except:
            return("請輸入正確的股票代號")   
    try: 
        buttons_template_message = TemplateSendMessage( 
        alt_text = "股票資訊",
        template=ButtonsTemplate( 
            thumbnail_image_url="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
            title= message + " 股票資訊", 
            text="請點選想查詢的股票資訊", 
            actions=[
                MessageAction( 
                    label= message + " 個股資訊",
                    text= "個股資訊 " + message),
                MessageAction( 
                    label= message + " 同業比較",
                    text= "同業比較 " + message),
                MessageAction( 
                    label= message + " 同業排名",
                    text= "同業排名 " + message),    
                ] 
            ) 
        )
        return buttons_template_message
    except:
        return("請輸入正確的股票名稱")