import requests
from bs4 import BeautifulSoup
import pyotp
import re
import os

DEBUG = False

# 用户配置
USERNAME = os.getenv("USERNAME")  # QRZ用户名
PASSWORD = os.getenv("PASSWORD") # QRZ密码
SECRET = os.getenv("SECRET")  # TOTP密钥
BID = os.getenv("BIT")  # QRZ日志薄ID
LOTW_PW = os.getenv("LOTW_PW")  # LOTW密码
DEBUG = os.getenv("DEBUG")

UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"

session = requests.Session()
response = session.get("https://www.qrz.com/login")
soup = BeautifulSoup(response.text, 'html.parser')

script_text = ''.join(script.text for script in soup.find_all('script') if 'loginTicket' in script.text)
match = re.search(r"loginTicket': '([a-zA-Z0-9]+)'", script_text)
login_ticket = match.group(1)

print(f"获取的loginTicket: {login_ticket}")

login_headers = {
    "User-Agent": UserAgent,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
}
login_data = {
    "loginTicket": login_ticket,
    "username": USERNAME,
    "password": PASSWORD,
    "step": "1"
}
response = session.post("https://www.qrz.com/login-handshake", headers=login_headers, data=login_data)
json_response = response.json()


def sync_lotw():
    url = f"https://logbook.qrz.com?op=lotw_get_all&bid={BID}&lotw_pw={LOTW_PW}&sbook=0&lotw_dl_type=new"
    if DEBUG:
        print(url)
    lotw_response = session.get(url)
    # 检查响应
    if lotw_response.status_code == 200:
        print("请求成功，响应内容：")
        print(lotw_response.text)
    else:
        print(f"请求失败，状态码：{lotw_response.status_code}")
        print(lotw_response.text)


if json_response.get('twofactor', True):
    totp = pyotp.TOTP(SECRET)
    otp_code = totp.now()
    print(f"当前生成的二步验证代码: {otp_code}")

    two_factor_data = {
        "login_ref": "https://www.qrz.com/",
        "username": USERNAME,
        "password": PASSWORD,
        "2fcode": otp_code,
        "target": "/",
        "flush": "1"
    }
    response = session.post("https://www.qrz.com/login", headers=login_headers, data=two_factor_data)

    if 'Authentication Code Was Not Valid' in response.text:
        print("登录失败：二步验证代码无效。")
    else:
        print("登录成功！")
        sync_lotw()

else:
    print("不需要二步验证，直接登录成功！")
    sync_lotw()
