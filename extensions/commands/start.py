from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, ContextTypes, CommandHandler


async def start(update: Update, _: ContextTypes.DEFAULT_TYPE):
    """
    Start the conversation.
    :param update: The update object from telegram.
    :param _: The context object from telegram.
    """
    keyboard = [
        [
            InlineKeyboardButton("<100m", callback_data="to_rates"),
            InlineKeyboardButton("100~1000m", callback_data="to_rates"),
            InlineKeyboardButton(">1000m", callback_data="to_rates")
        ],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_rates")]
    ]

    await update.message.reply_text("你想要走多遠？", reply_markup=InlineKeyboardMarkup(keyboard))


def setup(application: Application):
    application.add_handler(CommandHandler("start", start))
