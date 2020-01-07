"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
import random
import chats
import google_search


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')
    boto_message = boto_response(user_message)
    return json.dumps(boto_message)

def boto_response(user_message):

    user_message.lower()
    split_user_message = user_message.split(" ")

    if chats.name_checked == 0:
        name = split_user_message[-1]
        chats.name = name.capitalize()
        chats.name_checked = 1
        animation = "ok"
        boto_text = f"hi, {chats.name}! {random.choice(chats.bot_saying['greeting'])}"

    elif chats.swear_counter == 3:
        animation = "takeoff"
        boto_text = "That's it. Screw you guys, I'm going home."

    elif any(swear in split_user_message for swear in chats.bot_hearing["swearing"]):
        animation = "no"
        boto_text = random.choice(chats.bot_saying["swearing"])
        chats.swear_counter += 1

    elif check_search(user_message):
        animation = "excited"
        boto_text = google_search.chatbot_query(user_message)

    elif keyword_check(user_message):
        animation, boto_text = keyword_response(user_message)

    else:
        animation = "confused"
        boto_text = random.choice(chats.bot_saying["confused"]) + user_message

    return {"animation": animation, "msg": boto_text}

def check_search(message):
    search_triggers = ["who", "what", "when", "why"]
    if ("you know" in message) or (not "you" in message):
        for word in search_triggers:
            if word in message:
                return True
    elif "where" in message:
        return False
    elif "?" in message and not ("you" or "i") in message:
        return True
    else:
        return False

def keyword_check(user_message):
    for key in chats.bot_hearing:
        for word in chats.bot_hearing[key]:
            if word in user_message:
                return True

def keyword_response(user_message):
    for key in chats.bot_hearing:
        for word in chats.bot_hearing[key]:
            if word in user_message:
                response = random.choice(chats.bot_saying[key])
                return [key, response]

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
