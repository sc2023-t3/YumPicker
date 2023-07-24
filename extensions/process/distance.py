import random
import re

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

from classes.data import Distance
from classes.states import States
from extensions.process.rates import ask_rates


async def ask_distance(update: Update, _: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🩴 < 200m", callback_data="distance(200)")],
        [InlineKeyboardButton("👟 < 500m", callback_data="distance(500)")],
        [InlineKeyboardButton("🥾 < 5000m", callback_data="distance(5000)")],
        [InlineKeyboardButton("我不知道 / 幫我決定😶", callback_data="distance(random)")]
    ]

    await update.message.reply_text(
        text="你想要跑超馬、半馬還是學校體適能💦？",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_distance(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Ask user how far they want to go.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    distance = re.search(r"distance\((.*)\)", update.callback_query.data).group(1)

    if distance == "random":
        random.choice(["200", "500", "5000"])

    context.chat_data.get("data").distance = Distance(distance)

    await ask_rates(update, context)
    return States.ASKING_RATES
