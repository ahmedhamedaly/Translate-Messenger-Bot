# # Python libraries that we need to import for our bot
# import random
# from flask import Flask, request
# from pymessenger.bot import Bot
#
# app = Flask(__name__)
# ACCESS_TOKEN = 'EAAIkgXGxCgQBAEClB4WacH0ZAccXNV1irgQABA511TrgXG0gyz1965qcfxkYf52ZA2S5Ug8OE2NXNuWN7PsGbVoqpawOvp32qui6X7uVLGKuhZC1Pb2ZBqzEybU31wFiVXYCwb8n75dGHARptVpyS4f09YoHb0cgZBR25p4ytNAZDZD'
# VERIFY_TOKEN = 'hello'
# bot = Bot(ACCESS_TOKEN)
#
#
# # We will receive messages that Facebook sends our bot at this endpoint
# @app.route("/", methods=['GET', 'POST'])
# def receive_message():
#     if request.method == 'GET':
#         """Before allowing people to message your bot, Facebook has implemented a verify token
#         that confirms all requests that your bot receives came from Facebook."""
#         token_sent = request.args.get("hub.verify_token")
#         return verify_fb_token(token_sent)
#     # if the request was not get, it must be POST and we can just proceed with sending a message back to user
#     else:
#         # get whatever message a user sent the bot
#         output = request.get_json()
#         print(output)
#         for event in output['entry']:
#             messaging = event['messaging']
#             for message in messaging:
#                 if message.get('message'):
#                     # Facebook Messenger ID for user so we know where to send response back to
#                     recipient_id = message['sender']['id']
#                     if message['message'].get('text'):
#                         response_sent_text = get_message()
#                         send_message(recipient_id, response_sent_text)
#                     # if user sends us a GIF, photo,video, or any other non-text item
#                     if message['message'].get('attachments'):
#                         response_sent_nontext = get_message()
#                         send_message(recipient_id, response_sent_nontext)
#     return "Message Processed"
#
#
# def verify_fb_token(token_sent):
#     # take token sent by facebook and verify it matches the verify token you sent
#     # if they match, allow the request, else return an error
#     if token_sent == VERIFY_TOKEN:
#         return request.args.get("hub.challenge")
#     return 'Invalid verification token'
#
#
# # chooses a random message to send to the user
# def get_message():
#     sample_responses = ["You are stunning!", "We're proud of you.", "Keep on being you!",
#                         "We're greatful to know you :)"]
#     # return selected item to the user
#     return random.choice(sample_responses)
#
#
# # uses PyMessenger to send response to user
# def send_message(recipient_id, response):
#     # sends user the text message provided via input response parameter
#     bot.send_text_message(recipient_id, response)
#     return "success"
#
#
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)

import os, sys
from flask import Flask, request
from pymessenger import Bot

bot = Bot("EAAIkgXGxCgQBAPtK6yMZA2CtKnPZAHlgrasePkwFE541tZBZAaWdRvFfdfTZAHJC0N2RMv7HDfQbfZBpNZBrBfpYPKnUXbFCeViOOJx58ztNYuKINgV70x8xROARAE2CPZBPNcvOmqCMqCwZCJvZCBIWI8cc0BLpfHh6YSa9GGehgOsgZDZD")

app = Flask(__name__)


@app.route('/', methods=['GET'])
def verify():
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "hello":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200
    return "Hello Word", 200


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print(data)

    if data['object'] == 'page':
        for entry in data['entry']:
            for message in entry['messaging']:
                sender_id = message['sender']['id']
                receipient_id = message['recipient']['id']

                if message.get('message'):
                    if 'text' in message['message']:
                        message_text = message['message']['text']
                    else:
                        message_text = "no text"

                    response = message_text
                    bot.send_text_message(sender_id, response)

    return "ok", 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
