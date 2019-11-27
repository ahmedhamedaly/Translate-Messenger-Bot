from flask import Flask, request
from pymessenger.bot import Bot
from googletrans import Translator
from langdetect import detect

app = Flask(__name__)
ACCESS_TOKEN = "EAAIkgXGxCgQBAHREPjQwT9biWkQumEL3diMZBbJhZA4gBEnGFLpLZCStIlkC8H6f3GDEnS6ScFpnSM4VZCZAmy1ghKwmNNRNrmIZAPXFncz0HLcdQTrX7rPq8ol4wZASSB1c1WxKnESq9nO2ZBD45v2nfj0SYy8noLGGucAF0HKpXgZDZD"
VERIFY_TOKEN = "hello"
bot = Bot(ACCESS_TOKEN)


@app.route("/", methods=['GET'])
def get_request():
    token_sent = request.args.get("hub.verify_token")
    return verify_fb_token(token_sent)


@app.route("/", methods=['POST'])
def post_request():
    output = request.get_json()
    print(output)
    for event in output['entry']:
        messaging = event['messaging']
        for message in messaging:
            if message.get('message'):
                # Facebook Messenger ID for user so we know where to send response back to
                recipient_id = message['sender']['id']
                if message['message'].get('text'):
                    response_sent_text = get_message(message['message'].get('text'))
                    send_message(recipient_id, response_sent_text)
                # if user sends us a GIF, photo,video, or any other non-text item
                if message['message'].get('attachments'):
                    response_sent_nontext = get_message()
                    send_message(recipient_id, response_sent_nontext)
    return "ok", 200


def verify_fb_token(token_sent):
    if token_sent == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return 'Invalid verification token'


def get_message(message):
    translator = Translator()
    lang = detect(message)
    if lang == "en":
        return translator.translate(message, dest="ar").text
    else:
        return translator.translate(message, dest="en").text


def send_message(recipient_id, response):
    bot.send_text_message(recipient_id, response)
    return "success"


if __name__ == "__main__":
    app.run(debug=True, port=5000)