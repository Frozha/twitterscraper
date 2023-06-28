from selenium import webdriver
import time
from bs4 import BeautifulSoup as bs

data = {
    'user_handle' : [],
    'tweet' : [],
    'likes' : [],
    'retweets':[],
    'views' : [],
    'date' : []
}

#url = input("Enter url to scrape : ")
url = "https://twitter.com/skaijackson/status/1671691755450949632?s=20"
driver = webdriver.Chrome()
driver.get(url)

#page_end = input("press enter to continue")  
page_end = driver.execute_script("return document.body.scrollHeight;")
time.sleep(2)

first_iteration = 1
while True:
    driver.execute_script("window.scrollBy(0, 877);")
    time.sleep(1)
    current_page_end=driver.execute_script("return document.body.scrollHeight;")
    if current_page_end==page_end:
        break
    elif(first_iteration==1):
        first_iteration = 0;
        html = driver.page_source
        soup = bs(html,"html.parser")
        for a in soup.find_all('div',attrs="css-1dbjc4n r-eqz5dr r-16y2uox r-1wbh5a2"):
            handle=a.find('div',attrs="css-901oao css-1hf3ou5 r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0")
            if('@' in handle.text):
                data['user_handle'].append(handle.text)
            tweet_div = a.find('div',attrs="css-1dbjc4n r-1s2bzr4")
            print(tweet_div)
            data['tweet'].append(tweet_div.text)

        print(len(data['user_handle']))
    elif(first_iteration==0):
        html=driver.page_source
        soup = bs(html,"html.parser")
        temp = []
        for a in soup.find_all('div',attrs="css-1dbjc4n r-eqz5dr r-16y2uox r-1wbh5a2"):
            j=a.find('div',attrs="css-901oao css-1hf3ou5 r-18u37iz r-37j5jr r-1wvb978 r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0")
            if('@' in j.text):
                temp.append(j.text);
        #print(temp)
        #print(len(temp))
        offset=0
        #for a in range(0,len(temp))
                

        #for b in range(-1,-3):
        #    data['user_handle'].append(temp[b])
    page_end = current_page_end


driver.close()

print(data)