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
          f"?location={data.location.longitude},{data.location.latitude}" \
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

    restaurant: Restaurant = random.choice(fetch_restaurants(data))

    print(restaurant)

    keyboard = [
        [InlineKeyboardButton(
            "🗾 Google Map",
            url="https://www.google.com.tw/maps/place/%E5%9C%8B%E7%AB%8B%E9%99%BD%E6%98%8E%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%B8%E7%AC%AC%E4%BA%8C%E9%A4%90%E5%BB%B3/@24.7879049,120.9975688,17.63z/data=!3m1!5s0x3468360e62bbab7b:0x4cf3e94af2597f85!4m6!3m5!1s0x34683611dcf63a29:0xc53353416c0f7c1e!8m2!3d24.789302!4d120.997197!16s%2Fg%2F1pzwsht95?hl=zh-TW&entry=ttu"
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

    await context.bot.send_location(
        chat_id=update.effective_chat.id,
        latitude=restaurant.location.latitude,
        longtitude=restaurant.location.longitude
    )
    picture_url = "https://lh3.googleusercontent.com/places/ANJU3DvZWxia50ruLDuyjO4hJnYQwybjhkEo5ssN_bxAe5Ex7BxQADqrNI_kwW8EhfocsN8njDeGsjBOH7KGDP3Zbs-57XySvBqN0KA=s1600-w1280-h720"
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=picture_url
    )


async def receive_result_reactions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    match update.callback_query.data:
        case "result(retry)":
            await send_result(update, context)
            return States.RESULT

        case "result(stop)":
            await update.callback_query.edit_message_text("好的！我清除了對話資料，讓我們從頭再來一次 ✨")
            return ConversationHandler.END
