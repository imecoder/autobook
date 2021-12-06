
import requests
#
# url = 'https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp'
# # url = 'www.baidu.com'
# response = requests.get(url)
# print(response.text)

import requests
print('访问baidu网站 获取Response对象')
r = requests.get("https://www.sellingplatformconnect.amadeus.com/LoginService/login.jsp")
print(r.status_code)
print(r.encoding)
print(r.apparent_encoding)
print('将对象编码转换成UTF-8编码并打印出来')
r.encoding = 'utf-8'
print(r.text)
