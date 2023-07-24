from telegram import Update, ReplyKeyboardRemove
from telegram.ext import Application, ContextTypes, CommandHandler, ConversationHandler, MessageHandler, filters, \
    CallbackQueryHandler

from classes.data import UserAnswers
from classes.states import States
from extensions.process.distance import receive_distance
from extensions.process.kinds import no_keywords, receive_keywords
from extensions.process.location import receive_location
from extensions.process.prices import receive_prices
from extensions.process.rates import receive_rates
from extensions.process.result import receive_result_reactions


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Cancel the conversation.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    if context.chat_data.get("data"):
        context.chat_data.pop("data")

    await update.message.reply_text("好的！我清除了對話資料，讓我們從頭再來一次 ✨")

    return ConversationHandler.END


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start the conversation.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    context.chat_data.update({"data": UserAnswers()})

    await update.message.reply_text(
        "嗨！我是 YumPicker\n"
        "請傳送給我你的位置訊息，讓我幫你找出附近的餐廳 🍽️",
        reply_markup=ReplyKeyboardRemove()
    )

    return States.ASKING_LOCATION


def setup(application: Application):
    application.add_handler(
        ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                States.ASKING_LOCATION: [MessageHandler(filters.LOCATION, receive_location)],
                States.ASKING_DISTANCE: [CallbackQueryHandler(receive_distance, pattern=r"distance\(.*\)")],
                States.ASKING_RATES: [CallbackQueryHandler(receive_rates, pattern=r"rates\(.*\)")],
                States.ASKING_PRICES: [CallbackQueryHandler(receive_prices, pattern=r"prices\(.*\)")],
                States.ASKING_KEYWORDS: [CallbackQueryHandler(no_keywords, pattern=r"no_keyword"),
                                         MessageHandler(filters.TEXT, receive_keywords)],
                States.RESULT: [CallbackQueryHandler(receive_result_reactions, pattern=r"result\(.*\)")]
            },
            fallbacks=[CommandHandler("cancel", cancel)]
        )
    )
