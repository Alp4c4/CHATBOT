#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from email import header

from pkg_resources import ensure_directory
from flask import Flask, jsonify, render_template, request,make_response
import json
import numpy as np
import os 
import time
# import UseSentiment

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
)
from linebot.models.template import *
from linebot import  LineBotApi
from linebot.exceptions import LineBotApiError


app = Flask(__name__)
###################################
lineaccesstoken = 'CFGppk8AuPQl705iQwgP8cZE9Gn4CumoTp7BYNvKnbOtf9zSqOkRyFgMgz9fM/U58jsG2LyPB5ds7R99GHZde3y95T5988EWSbLEU0upcB6c12HhIYf4V+d+4oki21kgciXeA0fn5CxPienZ7e5UVwdB04t89/1O/w1cDnyilFU='
line_bot_api = LineBotApi(lineaccesstoken)

###################################
question_for_test=["ที่ผ่านมาคุณเป็นอย่างไรบ้าง รู้สึกมีเรื่องที่ไม่สบายใจหรือท้อแท้บ้างไหม","คุณรู้สึกเหนื่อยง่าย ไม่กระปรี้กระเปร่าบ้างไหม","คุณรู้สึกเบื่ออาหาร หรือกินมากเกินไปไหม","คุณรู้สึกว่าตัวเองหลับยาก หลับๆตื่นๆ หรือ หลับมากเกินไปไหม","คุณรู้สึกเบื่อบ้างไหม","คุณไม่มีสมาธิ เวลาทำงานที่ต้องใช้ความตั้งใจ เช่นการดูโทรทัศน์ หรือ อ่านหนังสือ ไหม","คุณรู้สึกไม่ดีกับตัวเอง คิดว่าตัวเองล้มเหลว หรือทำให้ตนเองหรือครอบครัวผิดหวังไหม","คุณคิดที่จะทำร้ายตนเอง หรือคิดว่าถ้าตายไปคงจะดี ไหม"]
never_answer=["เยี่ยมมากงั้นเราไปกันต่อเลยนะ","งั้นแสดงว่าคุณพักผ่อนได้เพียงพอและยังสนุกกับการทำสิ่งใหม่ๆอยู่ทุกวันแน่เลย"," ดีแล้วอย่าลืมหาอะไรอร่อยๆกินด้วยนะ"," ดีมากเลยคุณจะได้มีแรงเพื่อทำสิ่งที่ชอบในแต่ละวันได้อย่างเต็มที่","วันนี้คุณคงมีเรื่องสนุกๆให้ทำแน่เลย","โห แสดงว่าคุณมีความตั้งใจและมุ่งมั่นต่อสิ่งที่ทำอยู่ตลอดเวลาเลยนะ","โห แสดงว่าคุณต้องเป็นคนที่มีพลังงานเชิงบวกเยอะแน่ๆเลย","ขอให้เป้าหมายที่คุณตั้งไว้สำเร็จลุล่วง เราจะคอยเป็นกำลังใจให้คุณเอง","ดีแล้วค่ะอย่าทำอะไรอย่างงั้นเลยเราเป็นห่วงคุณนะ"]
score=0
##################################
@app.route('/')
def index():
    return "Hello World!"
@app.route('/', methods=['POST'])
def MainFunction():
    # Getting data from Dialogflow
    data_from_dialogflow_raw = request.get_json(silent=True,force=True)
    # เรียกใช่function generating_answer
    answer_from_bot=generating_answer(data_from_dialogflow_raw)
    # ส่งค่่ากลับไปที่dialogflow
    r = make_response(answer_from_bot)
    r,header['Content-Type'] = 'application/json' 
    return r

def generating_answer(data_from_dialogflow_dict):
    #Print intent  ที่รับมาจาก dialogflow
    print(json.dump(data_from_dialogflow_dict,indent=4,ensure_ascii=False))
    #เก็บค่าชื่อของintentที่รับมาจากdialogflow
    intent_group_question_str=data_from_dialogflow_dict["queryResult"]["intent"]["displayName"]
    #ลูปตัวเลือกของฟังชั่นสำหรับตอบคำถามกลับ
    if intent_group_question_str=="ลองทำแบบทดสอบ":
        answer_str=Depression_test(data_from_dialogflow_dict)

    #สร้างการแสดงของ dict
    answer_from_bot ={"fulfillmentText":answer_str}
    #แปลงจาก dict ให้เป็น Json
    answer_from_bot =json.dump(answer_from_bot,indent=4)
    return answer_from_bot


def Depression_test(respond_dict):
    print("นี่เป็นแเพียงแบบทดสอบเพื่อประเมินโรคซึมเศร้าเบื้องต้น แต่หากในกรณีที่มีผลคะแนนออกมาแล้วคุณเสี่ยงที่จะเป็นโรคซึมเศร้าเราขอให้คุณพบแพทย์โดยเร็ว ด้วยความเป็นห่วงจากเรา")
    print("พร้อมที่จะทำแบบทดสอบเลยไหม")
    if respond_dict=="พร้อม" :
        print("รูปแบบมีคำตอบคือ ไม่เคย,มีบ้าง,ค่อนข้างบ่อย,มีเกือบทุกวัน")
        time.slepp(2)
        print ("คุณลองคิิดถึงช่วง2สัปดาห์ที่ผ่านมานะ เริ่มแล้วนะ")
        time.sleep(2)
        print("ในช่วงที่ผ่านมาคุณเป้นอย่างไรบ้าง รู้สึกมีเรื่องไม่สบายใจหรือท้อแท้บ้างไหม")
        if respond_dict=="ไม่เคย":
            print("เยี่ยมเลยงั้นเราไปกันต่อเลยนะ")
            score=score
        elif respond_dict=="มีบ้าง":  
            print("")
            score+=1
        elif respond_dict=="ค่อนข้างบ่อย":  
            print("")
            score+=2
        elif respond_dict=="มีเกือบทุกวัน":  
            print("")
            score+=3

# def Get_infomation(input_from_user):
#     print("เราขออณุญาติในการเก็บขอมูลส่วนตัว")
#     userID = input_from_user[]

if __name__ == '__main__':
    app.run(debug=True)

    