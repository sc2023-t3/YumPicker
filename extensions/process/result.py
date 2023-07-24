import random
from os import getenv

import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from classes.data import UserAnswers
from classes.restaurant import Restaurant
from classes.states import States


def check_restaurant(restaurant: Restaurant, data: UserAnswers) -> bool:
    return restaurant.open_now and \
        restaurant.price_level >= int(data.price.value) and \
        restaurant.rating >= int(data.rates.value)


def fetch_restaurants(data: UserAnswers) -> list[Restaurant]:
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json" \
          f"?location={data.location.latitude},{data.location.longitude}" \
          f"&radius={data.distance.value}" \
          f"&type=restaurant" \
          f"&language=zh-TW" \
          f"&key={getenv('GOOGLE_MAP_API_KEY')}" + \
          (f"&keyword={data.keywords}" if data.keywords else "")

    response = requests.get(url).json()

    results: list[Restaurant] = []

    for entry in response["results"]:
        restaurant = Restaurant.from_dict(entry)
        if check_restaurant(restaurant, data):
            results.append(restaurant)

    return results


async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: UserAnswers = context.chat_data.get("data")  # skipcq: PYL-W0612

    try:
        restaurant: Restaurant = random.choice(fetch_restaurants(data))
    except IndexError:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="很抱歉，我找不到符合您需求的餐廳😢")
        return ConversationHandler.END

    keyboard = [
        [InlineKeyboardButton(
            "🗾 Google Map",
            url=f"https://www.google.com/maps/search/{restaurant.name}/@{restaurant.location.latitude},{restaurant.location.longitude},15z"
        )],
        [InlineKeyboardButton("🔁 再來一次", callback_data="result(retry)")],
        [InlineKeyboardButton("🛑 停止對話", callback_data="result(stop)")]
    ]

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="🍽️ 這是你的結果！\n\n"
             f"📍 店名：{restaurant.name}\n"
             f"💰 價位：{'$' * restaurant.price_level}\n"
             f"✨ 評價：{'⭐' * int(restaurant.rating)}\n",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def receive_result_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.callback_query.data:
        case "result(retry)":
            await send_result(update, context)
            return States.RESULT

        case "result(stop)":
            await update.callback_query.edit_message_text("好的！我清除了對話資料，讓我們從頭再來一次 ✨")
            return ConversationHandler.END
