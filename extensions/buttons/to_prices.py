from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, Application, CallbackQueryHandler


async def ask_prices(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Ask user how much they want to spend.
    :param update: The update object from telegram.
    :param _: The context object from telegram.
    """
    query = update.callback_query

    await query.answer()

    keyboard = [
        [InlineKeyboardButton("$", callback_data="to_types")],
        [InlineKeyboardButton("$$", callback_data="to_types")],
        [InlineKeyboardButton("$$$", callback_data="to_types")]
    ]

    await query.edit_message_text(text="你錢包有多深？", reply_markup=InlineKeyboardMarkup(keyboard))


def setup(application: Application):
    application.add_handler(CallbackQueryHandler(ask_prices, pattern="to_prices"))
