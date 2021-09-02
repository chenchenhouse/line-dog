import requests
from bs4 import BeautifulSoup 



def stock_id(message):
    url = "https://isin.twse.com.tw/isin/class_main.jsp?owncode=&stockname=&isincode=&market=1&issuetype=1&industry_code=&Page=1&chklike=Y"
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"h4"})
    s_id = []
    s_name = []
    for i in range(len(soup1.find_all("tr")[1:])):
        s_id_ = soup1.find_all("tr")[i+1].text.split("\n")[3]
        s_id.append(s_id_)
        s_name_ = soup1.find_all("tr")[i+1].text.split("\n")[4]
        s_name.append(s_name_)
    found_index = s_name.index(message)
    f_id = s_id[found_index]
    url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(f_id)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
    }
    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
    soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
    soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
    soup4 = soup3.find("a").text.split("\xa0")
    mes = "股票代號 :{} \n股票名稱 : {} \n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤 : {} \n最高 : {} \n最低 : {}".format(soup4[0],soup4[1],soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7])
    return mes