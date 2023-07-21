from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMedia
from telegram.ext import ContextTypes


async def ask_length(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("<100m", callback_data="to_rates"),
            InlineKeyboardButton("100~1000m", callback_data="to_rates"),
            InlineKeyboardButton(">1000m", callback_data="to_rates")
        ],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_rates")]
    ]

    await update.message.reply_text("你想要走多遠？", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_rates(query: CallbackQuery, update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("⭐⭐⭐⭐⭐", callback_data="to_prices")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_prices")],
    ]

    await query.edit_message_text(text="你能接受最低多爛的餐廳？", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_prices(query: CallbackQuery, update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("$", callback_data="to_types")],
        [InlineKeyboardButton("$$", callback_data="to_types")],
        [InlineKeyboardButton("$$$", callback_data="to_types")]
    ]

    await query.edit_message_text(text="你錢包有多深？", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_types(query: CallbackQuery, update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("中式", callback_data="to_result")],
        [InlineKeyboardButton("日式", callback_data="to_result")],
        [InlineKeyboardButton("韓式", callback_data="to_result")],
        [InlineKeyboardButton("西式", callback_data="to_result")],
        [InlineKeyboardButton("我不知道 / 幫我決定", callback_data="to_result")]
    ]

    await query.edit_message_text(text="你想吃什麼類型的料理？", reply_markup=InlineKeyboardMarkup(keyboard))


async def ask_result(query: CallbackQuery, update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "🗾 Google Map",
            url="https://www.google.com.tw/maps/place/%E5%9C%8B%E7%AB%8B%E9%99%BD%E6%98%8E%E4%BA%A4%E9%80%9A%E5%A4%A7%E5%AD%B8%E7%AC%AC%E4%BA%8C%E9%A4%90%E5%BB%B3/@24.7879049,120.9975688,17.63z/data=!3m1!5s0x3468360e62bbab7b:0x4cf3e94af2597f85!4m6!3m5!1s0x34683611dcf63a29:0xc53353416c0f7c1e!8m2!3d24.789302!4d120.997197!16s%2Fg%2F1pzwsht95?hl=zh-TW&entry=ttu"
        )],
        [InlineKeyboardButton("🔁 再來一次", callback_data="to_length")]
    ]

    await query.edit_message_text(
        text="🍽️ 這是你的結果！\n\n"
             "📍 店名：國立陽明交通大學第二餐廳\n"
             "🏷️ 類型：中式\n"
             "💰 價位：$ (100~200元)\n"
             "🚶 距離：1.2km",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
