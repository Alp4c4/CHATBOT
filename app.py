import json
import os
from flask import Flask, make_response, request
from flask import request
from flask import make_response
import requests
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
emotion=0
bucket=storage.bucket()
#############################
db = firestore.client()
collection=db.collection('User')
app = Flask(__name__)
@app.route('/', methods=['POST']) 
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
    if intent_group_question_str=="พร้อม2":
        global g_r
        g_r=0
        loop_check(data_from_dialogflow_dict)         
    elif intent_group_question_str=="พร้อม3":
        loop_check(data_from_dialogflow_dict)            
    elif intent_group_question_str=="พร้อม4":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม5":
        loop_check(data_from_dialogflow_dict)                 
    elif intent_group_question_str=="พร้อม6_":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม7_":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม8_":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม9_":
        loop_check(data_from_dialogflow_dict)               
    elif intent_group_question_str=="ตรวจสอบ1":
        loop_check(data_from_dialogflow_dict)              
    elif intent_group_question_str=="ดู1":
        status=cal_Score()
        update_status(status,data_from_dialogflow_dict)
        answer_str=notifyPic(check_respone(status))
    elif intent_group_question_str=="ผลการประเมิน":
        check= recheck(data_from_dialogflow_dict)
        answer_str=notifyPic(check_respone(check))
    elif intent_group_question_str=="คำแนะนำ1":
        url=check_advice(data_from_dialogflow_dict)
        answer_str=notifyPic(url)
    elif intent_group_question_str=="ยินยอม2":
          answer_str=user_info(data_from_dialogflow_dict)
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
def user_info(data):
    age=data["queryResult"]["outputContexts"][1]["parameters"]["age"]
    gender=data["queryResult"]["outputContexts"][1]["parameters"]["gender"]
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    db.collection('User').document(f'{user_Id}').set({
        u'userId':user_Id,
        u'age':age,
        u'gender':gender,
        u'status':""
    }) 
    return "บันทึกข้อมูลเสร็จสิ้น"
def notifyPic(url):  
    reply=[{"image":{"imageUri":url},"platform": "LINE"}]
    return reply
def upround(data_from):
    global g_r
    g_r=g_r+data_from
def loop_check(data)  :
    user_answer = data["originalDetectIntentRequest"]["payload"]["data"]["message"]["text"]
    if user_answer =="ไม่เคย":
        upround(0)
    elif user_answer=="มีบ้าง":
        upround(1)
    elif user_answer=="ค่อนข้างบ่อย":
        upround(2)
    elif user_answer=="มีเกือบทุกวัน":
        upround(3)
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
######################################################################################
if __name__ == '__main__':
    app.run(debug=True)

