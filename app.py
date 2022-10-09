#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from email import header
from flask import Flask, jsonify, render_template, request,make_response
import json
import numpy as np
import os 

import UseSentiment 

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
@app.route('/')
def index():
    return "Hello World!"
@app.route('/', methods=['POST'])
def MainFunction():
    # Getting data from Dialogflow
    data_from_dialogflow_raw = request.get_json(silent=True,force=True)
    # Call generating_answer function to classify the question
    answer_from_bot=generating_answer(data_from_dialogflow_raw)
    # Make a respond back to Dialogflow
    r = make_response(answer_from_bot)
    r,header['Content-Type'] = 'application/json' 
    return r




if __name__ == '__main__':
    app.run(debug=True)

    