from flask import Flask, request, abort
import os
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 獲取環境變數
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the LINE Bot!', 200

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 設置消息處理器
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Hello, {}'.format(event.message.text)))

@app.route('/healthz', methods=['GET'])
def health_check():
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True)
