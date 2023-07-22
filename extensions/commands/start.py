from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, \
    CallbackQueryHandler

from classes.states import States
from extensions.process.distance import receive_distance
from extensions.process.location import receive_location
from extensions.process.prices import receive_prices
from extensions.process.rates import receive_rates


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Start the conversation.
    :param update: The update object from telegram.
    :param _: The context object from telegram.
    """
    await update.message.reply_text(
        "Hello, I'm a bot that helps you find a restaurant to eat.\n"
        "Please send me your location so I can find the nearest restaurant for you.",
        reply_markup=ReplyKeyboardRemove()
    )

    return States.ASKING_LOCATION


async def done(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display the gathered info and end the conversation."""
    await update.message.reply_text(
        f"Done",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def setup(application: Application):
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                States.ASKING_LOCATION: [MessageHandler(filters.LOCATION, receive_location)],
                States.ASKING_DISTANCE: [CallbackQueryHandler(receive_distance, pattern="^to_prices$")],
                States.ASKING_RATES: [CallbackQueryHandler(receive_rates, pattern="^to_rates$")],
                States.ASKING_PRICES: [CallbackQueryHandler(receive_prices, pattern="^to_prices$")],
                States.ASKING_KINDS: []
            },
            fallbacks=[MessageHandler(filters.Regex("^Done$"), done)]
        )
    )
