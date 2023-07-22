from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes, Application, CallbackQueryHandler


async def ask_types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    keyboard = [
        [InlineKeyboardButton("中式", callback_data="to_result")],
        [InlineKeyboardButton("日式", callback_data="to_result")],
        [InlineKeyboardButton("韓式", callback_data="to_result")],
        [InlineKeyboardButton("西式", callback_data="to_result")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_result")]
    ]

    await query.edit_message_text(text="你想吃什麼類型的料理？", reply_markup=InlineKeyboardMarkup(keyboard))


def setup(application: Application):
    application.add_handler(CallbackQueryHandler(ask_types, pattern="to_types"))
