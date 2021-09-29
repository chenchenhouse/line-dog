from linebot.models import *
from bs4 import BeautifulSoup
import requests
import re
from stock import *

def base_3(message):
    if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
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
    df_4 = df_3[df_3["有價證券代號"] == str(message)]
    title_ = df_4.values[0,0] + " " + df_4.values[0,1]
    url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
        'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=' + str(message)
    }
    data = {
        "STEP": "DATA",
        "STOCK_ID": str(message),
        "RPT_CAT": "XX_M_YEAR"
    }
    res = requests.post(url,headers = headers,data = data)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup_t1 = soup.find_all("tr",{"class":"bg_h1 fw_normal"})[0]
    title = soup_t1.find_all("nobr")[:4]
    soup1 = soup.find_all("tr",{"bgcolor":"white"})
    a = soup1[0].find_all("nobr")[:4]  #毛利率
    b = soup1[1].find_all("nobr")[:4] #營業利益率
    c = soup1[3].find_all("nobr")[:4] #稅後淨利率
    d = soup1[6].find_all("nobr")[:4] #EPS
    e = soup1[8].find_all("nobr")[:4] #ROE
    f = soup1[9].find_all("nobr")[:4] #ROA
    # message = FlexSendMessage(
    #     alt_text = '獲利能力',
    #     contents = {
    #     "type": "bubble",
    #     "body": {
    #         "type": "box",
    #         "layout": "vertical",
    #         "contents": [
    #         {
    #             "type": "text",
    #             "text": title_,
    #             "weight": "bold",
    #             "color": "#1DB446",
    #             "size": "md"
    #         },
    #         {
    #             "type": "text",
    #             "text": title[0].text,
    #             "weight": "bold",
    #             "size": "xxl",
    #             "margin": "md"
    #         },
    #         {
    #             "type": "separator",
    #             "margin": "xxl"
    #         },
    #         {
    #             "type": "box",
    #             "layout": "vertical",
    #             "margin": "xxl",
    #             "spacing": "md",
    #             "contents": [
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": "期別",
    #                     "size": "xl",
    #                     "color": "#000000",
    #                     "flex": 0,
    #                     "weight": "bold"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": title[3].text,
    #                     "size": "xl",
    #                     "color": "#000000",
    #                     "align": "center",
    #                     "weight": "bold",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": title[2].text,
    #                     "size": "xl",
    #                     "color": "#000000",
    #                     "align": "center",
    #                     "weight": "bold",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": title[1].text,
    #                     "size": "xl",
    #                     "color": "#000000",
    #                     "align": "center",
    #                     "weight": "bold",
    #                     "gravity": "center"
    #                 }
    #                 ],
    #                 "spacing": "xxl",
    #                 "margin": "lg"
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": a[0].text,
    #                     "size": "md",
    #                     "color": "#555555",
    #                     "align": "start",
    #                     "gravity": "center",
    #                     "wrap": True
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": a[3].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": a[2].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": a[1].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 }
    #                 ],
    #                 "spacing": "none",
    #                 "margin": "md"
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": b[0].text,
    #                     "size": "md",
    #                     "color": "#555555",
    #                     "margin": "none",
    #                     "align": "start",
    #                     "gravity": "center",
    #                     "wrap": True
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": b[3].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": b[2].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": b[1].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 }
    #                 ],
    #                 "margin": "md"
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": c[0].text,
    #                     "size": "md",
    #                     "color": "#555555",
    #                     "margin": "none",
    #                     "align": "start",
    #                     "gravity": "center",
    #                     "wrap": True
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": c[3].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": c[2].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": c[1].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 }
    #                 ],
    #                 "margin": "md"
    #             },
    #             {
    #                 "type": "box",
    #                 "layout": "horizontal",
    #                 "contents": [
    #                 {
    #                     "type": "text",
    #                     "text": d[0].text,
    #                     "size": "md",
    #                     "color": "#555555",
    #                     "margin": "none",
    #                     "align": "start",
    #                     "gravity": "center",
    #                     "wrap": True
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": d[3].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": d[2].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 },
    #                 {
    #                     "type": "text",
    #                     "text": d[1].text,
    #                     "size": "lg",
    #                     "color": "#111111",
    #                     "align": "center",
    #                     "gravity": "center"
    #                 }
    #                 ],
    #                 "margin": "md"
    #             }
    #             ]
    #         },
    #         {
    #             "type": "box",
    #             "layout": "horizontal",
    #             "contents": [
    #             {
    #                 "type": "text",
    #                 "text": e[0].text,
    #                 "size": "md",
    #                 "color": "#555555",
    #                 "margin": "none",
    #                 "align": "start",
    #                 "gravity": "center",
    #                 "wrap": True
    #             },
    #             {
    #                 "type": "text",
    #                 "text": e[3].text,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             },
    #             {
    #                 "type": "text",
    #                 "text": e[2].text,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             },
    #             {
    #                 "type": "text",
    #                 "text": e[1].text,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             }
    #             ],
    #             "margin": "md"
    #         },
    #         {
    #             "type": "box",
    #             "layout": "horizontal",
    #             "contents": [
    #             {
    #                 "type": "text",
    #                 "size": "md",
    #                 "color": "#555555",
    #                 "margin": "none",
    #                 "align": "start",
    #                 "gravity": "center",
    #                 "wrap": True,
    #                 "text": f[0].text
    #             },
    #             {
    #                 "type": "text",
    #                 "text": f[3].text,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             },
    #             {
    #                 "type": "text",
    #                 "text": f[2].text,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             },
    #             {
    #                 "type": "text",
    #                 "text": f[1].text1,
    #                 "size": "lg",
    #                 "color": "#111111",
    #                 "align": "center",
    #                 "gravity": "center"
    #             }
    #             ],
    #             "margin": "md"
    #         }
    #         ],
    #         "margin": "none",
    #         "spacing": "none",
    #         "borderWidth": "none",
    #         "cornerRadius": "none"
    #     },
    #     "styles": {
    #         "footer": {
    #         "separator": True
    #         }
    #     }
    #     }
    # )
    return f[0].text