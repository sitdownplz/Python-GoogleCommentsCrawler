# -*- coding: utf-8 -*-
"""
Created on Mon May 31 13:30:52 2021

@author: tim
"""

import requests
import urllib
import pandas as pd
import re
import json

def getUserLocation():
    latitude = 0
    longtitude = 0
    locationURL = 'https://www.google.com.tw/maps';
    output = requests.get(locationURL)
    
    if output.ok != True:
        print('獲取使用者位置失敗')
        return
    else:
        raw = re.search('(center=.*?&amp?)',output.text).group()
        location = re.findall('\d*\.\d*',raw)
        latitude = location[0]
        longtitude = location[1]
        return latitude, longtitude
    
    if float(latitude) >= 0:
        lat_postfix = '°N'
    else:
        lat_postfix = '°S'
    if float(longtitude) >= 0:
        long_postfix = '°E'
    else: 
        long_postfix = '°W'
    print('使用者現在位置為: '\
          + latitude + lat_postfix\
              + ', ' + longtitude + long_postfix)

        
# 使用者輸入搜尋關鍵字        
searchToken = '麥當勞'
tokenEncode = urllib.parse.quote(searchToken)

# 獲取使用者當前經緯度
latitude, longtitude = getUserLocation()

# 建購搜尋條件與目標網址
url = 'https://www.google.com.tw/search?tbm=map&authuser=0&hl=zh-TW&gl=tw&pb=!4m9!1m3!1d1858071.018126'\
    + '!2d' + longtitude\
        + '!3d' + latitude\
            + '!2m0!3m2!1i406!2i762!4f13.1!7i20!10b1!12m8!1m1!18b1!2m3!5m1!6e2!20e3!10b1!16b1!19m4!2m3!1i360!2i120!4i8!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86!1m2!1i408!2i240!7m50!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2!1m3!1e2!2b0!3e3!1m3!1e3!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e3!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e9!2b1!3e2!1m3!1e10!2b0!3e3!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!2b1!4b1!9b0!22m6!1sBrqTYIG1CLLTmAXT-azADw%3A2!2s1i%3A0%2Ct%3A11886%2Cp%3ABrqTYIG1CLLTmAXT-azADw%3A2!7e81!12e5!17sBrqTYIG1CLLTmAXT-azADw%3A76!18e15!24m54!1m16!13m7!2b1!3b1!4b1!6i1!8b1!9b1!20b1!18m7!3b1!4b1!5b1!6b1!9b1!13b1!14b0!2b1!5m5!2b1!3b1!5b1!6b1!7b1!10m1!8e3!14m1!3b1!17b1!20m2!1e3!1e6!24b1!25b1!26b1!29b1!30m1!2b1!36b1!43b1!52b1!54m1!1b1!55b1!56m2!1b1!3b1!65m5!3m4!1m3!1m2!1i224!2i298!89b1!26m4!2m3!1i80!2i92!4i8!30m0!34m17!2b1!3b1!4b1!6b1!8m5!1b1!3b1!4b1!5b1!6b1!9b1!12b1!14b1!20b1!23b1!25b1!26b1!37m1!1e81!42b1!47m0!49m1!3b1!50m4!2e2!3m2!1b1!3b1!65m1!1b1!67m2!7b1!10b1!69i556'\
                + '&q=' + tokenEncode\
                    + '&oq=' + tokenEncode\
                        + '&gs_l=maps.3..38i39i111i426k1.127976.137501.1.143238.20.20.0.0.0.0.315.1499.8j3j1j1.17.0....0...1ac.1j4.64.maps..3.17.2417.2..38i39k1j38i426k1j38i376k1j115i144k1j38i442i426k1j38i72k1.12.&tch=1&ech=1&psi=BrqTYIG1CLLTmAXT-azADw.1620294152153.1'

# 爬取網站內容
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"}
response = requests.get(url,headers = header)
if response.ok != True:
    print('爬取失敗')
response.encoding ='utf-8'


# 清理爬取結果 (JSON格式)
response_fix = re.sub('\/\*""\*\/','',response.text)
rawInfo = json.loads(response_fix)
if 'd' in rawInfo:
    storeRaw = rawInfo.get('d')
else:
    print('解析失敗')

store_fix = re.sub('\)]}\'','',storeRaw)
storeInfo = json.loads(store_fix)

# 擷取店家資訊
# 如果搜尋不到匹配店家，使用最相關之結果
if len(storeInfo[0][1][0]) < 15:
    storeCode = storeInfo[0][1][1][14][72][0][0][29] #解析店家代碼
    storeChosen = storeInfo[0][1][1][14][11]
    print('搜尋為關鍵字，選擇最相關的搜尋結果爬取: ' + storeChosen)
else:
    storeCode = storeInfo[0][1][0][14][72][0][0][29] #解析店家代碼
    storeChosen = storeInfo[0][1][0][14][11]
    print('爬取搜尋結果: ' + storeChosen)
    
# 根據店家代碼建構評論爬取網址

pageList = list(range(0,101,10)) #每頁十則評論
commentResult =[]
for i in pageList:
    pages = str(i)
    commentURL = 'https://www.google.com/maps/preview/review/listentitiesreviews?authuser=0&hl=zh-TW&gl=tw&pb=!1m2'\
        + '!1y' + storeCode[0]\
            + '!2y' + storeCode[1]\
                + '!2m2!1i'\
                    + pages\
                        + '!2i10!3e1!4m5!3b1!4b1!5b1!6b1!7b1!5m2!1s_52TYKO3CNDr-QaSwqvYDQ!7e81'
    rawData = requests.get(commentURL)
    rawData_fix = re.sub('\)]}\'','',rawData.text)
    jsonData = json.loads(rawData_fix)
    extractData = jsonData[2]
    print('正在爬取第: ' + str(i) + '-' + str(i+10) + '篇評論')
    
    # 抓取評論內容資訊
    for commentInfo in extractData:
        username = commentInfo[0][1]
        day = commentInfo[1]
        comment = commentInfo[3]
        rate = commentInfo[4]
        tempresult = [username,day,comment,rate]
        commentResult.append(tempresult)
        
commentTable = pd.DataFrame(commentResult,columns=['使用者名稱','評論時間','評論內容','評論分數'])






