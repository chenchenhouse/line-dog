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
        flex_message = FlexSendMessage(
            alt_text = '陳陳的嘉理'
            contents = {
  "type": "bubble",
  "hero": {
    "type": "image",
    "size": "full",
    "aspectRatio": "20:13",
    "aspectMode": "cover",
    "action": {
      "type": "uri",
      "uri": "https://linecorp.com"
    },
    "url": "https://chenchenhouse.com//wp-content/uploads/2020/10/%E5%9C%96%E7%89%871-2.png"
  },
  "body": {
    "type": "box",
    "layout": "vertical",
    "spacing": "md",
    "action": {
      "type": "uri",
      "uri": "https://linecorp.com"
    },
    "contents": [
      {
        "type": "text",
        "text": "陳陳的嘉理",
        "size": "xxl",
        "weight": "bold",
        "align": "center",
        "margin": "none",
        "action": {
          "type": "uri",
          "label": "action",
          "uri": "https://chenchenhouse.com//"
        }
      },
      {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://png.pngtree.com/element_our/png_detail/20181227/stock-market-vector-icon-png_294394.jpg",
                "size": "lg",
                "margin": "none",
                "offsetBottom": "none",
                "offsetTop": "sm"
              },
              {
                "type": "text",
                "text": "股市報你知",
                "weight": "bold",
                "margin": "sm",
                "flex": 0,
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": "https://chenchenhouse.com/category/sstock/"
                },
                "color": "#8A8A00"
              },
              {
                "type": "text",
                "size": "sm",
                "align": "end",
                "color": "#0000C6",
                "text": "財經"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://steamcode.com.tw/img/device.png",
                "size": "xl",
                "margin": "none",
                "offsetTop": "sm",
                "offsetBottom": "none",
                "offsetStart": "none"
              },
              {
                "type": "text",
                "text": "程式交易",
                "weight": "bold",
                "margin": "sm",
                "flex": 0,
                "size": "md",
                "color": "#8A8A00",
                "action": {
                  "type": "uri",
                  "label": "action",
                  "uri": "https://chenchenhouse.com/category/program_transaction/"
                }
              },
              {
                "type": "text",
                "text": "資訊",
                "size": "sm",
                "align": "end",
                "color": "#0000C6"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://img.ixintu.com/download/jpg/20200718/9f93ffebc5ffdfe32c08de65fcfb8ec6_512_512.jpg!bg",
                "size": "xl",
                "margin": "none",
                "offsetTop": "sm",
                "offsetBottom": "none",
                "offsetStart": "none"
              },
              {
                "type": "text",
                "text": "美食愛分享",
                "weight": "bold",
                "margin": "sm",
                "flex": 0,
                "size": "md",
                "color": "#8A8A00"
              },
              {
                "type": "text",
                "text": "食記",
                "size": "sm",
                "align": "end",
                "color": "#0000C6"
              }
            ]
          },
          {
            "type": "box",
            "layout": "baseline",
            "contents": [
              {
                "type": "icon",
                "url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTL7jrrEUwqGbejfBH7lhHzUCAoYP3QZJkEgw&usqp=CAU",
                "size": "xl",
                "margin": "none",
                "offsetTop": "sm",
                "offsetBottom": "none",
                "offsetStart": "none"
              },
              {
                "type": "text",
                "text": "好書推薦",
                "weight": "bold",
                "margin": "sm",
                "flex": 0,
                "size": "md",
                "color": "#8A8A00"
              },
              {
                "type": "text",
                "text": "財經",
                "size": "sm",
                "align": "end",
                "color": "#0000C6"
              }
            ]
          }
        ]
      },
      {
        "type": "text",
        "text": "#股票#程式#大數據#美食",
        "wrap": True,
        "color": "#F75000",
        "size": "xxs"
      }
    ]
  },
  "footer": {
    "type": "box",
    "layout": "vertical",
    "contents": [
      {
        "type": "button",
        "style": "primary",
        "color": "#844200",
        "action": {
          "type": "uri",
          "label": "馬上觀看",
          "uri": "https://chenchenhouse.com//"
        },
        "margin": "none"
      }
    ]
  }
}
        )
        line_bot_api.reply_message(event.reply_token,flex_message)
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)