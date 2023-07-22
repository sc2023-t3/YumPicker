from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.states import States
from extensions.process.prices import ask_prices


async def ask_rates(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_prices")],
    ]

    await update.callback_query.edit_message_text(
        text="你猜這家餐廳評價多少？✨", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Ask user for the lowest rates of the restaurant they can accept.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    query = update.callback_query

    await query.answer()

    await ask_prices(update, context)
    return States.ASKING_PRICES
