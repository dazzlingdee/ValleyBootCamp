from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
from watson_developer_cloud import ConversationV1
import json
import sqlite3


print('hey')
conn = sqlite3.connect('mydatabase.db')
c = conn.cursor()
c.execute("SELECT * FROM mytab")
rows=c.fetchall()
#for row in rows:
    #print(row)                           
conn.commit()
conn.close()

context = None
print('hey1')

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    print('h')
    update.message.reply_text('Hey!Welcome to TravelHunt')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def message(bot, update):
    print('Received an update')
    global context

   # conversation = ConversationV1(username='28ec8318-c2b4-41de-b32d-c58c5a8c4506',  # TODO
    #                              password='Uym68zzKTA6X',  # TODO
	#			  version='2018-02-16')
    conversation = ConversationV1(version='2018-07-10',
                        iam_api_key='ypiFBBkjolaveQQBhjg6yIFnLZAZzxO7KY7dJ29Mc41F',
                        url='https://gateway-wdc.watsonplatform.net/assistant/api')

    print(conversation)
    print(type(context))
    print(context)
    #conversation.set_url('https://gateway-wdc.watsonplatform.net/assistant/api')
    
    print('hello' + update.message.text)

    # get response from watson
    response = conversation.message(
        workspace_id='62b52706-21b5-428d-9bba-780ccd785b6e',  # TODO
        input={'text': update.message.text},
        context=context)
    print('hello')
    if((update.message.text)=='Tamil'):
       print('Deeksha')
    print(json.dumps(response, indent=2))
    context = response['context']

    # build response
    resp = ''
    for text in response['output']['text']:
        resp += text
    
    update.message.reply_text(resp)
    



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

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    


if __name__ == '__main__':
    main()
