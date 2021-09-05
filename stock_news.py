import requests
from bs4 import BeautifulSoup 
from linebot.models import *


def headlines():
    url = "https://news.cnyes.com/news/cat/headline"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("a",{"class":"_1Zdp"},limit = 10)
    base = "https://news.cnyes.com"
    news =  ""
    for i in soup1:
        title = i.get("title")
        address = base + i.get("href")
        news += "新聞 : {} \n網址 : {} \n".format(title,address)
    return news

def tw_stock():
    url = "https://news.cnyes.com/news/cat/tw_stock"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("a",{"class":"_1Zdp"},limit = 10)
    base = "https://news.cnyes.com"
    news =  ""
    for i in soup1:
        title = i.get("title")
        address = base + i.get("href")
        news += "新聞 : {} \n網址 : {} \n".format(title,address)
    return news

def stock_new():
    buttons_template_message = TemplateSendMessage( 
    alt_text = "股票新聞",
    template=ButtonsTemplate( 
        thumbnail_image_url="https://github.com/chenchenhouse/line-dog/blob/f889bc55d8217d12c0c14dc59b733cab335b1825/%E9%89%85%E4%BA%A8%E7%B6%B2.png",
        title="股市新聞", 
        text="請點選想查詢的新聞種類", 
        actions=[
            MessageAction( 
                label="頭條新聞 TOP5",
                text="頭條新聞"),
            MessageAction( 
                label="台股新聞 TOP5",
                text="台股新聞")
            ] 
        ) 
    )
    return buttons_template_message

