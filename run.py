import os
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import getnews
import json

app = Flask(__name__)

# 從環境變數中讀取 access_token 和 secret
access_token = os.environ.get('LINE_ACCESS_TOKEN')
secret = os.environ.get('LINE_SECRET')

line_bot_api = LineBotApi(access_token)
handler = WebhookHandler(secret)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    try:
        json_data = json.loads(body)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        msg = json_data['events'][0]['message']['text']
        tk = json_data['events'][0]['replyToken']
        if msg == "/news":
            line_bot_api.reply_message(tk, TextSendMessage(getnews.news()))
            print(msg, tk)
    except:
        print(body)
    return 'OK'

if __name__ == "__main__":
    # 從環境變數中讀取 PORT，如果不存在，預設使用 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(port=port)
