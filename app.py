import os
import openai
from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import getnews
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                    # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                         # json 格式化訊息內容
        access_token = os.getenv('LINE_ACCESS_TOKEN')
        secret = os.getenv('LINE_CHANNEL_SECRET')
        openai.api_key = os.getenv('OPENAI_API')
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        if msg == "取得最新消息":
            line_bot_api.reply_message(tk, TextSendMessage(getnews.news()))
            print(msg, tk)                                     # 印出內容
        elif msg[0] == "$":
            response = openai.Completion.create(
                model='text-davinci-003',
                prompt=msg[1:],
                max_tokens=256,
                temperature=0.5,
            )
            reply_msg = response["choices"][0]["text"].replace('\n', '')
            text_message = TextSendMessage(text=reply_msg)
            line_bot_api.reply_message(tk, text_message)
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
    app.run()