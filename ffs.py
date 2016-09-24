import requests
import json


def isAdmin(chat_id):
    bot_id = 187719572
    chat_info = bot.getChatMember(chat_id, bot_id)
    stat = chat_info['status'].split(',')[0]
    if (stat.lower() == "administrator"):
        rr = '1'
    else:
        rr = '0'
    return rr


def getInfo(msg, chat_id,):
    if('reply_to_message' in msg):
        chat_info = bot.getChatMember(
            chat_id, msg['reply_to_message']['from']['id'])
        rr = "Status: " + chat_info['status'].split(',')[0] + "\nUsername: " + chat_info[
            'user']['username'] + "\nID: " + str(chat_info['user']['id'])
    else:
        rr = "Reply to a message with `getinfo`"

    return rr


def leave(c_id):
    bot.leaveChat(c_id)


def kick(c_id, u_id):
    bot.kickChatMember(c_id, u_id)


def unban(c_id, u_id):
    bot.unbanChatMember(c_id, u_id)


def mean(word, id=0):
    url = 'http://api.urbandictionary.com/v0/define?term=' + word
    data = requests.get(url).text
    j = json.loads(data)['list'][0]['definition']
    return j
