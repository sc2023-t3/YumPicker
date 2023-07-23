from telegram import Update
from telegram.ext import ContextTypes

from classes.states import States
from extensions.process.distance import ask_distance


async def receive_location(update: Update, context: ContextTypes.DEFAULT_TYPE) -> States:
    """
    Receive the location from the user.
    :param update: The update object from telegram.
    :param context: The context object from telegram.
    """
    context.chat_data.get("data").location = update.message.location

    await ask_distance(update, context)
    return States.ASKING_DISTANCE
