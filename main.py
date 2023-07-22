import logging
from os import getenv

from colorlog import ColoredFormatter
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from process import ask_length, ask_rates, ask_prices, ask_types, ask_result


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await ask_length(update, context)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    await query.answer()

    match query.data:
        case "to_rates":
            await ask_rates(query, update, context)
        case "to_prices":
            await ask_prices(query, update, context)
        case "to_types":
            await ask_types(query, update, context)
        case "to_result":
            await ask_result(query, update, context)


def setup_logging():
    """
    Set up the loggings for the bot
    :return: None
    """
    formatter = ColoredFormatter(
        '%(asctime)s %(log_color)s [%(levelname)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'white',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(filename="concept.log", encoding="utf-8", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logging.basicConfig(
        handlers=[stream_handler, file_handler], level=logging.INFO
    )


def main() -> None:
    load_dotenv()

    setup_logging()

    application = Application.builder().token(getenv("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
