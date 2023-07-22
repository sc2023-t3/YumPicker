import logging

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
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    logging.info(f"User {update.effective_user.id} sent location: {latitude}, {longitude}")

    context.user_data.update({"latitude": latitude, "longitude": longitude})

    await ask_distance(update, context)
    return States.ASKING_DISTANCE
