import requests
from bs4 import BeautifulSoup 
from linebot.models import *
import pandas as pd


def headlines():
    url = "https://news.cnyes.com/news/cat/headline"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find_all("a",{"class":"_1Zdp"},limit = 10)
    base = "https://news.cnyes.com"
    title = []
    address = []
    picture = []
    for i in soup1:
        title_ = i.get("title")
        address_ = base + i.get("href")
        picture_ = i.find("img")["src"]
        title.append(title_)
        address.append(address_)
        picture.append(picture_)
    df = pd.DataFrame({"標題": title,"網址":address,"圖片":picture})
    carousel_template_message  = TemplateSendMessage( 
        alt_text = "股票資訊",
        template=CarouselTemplate( 
            columns=[ 
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[0][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[0][0], 
                            uri=df.iloc[0][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[1][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[1][0], 
                            uri=df.iloc[1][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[2][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[2][0], 
                            uri=df.iloc[2][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[3][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[3][0], 
                            uri=df.iloc[3][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[4][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[4][0], 
                            uri=df.iloc[4][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[5][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[5][0], 
                            uri=df.iloc[5][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[6][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[6][0], 
                            uri=df.iloc[6][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[7][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[7][0], 
                            uri=df.iloc[7][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[8][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[8][0], 
                            uri=df.iloc[8][1]),
                    ]
                ),
                CarouselColumn( 
                        thumbnail_image_url =df.iloc[9][2],
                        title = "頭條新聞", 
                        text ="有興趣請點新聞", 
                        actions =[
                            URIAction( label= df.iloc[9][0], 
                            uri=df.iloc[9][1])
                        ]
                    )
                ]
            ) 
        )
    return carousel_template_message

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

def wd_stock():
    url = "https://news.cnyes.com/news/cat/wd_stock"
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
            MessageAction( 
                label="頭條新聞 TOP5",
                text="頭條新聞"),
            MessageAction( 
                label="台股新聞 TOP5",
                text="台股新聞"),
            MessageAction( 
                label="國際新聞 TOP5",
                text="國際新聞"),    
            ] 
        ) 
    )
    return buttons_template_message

