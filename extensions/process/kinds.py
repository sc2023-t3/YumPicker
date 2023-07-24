from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.states import States
from extensions.process.result import send_result


async def ask_keywords(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    keyboard = [
        [InlineKeyboardButton("我不知道 / 幫我決定😶", callback_data="no_keyword")]
    ]

    await query.edit_message_text(
        text="今晚，我想來點…🍽️？ (請輸入餐廳的關鍵字)", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Ask user what type of food they want to eat.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    context.chat_data.get("data").keywords = update.message.text

    await send_result(update, context)
    return States.RESULT


async def no_keywords(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    A callback called when user selected "random" in ask_keywords.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    context.chat_data.get("data").keywords = ""

    await send_result(update, context)
    return States.RESULT
