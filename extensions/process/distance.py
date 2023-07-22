from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from classes.states import States
from extensions.process.rates import ask_rates


async def ask_distance(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🩴 <100m", callback_data="to_rates")],
        [InlineKeyboardButton("👟 100~1000m", callback_data="to_rates")],
        [InlineKeyboardButton("🥾 >1000m", callback_data="to_rates")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_rates")]
    ]

    await update.message.reply_text(
        text="你想要跑超馬、半馬還是學校體適能？",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Ask user how far they want to go.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    query = update.callback_query

    await query.answer()

    await ask_rates(update, context)
    return States.ASKING_RATES
