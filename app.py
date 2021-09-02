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
import pandas as pd
import requests
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
    message = text=event.message.text
    if re.match('部落格',message):
        # Flex Message Simulator網頁：https://developers.line.biz/console/fx/
      flex_message = flex()
      line_bot_api.reply_message(event.reply_token,flex_message)
    elif re.match('台積電',message):
        stock_id_listed = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
        stock_id_otc = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=2&issuetype=4&industry_code=&Page=1&chklike=Y"
        data_listed = requests.get(stock_id_listed)
        data_listed = pd.read_html(data_listed.text)[0]
        data_listed.columns = data_listed.iloc[0]
        data_listed = data_listed[1:]
        data_listed = data_listed.loc[:,"有價證券代號":"產業別"]
        data_otc = requests.get(stock_id_otc)
        data_otc = pd.read_html(data_otc.text)[0]
        data_otc.columns = data_otc.iloc[0]
        data_otc = data_otc[1:]
        data_otc = data_otc.loc[:,"有價證券代號":"產業別"]
        stock_id = pd.concat([data_listed,data_otc],axis = 0)
        stock = stock_id[stock_id["有價證券名稱"] == message] 
        message ="股票代號 : {}".format(stock.values[0,0])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
      
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)