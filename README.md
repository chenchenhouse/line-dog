# 股票LINE Bot
製作日期 : 2021/7~2021/9  
製作人 : Rick
# 動機
每當要研究投資標的時，你是否也會覺得A網站的財報資料完整，又覺得B網站的選股條件完善，又覺得C網站的新聞比較重要，有時身邊又沒有隨身攜帶筆電怎麼好查詢呢?這時可能就在想怎麼沒有人開發一個程式能完成符合我想要的功能啊~~與其求助於人，不如自己動手做最好，有相同煩惱的人，「LINE Bot」就相當適合你!!
# 功能
- 部落格 : 串接FlexMessage，可以一鍵串接到我的部落格中
- 財經新聞查詢 : 透過爬蟲，從yahoo新聞中爬取最新財經新聞
- 個股查詢 : 基本資料、個股相關新聞、K線圖、殖利率等多種功能
- 股票關注 : 透過python串接MySQL資料庫，隨時追蹤股票價格走勢
- 自動選股 : Python設定選股條件，LINE一鍵即可查詢最新選股結果
# 工具
- Python : 利用jupyter與visual studio code撰寫程式，並且爬取相關金融網站數據，如鉅亨網、yahoo股市、Goodinfo等等。
- MySQL :透過Python中的 mysql.connector和database建立連線，運用SELECT、INSERT、WHERE、GROUP BY來製作股票清單追蹤，以利後續股票關注清單的新增、刪除及查詢功能。
- Github : 將撰寫好的程式上傳到GitHub，以利雲端執行程式碼。
- Heroku :利用Heroku雲端伺服器將GitHub與LINE結合使用。
