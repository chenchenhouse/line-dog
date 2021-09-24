import requests
from bs4 import BeautifulSoup
import jieba
import re

#選股策略1
def select_1():
    url = "https://goodinfo.tw/StockInfo/StockList.asp?MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&FL_ITEM0=%E4%B8%89%E5%A4%A7%E6%B3%95%E4%BA%BA%E7%B4%AF%E8%A8%88%E8%B2%B7%E8%B3%A3%E8%B6%85%E4%BD%94%E6%88%90%E4%BA%A4%28%25%29%E2%80%93%E6%9C%88&FL_VAL_S0=10&FL_VAL_E0=&FL_ITEM1=%E9%80%A3%E7%BA%8C%E9%85%8D%E7%99%BC%E7%8F%BE%E9%87%91%E8%82%A1%E5%88%A9%E6%AC%A1%E6%95%B8&FL_VAL_S1=10&FL_VAL_E1=&FL_ITEM2=%E8%BF%91%E5%9B%9B%E5%AD%A3%E2%80%93EPS%E5%B9%B4%E6%88%90%E9%95%B7%E7%8E%87%28%25%29%E2%80%93%E6%9C%AC%E5%AD%A3%E5%BA%A6&FL_VAL_S2=3&FL_VAL_E2=&FL_ITEM3=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29&FL_VAL_S3=&FL_VAL_E3=100&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_RULE0=%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%7C%7C%E6%9C%88%2F%E5%AD%A3%2F%E5%B9%B4%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%E4%B8%94%E5%9D%87%E7%B7%9A%E8%B5%B0%E6%8F%9A%40%40%E5%9D%87%E5%83%B9%E7%B7%9A%E5%A4%9A%E9%A0%AD%E6%8E%92%E5%88%97%E4%B8%94%E8%B5%B0%E6%8F%9A%40%40%E6%9C%88%2F%E5%AD%A3%2F%E5%B9%B4&FL_RULE1=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81%7C%7C%E8%82%A1%E5%83%B9%E6%8E%A5%E8%BF%91%E4%B8%80%E5%80%8B%E6%9C%88%E9%AB%98%E9%BB%9E%40%40%E8%82%A1%E5%83%B9%E6%8E%A5%E8%BF%91%E5%A4%9A%E6%97%A5%E9%AB%98%E9%BB%9E%40%40%E4%B8%80%E5%80%8B%E6%9C%88&FL_RULE2=&FL_RULE3=&FL_RULE4=&FL_RULE5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=&FL_FD1=&FL_FD2=&FL_FD3=&FL_FD4=&FL_FD5=&FL_SHEET=%E8%87%AA%E8%A8%82%E6%AC%84%E4%BD%8D_%E8%87%AA%E8%A8%82&FL_SHEET2=&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_QRY=%E6%9F%A5++%E8%A9%A2"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36"
    }

    res = requests.get(url,headers = headers)
    res.encoding = "utf-8"
    soup = BeautifulSoup(res.text,"html.parser")
    soup1 = soup.find("tr",{"id":"hrow0"}).text
    jieba.load_userdict('./斷字.txt')
    seg_list = jieba.lcut(soup1)
    stock_id = []
    stock_name = []
    compare = "1.三大法人進1月累計買賣10%以上 \n2.連續配發現金股利10次以上 \n3.近4季EPS年成長率3%以上 \n4.股價<100元 \n5.月/季/年均線多頭排列走揚 \n6.股價接近近1月高點 \n最新選股結果: \n"
    for i in seg_list:
        if re.match(r"[+-]?\d+$", i):
            stock_id.append(i)
        else:
            stock_name.append(i)
    for i in range(len(stock_id)):
        compare += "{} \t {} \n".format(stock_id[i],stock_name[i])
    return compare