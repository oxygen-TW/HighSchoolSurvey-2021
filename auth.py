import requests

from config import MainConfig

def verify(res):
    secret = MainConfig["secret"]
    baseApi = "https://www.google.com/recaptcha/api/siteverify"

    data = {
        "secret": secret,
        "response": res
    }

    r = requests.post(baseApi, data=data)
    return r.json()