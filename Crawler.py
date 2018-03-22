import requests
from bs4 import BeautifulSoup
import random
import tesserocr
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

session = requests.Session()
url_login='http://ecard.neu.edu.cn/SelfSearch/Login.aspx'
resp_login_page = session.get(url=url_login)
soup_login_page = BeautifulSoup(resp_login_page.text, 'html.parser')
VIEWSTATE= soup_login_page.find(id="__VIEWSTATE")['value']
EVENTVALIDATION= soup_login_page.find(id="__EVENTVALIDATION")['value']
# 获得验证码的url，你需要写一行,提示：你可能需要随机数函数
url_captcha='http://ecard.neu.edu.cn/SelfSearch/validateimage.ashx?' + str(random.random())
#向该链接发送get请求，并获取Response对象，你需要写一行
resp_captcha = requests.get(url=url_captcha)
with open('captcha.gif', 'wb') as f:
    f.write(resp_captcha.content)
    f.close()
img = mpimg.imread('captcha.gif')
plt.imshow(img)
image = Image.open('captcha.gif')
captcha_code=tesserocr.image_to_text(image)
print(captcha_code)
captcha=captcha_code
userName = 20175364
passwd=235956

postdata = {
    "_LASTFOCUS": '',
    "__EVENTTARGET": 'btnLogin',
    "__EVENTARGUMENT":'',
    "__VIEWSTATE":VIEWSTATE,
    "__EVENTVALIDATION":EVENTVALIDATION,
    "txtUserName":userName,
    "txtPassword":passwd,
    "txtVaildateCode":captcha,
    "hfIsManager":0
}
url_login ="http://ecard.neu.edu.cn/SelfSearch/login.aspx"
loginresponse = session.post(url=url_login,data=postdata)
print('跳转的链接：', loginresponse.url)
# 自己找消费记录是向哪个url请求的
url_consumeInfo='http://ecard.neu.edu.cn/SelfSearch/User/ConsumeInfo.aspx'

#获取页面
consume_response0=session.get(url_consumeInfo)
consume_soup = BeautifulSoup(consume_response0.text, 'html.parser')

#解析出以下两个变量的值
VIEWSTATE=consume_soup.find(id="__VIEWSTATE")['value']
EVENTVALIDATION=consume_soup.find(id="__EVENTVALIDATION")['value']
#构造postdata
postdata_consume = {
    "__EVENTTARGET":'ctl00$ContentPlaceHolder1$AspNetPager1' ,
    "__EVENTARGUMENT":"3", 
    "__VIEWSTATE":VIEWSTATE,
    "__EVENTVALIDATION":EVENTVALIDATION,
    "ctl00$ContentPlaceHolder1$rbtnType": 0,
    "ctl00$ContentPlaceHolder1$txtStartDate": '2018-03-15',
    "ctl00$ContentPlaceHolder1$txtEndDate": '2018-03-22',
    "ctl00$ContentPlaceHolder1$btnSearch": '查  询'
}

resp_consume_1=session.post(url_consumeInfo,data=postdata_consume)
soup_consume_1=BeautifulSoup(resp_consume_1.text, 'html.parser')

info_table=soup_consume_1.table
for i in range(5):
    print((list(info_table.find_all(class_="RowStyle")))[i].text)
    print(list(info_table.find_all(class_="AltRowStyle"))[i].text)
