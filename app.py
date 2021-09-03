# -*- coding: utf-8 -*-
#載入LineBot所需要的套件
from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
#*********function*****************
from blog import *
from stock import *
from stock_title import *
#*********function*****************



app = Flask(__name__)

# 必須放上自己的Channel Access Token
line_bot_api = LineBotApi('GMa6mfFfZZqtABUP9FgglJT5hDxbk5CgbkEqAJKtbbwS1RFNDlATTsdymJaJL7sb/OLwdPJ8hvIS9TYMAnj9ZLb9QuFbL4dCLf2TbyBnuq+XtKBhfotGSkdBJflw0QGQxbKocTXOfPmT6IqkkMG1BAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('4f5e5ee97334958569ff5a80f5744880')

line_bot_api.push_message('Ub2085f17e1830eb1e1612d30130cc761', TextSendMessage(text='你可以開始了'))


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

 
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

 
#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = text = event.message.text
    if re.match('部落格',message):
        # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
      flex_message = flex()
      line_bot_api.reply_message(event.reply_token,flex_message)
    elif re.match('更新',message):
        #-----------------------------------
        import gspread
        from oauth2client.service_account import ServiceAccountCredentials as SAC
        import requests
        from bs4 import BeautifulSoup
        from datetime import datetime

        def stock_name():
            Json = 'stock-search-324803-9c7ec6c7c26c.json' # Json 的單引號內容請改成妳剛剛下載的那個金鑰
            Url = ['https://spreadsheets.google.com/feeds']
            Connect = SAC.from_json_keyfile_name(Json, Url)
            GoogleSheets = gspread.authorize(Connect)
            Sheet = GoogleSheets.open_by_key('1FBTfERDyv-EN8F_PsdCThEfwlDBWFkDiqghj-WqS-XY') # 這裡請輸入妳自己的試算表代號
            Sheets = Sheet.sheet1
            url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
            res = requests.get(url)
            soup = BeautifulSoup(res.text,"html.parser")
            soup1 = soup.find("table",{"class":"h4"})
            url2 = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
            res2 = requests.get(url2)
            soup2 = BeautifulSoup(res2.text,"html.parser")
            soup3 = soup2.find("table",{"class":"h4"})
            s_id = []
            for i in range(len(soup1.find_all("tr"))):
                s_id_ = soup1.find_all("tr")[i].text.split("\n")[3:5]
                s_id.append(s_id_)
            for i in range(len(soup3.find_all("tr"))):
                s_id_ = soup3.find_all("tr")[i].text.split("\n")[3:5]
                s_id.append(s_id_)
            if len(Sheets.get_all_records()) == 0:
                Sheets.append_rows(s_id)
            else:
                Sheets.update(s_id)
            return "{} 更新完成".format(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
        #-----------------------------------
        update = stock_name()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(update))
    elif "股票 " in message:
        #found = found_id(message[3:])
        stock_message = stock_id(message[3:])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(stock_message))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)