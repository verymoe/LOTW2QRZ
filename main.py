import requests
from bs4 import BeautifulSoup
import pyotp
import re
import os

# 用户配置
USERNAME = os.getenv("USERNAME")  # QRZ用户名
PASSWORD = os.getenv("PASSWORD") # QRZ密码
SECRET = os.getenv("SECRET")  # TOTP密钥
BID = os.getenv("BID")  # QRZ日志薄ID
LOTW_PW = os.getenv("LOTW_PW")  # LOTW密码

UserAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
login_headers = {
    "User-Agent": UserAgent,
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "XMLHttpRequest",
}

# 初始化会话
session = requests.Session()
response = session.get("https://www.qrz.com/login")
soup = BeautifulSoup(response.text, 'html.parser')

script_text = ''.join(script.text for script in soup.find_all('script') if 'loginTicket' in script.text)
match = re.search(r"loginTicket': '([a-zA-Z0-9]+)'", script_text)
login_ticket = match.group(1) if match else None

# 第一步：提交用户名
step1_data = {
    'loginTicket': login_ticket,
    'username': USERNAME,
    'step': 1
}
response_step1 = session.post('https://www.qrz.com/login-handshake', headers=login_headers, data=step1_data)
response_step1_data = response_step1.json()

# 第二步：提交密码（和二次验证代码，如果需要）
step2_data = {
    'loginTicket': login_ticket,
    'username': USERNAME,
    'password': PASSWORD,
    'step': 2
}

response_step2 = session.post('https://www.qrz.com/login-handshake', headers=login_headers, data=step2_data)
response_step2_data = response_step2.json()

totp = pyotp.TOTP(SECRET)
otp_code = totp.now()
two_factor_data = {
    "login_ref": "https://www.qrz.com/",
    "username": USERNAME,
    "password": PASSWORD,
    "2fcode": otp_code,
    "target": "/",
    "flush": "1"
}
response_step3 = session.post("https://www.qrz.com/login", headers=login_headers, data=two_factor_data)

url = f"https://logbook.qrz.com?op=lotw_get_all&bid={BID}&lotw_pw={LOTW_PW}&sbook=0&lotw_dl_type=new"
lotw_response = session.get(url, headers=login_headers)
print(lotw_response.text)
