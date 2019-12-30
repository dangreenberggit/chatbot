"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
from chats import bot_hearing, bot_saying


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    boto_message = boto_response(user_message)
    return json.dumps(boto_message)

def boto_response(user_message):
    for string in bot_hearing["afraid"]:
        if string in user_message:
            animation = "afraid"
            boto_message = random.choice(bot_saying["afraid"])

    return {"animation": animation, "msg": boto_message}

@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)

if __name__ == '__main__':
    main()
