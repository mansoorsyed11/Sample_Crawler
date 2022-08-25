# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 11:48:24 2022

@author: msyed
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 11:24:52 2022

@author: msyed
"""

import requests
import pandas as pd
from bs4 import BeautifulSoup

def getFinancialInformation(symbol):
    url = "https://finance.yahoo.com/quote/"+symbol+"?p="+symbol
    
    
    #prop = "Stock market crash" 
    
    response = requests.get(url)
    
    t = response.text
    
    soup = BeautifulSoup(t, features = 'html.parser')
    
    #trs = soup.find_all('td', class_ = "Va(t) Fz(14px) Whs(nw) Ta(end) Pstart(10px) Py(6px)")
    
    trs = soup.find_all('tr')
    #print(trs[0].find('td', attrs = { "class":"gray-placeholder W(100%) H(30px) My(6px)"}))# class="gray-placeholder W(100%) H(30px) My(6px)"
    #print(trs[0].contents[1].text)
    
    #print(trs[0])
    finalName = 'Avg. Volume'
    names = []
    values = []
    
    namVal = {}
    #dict2 = {"names": names, "values":values}
    
    for i in range(len(trs)):
        for j in range(len(trs[i].contents)):
            if j==0:           #Name
                try:
                    name = trs[i].contents[j].text
                    names.append(name)
                except:
                    continue
               
            if j==1:#value
                try:
                    value = trs[i].contents[j].text
                    values.append(value)
                except:
                    pass
          
        namVal[name]=value
        if name ==finalName:
            break
   
    return names, values
# print(names)
# print(values)
# print(namVal)

def getCompanyList():
    wikiUrl = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    
    r = requests.get(wikiUrl)
    pageText = r.text
    
    soup = BeautifulSoup(pageText, features = 'html.parser')
    
    
    
    tickerSymbols = []
    values = []
    namVal = {}
    
    tbody = soup.find_all('tbody')
    #print(tbody[0].contents[6].contents[1].text)
    
    
    for i in range(len(tbody[0].contents)):
        if i<2:
            continue
        if i%2 !=0:
            continue
               
        symbol = tbody[0].contents[i].contents[1].text
        tickerSymbols.append(symbol.strip("\n"))
        if len(tickerSymbols)==505:
            break
    return tickerSymbols
data = {"symbol":[],
        "metric":[],
        "value":[]}       
tickerSymbols = getCompanyList()
for symbol in tickerSymbols:
    names, values = getFinancialInformation(symbol)
    #itearte over vales too
    # for name in range(len(names)):
    #     if name not in data:
    #         data[name]=[]
    #     data[name].append(value)
    
    for i in range(len(names)):
        data['symbol'].append(symbol)
        data['metric'].append(names[i])
        data['value'].append(values[i])
        
        # data['symbol']+=[symbol]*len(names)
        # data['metric']+=names
        # data['values']+=values
        
        # values, names = getCompanyList(symbol)
        # #iterate over values too
        # for name in range(len(names)):
        #     name = names[i]
        #     value = values[i]
        #     if name not in data:
        #         data[name]=[]
        #     data[name].append(value)
# print(tickerSymbols)

df = pd.DataFrame(data)
df.to_csv('financialData.csv')