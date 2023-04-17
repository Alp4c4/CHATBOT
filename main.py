import json
import os
from flask import Flask, make_response, request
from flask import request
from flask import make_response
import requests
import datetime
####################
from linebot import (
    LineBotApi, WebhookHandler,
)
###################################
lineaccesstoken = 'AE3nyFWyOAPMb7XmIjx/dXlFurdfhez3IJ34et7hLsRduBzDkeB7oDb2vntVLdiwav2K033FVNs4uIEiRslvU99/2gUxYK7WUAZ6ytOVXgTYSXp1mDZ6KWSlsnoQJgBzjMaT9XHwToLnAH0I2XiI3AdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)
handler = WebhookHandler('cf3954fc20dc1f7221437b5f0b811e85')
###################################
from random import randint
import firebase_admin
from firebase_admin import credentials,storage
from firebase_admin import firestore 
cred=credentials.Certificate("depreesion-4eb38-firebase-adminsdk-r6lnp-402912a06a.json")
firebase_admin.initialize_app(cred,{'storageBucket':'gs://depreesion-4eb38.appspot.com'})
##################################
g_r=0
urname=''
urlastname=''
emotion=0
bucket=storage.bucket()
#############################
db = firestore.client()
collection=db.collection('User')
app = Flask(__name__)
@app.route('/',methods=['POST']) 
def MainFunction():
    #รับ intent จาก Dailogflow
    data_from_dialogflow_raw = request.get_json(silent=True, force=True)
    #เรียกใช้ฟังก์ชัน generate_answer เพื่อแยกส่วนของคำถาม
    answer_from_bot = generating_answer(data_from_dialogflow_raw)
    #ตอบกลับไปที่ Dailogflow
    r = make_response(answer_from_bot)
    r.headers['Content-Type'] = 'application/json' #การตั้งค่าประเภทของข้อมูลที่จะตอบกลับไป
    return r
def generating_answer(data_from_dialogflow_dict):
    user_Id=data_from_dialogflow_dict["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    response_id=data_from_dialogflow_dict["responseId"]
    user_text = data_from_dialogflow_dict["queryResult"]["queryText"]
    #Print intent  ที่รับมาจาก dialogflow
    print(json.dumps(data_from_dialogflow_dict, indent=4 ,ensure_ascii=False))
    #เก็บค่าชื่อของintentที่รับมาจากdialogflow
    intent_group_question_str=data_from_dialogflow_dict["queryResult"]["intent"]["displayName"]
    #ลูปตัวเลือกของฟังชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str=="เก็บข้อมูล":
       answer_str=user_info(data_from_dialogflow_dict)
    elif intent_group_question_str=="start_con":
        global g_r 
        g_r =0
    elif intent_group_question_str=="ดูผลการประเมิน":
        status=cal_Score()
        update_status(status,data_from_dialogflow_dict)
        update_date_and_status(data_from_dialogflow_dict,status)
        update_data(data_from_dialogflow_dict)
        answer_str=notifyPic(check_respone(status))
    elif intent_group_question_str=="ผลการประเมินย้อนหลัง":
        check= recheck(data_from_dialogflow_dict)
        answer_str=notifyPic(check_respone(check))
    elif intent_group_question_str=="คำแนะนำ1":
        url=check_advice(data_from_dialogflow_dict)
        answer_str=notifyPic(url)
    elif intent_group_question_str=="ยินยอม2":
          answer_str=user_info(data_from_dialogflow_dict)
    # elif intent_group_question_str=="ลอง":
    #       answer_str=upround()
    elif intent_group_question_str=="ดูการประเมินย้อนหลัง":
          answer_str
################################################
    elif intent_group_question_str=="ไม่เคยคิดทำร้ายตัวเอง":
        loop_check(0)
        add_status('hurt yourself','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่ทำอะไรช้าลง":
        loop_check(0)
        add_status('do slow','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่เคยคิดว่าตัวเองล้มเหลว":
        loop_check(0)
        add_status('myself','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่หลับยาก":
        loop_check(0)
        add_status('sleep','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่เบื่อ":
        loop_check(0)
        add_status('bored','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่เบื่ออาหาร":
        loop_check(0)
        add_status('meal','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่มีเรื่องเครียด":
        loop_check(0)
        add_status('concern','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่เหนื่อยง่าย":
        loop_check(0)
        add_status('tired','ไม่เคย',data_from_dialogflow_dict)
    elif intent_group_question_str=="ไม่ไม่มีสมาธิ":
        loop_check(0)
        add_status('concentration','ไม่เคย',data_from_dialogflow_dict)
###########
    elif intent_group_question_str=="มีบ้าง_คิดทำร้ายตัวเอง":
        loop_check(1)
        add_status('hurt yourself','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_ทำอะไรช้าลง":
        loop_check(1)
        add_status('do slow','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_รู้สึกไม่ดีกับตัวเอง":
        loop_check(1)
        add_status('myself','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_หลับยาก":
        loop_check(1)
        add_status('sleep','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_เบื่อ":
        loop_check(1)
        add_status('bored','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_เบื่ออาหาร":
        loop_check(1)
        add_status('meal','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_เรื่องเครียด":
        loop_check(1)
        add_status('concern','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_เหนื่อยง่าย":
        loop_check(1)
        add_status('tired','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีบ้าง_ไม่มีสมาธิ":
        loop_check(1)
        add_status('concentration','มีบ้าง',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_คิดทำร้ายตัวเอง":
        loop_check(2)
        add_status('hurt yourself','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_ทำอะไรช้าลง":
        loop_check(2)
        add_status('do slow','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_รู้สึกไม่ดีกับตัวเอง":
        loop_check(2)
        add_status('myself','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_หลับยาก":
        loop_check(2)
        add_status('sleep','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_เบื่อ":
        loop_check(2)
        add_status('bored','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_เบื่ออาหาร":
        loop_check(2)
        add_status('meal','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_เรื่องเครียด":
        loop_check(2)
        add_status('concern','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_เหนื่อยง่าย":
        loop_check(2)
        add_status('tired','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีค่อนข้างบ่อย_ไม่มีสมาธิ":
        loop_check(2)
        add_status('concentration','มีค่อนข้างบ่อย',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_คิดทำร้ายตัวเอง":
        loop_check(3)
        add_status('hurt yourself','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_ทำอะไรช้าลง":
        loop_check(3)
        add_status('do slow','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_รู้สึกไม่ดีกับตัวเอง":
        loop_check(3)
        add_status('myself','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_หลับยาก":
        loop_check(3)
        add_status('sleep','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_เบื่อ":
        loop_check(3)
        add_status('bored','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_เบื่ออาหาร":
        loop_check(3)
        add_status('meal','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_เรื่องเครียด":
        loop_check(3)
        add_status('concern','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_เหนื่อยง่าย":
        loop_check(3)
        add_status('tired','มีเกือบทุกวัน',data_from_dialogflow_dict)
    elif intent_group_question_str=="มีเกือบทุกวัน_ไม่มีสมาธิ":
        loop_check(3)
        add_status('concentration','มีเกือบทุกวัน',data_from_dialogflow_dict)
    # else :
    #     answer_str= "เราไม่เข้าใจ"
    answer_from_bot ={"fulfillmentMessages":answer_str}
            
                    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    print(answer_from_bot)
    return answer_from_bot
def check_advice(answer):
    answer=answer["queryResult"]["queryText"]
    if answer=='ท้อแท้':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/1.jpg?alt=media&token=78cafbeb-4462-4bbe-89aa-9b76dd211874'
    elif answer=='เรื่องที่ไม่สบายใจ':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/2.jpg?alt=media&token=f03dc04a-601a-44d4-b862-38e535858ad1'
    elif answer=='เบื่ออาหาร':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/3.jpg?alt=media&token=052465db-5a33-4747-9192-2d64e152aaed'
    elif answer=='หลับยาก':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/4.jpg?alt=media&token=d99b4767-6032-4996-8386-7c18c252fc7b'
    elif answer=='เบื่อ':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/5.jpg?alt=media&token=b2ef8ab1-4401-4b70-90c3-b9772f12d3f6'
    elif answer=='ไม่มีสมาธิ':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/6.jpg?alt=media&token=6a43f9d1-84ac-44ec-82cc-320c775a54c9'
    elif answer=='ทำอะไรช้าลง':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/7.jpg?alt=media&token=cda2aca2-173e-47c4-bce8-712402a3d29a' 
    elif answer=='รู้สึกไม่ดีกับตัวเอง':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/8.jpg?alt=media&token=533b6c61-3233-4c10-9cf1-22f993ff70a6'
    elif answer=='คิดทำร้ายตัวเอง':
        photo_url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/9.jpg?alt=media&token=ae9d91c7-d48c-49dc-803c-102fdaa3415a'
    return photo_url
def update_status(status,data):
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{user_Id}').update({
        u'status':status
    }) 
###################################################
def user_info(data):
    username=data["queryResult"]["outputContexts"][1]["parameters"]["firstname"]
    lastname=data["queryResult"]["outputContexts"][1]["parameters"]["lastname"]
    nickname=data["queryResult"]["outputContexts"][1]["parameters"]["nickname1"]
    age=data["queryResult"]["outputContexts"][1]["parameters"]["number"]
    gender=data["queryResult"]["outputContexts"][1]["parameters"]["gender"]
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{user_Id}').set({
        u'username':username,
        u'userlastname':lastname,
        u'usernickname':nickname,
        u'age':age,
        u'gender':gender,
        u'userId':user_Id,
        u'round':"1",
        u'status':""
    }) 
    doc_ref = db.collection('User').document(f'{user_Id}')
    sub_collection_ref = doc_ref.collection('รอบในการทำประเมิน')
    sub_collection_ref.document(f'1').set({
        u'tired':"",
        u'sleep':"",
        u'concern':"",
        u'myself':"",
        u'concentration':"",
        u'doslow':"",
        u'hurtyourself':"",
        u'bored':"",
        u'meal':"",
        u'status':"",
        u'datetime':""
    })
    return 'บันทึกข้อมูลเสร็จสิ้น'
def update_data(data):
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    doc_ref = db.collection('User').document(f'{user_Id}')
    sub_collection_ref = doc_ref.collection('รอบในการทำประเมิน')
    doc=collection.document(user_Id)
    res=doc.get().to_dict()
    resp=res['round']
    resp=int (resp)+1
    db.collection('User').document(f'{user_Id}').update({
        u'round':resp
    })
    sub_collection_ref.document(f'{resp}').set({
        u'tired':"",
        u'sleep':"",
        u'concern':"",
        u'myself':"",
        u'concentration':"",
        u'doslow':"",
        u'hurtyourself':"",
        u'bored':"",
        u'meal':"",
        u'status':"",
        u'datetime':""
    })  
def update_date_and_status(data,status):
    status=status
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    doc_ref = db.collection('User').document(f'{user_Id}')
    sub_collection_ref = doc_ref.collection('รอบในการทำประเมิน')
    doc=collection.document(user_Id)
    res=doc.get().to_dict()
    resp=res['round']
    now=datetime.datetime.now()
    formatted_date=now.strftime("%d/%m/%Y")
    sub_collection_ref.document(f'{resp}').update({
        u'status':status,
        u'datetime':formatted_date
    })  

#########################################
def notifyPic(url):  
    reply=[{"image":{"imageUri":url},"platform": "LINE"}]
    return reply
# def upround(data):#this function make  
#     user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
#     doc_ref = db.collection('User').document(f'{user_Id}')
#     res=doc_ref.get().to_dict()
#     resp=res['round']
#     resp=resp+1
#     db.collection('User').document(f'{user_Id}').update({
#         u'round':resp
#     })
def loop_check(data)  :
    global g_r
    g_r=g_r+data
    print(g_r)
def cal_Score():   
    global g_r
    score= g_r
    if score<7:
        sum="ไม่มีอาการของโรคซึมเศร้าหรือมีอาการของโรคซึมเศร้าในปริมาณน้อย"
    elif 7<=score<=12:
        sum="ระดับน้อย"
    elif 13<=score<=18:
        sum="ระดับปานกลาง"
    elif score>=19:
        sum="ระดับรุนแรง" 
    g_r=0
    return sum
def check_respone(answer):
    if answer =="ไม่มีอาการของโรคซึมเศร้าหรือมีอาการของโรคซึมเศร้าในปริมาณน้อย":    
        url= 'https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/normal.png?alt=media&token=bb8998dd-1c5a-4c99-8ff9-23cc3e765763',
    elif answer =="ระดับน้อย":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/little.png?alt=media&token=6417a605-ce7a-4875-849f-2feeadebb866',
    elif answer =="ระดับปานกลาง":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/medium.png?alt=media&token=b49c9e52-acd4-402e-9630-0d37c9d4ab2b'
    elif answer =="ระดับรุนแรง":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/severe.png?alt=media&token=53678518-9998-440e-be1e-76401383aed8',    
    return url
def recheck(data):
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    doc=collection.document(user_Id)
    res=doc.get().to_dict()
    resp=res['status']
    return resp
#######################################
def add_status(topic,status,data):
    topic=topic
    status=status
    ######
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    doc_ref = db.collection('User').document(f'{user_Id}')
    sub_collection_ref = doc_ref.collection('รอบในการทำประเมิน')
    doc=collection.document(user_Id)
    res=doc.get().to_dict()
    resp=res['round']
   
    ######
    if  topic=='tired':
        sub_collection_ref.document(f'{resp}').update({
        u'tired':status,
    })
    elif topic=='sleep':
        sub_collection_ref.document(f'{resp}').update({
        u'sleep':status,
    })
    elif topic=='concern':
        sub_collection_ref.document(f'{resp}').update({
        u'concern':status,
    })
    elif topic=='myself':
        sub_collection_ref.document(f'{resp}').update({
        u'myself':status,
    })
    elif topic=='concentration':
        sub_collection_ref.document(f'{resp}').update({
        u'concentration':status,
    })
    elif topic=='do slow':
        sub_collection_ref.document(f'{resp}').update({
        u'doslow':status,
    })
    elif topic=='hurt yourself':
        sub_collection_ref.document(f'{resp}').update({
        u'hurtyourself':status,
    })
    elif topic=='bored':
        sub_collection_ref.document(f'{resp}').update({
        u'bored':status,
    })
    elif topic=='meal':
        sub_collection_ref.document(f'{resp}').update({
        u'meal':status,
    })
######################################################################################
if __name__ == '__main__':
    app.run(debug='True')

