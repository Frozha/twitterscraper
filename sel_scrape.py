from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs
import csv
import pandas as pd
import os
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller
keyboard = Controller()
def scraper(a, html_clss,tag):
    div_str = str(a.find(tag, class_=html_clss))
    div = bs(div_str,"html.parser")
    return div.text

data = {
    'user_handle' : [],
    'tweet' : [],
    
}
'''  "likes" : []  ,
    "retweets":[],
    "views" : [],
'''
df1 = pd.DataFrame(data)



'''logging in because twitter not work else'''
url= "https://twitter.com/i/flow/login"
#driver = webdriver.Chrome()
driver = webdriver.Firefox()

driver.get(url)
time.sleep(3)


keyboard.type('\t\t\t\t')
keyboard.type(os.environ.get('TWT_USERN'))
keyboard.press(Key.enter)

time.sleep(2)
keyboard.type(os.environ.get('TWT_PSWD'))
driver.find_element(By.XPATH,'//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div/div').click()

time.sleep(3)

with open('url.txt','r') as file:
    urls = file.readlines()


for url in urls:
    driver.get(url)
    time.sleep(4)
    page_end = driver.execute_script("return document.body.scrollHeight;")
    time.sleep(5)

    tweet_div_class = "css-1dbjc4n r-eqz5dr r-16y2uox r-1wbh5a2"
    user_handle_class = "css-4rbku5 css-18t94o4 css-1dbjc4n r-1loqt21 r-1wbh5a2 r-dnmrzs r-1ny4l3l"
    daughter_tweet_class = "css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0"
    main_tweet_class = "css-901oao r-1nao33i r-37j5jr r-1inkyih r-16dba41 r-135wba7 r-bcqeeo r-bnwqim r-qvutc0"
    
    first_iteration = 1
    while True:
        driver.execute_script("window.scrollBy(0, 877);")
        time.sleep(3)
        current_page_end=driver.execute_script("return document.body.scrollHeight;")
        if current_page_end==page_end:
            break
        elif(first_iteration==1):
            '''taking first tweet that is the largest and has diff formatting before scrolling'''
            html = driver.page_source
            data['tweet']=[]
            data['user_handle']=[]
            soup = bs(html,"html.parser")
            for a in soup.find_all('div',class_=tweet_div_class):
                '''user handle logic'''
                data['user_handle'] = scraper(a,user_handle_class,'a')                
                '''tweet logic'''
                if first_iteration==1:
                    data['tweet'] = scraper(a,main_tweet_class,'div')
                    first_iteration = 0
                else:
                    data['tweet'] = scraper(a,daughter_tweet_class,'div')
                '''writes to dataframe'''
                df1 = df1.append(data,ignore_index = True)

            '''after scrolling'''
        elif(first_iteration==0):
            html=driver.page_source
            soup = bs(html,"html.parser")
            data['tweet']=[]
            data['user_handle']=[]
            tempdf = pd.DataFrame(data)
            for a in soup.find_all('div',attrs=tweet_div_class):
                '''user handle logic'''
                data['user_handle'] = scraper(a,user_handle_class,'a')
                '''tweet logic'''
                data['tweet'] = scraper(a,daughter_tweet_class,'div')
                
                tempdf = tempdf.append(data,ignore_index = True)
            '''adds dataframes and removes duplicates'''
            df1=pd.concat([df1,tempdf]).drop_duplicates()
            del tempdf

        page_end = current_page_end

    print(df1)

   
df1.to_csv('file1.csv')
driver.close()