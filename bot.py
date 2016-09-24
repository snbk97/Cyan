import requests
import time
from unidecode import unidecode
from pprint import pprint
import telepot
import json
from new_google import *
from ffs import isAdmin

__Author__ = "@snbk97"


def url_short(msg, chat_id):
    if('reply_to_message' in msg):
        x_msg = msg['reply_to_message']['text'].lower().strip().split(' ')
        # bot.sendMessage(chat_id, x_msg)
        for i in range(-1, len(x_msg)):  # for x in x_msg:
            if(x_msg[i][:4] == "http"):
                final_url = "Short URL: " + g_short(x_msg[i])
            else:
                final_url = "No URL in this Message"

    else:
        final_url = "Reply to a message having an URL with url.short"

    return final_url


def isAdmin(chat_id):
    bot_id = 187719572
    chat_info = bot.getChatMember(chat_id, bot_id)
    stat = chat_info['status'].split(',')[0]
    if (stat.lower() == "administrator"):
        rr = '1'
    else:
        rr = '0'
    return rr


def getInfo(msg, chat_id):
    if('reply_to_message' in msg):
        chat_info = bot.getChatMember(
            chat_id, msg['reply_to_message']['from']['id'])
        rr = "Status: " + chat_info['status'].split(',')[0] + "\nUsername: " + chat_info[
            'user']['username'] + "\nID: " + str(chat_info['user']['id'])
    else:
        rr = "Reply to a message with getinfo"

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


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    # print (content_type, chat_type, chat_id)
    if(chat_type == "group" or chat_type == "supergroup"):
        try:
            if(msg['text'].lower()[:7] == "hi cyan"):
                hi_msg = "Hi! " + msg['from']['first_name']
                bot.sendMessage(chat_id, hi_msg,
                                reply_to_message_id=msg['message_id'])
#---------------------------------------------------------------------------------------------------------------------------#
                ## GROUP ADMINISTRATION ##
            if(isAdmin(chat_id) == '1'):
                if(msg['from']['id'] == 167122186 and msg['text'].lower().strip().split(' ')[0] == "kick"):
                    kick(chat_id, msg['text'].lower().strip().split(' ')[1])
                    bot.sendMessage(chat_id, "Kicked")

                if(msg['text'].lower().strip().split(' ')[0] == "unban" and msg['from']['id'] == 167122186):
                    unban(chat_id, msg['text'].lower().strip().split(' ')[1])
                    bot.sendMessage(
                        chat_id, "Unbanned" + str(msg['text'].lower().strip().split(' ')[1]))

                elif(msg['from']['id'] != 167122186 and msg['text'].lower().strip().split(' ')[0] == "kick"):
                    bot.sendMessage(chat_id, "You're not the bot's owner")

            elif(isAdmin(chat_id) == '0' and msg['text'].lower().strip().split(' ')[0] == "kick"):
                bot.sendMessage(chat_id, "I'm not Admin here",
                                reply_to_message_id=msg['message_id'])
#---------------------------------------------------------------------------------------------------------------------------#
            if(msg['text'].lower().strip().split(' ')[0] == "bot.admin"):
                if(isAdmin(chat_id) == '1'):
                    isadmin_msg = 'Yes'
                else:
                    isadmin_msg = 'No'
                bot.sendMessage(chat_id, isadmin_msg,
                                reply_to_message_id=msg['message_id'])

            if(msg['text'].lower().strip().split(' ')[0] == "bot.leave" and msg['from']['id'] == 167122186):
                bot.sendMessage(chat_id, "Bye!")
                leave(chat_id)
            elif(msg['text'].lower().strip().split(' ')[0] == "bot.leave" and msg['from']['id'] != 167122186):
                bot.sendMessage(chat_id, "Not Allowed",
                                reply_to_message_id=msg['message_id'])

            if(msg['text'].lower().strip().split(' ')[0] == "whoami"):
                chat_info = bot.getChatMember(
                    chat_id, msg['from']['id'])
                bot.sendMessage(chat_id, "Status: " + chat_info['status'].split(',')[0] + "\nUsername: " + chat_info['user']['username'] + "\nID: " + str(chat_info['user']['id']),
                                reply_to_message_id=msg['message_id'])

            if(msg['text'].lower().strip().split(' ')[0] == "getinfo"):
                bot.sendMessage(chat_id, getInfo(msg, chat_id),
                                reply_to_message_id=msg['message_id'])

            if(msg['text'].lower().strip().split(' ')[0] == "group.count"):
                chat_count = bot.getChatMembersCount(chat_id)
                bot.sendMessage(chat_id, "Total Member: " + str(chat_count) +
                                " ", reply_to_message_id=msg['message_id'])

        except:
            pass

# ----------------------------------------------------------------------------------------------------------------------------#
    if (content_type == 'text' and chat_type == 'private'):
        # pprint(msg)
        print"\n"
        print (msg['from']['first_name'] + "(" +
               str(msg['chat']['id']) + ")" + " --> " + unidecode(msg['text']).encode("unicode-escape"))
        if(msg['text'].lower() == "hi"):
            hi_msg = "Hi! " + msg['from']['first_name']
            bot.sendMessage(chat_id, hi_msg,
                            reply_to_message_id=msg['message_id'])
        if(msg['text'].lower() == "/start"):
            start_msg = " I'm Cyan\nI'm a naural talking bot, but still in development process.\nFor starters, I know few stuffs" + \
                (u'\U0001f61c') + \
                ": \n- define <word>\n- shorten url [url.short]\n- and few group admininstering features"
            bot.sendMessage(chat_id, start_msg)
    try:
        if (content_type == 'text' and chat_type == 'group' or chat_type == 'supergroup'):
            pprint(msg)
            print"\n"
            print (msg['from']['first_name'] +
                   "(group:" + msg['chat']['title'] + ")" + " --> " + unidecode(msg['text']).encode("unicode-escape"))
            print "--------------------------------------\n"
    except KeyError:
        print "KeyError line 28"
# ----------------------------------------------------------------------------------------------------------------------------#
        # Dictionary module / Define
    try:
        if(msg['text'][:6] == 'define' or msg['text'][:6] == 'Define'):
            try:
                msg_split = msg['text'].strip().split(msg['text'][:6])
                if(len(msg_split) > 1 and msg_split[0] == ''):
                    x = mean(unidecode(msg_split[1]))
                    # pprint(x)
                    bot.sendMessage(
                        chat_id, x, reply_to_message_id=msg['message_id'])
            except IndexError:
                err_msg = "Sorry Definition not found"
                bot.sendMessage(chat_id, err_msg,
                                reply_to_message_id=msg['message_id'])

    except KeyError:
        if('new_chat_member' in msg):
            # pprint(msg)
            if(len(msg['new_chat_member']['first_name']) > 0):
                welcome_msg = "Hello! " + \
                    msg['new_chat_member']['first_name'] + \
                    "\n[" + str(msg['new_chat_member']['id']) + "]"
                bot.sendMessage(chat_id, welcome_msg,
                                reply_to_message_id=msg['message_id'])
        else:
            pass

# ----------------------------------------------------------------------------------------------------------------------------#
    try:
        rockr = msg['text'].lower().strip().split(' ')
        props = ["rocks", "rock", "awesome", "cool"]
        cons = ["suck", "sucks", "dumb", "fag",
                        "faggot", "ugly", "gay", "fuck"]
        # if("nigga")

        if("cyan" in rockr):
            for rox in rockr:
                for prop in props:
                    if rox.lower() == prop:
                        if(prop in props):
                            bot.sendMessage(chat_id, "Thanks Boo-!",
                                            reply_to_message_id=msg['message_id'])

        if("cyan" in rockr):
            for rox in rockr:
                for con in cons:
                    if (rox.lower() == con):
                        if(con == "suck" or con == "sucks" or con == "fuck"):
                            reply_vid = open('gif/con_reply.gif.mp4', 'rb')
                            bot.sendVideo(chat_id, reply_vid,
                                          reply_to_message_id=msg['message_id'])
                        elif(con == "ugly"):
                            bot.sendMessage(chat_id, "LoL! Look Who's talking!",
                                            reply_to_message_id=msg['message_id'])
                        elif(con == "dumb"):
                            bot.sendMessage(chat_id, "According to recent studies, people like" +
                                            " you have IQ lower than the room temperature!",
                                            reply_to_message_id=msg['message_id'])
                        elif(con == "gay" or con == "faggot" or con == "fag"):
                            bot.sendMessage(chat_id, "That's not what your mommy would say !",
                                            reply_to_message_id=msg['message_id'])
        if(msg['text'].lower() == "ping cyan"):
            bot.sendMessage(chat_id, "Pong",
                            reply_to_message_id=msg['message_id'])

        if(msg['text'].lower()[:7] == "hi cyan"):
            hi_msg = "Hi! " + msg['from']['first_name']
            bot.sendMessage(chat_id, hi_msg,
                            reply_to_message_id=msg['message_id'])
        if(msg['text'].lower().strip() == "url.short"):
            bot.sendMessage(chat_id, url_short(msg, chat_id),
                            disable_web_page_preview=1)

    except KeyError:
        pass
# ----------------------------------------------------------------------------------------------------------------------------#


key = 'YOUR_TG_API_KEY'
bot = telepot.Bot(key)
bot.getUpdates(offset=100000001)
bot.message_loop(handle,)

print ("Listening...\n")

while 1:
    time.sleep(10)
