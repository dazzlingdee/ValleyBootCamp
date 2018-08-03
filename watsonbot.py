from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3

import time
import telegram
from subprocess import call
from io import BytesIO
import logging
import os
import os.path
import datetime
import sys
#updater = Updater(token= '692389114:AAEtTGqjTtaoxPHrlaay3ACYnu2uj_kjRXQ')
time = datetime.datetime.now().strftime("%d-%m-%y_%H:%M,%S")

bot = telegram.Bot(token='692389114:AAEtTGqjTtaoxPHrlaay3ACYnu2uj_kjRXQ')

stt='/home/admin1/watson/sample-telegram-app/photos/'
#bot.sendPhoto(chat_id=599070941,photo=open("/home/admin1/watson/sample-telegram-app/photos/keralahills.jpeg",'rb'))

context = None


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hey!Welcome to TravelHunt')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
   # print(places)
    print('Received an update')
    global context

   # conversation = ConversationV1(username='28ec8318-c2b4-41de-b32d-c58c5a8c4506',  # TODO
    #                              password='Uym68zzKTA6X',  # TODO
	#			  version='2018-02-16')
    conversation = ConversationV1(version='2018-07-10',
                        iam_api_key='ypiFBBkjolaveQQBhjg6yIFnLZAZzxO7KY7dJ29Mc41F',
                        url='https://gateway-wdc.watsonplatform.net/assistant/api')

    
    print('Message' + update.message.text)
    msg=update.message.text

    # get response from watson
    response = conversation.message(
        workspace_id='62b52706-21b5-428d-9bba-780ccd785b6e',  # TODO
        input={'text': update.message.text},
        context=context)
    #print('hello123')
    s=0
   
       
   #update.message.reply(img=urllib2.urlopen('index.jpeg').read())
    context = response['context']
    print(context)
    if "places" in context.keys() and "category" in context.keys():
        pl=context["places"]
        ct=context["category"]
        print(ct)
        str=""
        print(context["places"])
        conn=sqlite3.connect('mydatabase.db')
        c=conn.cursor()
        print("Entered SQL")
        try:
           c.execute("SELECT place FROM cat WHERE state=? and category=?",(pl,ct))
           rows=c.fetchall()
           update.message.reply_text("You can visit these places")
           for row in rows:
                update.message.reply_text(str.join(row))
                #update.message.reply_text(row)
           c.execute("SELECT name FROM images WHERE st=? and category=?",(pl,ct))
           rows=c.fetchall()

           for row in rows:
            #update.message.reply_text(str.join(row))
               print(row)
               print(stt+stt.join(row))
               bot.sendPhoto(chat_id=599070941,photo=open(stt+stt.join(row), 'rb'))

           conn.commit()
           conn.close()
        except:
           print("Fail")
        #del context["places"]
        del context["category"]

#insert the details of booking
    id1=" "
    name=""
    if "person" in context.keys() and "number" in context.keys() and "date" in context.keys():
        person=context["person"]
        number=context["number"]
        date=context["date"]
        conn=sqlite3.connect('mydatabase.db')
        c=conn.cursor()
        print("Enter sql")
       # c.execute("SELECT person from booking")
        #print("hat man")
        #rows=c.fetchall()
        #print("am ")
        #print(rows)
        #for row in rows:
         #  if person==name.join(row):
          #    update.message.reply_text("This name already exists..Try with different one!") 
        c.execute("INSERT INTO booking(person,number,date) values(?,?,?) ",(person,number,date))
        print("hhhhhhiiiiiii")
        conn.commit()
        conn.close()
        conn=sqlite3.connect('mydatabase.db')
        c=conn.cursor()
        print("kk")
        c.execute("SELECT rowid FROM booking WHERE person=? and number=? and date=?",(person,number,date))
        rows=c.fetchall()
        print("gggg")
        #update.message.text("Thank you for booking" )
        for row in rows:
            print(row)
            update.message.reply_text(row)
            #update.message.reply_text(row)
            print(id1)
        del context["person"]
        del context["number"]
        del context["date"]
        
        conn.commit()
        conn.close()
#cancellation
    if "cancel" in context.keys() and "person" in context.keys() and "ask" in context.keys():
        cancel=""
        person=context["person"]
        conn=sqlite3.connect('mydatabase.db')
        c=conn.cursor()
        print("Enter sql for delete")
       # c.execute("SELECT rowid from booking where person=?",(person,))
        #rows=c.fetchall()
        #for row in rows:
         #   update.message.reply_text(cancel.join(row))
        ask=context["ask"]
        if ask=="Yes":
            c.execute("DELETE FROM booking where person=? ",(person,))
            update.message.reply_text("Thank you")
        conn.commit()
        conn.close()
      
    # sql(pl)
    # build response
    resp = ''
    for text in response['output']['text']:
       print("Execute1")
       resp += text
    print('Resp',resp)
    update.message.reply_text(resp)
    if resp=="Please enter the state you want to visit..":
       flag=1
       print("after flag=",flag)
    
    print("Bad")
    print(ref)
 
    if (ref==20):
        sql()
    if ((flag==1) and (ref==10)):
        ref=20
        print('ref=',ref)
        return
   
    print("after2 flag=",flag)


   
#handle image
#print("image image")
#def photo_up(bot, update, user_data):
 #   print("I am here")
   # user = update.message.from_user
   # photo_file = bot.get_file(update.message.photo[-1].file_id)
    
   # user_data['photo'] = photo_file
    #contact_keyboard = KeyboardButton("Compartilhar telefone", request_contact=True)
    #custom_keyboard = [[contact_keyboard]]
    #reply_markup = ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True)
    #update.message.reply_text('Para completar o processo, preciso do seu telefone, pode me enviar?')
    #return PHONE
def photo_up(bot, update,user_data):
    print("Image received")
    save_path = '/home/admin1/watson/sample-telegram-app/'
    file_id = update.message.photo[-1].file_id
    newFile = bot.getFile(file_id)
    newFile.download(os.path.join(save_path, time+'.jpg'))
    bot.sendMessage(chat_id=update.message.chat_id, text="download succesful")
    filename = (time+'.jpg')
    metadata={}
    print("New one")
    print(filename)
    image=Image.open(filename)
    print("Getting meta data")
    info=image._getexif()
    #if info:

    print("Found metadata")
    for (tag,value) in image.info.items():
            tagname=TAGS.get(tag,tag)
            metadata[tagname]=value
        
            print (tagname,str(value))
    #for (tagname,value) in metadata.items():
   #         print("data aaa")
  #          print(str(tagname)+"\t"+str(value))
       
    with open(filename,"rb") as f:
        Jpegcontents = (f.read())
        if Jpegcontents.startswith(b"\xff\xd8") and Jpegcontents.endswith(b"\xff\xd9"):
            bot.sendMessage(chat_id=update.message.chat_id, text="Valid Image")
        if not Jpegcontents.startswith(b"\xff\xd8") and Jpegcontents.endswith(b"\xff\xd9"):
           os.system("rm ",filename)
    


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('692389114:AAEtTGqjTtaoxPHrlaay3ACYnu2uj_kjRXQ')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, message))

    #on command i.e image-echo the message
    try:
       dp.add_handler(MessageHandler(Filters.photo, photo_up, pass_user_data=True))
    except:
       print("Not executed")

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    


if __name__ == '__main__':
    main()
