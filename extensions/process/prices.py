from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.states import States
from extensions.process.kinds import ask_kinds


async def ask_prices(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💰", callback_data="to_types")],
        [InlineKeyboardButton("💰💰", callback_data="to_types")],
        [InlineKeyboardButton("💰💰💰", callback_data="to_types")]
    ]

    await update.callback_query.edit_message_text(
        text="你的錢包有多深？",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Ask user how much they want to spend.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    query = update.callback_query

    await query.answer()

    await ask_kinds(update, context)
    return States.ASKING_KINDS
