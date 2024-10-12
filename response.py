from linebot.models import TextSendMessage
from datetime import datetime, timedelta

class LineBotResponse:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.user_last_message_time = {}

    def handle_message(self, event):
        user_id = event.source.user_id
        current_time = datetime.now()

        # 判斷用戶是否在三分鐘內發送過消息
        if user_id in self.user_last_message_time:
            last_time = self.user_last_message_time[user_id]
            if current_time - last_time < timedelta(minutes=3):
                return  # 在三分鐘內不再回覆

        # 更新用戶的最後消息時間
        self.user_last_message_time[user_id] = current_time

        # 發送回覆
        self.line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='Hello, {}, what can I help?'.format(event.message.text))
        )
