from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('7n7MQLPTsZ8EIb4ZMOlaCuxMkHpgYOJsf04NXx9nbzz3VyW6bLl5vDK0ImWs6lNtI9URGF8GOm1VYMcI7QBUMHrW+SuUjK+n1MWSEQlYl7DEQ4b5JF1COpTo5NA5jCeTQkTSwFKZmEExO0UsVc7PMwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('65207b8508f7f03070e0eba4d5b69deb')

# 監聽所有來自 /callback 的 Post Request
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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
