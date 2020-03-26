import urllib.request
import http.cookiejar
import requests
import os
import json

def request_cookies(username, password):
    """
        login and get the cookies
    """
    # login url
    url = 'https://odinro.online/account/login/?return_url='
    data = {
        'username': username,
        'password': password,
        'server': 'OdinRO',
    }
    post_data = urllib.parse.urlencode(data).encode('utf-8')
    headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

    req = urllib.request.Request(url, data = post_data)

    cookies = http.cookiejar.CookieJar()

    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))

    resp = opener.open(req)

    text = resp.read().decode('utf-8')

    if '登出' in text:
        return requests.utils.dict_from_cookiejar(cookies)
    else:
        raise Exception("request_cookies fail check for 'username' nad 'password'")

def get_cookies(username, password):
    """
        read local file to get cookies or requests_cookie
    """
    if os.path.isfile('cookies.json'):
        with open('cookies.json', 'r') as f:
            cookies = json.load(f)
        print('read cookies: {} from cookies.json'.format(cookies))
        if check_cookies(cookies):
            return cookies
        else:
            print('existing cookies fail')
            
    print('requesting cookies')
    cookies = request_cookies(username, password)
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
    print('save cookies: {} at cookies.json'.format(cookies))

    return cookies

def check_cookies(cookies):
    """
        send request to url that require login to validate the cookies
    """
    # url that require login
    url = 'https://odinro.online/item/?&equip_loc=-1/'

    resp = requests.get(url = url, cookies = cookies)

    if '登出' in resp.text:
        return True
    else:
        return False

if __name__ == "__main__":
    username = '2064162186'
    password = 'king88628'


    try:
        cookies = get_cookies(username, password)
    except Exception as e:
        print(e)
        exit()

    # print(check_cookies(username, password, cookies))