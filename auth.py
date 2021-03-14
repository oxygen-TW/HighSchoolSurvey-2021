import requests
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity

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

#TODO 需加入identity
def generateJWTtoken(_identityTime):
    access_token = create_access_token(identity=_identityTime)
    return access_token