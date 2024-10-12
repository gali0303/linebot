# response.py
from linebot import LineBotApi
from linebot.models import TextSendMessage

class LineBotResponse:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.user_last_message_time = {}  # 用來跟蹤每個用戶的消息時間

    def handle_message(self, event):
        user_id = event.source.user_id
        current_time = datetime.now()

        # 檢查用戶是否在字典中
        if user_id not in self.user_last_message_time:
            # 第一次收到該用戶的消息
            self.user_last_message_time[user_id] = current_time
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='Hello, {}, what can I help?'.format(event.message.text))
            )
        else:
            last_time = self.user_last_message_time[user_id]
            # 判斷是否在三分鐘內
            if current_time - last_time > timedelta(minutes=3):
                self.user_last_message_time[user_id] = current_time
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='Hello, {}, what can I help?'.format(event.message.text))
                )
            else:
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='You said: {}'.format(event.message.text))
                )
