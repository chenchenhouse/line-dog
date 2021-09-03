import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def stock_name():
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



# def found_id(stock):
#     Json = 'stock-search-324803-9c7ec6c7c26c.json' # Json 的單引號內容請改成妳剛剛下載的那個金鑰
#     Url = ['https://spreadsheets.google.com/feeds']
#     Connect = SAC.from_json_keyfile_name(Json, Url)
#     GoogleSheets = gspread.authorize(Connect)
#     Sheet = GoogleSheets.open_by_key('1FBTfERDyv-EN8F_PsdCThEfwlDBWFkDiqghj-WqS-XY') # 這裡請輸入妳自己的試算表代號
#     Sheets = Sheet.sheet1
#     for i in Sheets.get_all_records():
#         if stock in i.values():
#             found = list(i.values())[0]
#     return found