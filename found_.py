import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

def found_id(stock):
    Json = 'stock-search-324803-9c7ec6c7c26c.json' # Json 的單引號內容請改成妳剛剛下載的那個金鑰
    Url = ['https://spreadsheets.google.com/feeds']
    Connect = SAC.from_json_keyfile_name(Json, Url)
    GoogleSheets = gspread.authorize(Connect)
    Sheet = GoogleSheets.open_by_key('1FBTfERDyv-EN8F_PsdCThEfwlDBWFkDiqghj-WqS-XY') # 這裡請輸入妳自己的試算表代號
    Sheets = Sheet.sheet1
    for i in Sheets.get_all_records():
        if stock in i.values():
            found = list(i.values())[0]
    return found