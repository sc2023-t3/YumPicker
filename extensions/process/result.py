from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler

from classes.data import UserAnswers
from classes.states import States


async def send_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data: UserAnswers = context.chat_data.get("data")  # skipcq: PYL-W0612

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
             "📍 店名：國立陽明交通大學第二餐廳\n"
             "🏷️ 類型：中式\n"
             "💰 價位：$ (100~200元)\n"
             "🚶 距離：1.2km",
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
