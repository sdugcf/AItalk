from flask import Flask, request
from flask_cors import CORS
import requests
import json
import os
import sys






app = Flask(__name__)
CORS(app, supports_credentials=True)



@app.route('/login', methods=['POST', 'GET'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    x =DB.Judge(username,'username', 'passwd','img','id')
    print(x)
    if x['code'] == 4002:
        return x
    else:
        if x['msg'][0] == password:
            return x
        else:
            return {
            'code': 4001,
            'msg': '密码错误'
            }




@app.route('/signup', methods=['POST'])
def signup():
    username = request.json.get('username')
    password = request.json.get('password')
    mibao_question = request.json.get('mibao_question')
    mibao_answer = request.json.get('mibao_answer')
    img = ''

    judge_username_exist = DB.Register_judge(username, 'username')
    if judge_username_exist['code'] == 0:
        return {
            'code': 4003,
            'msg': '用户名已存在'
        }
    else:
        DB.InserttDB(username, password, img, mibao_question, mibao_answer)
        secret_information = DB.Get_security_information(username, 'username', 'mibaoQ', 'mibaoA', 'passwd', 'id')
        t_id = secret_information['msg'][3]
        return {
            'code': 0,
            'msg': {
                'msg': '注册成功',
                't_id': t_id
                }
        }



@app.route('/pwdforget', methods=['POST'])
def pwdforget():
    username = request.json.get('username_secret')
    mibao_answer = request.json.get('mibao_answer')
    secret_information = DB.Get_security_information(username, 'username', 'mibaoQ', 'mibaoA', 'passwd', 'id')
    mibaoQ = secret_information['msg'][0]
    mibaoA = secret_information['msg'][1]
    passwd = secret_information['msg'][2]
    t_id = secret_information['msg'][3]
    print(secret_information)
    if not mibao_answer:
            if secret_information['code'] == 4002:
                return secret_information
            if secret_information['code'] == 0:
                return {
                    'code': 0,
                    'msg': {
                        'mibao_question': mibaoQ
                    }
                }

    if mibao_answer:
        if secret_information['code'] == 0:
            if mibao_answer == mibaoA:
                return {
                    'code': 0,
                    'msg': {
                        'passwd': passwd,
                        't_id': t_id
                    }
                }
            if mibao_answer != mibaoA:
                return {
                    'code': 4005,
                    'msg': '答案错误'
                }




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
