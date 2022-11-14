# !/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from cgitb import handler
from email import header
from re import S
from tkinter import scrolledtext
from turtle import update
from matplotlib import image
from numpy import deprecate, round_

from pkg_resources import ensure_directory

import json
import os
from flask import Flask, make_response, request
from flask import request
from flask import make_response
import requests
# import UseSentiment
import Usesentiment
####################
from linebot import (
    LineBotApi, WebhookHandler,
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,ImageSendMessage
)




###################################
lineaccesstoken = 'CFGppk8AuPQl705iQwgP8cZE9Gn4CumoTp7BYNvKnbOtf9zSqOkRyFgMgz9fM/U58jsG2LyPB5ds7R99GHZde3y95T5988EWSbLEU0upcB6c12HhIYf4V+d+4oki21kgciXeA0fn5CxPienZ7e5UVwdB04t89/1O/w1cDnyilFU='
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
# question_for_test=[("ที่ผ่านมาคุณเป็นอย่างไรบ้าง รู้สึกมีเรื่องที่ไม่สบายใจหรือท้อแท้บ้างไหม"),("คุณรู้สึกเหนื่อยง่าย ไม่กระปรี้กระเปร่าบ้างไหม"),("คุณรู้สึกเบื่ออาหาร หรือกินมากเกินไปไหม"),("คุณรู้สึกว่าตัวเองหลับยาก หลับๆตื่นๆ หรือ หลับมากเกินไปไหม"),("คุณรู้สึกเบื่อบ้างไหม"),("คุณไม่มีสมาธิ เวลาทำงานที่ต้องใช้ความตั้งใจ เช่นการดูโทรทัศน์ หรือ อ่านหนังสือ ไหม"),("คุณรู้สึกว่าตัวเองพูดช้า ทำอะไรช้าลง จนคนอื่นสังเกตเห็นได้ หรือกระสับกระส่ายไม่สามารถอยู่นิ่งได้เหมือนที่เคยเป็นไหม"),("คุณรู้สึกไม่ดีกับตัวเอง คิดว่าตัวเองล้มเหลว หรือทำให้ตนเองหรือครอบครัวผิดหวังไหม"),("คุณคิดที่จะทำร้ายตนเอง หรือคิดว่าถ้าตายไปคงจะดี ไหม")]
# never_answer=["เยี่ยมมากงั้นเราไปกันต่อเลยนะ","งั้นแสดงว่าคุณพักผ่อนได้เพียงพอและยังสนุกกับการทำสิ่งใหม่ๆอยู่ทุกวันแน่เลย","ดีแล้วอย่าลืมหาอะไรอร่อยๆกินด้วยนะ","ดีมากเลยคุณจะได้มีแรงเพื่อทำสิ่งที่ชอบในแต่ละวันได้อย่างเต็มที่","วันนี้คุณคงมีเรื่องสนุกๆให้ทำแน่เลย","โห แสดงว่าคุณมีความตั้งใจและมุ่งมั่นต่อสิ่งที่ทำอยู่ตลอดเวลาเลยนะ","โห แสดงว่าคุณต้องเป็นคนที่มีพลังงานเชิงบวกเยอะแน่ๆเลย","ขอให้เป้าหมายที่คุณตั้งไว้สำเร็จลุล่วง เราจะคอยเป็นกำลังใจให้คุณเอง","ดีแล้วค่ะอย่าทำอะไรอย่างงั้นเลยเราเป็นห่วงคุณนะ"]
# sometimes_answer=["ไม่เป็นไรนะเดี๋ยวมันก็ผ่านไปนะ","อย่าลืมดื่มน้ำเยอะๆ และ อย่าลืมพักสายตาบ้างนะคะ เราเป็นห่วงคุณนะ","ลองเปลี่ยนรสชาติอาหารดูไหม จะได้ลองกินของอร่อยๆที่ไม่เคยกินด้วยน้า","ลองอ่านหนังสือหรือฟังเพลงเบาๆสบายๆดูนะจะทำให้ผ่อนคลายได้","ถ้าคุณรู้สึกเบื่อ ลองหากิจกรรมหรืองานอดิเรกที่ชอบทำไหมสิ่งเหล่านี้จะทำให้คุณหายเบื่อได้นะ","การหยุดพักจากการทำงานจะช่วยเพิ่มสมาธิได้นะ เมื่อไหร่ที่คุณทำงานเป็นเวลานาน อย่าลืมให้ตัวเองได้พักสมองบ้างเป็นบางครั้งนะ","ลองออกไปเดินเล่นข้างนอกเพื่อผ่อนคลายดูไหม มันจะทำให้คุณรู้สึกดีขึ้นนะ","ลองอดทนต่ออีกนิดดูนะ เชื่อซิว่าคุณจะค่อยๆดีขึ้น","คงไม่มีใครอยากให้เรื่องไม่ดีมาเกิดกับตัวเราหรอกนะ"]
# often_answer=["ไม่เป็นไรนะไม่ต้องเครียด เดี๋ยวเรื่องแย่ๆก็ผ่านไปนะ","การออกกำลังกายและกินของที่มีประโยชน์ เช่น พวกผลไม้ จะทำให้เราสดชื่นได้น้า","ลองออกกำลังกายแบบเบาๆดูไหม มันจะช่วยกระตุ้นการอยากอาหารได้นะ","ลองออกกำลังกายอย่างสม่ำเสมอดูนะ นอกจากจะทำให้คุณนอนหลับสนิทแล้ว ก็ยังช่วยให้ร่างกายของคุณแข็งแรงอีกด้วยนะ","ลองหาเวลาเพื่อทำกิจกรรมต่างๆ ร่วมกับคนในครอบครัว หรือเพื่อนๆดูนะ","การเปิดเพลงขณะทำงานจะช่วยเรื่องสมาธิได้นะ ถึงแม้ว่าคุณจะไม่ชอบฟังเพลงขณะทำงาน แต่การใช้เสียงธรรมชาติหรือเสียงดนตรีเบาๆ อาจช่วยเพิ่มสมาธิในการทำงานได้","หายใจเข้าลึกๆตั้งสติให้ดีนะ เดี๋ยวทุกจะดีขึ้นเองนะ","อย่าโทษตัวเองเลยคุณทำได้ดีแล้วลองพยายามต่อไปนะ เราจะช่วยคุณเอง","อย่าคิดจะทำมันอะไรอย่างงั้นเลยมันไม่ดีต่อทั้งตัวคุณและคนที่คุณรักนะ"]
# all_the_time_answer=["ช่วงนี้คงหนักมากสำหรับคุณ แต่ไม่เป็นไรนะ เราอยู่ข้างๆคุณเสมอ","ลองพักจากสิ่งที่ทำอยู่ แล้วออกไปสูดอากาศบริสุทธิ์ข้างนอกดูดีไหม จะได้รู้สึกสดชื่น เมื่อพักอย่างเต็มที่แล้วจะได้มีแรงทำสิ่งต่างๆได้อย่างเต็มที่","ลองเปลี่ยนบรรยากาศหรือสถานที่ในการรับประทานอาหารไหม คุณจะได้รู้สึกสนุกกับการรับประทานอาหารมากขึ้นน้า","ถ้าคุณทุกข์ใจหรือมีเรื่องที่ไม่สบายใจ อย่าเครียดไปเลยนะ ทุกปัญหามีทางออกเสมอ ปล่อยใจให้สงบตั้งสติดีๆ แล้วคุณจะผ่านไปได้ทุกเรื่องนะ","ไม่เป็นไรนะ ลองออกกำลังกาย หลับพักผ่อนให้เพียงพอ คุณจะได้รู้สึกกระปรี้กระเปร่า และอย่าลืมรับประทานอาหารอร่อยๆ และมีประโยชน์ด้วยนะคุณจะได้มีแรงในการทำกิจกรรมต่างๆได้เต็มที่","ลองออกกำลังกายก่อนที่จะต้องจดจ่อกับงาน หรือเมื่อต้องการพักสมองดูนะคะ จะทำให้เรามีสมาธิมากขึ้น หรือคุณอาจจะไปออกไปเดินสูดอากาศข้างนอกก้ได้นะ","อย่าเครียดเกินไปเลยนะคะมันมีแต่ผลไม่ดีต่อร่างกายและจิตลองหาสิ่งใหม่ๆทำให้มี  พลังทั้งกายและจิตใจเพิ่มนะ","คุณไม่ได้ตัวคนเดียวลำพังนะ ฉันอยู่ที่นี่กับคุณเอง","ฉันไม่รู้ว่าคุณไปเจออะไรมาบ้าง แต่ฉันจะไม่ทิ้งคุณและฉันจะอยู่ข้างๆคุณเองนะ"]
g_r=0
emotion=0
bucket=storage.bucket()

#############################
db = firestore.client()
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
    # if intent_group_question_str=="พร้อม":
    #     
    # if intent_group_question_str=="ดู":
    #         global g_r
    #         answer_str=cal_Score(g_r)
    if intent_group_question_str=="พร้อม2":
        loop_check(data_from_dialogflow_dict)         
    elif intent_group_question_str=="พร้อม3":
        loop_check(data_from_dialogflow_dict)            
    elif intent_group_question_str=="พร้อม4":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม5":
        loop_check(data_from_dialogflow_dict)                 
    elif intent_group_question_str=="พร้อม6":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม7":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม8":
        loop_check(data_from_dialogflow_dict)
    elif intent_group_question_str=="พร้อม9":
        loop_check(data_from_dialogflow_dict)               
    elif intent_group_question_str=="ตรวจสอบ":
        loop_check(data_from_dialogflow_dict)              
    elif intent_group_question_str=="ดู":
        status=cal_Score()
        # answer_str=status
        update_status(status,data_from_dialogflow_dict)
        answer_str=notifyPic(check_respone(status))
    
    elif intent_group_question_str=="ผู้ใช้ทั้งหมด" :  
        answer_str=show_record(data_from_dialogflow_dict)
    elif intent_group_question_str=="คำแนะนำ1":
        answer_str=advice(data_from_dialogflow_dict)        
        
    # elif intent_group_question_str=="เล่า":
    #     answer_str=notifyPic()
    # elif intent_group_question_str=="มี2":
    #      answer_str=  Chat_with_me(data_from_dialogflow_dict)
    elif intent_group_question_str=="ยินยอม2":
          answer_str=user_info(data_from_dialogflow_dict)
       
    # else :
    #     answer_str= "เราไม่เข้าใจ"
    answer_from_bot ={"fulfillmentMessages":answer_str}
            
                    #แปลงจาก dict ให้เป็น JSON
    answer_from_bot = json.dumps(answer_from_bot, indent=4) 
    print(answer_from_bot)
    return answer_from_bot
def advice(data):
    if data =="ท้อแท้":
        a=[{"text": {"text": ["We could find few matching products based on your query"]}}]
    elif data=="เรื่องที่ไม่สบายใจ":
        a=1
    elif data=="เบื่ออาหาร":
        a=1
    elif data=="หลับยาก":
        a=1
    elif data=="เบื่อ":
        a=1
    elif data=="ไม่มีสมาธิ":
        a=1
    elif data=="ทำอะไรช้าลง":
        a=1
    elif data=="รู้สึกไม่ดีกับตัวเอง":
        a=1
    elif data=="คิดทำร้ายตัวเอง":
        a=1
    return a
    
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

def check_respone(answer):
    if answer =="ไม่มีอาการของโรงซึมเศร้าหรือมีอาการของโรงซึมเศร้าในปริมาณน้อย":    
        url= 'https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/normal.png?alt=media&token=bb8998dd-1c5a-4c99-8ff9-23cc3e765763',
    elif answer =="ระดับน้อย":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/little.png?alt=media&token=6417a605-ce7a-4875-849f-2feeadebb866',
    elif answer =="ระดับปานกลาง":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/medium.png?alt=media&token=b49c9e52-acd4-402e-9630-0d37c9d4ab2b'
    elif answer =="ระดับรุนแรง":
        url='https://firebasestorage.googleapis.com/v0/b/depreesion-4eb38.appspot.com/o/severe.png?alt=media&token=53678518-9998-440e-be1e-76401383aed8',    
    return url
def cal_Score():   
    global g_r
    score= g_r
    if score<7:
        sum="ไม่มีอาการของโรงซึมเศร้าหรือมีอาการของโรงซึมเศร้าในปริมาณน้อย"
    elif 7<=score<=12:
        sum="ระดับน้อย"
    elif 13<=score<=18:
        sum="ระดับปานกลาง"
    elif score>=19:
        sum="ระดับรุนแรง" 
    return sum

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
# def Chat_with_me(input_from_user):
#     userID = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
#     user_text = input_from_user["originalDetectIntentRequest"]["payload"]["data"]["message"]["text"]
#     analyzed_word=str(Usesentiment.useSentiment(str(user_text)))
#     if analyzed_word=='pos':
#             return "pos"
#     elif analyzed_word=='neg':
#             return "neg"

def show_record(data):
    user_Id=data["originalDetectIntentRequest"]["payload"]["data"]["source"]["userId"]
    user=db.collection('User').document(f'{user_Id}').count()
    return user
if __name__ == '__main__':
    app.run(debug=True)

