from flask import Flask, request, Response
from flask import render_template
from pymysql import NULL
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from database import Database
from config import schoolCodeDict, MainConfig
from auth import verify, generateJWTtoken

app = Flask(__name__)

#setup jwt
app.config["JWT_SECRET_KEY"] = MainConfig["JWTsecret"]
jwt = JWTManager(app)

@app.route("/")
def hello():
    return "Flask running"

#reCaptcha verify
@app.route("/auth", methods=["POST"])
def authFunction():
    res = request.values.get('token')
    verifyRes = verify(res)
    
    if(not(verifyRes["success"])):
        return "<script>alert('請完成 recaptcha 人機驗證');history.back();</script>"
    
    return generateJWTtoken()

@jwt_required
@app.route("/submit", methods=['POST'])
def submit():
    # 建立資料庫控制器
    d = Database("Main")

    # 檢查學校代碼
    schoolCode = request.values.get('schoolCode')
    if(schoolCode not in schoolCodeDict):
        schoolCode = NULL
        return "<h1>學校代碼錯誤</h1><br>請聯絡開發人員 code=" + request.values.get('schoolCode')
    else:
        schoolCode = schoolCodeDict[request.values.get('schoolCode')]
        print(request.values.get('stuId'))

    # 檢查學號是否重複，並且防止SQL注入
    result = d.checkStuId(request.values.get('stuId'), schoolCode)

    if(result and (request.values.get('stuId') != MainConfig["bypassCode"])):
        return "<h1>感謝您，已經填寫過囉~</h1>"
        # return request.values.get('stuId')

    # 建立資料
    data = {
        "stuId": request.values.get('stuId'),
        "school": schoolCode,
        "sex": request.values.get('sex'),
        "grade": request.values.get('grade'),
        "department": request.values.get('dept'),
        "Q1": request.values.get('Q1'),
        "Q2": request.values.get('Q2'),
        "Q3": request.values.get('Q3'),
        "Q4": request.values.get('Q4'),
        "Q5": request.values.get('Q5'),
        "Q6": request.values.get('Q6'),
        "Q7": request.values.get('Q7'),
    }

    # 寫入資料庫
    d.insertDict(data)
    d.closeDB()

    return "<h1>感謝您的填寫!</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=MainConfig["port"])
