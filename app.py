from flask import Flask
from flask import request
import os
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (FollowEvent, MessageEvent, TextMessage, TextSendMessage,)
from UserModel import User
from AttendanceModel import Attendance
from setting import session

# generate instance
app = Flask(__name__)

# get environmental value from heroku
ACCESS_TOKEN = "g0sM8WGTf6pw+qNynFHG8A0w3es9+Xwb0dfYj7o60fok2+hSD2eqf4FmMIultNkOzU57RmkRQlRbzp6MZ2RLUuSR7dGGZ/qcfdJCO6meha31mPDaoj3ZS+Rok4/kd9QVuu14ut/ya6JrPAK8nIKFDwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "e5088dcddfd4d73a48b580ca70f23381"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# endpoint
@app.route("/")
def test():
    return "<h1>It Works!</h1>"

# endpoint from linebot
@app.route("/callback", methods=['POST'])
def callback():
      # get X-Line-Signature header value
  signature = request.headers['X-Line-Signature']

  # get request body as text
  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  # handle webhook body
  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    print("Invalid signature. Please check your channel access token/channel secret.")
    abort(400)
  return 'OK'

# handle message from LINE
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  messageText = event.message.text.split("\n")
  # print(messageText)
  print(messageText[0])
  print(messageText[1])
  # replyText = "test"
  user = session.query(User).\
    filter(User.line_user_id == event.source.user_id).\
    first()
  print(user.line_user_id)
  print(user.name)
  print(user.student_number)
  if not user.name:
    replyText = "名前：" + messageText[0] + "\n学籍番号：" + messageText[1] + "\nでよろしいでしょうか"
  # if(event.message.text == ):
  #   replyText = "「あ」って送りましたね？"
  else:
    replyText = event.source.user_id
  # print(event.message.text)
  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=replyText))

@handler.add(FollowEvent)# FollowEventをimportするのを忘れずに！
def follow_message(event):# event: LineMessagingAPIで定義されるリクエストボディ
  if event.type == "follow":# フォロー時のみメッセージを送信
    line_bot_api.reply_message(
      event.reply_token,# イベントの応答に用いるトークン
      TextSendMessage(text="フォローありがとうございます！"))

  session.add(User(line_user_id = event.source.user_id))
  session.commit()

if __name__ == "__main__":
  app.run()