import json, requests

class email_verifier:
    def __init__(self) -> None:
        self.key = ""
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        self.proxyless = False
        self.threads = 1
        self.session = requests.Session()
        self.proxy = ""

    def _cookies(self):
        s = requests.Session()
        s.get("https://discord.com")
        cookies = s.cookies.get_dict()
        all = []
        for cookie in cookies:
            real = cookies.get(cookie)
            all.append("{}={}".format(cookie, real))
        s.close()
        return all
        
    def headers(self, token):
        fingerprint = self.session.get("https://discord.com/api/v9/experiments").json()["fingerprint"]
        cookies = self._cookies()
        __dcfduid, __sdcfduid, __cfruid = cookies[0], cookies[1], cookies[2]
        headers: dict = {
            "accept": "*/*",
            'accept-encoding': 'gzip, deflate',
            "accept-language": "en-US,en;q=0.9",
            "authorization": token,
            "cookie": f'{__dcfduid}; {__sdcfduid}; {__cfruid}; locale=en-US',
            'origin': "https://discord.com",
            'referer': "https://discord.com/channels/@me",
            'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
            'sec-ch-ua-mobile': "?0",
            'sec-ch-ua-platform': '"Windows"',    
            "sec-fetch-dest": 'empty',
            "sec-fetch-mode": 'cors',
            "sec-fetch-site": 'same-origin',
            "user-agent": self.user_agent,
            'x-debug-options': 'bugReporterEnabled',
            'x-discord-locale': 'en-US',
            'x-fingerprint': fingerprint,
            'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiQ2hyb21lIiwiZGV2aWNlIjoiIiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiYnJvd3Nlcl91c2VyX2FnZW50IjoiTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzEwNi4wLjAuMCBTYWZhcmkvNTM3LjM2IiwiYnJvd3Nlcl92ZXJzaW9uIjoiMTA2LjAuMC4wIiwib3NfdmVyc2lvbiI6IjEwIiwicmVmZXJyZXIiOiJodHRwczovL2R5bm8uZ2cvIiwicmVmZXJyaW5nX2RvbWFpbiI6ImR5bm8uZ2ciLCJyZWZlcnJlcl9jdXJyZW50IjoiIiwicmVmZXJyaW5nX2RvbWFpbl9jdXJyZW50IjoiIiwicmVsZWFzZV9jaGFubmVsIjoic3RhYmxlIiwiY2xpZW50X2J1aWxkX251bWJlciI6MTUwNDg5LCJjbGllbnRfZXZlbnRfc291cmNlIjpudWxsfQ=='
            }
        return headers
        

    def add_email(self, mail, headers):
        payload = {
            'email': mail,
            'email_token': None,
            'bio': "Developed by hoku <3",
            "password": "Hokuine<321@"
            }
        headers["Content-Length"] = str(len(json.dumps(payload)))
        r = self.session.patch("https://discord.com/api/v9/users/@me", json=payload, headers=headers)
        if r.status_code == 200:
            return True, r.json()["token"]
        else:
            print(f"Error: {r.json()}")
            return False

    def get_mail(self) -> str:
        r = self.session.get(f"http://api.kopeechka.store/mailbox-get-email?site=discord.com&mail_type=hotmail.com&token={self.key}&api=2.0").json()
        if r["status"] == "OK":
            task = r["id"]
            mail = r["mail"]
            print(f"got mail {mail}")
            return task, mail

    def get_verify_token(self, task):
        r = self.session.get(f"http://api.kopeechka.store/mailbox-get-message?full=$FULL&id={task}&token={self.key}&&api=2.0").json()
        if r["status"] == "OK":
            url = r["value"]
            r = self.session.get(url, allow_redirects=True, timeout=None).url
            token = r.replace("https://discord.com/verify#token=", "")
            return token
        
    def verify_mail(self, verify_token, headers):
        payload = {
        'captcha_key': "",
        'token': verify_token
        }
        headers['Content-Length'] = str(len(json.dumps(payload)))
        r = self.session.post("https://discord.com/api/v9/auth/verify", json=payload, headers=headers)
        print(r.json())
        if r.status_code == 200:
            return True
        else:
            return False

    def main(self, token):
        task, mail = self.get_mail()
        headers = self.headers(token)
        a, TOKEN = self.add_email(mail, headers)
        if a:
            headers.pop("authorization")
            headers["authorization"] = TOKEN
            verify_token = self.get_verify_token(task)
            if self.verify_mail(verify_token, headers):
                print(f"verified token {token}")

s = email_verifier()
s.main("MTA0MDA4MDg5MTk4MjExODk0Mg.Go7H1C.t3TP19ImlBjuHRtDsw6PR0LA9kMHXyuNMxLNts")
