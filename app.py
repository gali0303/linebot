from flask import Flask, request, abort
import os
import logging
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage
from response import LineBotResponse  # 確保正確導入

app = Flask(__name__)

# 設定日誌
logging.basicConfig(level=logging.INFO)

# 獲取環境變數
channel_access_token = os.getenv('CHANNEL_ACCESS_TOKEN')
channel_secret = os.getenv('CHANNEL_SECRET')

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 創建 LineBotResponse 實例（確保在全局範圍內）
line_bot_response = LineBotResponse(line_bot_api)

@app.route('/', methods=['GET'])
def home():
    return 'Welcome to the LINE Bot!', 200

@app.route('/callback', methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    logging.info(f"Request body: {body}")  # 記錄請求的主體
    logging.info(f"Signature: {signature}")  # 記錄簽名

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        logging.error("Invalid signature. Aborting.")
        abort(400)

    return 'OK'

# 設置消息處理器
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 使用全局範圍內定義的 line_bot_response 來處理消息
    line_bot_response.handle_message(event)

@app.route('/healthz', methods=['GET'])
def health_check():
    return 'OK', 200

if __name__ == "__main__":
    app.run(debug=True)
