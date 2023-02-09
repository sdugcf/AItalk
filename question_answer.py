import os
import numpy as np
import requests
import json
import sdu_news


def access_token_get():


    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=GxQOGlNeXZ25EF7EPA3h3XPE&client_secret=hGuMCnQgXiiSKEexKtiGxLp7MnCX9YW7'
    payload = {}
    headers = {}

    r = requests.request("POST", url, headers=headers, data=payload)
    token=json.loads(r.text)['access_token']
    return token


def ask_question(token,t_id,s_id,l_id,query):
    url = "https://aip.baidubce.com/rpc/2.0/unit/service/v3/chat?access_token="+token
    payload = json.dumps({
        "service_id": "S78508",
        "log_id": ""+l_id,
        "session_id": ""+s_id,
        "request": {
            "query": ""+query,
            "terminal_id": ""+t_id,
            "query_info": {
                "type": "TEXT"
            }
        },
        "version": "3.0"
    })
    headers = {
        'Content-Type': 'text/plain'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.text



def answer(x,question,token,t_id='001', s_id="", l_id="S001"):
    if 3 not in x and 4 not in x and 5 not in x:
         a=answer1(x,question,token,t_id, s_id, l_id)
         return a
    elif 1 not in x and 2 not in x:
         a=answer2(question)
         return a
    else:
        a1=answer1(x,question,token,t_id, s_id, l_id)
        a2=answer2(question)
        a=a1+a2
        return a





if __name__ == "__main__":
    # 先读取token
    with open("/root/Dev/ALGO/token.txt", "r") as f:  #
     token = f.read()
    question=input("您好，智能校园问答系统为您服务，请问您有什么想问的呢？")
    #获取关键词
    key=key_word(question)
    #return 返回答案，文字答案均为列表格式，还需进一步处理
    a=answer(key,question,token)
    print(a)