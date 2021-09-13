import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from linebot.models import *
import matplotlib.pyplot as plt
import pyimgur
import mpl_finance as mpf
import talib
import json
from random import choice
import time
import arrow
import numpy as np

#股票名稱換代號
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


#個股資訊
def stock_id(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
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

#平均股利1
def contiun_dividend(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/dividend"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("p",{"class":"Mb(20px) Mb(12px)--mobile Fz(16px) Fz(18px)--mobile C($c-primary-text)"}).text
    return soup1

#平均股利2
def average_dividend(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://goodinfo.tw/StockInfo/StockDividendPolicy.asp?STOCK_ID=" + str(message)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers=headers )
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("tr",{"align":"center","bgcolor":"white"})
    title = ["類別","平均股利(元)","平均增減(元)","均填權息日數","平均殖利率(%)","連續分派年數"]
    content = pd.DataFrame()
    for i in range(4,7):
            soup2 = soup1[i].find_all("td")
            content = content.append([[soup2[0].text,soup2[1].text,soup2[2].text,soup2[3].text,soup2[4].text,soup2[7].text]])
    content.columns = title
    content.index = content["類別"]
    content.drop("類別",axis=1,inplace = True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('平均股利')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, content, loc='center')
    plt.savefig(str(message) + "平均股利.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "平均股利.png" #A Filepath to an image on your computer"
    title = str(message) + "平均股利"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message


#歷年股利
def year_dividend(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) + "/dividend"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text,"html.parser")
    soup_period = soup.find_all("div",{"class" :"D(f) W(98px) Ta(start)"})[1:]
    period = []
    for i in soup_period:
        period.append(i.text)
    soup_dividend = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(68px)"})[3:]
    cash_dividend = []
    stock_dividend = []
    Interest_days = []
    for i in range(0,len(soup_dividend),3):
        cash_dividend.append(soup_dividend[i].text)
        stock_dividend.append(soup_dividend[i+1].text)
        Interest_days.append(soup_dividend[i+2].text)
    soup_date = soup.find_all("div",{"class":"Fxg(1) Fxs(1) Fxb(0%) Ta(end) Mend($m-table-cell-space) Mend(0):lc Miw(108px)"})[2:]
    Ex_dividend_date = []
    Dividend_payment_date = []
    for i in range(0,len(soup_date),2):
        Ex_dividend_date.append(soup_date[i].text)
        Dividend_payment_date.append(soup_date[i+1].text)
    df = pd.DataFrame({"股利所屬期間":period,"現金股利":cash_dividend,"股票股利":stock_dividend,"填息天數":Interest_days,
                       "除權息日":Ex_dividend_date,"股利發放日":Dividend_payment_date})
    df.index = df["股利所屬期間"]
    df.drop("股利所屬期間",axis = 1,inplace=True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('歷年股利')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, df, loc='center')
    plt.savefig(str(message) + "歷年股利.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "歷年股利.png" #A Filepath to an image on your computer"
    title = str(message) + "歷年股利"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#同業比較   
def compare_one(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/compare"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("a",{"class":"D(ib) Fz(14px) Lh(20px) C($c-button) Mb(20px) Mb(16px)--mobile C($c-active-text):h Td(n)"}).text
    soup2 = soup.find_all("span",{"class":"C(#000) Fz(24px) Fw(600)"})
    message = "{} \n近一年漲跌幅 : 第{}名 \n近一年每股盈餘 : 第{}名 \n近一年殖利率 : 第{}名".format(soup1,soup2[0].text,soup2[1].text,soup2[2].text)
    return message


#同業排名
def compare_other(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/compare"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers= headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers= headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    compare = "股票代號 \t股票名稱 \t近一月漲跌幅 \n"
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
        compare += "{} \t{} \t {}\t{} \n".format(stock_id[i].text,stock_name[i].text,ud,stock_quote[i].text)
    return compare

#個股新聞
def one_new(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/"+str(message) +  "/news"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    while str(res) != "<Response [200]>":
        res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("h3",{"class":"Mt(0) Mb(8px)"},limit = 13)
    news = ""
    for i in range(len(soup1)):
        if i != 1 and i != 5 and i != 9:
            new_ = soup1[i].find("a").get("href")
            news += "新聞 : {} \n網址 : {} \n".format(soup1[i].text,new_)
    return news

#分鐘圖
def min_close(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/_td-stock/api/resource/FinanceChartService.ApacLibraCharts;autoRefresh=1631105443818;symbols=%5B%22" + str(message) +".TW%22%5D;type=tick?bkt=tw-qsp-exp-no4&device=desktop&ecma=modern&feature=ecmaModern%2CuseVersionSwitch%2CuseNewQuoteTabColor%2ChideMarketInfo&intl=tw&lang=zh-Hant-TW&partner=none&prid=3j6j761gjhcda&region=TW&site=finance&tz=Asia%2FTaipei&ver=1.2.1132&returnMeta=true"
    res = requests.get(url)
    jd = res.json()["data"][0]["chart"]["indicators"]["quote"][0]
    open_ = jd["open"]
    high = jd["high"]
    low = jd["low"]
    close = jd["close"]
    volume = jd["volume"]
    time = res.json()["data"][0]["chart"]["timestamp"]
    df = pd.DataFrame({"timestamp" :  time , "open" : open_ , "high" : high , "low" : low , "close" : close , "volume" : volume})
    time_ = pd.to_datetime(df["timestamp"] + 3600 * 8 , unit = "s")
    df["timestamp"] = time_
    df = df.fillna(method= "ffill")
    df = df[1:]
    jd_ = res.json()["data"][0]["chart"]["meta"]
    previousClose = jd_["previousClose"]
    close1 = []   #上漲
    close2 = []   #下跌
    for i in range(len(df)):
        if df["close"].values[i] >=  previousClose:
            close1.append(df["close"].values[i])
        else:
            close1.append(previousClose)
    for i in range(len(df)):
        if df["close"].values[i] <=  previousClose:
            close2.append(df["close"].values[i])
        else:
            close2.append(previousClose)
    df["close1"] = close1
    df["close2"] = close2
    df["Previous"] = previousClose
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == message]
    title = df_4.values[0,0] + " " + df_4.values[0,1]
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.subplots(figsize=(15, 5)) 
    plt.title(title,fontsize = 15)
    plt.xlabel('時段',fontsize = 15)
    plt.ylabel('股價',fontsize = 15)
    plt.grid()
    plt.plot(df["timestamp"],df["close1"],"r")
    plt.plot(df["timestamp"],df["close2"],"g")
    plt.plot(df["timestamp"],df["Previous"],"yellow")
    plt.fill_between(df["timestamp"],df["close1"], df["Previous"], color = 'lightcoral')
    plt.fill_between(df["timestamp"],df["close2"], df["Previous"], color = 'palegreen')
    plt.savefig(str(message) + "分鐘圖.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "分鐘圖.png" #A Filepath to an image on your computer"
    title = str(message) + "分鐘圖"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message

#日線圖
def stock_day(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    ip_url = [{"http" : "110.74.208.154"},{"http" : "13.112.197.90"},{"http" : "47.254.75.151'"},{"http" : "181.192.2.233"},{"http" : "62.252.146.74"},
    {"http" : "185.56.209.114"},{"http" : "109.86.182.203"},{"http" : "179.108.123.210"},{"http" : "202.158.15.146"},{"http" : "47.75.145.229"},
    {"http" : "72.255.57.189"},{"http" : "195.91.221.230"},{"http" : "187.243.253.2"},{"http" : "158.140.167.148"},{"http" : "198.27.74.6:9300"},
    {"http" : "20.82.200.229:3128"},{"http" : "45.70.15.3:8080"},{"http" : "183.87.153.98:49602"},{"http" : "41.231.54.37:8888"},{"http" : "221.141.87.130:808"},
    {"http" : "188.225.253.222:8080"},{"http" : "80.154.203.122:8080"},{"http" : "212.42.62.69:8080"},{"http" : "14.161.252.185:55443"},{"http" : "194.233.67.98:443"},
    {"http" : "89.222.182.144:3128"},{"http" : "148.251.249.243:3128"}]
    df = pd.DataFrame()
    for date in range(-3,1):
        t = arrow.now().shift(months = date).strftime("%Y%m")
        url = "https://www.twse.com.tw/exchangeReport/STOCK_DAY?response=json&date=" + str(t) + "01&stockNo=" + str(message)
        ip = choice(ip_url)
        res = requests.get(url)
        s = json.loads(res.text)
        data = []
        for i in (s["data"]):
            data.append(i)
        df_i = pd.DataFrame(data,columns = s["fields"])
        df = df.append(df_i)
        time.sleep(3)
    for i in range(len(df)):
        df["日期"].iloc[i]=df["日期"].iloc[i].replace(df["日期"].iloc[i][0:3],str(  int( df["日期"].iloc[i][0:3] ) + 1911))
    df.index = pd.to_datetime(df["日期"])
    df.index = df.index.format(formatter=lambda x: x.strftime('%Y-%m-%d')) 
    df.drop("日期",axis = 1,inplace=True)
    int_ = ["成交股數","成交金額","成交筆數"]
    float_ = ["開盤價","最高價","最低價","收盤價"]
    for i in int_:
        df[i] = df[i].apply(lambda x: x.replace(",","")).astype("int64")
    for i in float_:
        df[i] = df[i].astype("float")
    url_ = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    df_ = pd.read_html(requests.get(url_).text)[0]
    df_ = df_.iloc[:,2:7]
    df_.columns = df_.iloc[0,:]
    df_ = df_[1:]
    url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
    df_2 = pd.read_html(requests.get(url2).text)[0]
    df_2 = df_2.iloc[:,2:7]
    df_2.columns = df_2.iloc[0,:]
    df_2 = df_2[1:]
    df_3 = pd.concat([df_,df_2])
    df_4 = df_3[df_3["有價證券代號"] == "2330"]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1]
    sma_10 = talib.SMA(np.array(df['最低價']), 10)
    sma_20 = talib.SMA(np.array(df['最低價']), 20)
    fig = plt.figure(figsize=(24, 15))
    ax = fig.add_axes([0,0.2,1,0.5])
    ax2 = fig.add_axes([0,0,1,0.2])
    ax.set_xticks(range(0, len(df.index),10))
    ax.set_title(title_,fontsize=30)
    ax.yaxis.set_tick_params(labelsize=15)
    ax.grid(True)
    ax.set_xticklabels(df.index[::10])
    mpf.candlestick2_ochl(ax, df['開盤價'], df['收盤價'], df['最高價'],
                          df['最低價'], width=0.6, colorup='r', colordown='g', alpha=0.75); 
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    ax.plot(sma_10, label='10日均線')
    ax.plot(sma_20, label='20日均線')
    mpf.volume_overlay(ax2, df['開盤價'], df['收盤價'], df['成交股數'], colorup='r', colordown='g', width=0.5, alpha=0.8)
    ax2.grid(True)
    ax2.set_xticks(range(0, len(df.index), 10))
    ax2.set_xticklabels(df.index[::10])
    plt.xticks(rotation=45,fontsize=20)
    plt.yticks(fontsize=15)
    ax.legend(fontsize=20,loc = "upper left")
    plt.savefig(str(message) + "日線圖.png", bbox_inches = "tight")  
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "日線圖.png" #A Filepath to an image on your computer"
    title = str(message) + "日線圖"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message



#個股資訊統整
def stock_message(message):
    if re.match(r"[+-]?\d+$", message):
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
        carousel_template_message  = TemplateSendMessage( 
        alt_text = "股票資訊",
        template=CarouselTemplate( 
            columns=[ 
                    CarouselColumn( 
                        thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                        title = message + " 股票資訊", 
                        text ="請點選想查詢的股票資訊", 
                        actions =[
                            MessageAction( 
                                label= message + " 個股資訊",
                                text= "個股資訊 " + message),
                            MessageAction( 
                                label= message + " 個股新聞",
                                text= "個股新聞 " + message),
                      
                        ]
                    ),
                    CarouselColumn( 
                        thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                        title = message + " 股票資訊", 
                        text ="請點選想查詢的股票資訊", 
                        actions =[
                            MessageAction( 
                                label= message + " 最新分鐘圖",
                                text= "最新分鐘圖 " + message), 
                            MessageAction( 
                                label= message + " 日線圖",
                                text= "日線圖 " + message),
                      
                        ]
                    ),
                    CarouselColumn( 
                        thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                        title = message + " 股利資訊", 
                        text ="請點選想查詢的股票資訊", 
                        actions =[
                            MessageAction( 
                                label= message + " 平均股利",
                                text= "平均股利 " + message),
                            MessageAction( 
                                label= message + " 歷年股利",
                                text= "歷年股利 " + message)
                        ]
                    ),
                    CarouselColumn( 
                        thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                        title = message + " 同業資訊", 
                        text ="請點選想查詢的股票資訊", 
                        actions =[
                            MessageAction( 
                                label= message + " 同業比較",
                                text= "同業比較 " + message),
                            MessageAction( 
                                label= message + " 同業排名",
                                text= "同業排名 " + message)
                        ]
                    ),
                    CarouselColumn( 
                        thumbnail_image_url ="https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png",
                        title = message + " 同業資訊", 
                        text ="請點選想查詢的股票資訊", 
                        actions =[
                            MessageAction( 
                                label= message + " 最新法人買賣超",
                                text= "最新法人買賣超 " + message),
                            MessageAction( 
                                label= message + " 歷年法人買賣超",
                                text= "歷年法人買賣超 " + message)
                         ]
                    ),                               
                ]
            ) 
        )
        return carousel_template_message
    except:
        return("請輸入正確的股票名稱")