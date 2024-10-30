from linebot.models import TextSendMessage
from datetime import datetime, timedelta

class LineBotResponse:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.user_last_message_time = {}

    def handle_message(self, event):
        user_id = event.source.user_id
        current_time = datetime.now()

        # 判斷用戶是否在一分鐘內發送過消息
        if user_id in self.user_last_message_time:
            last_time = self.user_last_message_time[user_id]
            if current_time - last_time < timedelta(minutes=1):
                # 在一分鐘內已經發送過消息
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='好的， {}, 我來看看!'.format(event.message.text))
                )
                return
        else:
            # 是第一次發送消息
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='哈囉! {}, 我可以幫你什麼?'.format(event.message.text))
            )

        # 更新用戶的最後消息時間
        self.user_last_message_time[user_id] = current_time
