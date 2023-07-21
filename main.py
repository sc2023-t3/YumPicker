from os import getenv

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

from process import ask_length, ask_rates, ask_prices, ask_types, ask_result
from utils.wait_for import Waiter

waiter = Waiter()


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


def main() -> None:
    load_dotenv()

    application = Application.builder().token(getenv("TELEGRAM_TOKEN")).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
