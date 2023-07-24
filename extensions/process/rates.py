import re

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.data import Rates
from classes.states import States
from extensions.process.prices import ask_prices


async def ask_rates(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐", callback_data="rates(1)")],
        [InlineKeyboardButton("⭐⭐", callback_data="rates(2)")],
        [InlineKeyboardButton("⭐⭐⭐", callback_data="rates(3)")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data="rates(4)")],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="rates(5)")],
        [InlineKeyboardButton("我不知道 / 幫我決定😶", callback_data="rates(0)")],
    ]

    await update.callback_query.edit_message_text(
        text="就是要對決✨？", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Ask user for the lowest rates of the restaurant they can accept.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    rates = re.search(r"rates\((.*)\)", update.callback_query.data)

    context.chat_data.get("data").rates = Rates(rates.group(1))

    await ask_prices(update, context)
    return States.ASKING_PRICES
