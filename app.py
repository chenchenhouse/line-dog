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
from stock_news import *
from stock_select import *
from stock_base import *
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
    elif "股票 " in message:
        stock_mes = stock_message(message[3:])
        line_bot_api.reply_message(event.reply_token,stock_mes)
    elif "個股資訊 " in message:
        stock_n = stock_id(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_n),cont])
    elif "最新分鐘圖 " in message:
        m = min_close(message[6:])
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[m,cont])
    elif "日線圖 " in message:
        d = stock_day(message[4:])
        cont = continue_after(message[4:])
        line_bot_api.reply_message(event.reply_token,[d,cont])
    elif "個股新聞 " in message:
        new_one = one_new(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(new_one),cont])
    elif "平均股利 " in message:
        contiun = contiun_dividend(message[5:])
        dividend_one = average_dividend(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(contiun),dividend_one,cont])    
    elif "歷年股利 " in message:
        dividend_year = year_dividend(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[dividend_year,cont])     
    elif "同業比較 " in message:
        stock_one = compare_one(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_one),cont])
    elif "同業排名 " in message:
        stock_other = compare_other(message[5:])
        cont = continue_after(message[5:])
        line_bot_api.reply_message(event.reply_token,[TextSendMessage(stock_other),cont])  
    elif "大戶籌碼 " in message:
        st = message[5:]
        flex_message = TextSendMessage(text="請選擇要顯示的買賣超資訊", 
                                    quick_reply=QuickReply(items=[ 
                                        QuickReplyButton(action=MessageAction(label="最新法人", text="最新法人買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="歷年法人", text="歷年法人買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="外資", text="外資買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="投信", text="投信買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="自營商", text="自營商買賣超 " + st)),
                                        QuickReplyButton(action=MessageAction(label="三大法人", text="三大法人買賣超 " + st))
                                    ]))
        line_bot_api.reply_message(event.reply_token,flex_message)
    elif "最新法人買賣超 " in message:
        inv = investors(message[8:])
        cont = continue_after(message[8:])
        line_bot_api.reply_message(event.reply_token,[inv,cont])
    elif "歷年法人買賣超 " in message:
        t_d = total_data(message[8:])
        cont = continue_after(message[8:])
        line_bot_api.reply_message(event.reply_token,[t_d,cont])
    elif "外資買賣超 " in message:
        t_m = total_major(message[6:])
        f_i = foreign_inv(message[6:],t_m)
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[f_i,cont])
    elif "投信買賣超 " in message:
        t_m = total_major(message[6:])
        c_i = credit_inv(message[6:],t_m)
        cont = continue_after(message[6:])
        line_bot_api.reply_message(event.reply_token,[c_i,cont])
    elif "自營商買賣超 " in message:
        t_m = total_major(message[7:])
        s_i = self_employed_inv(message[7:],t_m)
        cont = continue_after(message[7:])
        line_bot_api.reply_message(event.reply_token,[s_i,cont])      
    elif "三大法人買賣超 " in message:
        t_m = total_major(message[8:])
        m_i = major_inv(message[8:],t_m)
        cont = continue_after(message[8:])
        line_bot_api.reply_message(event.reply_token,[m_i,cont])  
    elif re.match("新聞",message):
        news = stock_new()
        line_bot_api.reply_message(event.reply_token,news)
    elif re.match("頭條新聞",message):
        news = headlines()
        line_bot_api.reply_message(event.reply_token,news)
    elif re.match("台股新聞",message):
        news = tw_stock()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(news))
    elif re.match("國際新聞",message):
        news = wd_stock()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(news))
    elif re.match("選股1",message):
        sel = select_1()
        line_bot_api.reply_message(event.reply_token,TextSendMessage(sel))
    elif "獲利能力 " in message:
        base = base_3(message)
        line_bot_api.reply_message(event.reply_token,base)
    elif "償債能力 " in message:
        base = base_3(message)
        line_bot_api.reply_message(event.reply_token,base) 
    elif "經營能力 " in message:
        base = base_3(message)
        line_bot_api.reply_message(event.reply_token,base)           
    elif re.match("退出",message):
        line_bot_api.reply_message(event.reply_token,TextSendMessage("那我先休息囉!!"))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(message))
#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)