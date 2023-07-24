import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.data import Price
from classes.states import States
from extensions.process.kinds import ask_keywords


async def ask_prices(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰💰", callback_data="prices(1)")],
        [InlineKeyboardButton("💰💰💰", callback_data="prices(2)")],
        [InlineKeyboardButton("💰💰💰💰", callback_data="prices(3)")],
        [InlineKeyboardButton("💰💰💰💰💰", callback_data="prices(4)")],
        [InlineKeyboardButton("我不知道 / 幫我決定😶", callback_data="prices(0)")]
    ]

    await update.callback_query.edit_message_text(
        text="你的錢包有多深💲？",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Ask user how much they want to spend.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    prices = re.search(r"prices\((.*)\)", update.callback_query.data)

    context.chat_data.get("data").price = Price(prices.group(1))

    await ask_keywords(update, context)
    return States.ASKING_KEYWORDS
