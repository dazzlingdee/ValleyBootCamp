from telegram.ext import Updater, MessageHandler, CommandHandler, Filters
import sqlite3
conn = sqlite3.connect('mydatabase.db')

context = None

c=conn.cursor()
c.execute("INSERT INTO mytab VALUES ('Tamilnadu','ooty')")
conn.commit()
conn.close()

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    print('Received /start command')
    update.message.reply_text('Hi!')


def help(bot, update):
    print('Received /help command')
    update.message.reply_text('Help!')


def echo(bot, update):
    print('Received an update')
    update.message.reply_text(update.message.text.upper())


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater('692389114:AAEtTGqjTtaoxPHrlaay3ACYnu2uj_kjRXQ')  # TODO

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
