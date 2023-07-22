from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CallbackQueryHandler, ContextTypes


async def ask_rates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    keyboard = [
        [InlineKeyboardButton("⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_prices")],
    ]

    await query.edit_message_text(text="你能接受最低多爛的餐廳？", reply_markup=InlineKeyboardMarkup(keyboard))


def setup(application: Application):
    application.add_handler(CallbackQueryHandler(ask_rates, pattern="to_rates"))
