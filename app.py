from flask import Flask, request, Response
from flask import render_template

from database import Database
from config import schoolCodeDict, MainConfig

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello Flask!"


@app.route("/submit", methods=['POST'])
def submit():
    # 建立資料庫控制器
    d = Database("Main")

    # 檢查學號是否重複，並且防止SQL注入
    result = d.checkStuId(request.values.get('stuId'))
    if(result == -1):
        return Response(status=403)

    if(d.checkStuId(request.values.get('stuId'))):
        return "<h1>感謝您，已經填寫過囉~</h1>"
        # return request.values.get('stuId')

    data = {
        "stuId": request.values.get('stuId'),
        "school": schoolCodeDict[request.values.get('schoolCode')],
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
    d.insertDict(data)
    d.closeDB()

    return "<h1>感謝您的填寫!</h1>"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=MainConfig["port"])
