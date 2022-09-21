#!/usr/bin/python
#-*-coding: utf-8 -*-
##from __future__ import absolute_import
###
from flask import Flask, jsonify, render_template, request
import json
import numpy as np

# from linebot.models import (
#     MessageEvent, TextMessage, TextSendMessage,TemplateSendMessage,ImageSendMessage, StickerSendMessage, AudioSendMessage
# )
# from linebot.models.template import *
# from linebot import (
#     LineBotApi, WebhookHandler
# )

app = Flask(__name__)

# lineaccesstoken = 'CFGppk8AuPQl705iQwgP8cZE9Gn4CumoTp7BYNvKnbOtf9zSqOkRyFgMgz9fM/U58jsG2LyPB5ds7R99GHZde3y95T5988EWSbLEU0upcB6c12HhIYf4V+d+4oki21kgciXeA0fn5CxPienZ7e5UVwdB04t89/1O/w1cDnyilFU='
# line_bot_api = LineBotApi(lineaccesstoken)

###################################
@app.route('/')
def index():
    return "Hello World!"



if __name__ == '__main__':
    app.run(debug=True)