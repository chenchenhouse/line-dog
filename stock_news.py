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
        thumbnail_image_url="https://s.yimg.com/ny/api/res/1.2/RqETwlh8PY7yrbaDIhyxdQ--/YXBwaWQ9aGlnaGxhbmRlcjt3PTY0MDtoPTM4MC40NDQ0NDQ0NDQ0NDQ0Ng--/https://s.yimg.com/uu/api/res/1.2/Vn5SfDtQIEZNmoxFT0hVQw--~B/aD0yMTQ7dz0zNjA7YXBwaWQ9eXRhY2h5b24-/https://media.zenfs.com/zh-tw/cnyes.com.tw/bfd0fd8921c2a100ac91dab8014a84af",
        title="股市新聞", 
        text="請點選想查詢的新聞種類", 
        actions=[
             PostbackAction( 
                label="頭條新聞 TOP5",
                display_text = "頭條新聞 TOP5",
                data= headlines()),
            PostbackAction(
                label="台股新聞 TOP5",
                display_text = "台股新聞 TOP5",
                data= tw_stock()),
            ] 
        ) 
    )
    return buttons_template_message

