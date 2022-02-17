import requests
from bs4 import BeautifulSoup
import jieba
import re
import emoji
from stock import *
from linebot.models import *

#選股策略1
def select_1():
  url = "https://goodinfo.tw/tw/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B3%A3%E8%B6%85%E4%BD%94%E6%88%90%E4%BA%A4%28%25%29%E2%80%93%E6%9C%88&FL_VAL_S0=10&FL_VAL_E0=&FL_VAL_CHK0=T&FL_ITEM1=%E9%80%A3%E7%BA%8C%E9%85%8D%E7%99%BC%E7%8F%BE%E9%87%91%E8%82%A1%E5%88%A9%E6%AC%A1%E6%95%B8&FL_VAL_S1=10&FL_VAL_E1=&FL_ITEM2=%E8%BF%91%E5%9B%9B%E5%AD%A3%E2%80%93EPS%E5%B9%B4%E6%88%90%E9%95%B7%E7%8E%87%28%25%29%E2%80%93%E6%9C%AC%E5%AD%A3%E5%BA%A6&FL_VAL_S2=3&FL_VAL_E2=&FL_VAL_CHK2=T&FL_ITEM3=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29&FL_VAL_S3=&FL_VAL_E3=100&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%7C%7C%E6%9C%88%2F%E5%AD%A3%2F%E5%B9%B4%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%E4%B8%94%E5%9D%87%E7%B7%9A%E8%B5%B0%E6%8F%9A%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%E4%B8%94%E8%B5%B0%E6%8F%9A%40%40%E6%9C%88%2F%E5%AD%A3%2F%E5%B9%B4&FL_RULE_CHK0=T&FL_RULE1=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81%7C%7C%E8%82%A1%E5%83%B9%E6%8E%A5%E8%BF%91%E4%B8%80%E5%80%8B%E6%9C%88%E9%AB%98%E9%BB%9E%40%40%E8%82%A1%E5%83%B9%E6%8E%A5%E8%BF%91%E5%A4%9A%E6%97%A5%E9%AB%98%E9%BB%9E%40%40%E4%B8%80%E5%80%8B%E6%9C%88&FL_RULE_CHK1=T&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&FL_SHEET2=%E6%97%A5&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
  headers = {
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
  }

  res = requests.get(url,headers = headers)
  res.encoding = "utf-8"
  soup = BeautifulSoup(res.text,"html.parser")
  try: 
      soup1 = soup.find("tr",{"id":"hrow0"}).text
  except:
      print("目前無符合標準的個股")
  jieba.load_userdict(r'C:\Users\adsad\OneDrive\Desktop\機器學習\line\斷字.txt')
  seg_list = jieba.lcut(soup1)
  stock_id = []
  stock_name = []
  compare = "1.單日成交量增減幅(%) > 20% \n2.連續配發現金股利10次以上 \n3.近四季EPS(元)創近5年同期新高 \n4.股價<100元 \n5.月/季/年均線多頭排列走揚 \n6.月均線向上走揚 \n最新選股結果: \n"
  for i in seg_list:
      if re.match(r"[+-]?\d+$", i):
          stock_id.append(i)
      else:
          stock_name.append(i)
  for i in range(len(stock_id)):
      compare += "{} \t {} \n".format(stock_id[i],stock_name[i])
  return compare

#地雷股檢測
def select_2(message):
  if not re.match(r"[+-]?\d+$", message):
        message = stock_change(message)
  url = "https://goodinfo.tw/StockInfo/StockFinDetail.asp"
  headers = {
      "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
      'referer': 'https://goodinfo.tw/StockInfo/StockFinDetail.asp?RPT_CAT=XX_M_QUAR_ACC&STOCK_ID=' + str(message)
  }
  data = {
      "STEP": "DATA",
      "STOCK_ID": str(message),
      "RPT_CAT": "XX_M_YEAR",
  }
  res = requests.post(url,headers = headers,data = data)
  res.encoding = "utf-8"
  soup = BeautifulSoup(res.text,"html.parser")
  soup_t1 = soup.find_all("tr",{"class":"bg_h1 fw_normal"})[0]
  title = soup_t1.find_all("nobr")[:4]
  soup1 = soup.find_all("tr",{"bgcolor":"white"})
  for i in range(len(soup1)):
      if soup1[i].find_all("nobr")[0].text == "每股自由現金流量\xa0(元)": #自由現金流量
          fcfps = soup1[i].find_all("nobr")[:6] 
      if soup1[i].find_all("nobr")[0].text == "每股稅後盈餘\xa0(元)": #每股稅後盈餘
          eps = soup1[i].find_all("nobr")[:6] 
      if soup1[i].find_all("nobr")[0].text =="負債總額年成長率": #負債總額年成長率
          debt = soup1[i].find_all("nobr")[:6] 
      if soup1[i].find_all("nobr")[0].text == "股東權益報酬率": #股東權益報酬率
          roe = soup1[i].find_all("nobr")[:6]
      if soup1[i].find_all("nobr")[0].text == "資產報酬率": #資產報酬率
          roa = soup1[i].find_all("nobr")[:6]
  sum_count = 0
  #自由現金流量近五年有三年> 0
  count_1 = 0  
  for i in fcfps[1:]:
      if float(i.text) > 0:
          count_1 += 1
  if count_1 >= 3:
      a = "{} 通過 自由現金流量近五年有三年 > 0 ({}/5)".format(emoji.emojize(':green_circle:',use_aliases=True),count_1)
  else:
      a = "{} 沒過 自由現金流量近五年有三年 > 0 ({}/5)".format(emoji.emojize(':x:',use_aliases=True),count_1)
      sum_count += 1
  #自由現金流量近五年平均> 0
  sum_1 = 0
  for i in fcfps[1:]:
      sum_1 += float(i.text)
  av_1 = sum_1/5
  if  av_1> 0:
      b = "{} 通過 自由現金流量近五年平均大於 > 0 ({:.2f}元)".format(emoji.emojize(':green_circle:',use_aliases=True),av_1)
  else:
      b = "{} 沒過 自由現金流量近五年平均大於 > 0 ({:.2f}元)".format(emoji.emojize(':x:',use_aliases=True),av_1)
      sum_count += 1
  #每股稅後盈餘近五年有三年大>0
  count_2 = 0
  for i in eps[1:]:
      if float(i.text) > 0:
          count_2 += 1
  if count_2 >= 3:
      c = "{} 通過 每股稅後盈餘近五年有三年大於 > 0 ({}/5)".format(emoji.emojize(':green_circle:',use_aliases=True),count_2)
  else:
      c = "{} 沒過 每股稅後盈餘近五年有三年大於 > 0 ({}/5)".format(emoji.emojize(':x:',use_aliases=True),count_2)
      sum_count += 1
  #自由現金流量近五年平均> 0
  sum_2 = 0
  for i in eps[1:]:
      sum_2 += float(i.text)
  av_2 = sum_2/5
  if  av_2> 0:
      d = "{} 通過 每股稅後盈餘近五年平均大於 > 0 ({:.2f}元)".format(emoji.emojize(':green_circle:',use_aliases=True),av_2)
  else:
      d = "{} 沒過 每股稅後盈餘近五年平均大於 > 0 ({:.2f}元)".format(emoji.emojize(':x:',use_aliases=True),av_2)
      sum_count += 1
  #負債總額年成長率平均<20%
  sum_3 = 0
  for i in debt[1:]:
      sum_3 += float(i.text)
  av_3 = sum_3/5
  if  av_3< 20:
      e = "{} 通過 負債總額年成長率平均<20% ({:.2f}%)".format(emoji.emojize(':green_circle:',use_aliases=True),av_3)
  else:
      e = "{} 沒過 負債總額年成長率平均<20% ({:.2f}%)".format(emoji.emojize(':x:',use_aliases=True),av_3)
      sum_count += 1
  #ROE近五年有三年 > ROA
  count_3 = 0
  for i,j in zip(roe[1:],roa[1:]):
      if float(i.text) > float(j.text):
          count_3 += 1
  if count_3 == 5:
      f = "{} 通過 ROE近五皆 > ROA ({}/5)".format(emoji.emojize(':green_circle:',use_aliases=True),count_3)
  else:
      f = "{} 沒過 ROE近五年皆 > ROA ({}/5)".format(emoji.emojize(':x:',use_aliases=True),count_3)
      sum_count += 1
  #ROE近五年有三年> 10%
  count_4 = 0
  for i in roe[1:]:
      if float(i.text) > 10:
          count_4 += 1
  if count_4 >= 3:
      g = "{} 通過 ROE近五年有三年> 10% ({}/5)".format(emoji.emojize(':green_circle:',use_aliases=True),count_4)
  else:
      g = "{} 沒過 ROE近五年有三年> 10% ({}/5)".format(emoji.emojize(':x:',use_aliases=True),count_4)
      sum_count += 1
  #暴雷程度
  thunder = sum_count / 7 *100
  sum = "{} 暴雷程度 : {:.2f}%".format(emoji.emojize(':zap:',use_aliases=True),thunder)
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
  df_4 = df_3[df_3["有價證券代號"] == message]
  title_ = df_4.values[0,0] + " " + df_4.values[0,1]
  message = FlexSendMessage(
              alt_text = '陳陳的嘉理',
              contents = {
    "type": "bubble",
    "body": {
      "type": "box",
      "layout": "vertical",
      "contents": [
        {
          "type": "text",
          "text": str(title_),
          "weight": "bold",
          "size": "xxl",
          "margin": "none",
          "wrap": True,
          "align": "center"
        },
        {
          "type": "text",
          "text": "地雷股檢測報告",
          "weight": "bold",
          "size": "xxl",
          "margin": "none",
          "wrap": True,
          "align": "center"
        },
        {
          "type": "image",
          "url": "https://i04piccdn.sogoucdn.com/4df8bda2750d575f",
          "size": "full",
          "aspectRatio": "20:13",
          "aspectMode": "fit",
          "action": {
            "type": "uri",
            "uri": "https://linecorp.com"
          }
        },
        {
          "type": "text",
          "text": "透過自由現金流量、EPS、負債比、ROE及ROA之相關比較，檢測公司是否存在虛增獲利、負債過高以至還不出來的風險",
          "size": "sm",
          "color": "#aaaaaa",
          "wrap": True
        },
        {
          "type": "separator",
          "margin": "xxl"
        },
        {
          "type": "box",
          "layout": "vertical",
          "margin": "xxl",
          "spacing": "sm",
          "contents": [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "X",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0,
                  "margin": "none",
                  "align": "start"
                },
                {
                  "type": "text",
                  "text": "沒過",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0,
                  "align": "center",
                  "wrap": True,
                  "margin": "xs"
                },
                {
                  "type": "text",
                  "text": "自由現金流量近五年有三年>0",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0,
                  "wrap": True,
                  "align": "center",
                  "margin": "sm"
                },
                {
                  "type": "text",
                  "text": "(2/5)",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0,
                  "margin": "sm"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "Chewing Gum",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0
                },
                {
                  "type": "text",
                  "text": "$0.99",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "Bottled Water",
                  "size": "sm",
                  "color": "#555555",
                  "flex": 0
                },
                {
                  "type": "text",
                  "text": "$3.33",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
            {
              "type": "separator",
              "margin": "xxl"
            },
            {
              "type": "box",
              "layout": "horizontal",
              "margin": "xxl",
              "contents": [
                {
                  "type": "text",
                  "text": "ITEMS",
                  "size": "sm",
                  "color": "#555555"
                },
                {
                  "type": "text",
                  "text": "3",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "TOTAL",
                  "size": "sm",
                  "color": "#555555"
                },
                {
                  "type": "text",
                  "text": "$7.31",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "CASH",
                  "size": "sm",
                  "color": "#555555"
                },
                {
                  "type": "text",
                  "text": "$8.0",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            },
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                  "type": "text",
                  "text": "CHANGE",
                  "size": "sm",
                  "color": "#555555"
                },
                {
                  "type": "text",
                  "text": "$0.69",
                  "size": "sm",
                  "color": "#111111",
                  "align": "end"
                }
              ]
            }
          ]
        },
        {
          "type": "separator",
          "margin": "xxl" 
        },
        {
          "type": "box",
          "layout": "horizontal",
          "margin": "md",
          "contents": [
            {
              "type": "text",
              "text": "PAYMENT ID",
              "size": "xs",
              "color": "#aaaaaa",
              "flex": 0
            },
            {
              "type": "text",
              "text": "#743289384279",
              "color": "#aaaaaa",
              "size": "xs",
              "align": "end"
            }
          ]
        }
      ],
      "margin": "none",
      "spacing": "none"
    },
    "styles": {
      "footer": {
        "separator": True
      }
    }
  }
  )