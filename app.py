from flask_ngrok import run_with_ngrok
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
        access_token = 'yao3NtqrYqxOIh60KwZ6i6JDrwvf3JEfEcbV7tr+FqQ/k3IxP3j64KXYALwvikIr2fcq1nztZwx+aU9MPj3CC4BUfb9IEaEWdRZk0fntX0fbxZIUv32BE5Xsy5fapeQRa4jxOj+D/4B2CF6p5wq2aAdB04t89/1O/w1cDnyilFU='
        secret = '33dbbefeb9a63385fc7421441493a306'
        line_bot_api = LineBotApi(access_token)              # 確認 token 是否正確
        handler = WebhookHandler(secret)                     # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']      # 加入回傳的 headers
        handler.handle(body, signature)                      # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']      # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']            # 取得回傳訊息的 Token
        if msg == "/news":
            line_bot_api.reply_message(tk,TextSendMessage(getnews.news()))
            print(msg, tk)                                     # 印出內容
    except:
        print(body)                                          # 如果發生錯誤，印出收到的內容
    return 'OK'                 # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  run_with_ngrok(app)           # 串連 ngrok 服務
  app.run()