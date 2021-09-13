import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re
from linebot.models import *
import matplotlib.pyplot as plt
import pyimgur
from stock import stock_change



#最新三大法人買賣超
def investors(message):
    if re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
    url = "https://tw.stock.yahoo.com/quote/" + str(message) +"/institutional-trading"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    while str(res) != "<Response [200]>":
            res = requests.get(url,headers= headers)
    soup = BeautifulSoup(res.text)
    soup1 = soup.find_all("div",{"style":"padding:0 12px 0 0"})[0:4]
    name = []
    buy = []
    sell = []
    b_s = []
    contuin = []
    for i in soup1:
        soup2 = i.find_all("span")
        name.append(soup2[0].text)
        buy.append(soup2[1].text)
        sell.append(soup2[2].text)
        b_s.append(soup2[3].text)
        #contuin.append(soup2[4].text)
    df = pd.DataFrame({"單位(張)":name,"買進":buy,"賣出":sell,"買賣超":b_s})
    df.index = df["單位(張)"]
    df.drop("單位(張)",axis = 1,inplace = True)
    plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei'] 
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure('最新法人買賣超')            # 視窗名稱
    plt.figure(dpi = 500)
    ax = plt.axes(frame_on=False)# 不要額外框線
    ax.xaxis.set_visible(False)  # 隱藏X軸刻度線
    ax.yaxis.set_visible(False)  # 隱藏Y軸刻度線
    pd.plotting.table(ax, df, loc='center')
    plt.savefig(str(message) + "最新法人買賣超.png", bbox_inches = "tight")
    CLIENT_ID = "0214ca80ccacfe5"
    PATH = str(message) + "最新法人買賣超.png" #A Filepath to an image on your computer"
    title = str(message) + "最新法人買賣超"
    im = pyimgur.Imgur(CLIENT_ID)
    uploaded_image = im.upload_image(PATH, title=title)
    image_message = ImageSendMessage( 
        original_content_url= uploaded_image.link,
        preview_image_url= uploaded_image.link)
    return image_message