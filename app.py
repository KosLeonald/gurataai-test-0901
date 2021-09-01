from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)


line_bot_api = LineBotApi('7GS55ur/ZBDmVoeJhDMupAphR9iHtvO9HiY4oidq9PH7HxxTzhzI9WQNYbaZPeMbEIwu82HhxPxm23oG7g56YBxSDKdVTeQKGjbVeCNTtZyQsDXegjd1N1o3Vq4jJ0hdEL2GO/TCPnPF4R+rNW4sTAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('37f4a61b28793e467570d6414dc83a96')

@app.route("/")
def test():
    return "OK"


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

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
