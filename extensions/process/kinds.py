from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from classes.states import States


async def ask_kinds(update: Update, _: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    keyboard = [
        [InlineKeyboardButton("中式🥟", callback_data="to_result")],
        [InlineKeyboardButton("日式🍣", callback_data="to_result")],
        [InlineKeyboardButton("韓式🥘", callback_data="to_result")],
        [InlineKeyboardButton("西式🍕", callback_data="to_result")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_result")]
    ]

    await query.edit_message_text(text="今晚,我想來點🍽️？", reply_markup=InlineKeyboardMarkup(keyboard))


async def receive_kinds(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Ask user what type of food they want to eat.
    :param update: The update object from telegram.
    :param _: The context object from telegram.
    """
    query = update.callback_query

    await query.answer()

    keyboard = [
        [InlineKeyboardButton("中式🥟", callback_data="to_result")],
        [InlineKeyboardButton("日式🍣", callback_data="to_result")],
        [InlineKeyboardButton("韓式🥘", callback_data="to_result")],
        [InlineKeyboardButton("西式🍕", callback_data="to_result")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_result")]
    ]

    await query.edit_message_text(text="今晚,我想來點🍽️？", reply_markup=InlineKeyboardMarkup(keyboard))

    return States.RESULT
