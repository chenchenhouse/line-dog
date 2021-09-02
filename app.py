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
        stock_message = '股票代號 : 2330'
        line_bot_api.reply_message(event.reply_token,stock_message)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)