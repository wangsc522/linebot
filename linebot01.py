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

line_bot_api = LineBotApi('rNuJcLVeCoJwBooBW8AhsyoFTKWDN/15SdFP8ObH1SBMAbdtWK0tEQReHXE+8fRo1NtNxt1kX/6KKvqSzytsZy8RvuuFhpjmbi9a+V+eVqt+NJrYwrefxT31ckJGaZt6dtG66trfbDULq4f3bdd60QdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a2107f4d8710940b1568c6ae14415089')


@app.route("/", methods=['POST'])
def home():
#'{"events":[{"type":"message","replyToken":"1bf3506d304941edafd27e6d7e440e90",
#              "source":{"userId":"U6b48dcbad37c37ed6f30eb8b64906369","type":"user"},
#              "timestamp":1506152275814,"message":{"type":"text","id":"6738796323388","text":"ggff"}}]}'
   
    
#    print("Request body: %s" % body)
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    user_id=request.json["events"][0]["source"]["userId"]
    print("message: %s " %  request.json["events"][0]["message"]["text"])
    print("userId: %s " %  request.json["events"][0]["source"]["userId"])
    #print(body["event"][0]["sourec"]["userID"])
    #print(body["event"][0]["message"]["text"])

    line_bot_api.push_message(user_id, TextSendMessage(text='Hello World!'))

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()