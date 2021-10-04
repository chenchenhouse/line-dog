import mysql.connector
import pandas as pd
import requests
from stock import  stock_change
import re

#新增股票到關注清單
def stock_database_add(message):
    try:
        if not re.match(r"[+-]?\d+$", message):
            message = stock_change(message)
            connection = mysql.connector.connect(host = "us-cdbr-east-04.cleardb.com",
                                                port = "3306",
                                                user = "b86c99dac9f77e",
                                                password = "b183a5fc",
                                                database = "heroku_f983eed4d77f4a1",
                                                charset = 'utf8')
            cursor = connection.cursor()
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
            stock_i = df_4.values[0,0]
            stock_n = df_4.values[0,1]
            cursor.execute("SELECT * FROM `list`;")
            records = cursor.fetchall()
            s_d = pd.DataFrame(records,columns=["股票代號","股票名稱"])
            if str(stock_i) not in s_d["股票代號"].values:
                cursor.execute("INSERT INTO `list` VALUES (%s,'%s');" % (stock_i,stock_n))
                connection.commit()
                cursor.close()
                connection.close()
                return stock_i + stock_n + " 已關注"
            else:
                return stock_i + stock_n + " 已是關注股票"
    except:
        return "查無您輸入的" + message + "，請重新輸入確認"

#刪除股票清單中的股票
def stock_database_del(message):
    try:
        if not re.match(r"[+-]?\d+$", message):
            message = stock_change(message)
        connection = mysql.connector.connect(host = "us-cdbr-east-04.cleardb.com",
                                            port = "3306",
                                            user = "b86c99dac9f77e",
                                            password = "b183a5fc",
                                            database = "heroku_f983eed4d77f4a1",
                                            charset = 'utf8')
        cursor = connection.cursor()
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
        stock_i = df_4.values[0,0]
        stock_n = df_4.values[0,1]
        cursor.execute("SELECT * FROM `list`;")
        records = cursor.fetchall()
        s_d = pd.DataFrame(records,columns=["股票代號","股票名稱"])
        if str(stock_i) in s_d["股票代號"].values:
            cursor.execute("DELETE FROM `list` WHERE `id` = %s;" % (stock_i))
            connection.commit()
            cursor.close()
            connection.close()
            return stock_i + stock_n + " 已取消關注"
        else:
            return stock_i + stock_n + " 並非已關注股票"
    except:
        return "查無您輸入的" + message + "，請重新輸入確認"

#查詢清單
def find_list():
    connection = mysql.connector.connect(host = "us-cdbr-east-04.cleardb.com",
                                         port = "3306",
                                        user = "b86c99dac9f77e",
                                        password = "b183a5fc",
                                        database = "heroku_f983eed4d77f4a1",
                                        charset = 'utf8')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM `list`;")
    records = cursor.fetchall()
    s_d = pd.DataFrame(records,columns=["股票代號","股票名稱"])
    list_n = "目前關注中的股票有 : \n"
    for i in range(len(s_d)):
        list_n += s_d.iloc[i][0] + " " + s_d.iloc[i][1] + "\n"
    return list_n