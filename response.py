from linebot.models import TextSendMessage
from datetime import datetime, timedelta
import random

class LineBotResponse:
    def __init__(self, line_bot_api):
        self.line_bot_api = line_bot_api
        self.user_last_message_time = {}
        self.dinner_suggestion_triggered = False  # 用來追蹤是否需要提供晚餐建議
        self.dinner_options = ["炒飯", "雞絲麵", "便當", "炒米粉", "滷味", "咖哩飯", "土魠魚羹"]  # 晚餐選項

    def handle_message(self, event):
        user_id = event.source.user_id
        current_time = datetime.now()
        message_text = event.message.text.lower()

        # 判斷用戶是否在一分鐘內發送過消息
        if user_id in self.user_last_message_time:
            last_time = self.user_last_message_time[user_id]
            if current_time - last_time < timedelta(minutes=1):
                self.line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='好的， {}, 我來看看!'.format(event.message.text))
                )
                return
        else:
            # 第一次發送消息
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='哈囉! {}, 我可以幫你什麼?'.format(event.message.text))
            )

        # 偵測詢問「晚餐吃什麼」
        if "晚餐吃什麼" in message_text:
            self.dinner_suggestion_triggered = True

        
        # 偵測回答「不知道」
        elif "不知道" in message_text and self.dinner_suggestion_triggered:
            # 隨機從晚餐選項中挑選一個
            suggestion = random.choice(self.dinner_options)
            self.line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=f'吃{suggestion}好嗎？')
            )
            self.dinner_suggestion_triggered = False  # 重置觸發狀態

        # 更新用戶的最後消息時間
        self.user_last_message_time[user_id] = current_time
