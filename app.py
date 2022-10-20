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
question_for_test=[("ที่ผ่านมาคุณเป็นอย่างไรบ้าง รู้สึกมีเรื่องที่ไม่สบายใจหรือท้อแท้บ้างไหม"),("คุณรู้สึกเหนื่อยง่าย ไม่กระปรี้กระเปร่าบ้างไหม"),("คุณรู้สึกเบื่ออาหาร หรือกินมากเกินไปไหม"),("คุณรู้สึกว่าตัวเองหลับยาก หลับๆตื่นๆ หรือ หลับมากเกินไปไหม"),("คุณรู้สึกเบื่อบ้างไหม"),("คุณไม่มีสมาธิ เวลาทำงานที่ต้องใช้ความตั้งใจ เช่นการดูโทรทัศน์ หรือ อ่านหนังสือ ไหม"),("คุณรู้สึกว่าตัวเองพูดช้า ทำอะไรช้าลง จนคนอื่นสังเกตเห็นได้ หรือกระสับกระส่ายไม่สามารถอยู่นิ่งได้เหมือนที่เคยเป็นไหม"),("คุณรู้สึกไม่ดีกับตัวเอง คิดว่าตัวเองล้มเหลว หรือทำให้ตนเองหรือครอบครัวผิดหวังไหม"),("คุณคิดที่จะทำร้ายตนเอง หรือคิดว่าถ้าตายไปคงจะดี ไหม")]
never_answer=["เยี่ยมมากงั้นเราไปกันต่อเลยนะ","งั้นแสดงว่าคุณพักผ่อนได้เพียงพอและยังสนุกกับการทำสิ่งใหม่ๆอยู่ทุกวันแน่เลย","ดีแล้วอย่าลืมหาอะไรอร่อยๆกินด้วยนะ","ดีมากเลยคุณจะได้มีแรงเพื่อทำสิ่งที่ชอบในแต่ละวันได้อย่างเต็มที่","วันนี้คุณคงมีเรื่องสนุกๆให้ทำแน่เลย","โห แสดงว่าคุณมีความตั้งใจและมุ่งมั่นต่อสิ่งที่ทำอยู่ตลอดเวลาเลยนะ","โห แสดงว่าคุณต้องเป็นคนที่มีพลังงานเชิงบวกเยอะแน่ๆเลย","ขอให้เป้าหมายที่คุณตั้งไว้สำเร็จลุล่วง เราจะคอยเป็นกำลังใจให้คุณเอง","ดีแล้วค่ะอย่าทำอะไรอย่างงั้นเลยเราเป็นห่วงคุณนะ"]
sometimes_answer=["ไม่เป็นไรนะเดี๋ยวมันก็ผ่านไปนะ","อย่าลืมดื่มน้ำเยอะๆ และ อย่าลืมพักสายตาบ้างนะคะ เราเป็นห่วงคุณนะ","ลองเปลี่ยนรสชาติอาหารดูไหม จะได้ลองกินของอร่อยๆที่ไม่เคยกินด้วยน้า","ลองอ่านหนังสือหรือฟังเพลงเบาๆสบายๆดูนะจะทำให้ผ่อนคลายได้","ถ้าคุณรู้สึกเบื่อ ลองหากิจกรรมหรืองานอดิเรกที่ชอบทำไหมสิ่งเหล่านี้จะทำให้คุณหายเบื่อได้นะ","การหยุดพักจากการทำงานจะช่วยเพิ่มสมาธิได้นะ เมื่อไหร่ที่คุณทำงานเป็นเวลานาน อย่าลืมให้ตัวเองได้พักสมองบ้างเป็นบางครั้งนะ","ลองออกไปเดินเล่นข้างนอกเพื่อผ่อนคลายดูไหม มันจะทำให้คุณรู้สึกดีขึ้นนะ","ลองอดทนต่ออีกนิดดูนะ เชื่อซิว่าคุณจะค่อยๆดีขึ้น","คงไม่มีใครอยากให้เรื่องไม่ดีมาเกิดกับตัวเราหรอกนะ"]
often_answer=["ไม่เป็นไรนะไม่ต้องเครียด เดี๋ยวเรื่องแย่ๆก็ผ่านไปนะ","การออกกำลังกายและกินของที่มีประโยชน์ เช่น พวกผลไม้ จะทำให้เราสดชื่นได้น้า","ลองออกกำลังกายแบบเบาๆดูไหม มันจะช่วยกระตุ้นการอยากอาหารได้นะ","ลองออกกำลังกายอย่างสม่ำเสมอดูนะ นอกจากจะทำให้คุณนอนหลับสนิทแล้ว ก็ยังช่วยให้ร่างกายของคุณแข็งแรงอีกด้วยนะ","ลองหาเวลาเพื่อทำกิจกรรมต่างๆ ร่วมกับคนในครอบครัว หรือเพื่อนๆดูนะ","การเปิดเพลงขณะทำงานจะช่วยเรื่องสมาธิได้นะ ถึงแม้ว่าคุณจะไม่ชอบฟังเพลงขณะทำงาน แต่การใช้เสียงธรรมชาติหรือเสียงดนตรีเบาๆ อาจช่วยเพิ่มสมาธิในการทำงานได้","หายใจเข้าลึกๆตั้งสติให้ดีนะ เดี๋ยวทุกจะดีขึ้นเองนะ","อย่าโทษตัวเองเลยคุณทำได้ดีแล้วลองพยายามต่อไปนะ เราจะช่วยคุณเอง","อย่าคิดจะทำมันอะไรอย่างงั้นเลยมันไม่ดีต่อทั้งตัวคุณและคนที่คุณรักนะ"]
all_the_time_answer=["ช่วงนี้คงหนักมากสำหรับคุณ แต่ไม่เป็นไรนะ เราอยู่ข้างๆคุณเสมอ","ลองพักจากสิ่งที่ทำอยู่ แล้วออกไปสูดอากาศบริสุทธิ์ข้างนอกดูดีไหม จะได้รู้สึกสดชื่น เมื่อพักอย่างเต็มที่แล้วจะได้มีแรงทำสิ่งต่างๆได้อย่างเต็มที่","ลองเปลี่ยนบรรยากาศหรือสถานที่ในการรับประทานอาหารไหม คุณจะได้รู้สึกสนุกกับการรับประทานอาหารมากขึ้นน้า","ถ้าคุณทุกข์ใจหรือมีเรื่องที่ไม่สบายใจ อย่าเครียดไปเลยนะ ทุกปัญหามีทางออกเสมอ ปล่อยใจให้สงบตั้งสติดีๆ แล้วคุณจะผ่านไปได้ทุกเรื่องนะ","ไม่เป็นไรนะ ลองออกกำลังกาย หลับพักผ่อนให้เพียงพอ คุณจะได้รู้สึกกระปรี้กระเปร่า และอย่าลืมรับประทานอาหารอร่อยๆ และมีประโยชน์ด้วยนะคุณจะได้มีแรงในการทำกิจกรรมต่างๆได้เต็มที่","ลองออกกำลังกายก่อนที่จะต้องจดจ่อกับงาน หรือเมื่อต้องการพักสมองดูนะคะ จะทำให้เรามีสมาธิมากขึ้น หรือคุณอาจจะไปออกไปเดินสูดอากาศข้างนอกก้ได้นะ","อย่าเครียดเกินไปเลยนะคะมันมีแต่ผลไม่ดีต่อร่างกายและจิตลองหาสิ่งใหม่ๆทำให้มี  พลังทั้งกายและจิตใจเพิ่มนะ","คุณไม่ได้ตัวคนเดียวลำพังนะ ฉันอยู่ที่นี่กับคุณเอง","ฉันไม่รู้ว่าคุณไปเจออะไรมาบ้าง แต่ฉันจะไม่ทิ้งคุณและฉันจะอยู่ข้างๆคุณเองนะ"]
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
    r.header['Content-Type'] = 'application/json' 
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
    #เก็บค่าจาก input dialogflow
    d=1
    Input_from_dialog=respond_dict["queryResult"]["outputContexts"][1]["parameters"]["any.original"]
    print("นี่เป็นแเพียงแบบทดสอบเพื่อประเมินโรคซึมเศร้าเบื้องต้น แต่หากในกรณีที่มีผลคะแนนออกมาแล้วคุณเสี่ยงที่จะเป็นโรคซึมเศร้าเราขอให้คุณพบแพทย์โดยเร็ว ด้วยความเป็นห่วงจากเรา")
    print("พร้อมที่จะทำแบบทดสอบเลยไหม")
    for i in range(9):
        print(question_for_test[i])
        match d:
            case "ไม่เคย":
                 print(never_answer[i])
                 score=+0
            case "มีบ้าง":
                 print(never_answer[i])
                 score=+0
            case "ค่่อนข้างบ่อย":
                 print(never_answer[i])
                 score=+0
            case "มีเกือบทุกวัน":
                 print(never_answer[i])
                 score=+0
            case _:
                 print("เราไม่เข้าใจ")
                 
        break
        # if(respond_dict=="ไม่เคย"):
        #     print(never_answer[i])
        #     score=+0
        # elif(respond_dict=="มีบ้าง"):
        #     print(sometimes_answer[i])
        #     score=+1
        # elif(respond_dict=="ค่่อนข้างบ่อย"):
        #     print(often_answer[i])
        #     score=+2
        # elif(respond_dict=="มีเกือบทุกวัน"):
        #     print(all_the_time_answer[i])
        #     score=+3
    if score>=19:
        sum=print("คุณมีอาการของโรคซึมเศร้าในระดับรุนแรง")
    elif 13>=score<=18:
        sum=print("คุณมีอาการของโรคซึมเศร้าในระดับปานกลาง")
    elif 7>=score<=12:
        sum=print("คุณมีอาการของโรคซึมเศร้าในระดับน้อย")
    elif score<7:
        sum=print("คุณมีอาการของโรคซึมเศร้าในระดับน้อยมาก")
    return sum

# def Get_infomation(input_from_user):
#     print("เราขออณุญาติในการเก็บขอมูลส่วนตัว")
#     userID = input_from_user[]

if __name__ == '__main__':
    app.run(debug=True)


    