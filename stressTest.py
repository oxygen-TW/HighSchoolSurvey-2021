import requests

url = "http://web.oxygentw.net:3000/submit"

#模擬請求進行壓力測試
for i in range(1,500):
    data = {
        "g-recaptcha-response": "JustTest",
        "schoolCode": "dev",
        "stuId": str(i)
    }

    r = requests.post(url, data=data)
    print(str(i) + " => " + str(r.status_code))