import requests

def get_response_cookie(set_cookies) :
    cookie = {}
    for coo in set_cookies:
        data = coo.split(';')[0]
        key = data.split('=')[0]
        value = data[data.find('=')+1:]
        cookie[key] = value

    return cookie


url = "https://accounts.havail.sabre.com/login/srw"

querystring = {"goto":"https://srw.sabre.com/login/login.html?force=true"}

payload = ""
headers = {
    'cache-control': "no-cache",
    'Postman-Token': "d40accb4-359c-4c4f-9af8-67096c1b5b36"
    }

thesession = requests.session()

response = thesession.request("GET", url, data=payload, headers=headers, params=querystring)

print(response.raw.headers.getlist('Set-Cookie'))
set_cookie = response.raw.headers.getlist('Set-Cookie')
cookie = get_response_cookie(set_cookie)

lines = response.text.split('\n')
for line in lines:
    if '<input type="hidden" name="_csrf" value="' in line:
        csrf = line.split('value="')[1].split('" /></form>')[0]
        print('csrf=' + csrf)

# print(response.text)

url = "https://accounts.havail.sabre.com/login/srw"

payload = "goto=https%3A%2F%2Fsrw.sabre.com%2Flogin%2Flogin.html%3Fts%3D555880&siteId=srw&userId=1004&password=1A2B3C4D&group=2Q4J&_csrf=" + csrf + "&undefined="

cookie_str = ''
for key in cookie:
    cookie_str += (key + '=' + cookie[key] + '; ')

headers = {
    'Content-Type': "application/x-www-form-urlencoded",
    'cache-control': "no-cache",
    'Cookie' : cookie_str
    }

print(headers)
print(payload)

new_response = thesession.request("POST", url, data=payload, headers=headers)
print(new_response.raw.headers.getlist('Set-Cookie'))
