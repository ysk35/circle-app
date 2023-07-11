from flask import Flask, jsonify, request
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from db import User, Attendance, AdminUser, app, db
from flask_cors import CORS
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (FollowEvent, MessageEvent, TextMessage, TextSendMessage)
import datetime

CORS(
  app,
  supports_credentials=True
)

app.config["SECRET_KEY"] = "9abecf1b701c38448a21bbba5bad84d7c6e7e0255961a9e891d42efa8c989dcc"

login_manager = LoginManager()
login_manager.init_app(app)

ACCESS_TOKEN = "g0sM8WGTf6pw+qNynFHG8A0w3es9+Xwb0dfYj7o60fok2+hSD2eqf4FmMIultNkOzU57RmkRQlRbzp6MZ2RLUuSR7dGGZ/qcfdJCO6meha31mPDaoj3ZS+Rok4/kd9QVuu14ut/ya6JrPAK8nIKFDwdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "e5088dcddfd4d73a48b580ca70f23381"
line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
  signature = request.headers['X-Line-Signature']

  body = request.get_data(as_text=True)
  app.logger.info("Request body: " + body)

  try:
    handler.handle(body, signature)
  except InvalidSignatureError:
    abort(400)
  return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
  messageText = event.message.text.split("\n")
  user = db.query(User).\
    filter(User.line_user_id == event.source.user_id).\
    first()
  if (not user.name and not user.student_number) or user.is_temporary == True:
    if user.is_confirm == False:
      if not messageText[1]:
        replyText = "2行で以下のような形式で回答してください\n例:\n1行目：74○○○○○\n2行目：理科大太郎"
      else:
        user.is_confirm = True
        user.student_number = messageText[0]
        user.name = messageText[1]
        user.is_temporary = True
        db.session.commit()
        replyText = "学籍番号：" + messageText[0] + "\n名前：" + messageText[1] + "\nでよろしいでしょうか？\n「はい」又は「いいえ」で答えてください"
    elif user.is_confirm == True:
      if event.message.text == "はい":
        user.is_temporary = False
        db.session.commit()
        replyText = "登録しました"
      elif event.message.text == "いいえ":
        replyText = "以下のような形式で送信してください\n例:\n1行目：74○○○○○\n2行目：理科大太郎"
        user.is_confirm = False
        user.student_number = None
        user.name = None
        db.session.commit()
      else:
        replyText = "「はい」又は「いいえ」で答えてください"
  else:
    if event.message.text == "出席":
      dt_now = datetime.datetime.now()
      dt_now_ar = dt_now.strftime('%Y/%m/%d')
      attendance = Attendance.query.\
        filter(Attendance.user_id == user.id, Attendance.date == dt_now_ar).\
        first()
      if not attendance:
        db.session.add(Attendance(user_id = user.id, name = user.name, date = dt_now_ar))
        db.session.commit()
        replyText = "出席登録が完了しました"
      else:
        replyText = "出席登録が完了しています"
    else:
      replyText = "出席登録以外の情報は送信しないでください"

  line_bot_api.reply_message(
    event.reply_token,
    TextSendMessage(text=replyText))

@handler.add(FollowEvent)
def follow_message(event):
  if event.type == "follow":
    line_bot_api.reply_message(
      event.reply_token,
      TextSendMessage(text="フォローありがとうございます！"))

  db.session.add(User(line_user_id = event.source.user_id, is_confirm = False))
  db.session.commit()


@app.route('/signup', methods=['POST'])
def signup():
  try:
    email = request.form.get('email')
    password = request.form.get('password')
    admin_user = AdminUser(email=email, password=password)
    db.session.add(admin_user)
    db.session.commit()
    return jsonify({"is_success": True, "error": ""}), 200
  except:
    return jsonify({"is_success": False, "error": "error"}), 200

@app.route('/login', methods=['POST'])
def login():
  email = request.form.get('email')
  password = request.form.get('password')

  admin_user = AdminUser.query.filter_by(email=email).first()

  if check_password_hash(admin_user.password, password):
    login_user(admin_user)
    return jsonify({"is_success": True, "error": ""}), 200
  else:
    return jsonify({"is_success": False, "error": "登録されていません"}), 200

@app.route("/logout", methods=["GET"])
def logout():
  logout_user()

  return jsonify({}), 200

@app.route('/getmember', methods=['POST'])
def get_member():
  try:
    list = []
    attend_user = Attendance.query.filter_by(date=request.form.get('date')).all()
    for user in attend_user:
      list.append(user.name)
    print(list)
    return jsonify({'users': list}), 200
  except:
    return jsonify({}), 400

@app.route("/")
def index():
  return "index page"