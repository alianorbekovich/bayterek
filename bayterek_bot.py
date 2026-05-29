import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8544157950:AAGPPC_acxKZWu7Z6LzX3qFhW03xIAzyXS0")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

MENU = {
    "beshbarmaq": {
        "title": "🍲 Бешбармоқлар ва Ассортилар",
        "items": [
            ("Бешбармоқ (1 порция)", "110 000"),
            ("Бешбармоқ (2 порция)", "220 000"),
            ("Бешбармоқ (3 порция)", "330 000"),
            ("Бешбармоқ (Кичик порция)", "65 000"),
            ("Астау Ассорти", "210 000"),
            ("Астау Ассорти (Катта)", "320 000"),
            ("Гўштли Ассорти Байтерек", "155 000"),
            ("Гўштли Ассорти (Оддий)", "135 000"),
            ("Қази (Донаси)", "15 000"),
            ("Қўшимча Хамир (100 гр)", "20 000"),
            ("Хамир устига гўшт (100 гр)", "30 000"),
        ]
    },
    "issiq": {
        "title": "🔥 Иссиқ ва Миллий Таомлар",
        "items": [
            ("Қозон кабоб", "60 000"),
            ("Норин (Қазилик)", "45 000"),
            ("Норин (Қазисиз)", "30 000"),
            ("Қовурма Лағмон", "40 000"),
            ("Уйғурча Лағмон", "40 000"),
            ("Тушёнка", "45 000"),
            ("Фаршированный перец", "30 000"),
            ("Пегодя (1 дона)", "10 000"),
            ("Кукси (Катта порция)", "35 000"),
            ("Кукси (Ўртача порция)", "30 000"),
        ]
    },
    "shorva": {
        "title": "🥣 Шўрвалар",
        "items": [
            ("Шўрва қайнатма (Мол гўштли)", "40 000"),
            ("Фрикаделка шўрва", "30 000"),
            ("Чучвара шўрва", "30 000"),
            ("Чучвара (Қуюқ)", "35 000"),
            ("Ассорти шўрва", "40 000"),
            ("Қази бульон", "40 000"),
        ]
    },
    "salat": {
        "title": "🥗 Салатлар (300 гр)",
        "items": [
            ("Байтерек фирмий салати", "50 000"),
            ("Мимоза салати", "45 000"),
            ("Сельдь под шубой", "45 000"),
            ("Оливье салати", "40 000"),
            ("Грекча салат", "45 000"),
            ("Цезар салати", "45 000"),
            ("Пикантный салати", "45 000"),
            ("Нежность салати", "45 000"),
            ("Аппетитный салати", "45 000"),
            ("Гурман салати", "45 000"),
            ("Восточный салати", "45 000"),
            ("Испанский салати", "45 000"),
            ("Солнце салати", "45 000"),
            ("Баҳорги салат", "18 000"),
            ("Ачиқ-чучук салати", "18 000"),
        ]
    },
    "gazak": {
        "title": "🥒 Газаклар ва Қўшимчалар",
        "items": [
            ("Балиқли Хе", "45 000"),
            ("Қозоқча Наггетслар", "45 000"),
            ("Кавказча Ассорти", "35 000"),
            ("Русча Сельдь", "30 000"),
            ("Сабзавотли Ассорти", "22 000"),
            ("Тузламалар Ассортиси", "22 000"),
            ("Сузма", "12 000"),
            ("Баурсак (Донаси)", "3 000"),
            ("Лепёшка (Иссиқ нон)", "5 000"),
            ("Лимон (Тилимланган)", "6 000"),
        ]
    },
    "ichimlik": {
        "title": "🥤 Сувлар ва Ичимликлар",
        "items": [
            ("Coca-Cola / Fanta / Pepsi", "нарх сўранг"),
            ("Сок Сочная долина", "нарх сўранг"),
            ("Чортоқ минерал суви", "нарх сўранг"),
            ("Biolife минерал суви", "нарх сўранг"),
            ("Уй кампоти", "нарх сўранг"),
            ("Тоза Қимиз", "нарх сўранг"),
        ]
    },
}

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🍲 Бешбармоқлар", callback_data="beshbarmaq")],
        [InlineKeyboardButton("🔥 Иссиқ таомлар", callback_data="issiq")],
        [InlineKeyboardButton("🥣 Шўрвалар", callback_data="shorva")],
        [InlineKeyboardButton("🥗 Салатлар", callback_data="salat")],
        [InlineKeyboardButton("🥒 Газаклар", callback_data="gazak")],
        [InlineKeyboardButton("🥤 Ичимликлар", callback_data="ichimlik")],
        [InlineKeyboardButton("📞 Буюртма бериш", callback_data="buyurtma")],
        [InlineKeyboardButton("📍 Манзил", callback_data="manzil")],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_keyboard():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Асосий меню", callback_data="main")]])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "🍽 *БАЙТЕРЕК — МИЛЛИЙ ТАОМЛАР МАСКАНИ* ✨\n\n"
        "Хуш келибсиз! Ҳар бир шохона лаззат — сиз учун!\n\n"
        "Қуйидаги бўлимлардан бирини танланг:"
    )
    await update.message.reply_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        text = "🍽 *БАЙТЕРЕК* ✨\n\nБўлимни танланг:"
        await query.edit_message_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")

    elif data in MENU:
        cat = MENU[data]
        lines = [f"*{cat['title']}*\n"]
        for name, price in cat["items"]:
            lines.append(f"• {name} — *{price} сўм*")
        text = "\n".join(lines)
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif data == "buyurtma":
        text = (
            "📞 *Буюртма бериш учун:*\n\n"
            "📱 +998 99 788-60-67\n\n"
            "🚀 Етказиб бериш хизмати мавжуд!"
        )
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

    elif data == "manzil":
        text = (
            "📍 *Манзилимиз:*\n\n"
            "Қибрай тумани, Уймоут,\n"
            "Соҳибкор кўчаси, 156-уй\n\n"
            "📱 +998 99 788-60-67"
        )
        await query.edit_message_text(text, reply_markup=back_keyboard(), parse_mode="Markdown")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)
