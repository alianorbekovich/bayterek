import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get("TOKEN", "8544157950:AAGPPC_acxKZWu7Z6LzX3qFhW03xIAzyXS0")

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Menyu
MENU = {
    "beshbarmaq": {
        "title": "🍲 Бешбармоқлар",
        "items": {
            "b1": ("Бешбармоқ (1 порция)", 110000),
            "b2": ("Бешбармоқ (2 порция)", 220000),
            "b3": ("Бешбармоқ (3 порция)", 330000),
            "b4": ("Бешбармоқ (Кичик)", 65000),
            "b5": ("Астау Ассорти", 210000),
            "b6": ("Астау Ассорти (Катта)", 320000),
            "b7": ("Гўштли Ассорти Байтерек", 155000),
            "b8": ("Гўштли Ассорти (Оддий)", 135000),
            "b9": ("Қази (Донаси)", 15000),
            "b10": ("Қўшимча Хамир (100гр)", 20000),
            "b11": ("Хамир устига гўшт (100гр)", 30000),
        }
    },
    "issiq": {
        "title": "🔥 Иссиқ таомлар",
        "items": {
            "i1": ("Қозон кабоб", 60000),
            "i2": ("Норин (Қазилик)", 45000),
            "i3": ("Норин (Қазисиз)", 30000),
            "i4": ("Қовурма Лағмон", 40000),
            "i5": ("Уйғурча Лағмон", 40000),
            "i6": ("Тушёнка", 45000),
            "i7": ("Фаршированный перец", 30000),
            "i8": ("Пегодя (1 дона)", 10000),
            "i9": ("Кукси (Катта)", 35000),
            "i10": ("Кукси (Ўртача)", 30000),
        }
    },
    "shorva": {
        "title": "🥣 Шўрвалар",
        "items": {
            "sh1": ("Шўрва қайнатма", 40000),
            "sh2": ("Фрикаделка шўрва", 30000),
            "sh3": ("Чучвара шўрва", 30000),
            "sh4": ("Чучвара (Қуюқ)", 35000),
            "sh5": ("Ассорти шўрва", 40000),
            "sh6": ("Қази бульон", 40000),
        }
    },
    "salat": {
        "title": "🥗 Салатлар",
        "items": {
            "s1": ("Байтерек фирмий салати", 50000),
            "s2": ("Мимоза", 45000),
            "s3": ("Сельдь под шубой", 45000),
            "s4": ("Оливье", 40000),
            "s5": ("Грекча салат", 45000),
            "s6": ("Цезар", 45000),
            "s7": ("Пикантный", 45000),
            "s8": ("Нежность", 45000),
            "s9": ("Аппетитный", 45000),
            "s10": ("Гурман", 45000),
            "s11": ("Восточный", 45000),
            "s12": ("Испанский", 45000),
            "s13": ("Солнце", 45000),
            "s14": ("Баҳорги салат", 18000),
            "s15": ("Ачиқ-чучук", 18000),
        }
    },
    "gazak": {
        "title": "🥒 Газаклар",
        "items": {
            "g1": ("Балиқли Хе", 45000),
            "g2": ("Қозоқча Наггетслар", 45000),
            "g3": ("Кавказча Ассорти", 35000),
            "g4": ("Русча Сельдь", 30000),
            "g5": ("Сабзавотли Ассорти", 22000),
            "g6": ("Тузламалар Ассортиси", 22000),
            "g7": ("Сузма", 12000),
            "g8": ("Баурсак (Донаси)", 3000),
            "g9": ("Лепёшка", 5000),
            "g10": ("Лимон (Тилимланган)", 6000),
        }
    },
    "ichimlik": {
        "title": "🥤 Ичимликлар",
        "items": {
            "ich1": ("Coca-Cola", 15000),
            "ich2": ("Fanta", 15000),
            "ich3": ("Pepsi", 15000),
            "ich4": ("Сок Сочная долина", 12000),
            "ich5": ("Чортоқ минерал суви", 8000),
            "ich6": ("Biolife минерал суви", 8000),
            "ich7": ("Уй кампоти", 10000),
            "ich8": ("Тоза Қимиз", 20000),
        }
    },
}

# Barcha itemlarni tekshirish uchun
ALL_ITEMS = {}
for cat_key, cat_val in MENU.items():
    for item_key, item_val in cat_val["items"].items():
        ALL_ITEMS[item_key] = {"name": item_val[0], "price": item_val[1], "cat": cat_key}

# Foydalanuvchi savatchalari
carts = {}

def get_cart(user_id):
    if user_id not in carts:
        carts[user_id] = {}
    return carts[user_id]

def format_price(price):
    return f"{price:,}".replace(",", " ")

def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🍲 Бешбармоқлар", callback_data="cat_beshbarmaq")],
        [InlineKeyboardButton("🔥 Иссиқ таомлар", callback_data="cat_issiq")],
        [InlineKeyboardButton("🥣 Шўрвалар", callback_data="cat_shorva")],
        [InlineKeyboardButton("🥗 Салатлар", callback_data="cat_salat")],
        [InlineKeyboardButton("🥒 Газаклар", callback_data="cat_gazak")],
        [InlineKeyboardButton("🥤 Ичимликлар", callback_data="cat_ichimlik")],
        [InlineKeyboardButton("🛒 Саватча", callback_data="cart")],
        [InlineKeyboardButton("📍 Манзил", callback_data="manzil")],
    ]
    return InlineKeyboardMarkup(keyboard)

def category_keyboard(cat_key, user_id):
    cat = MENU[cat_key]
    cart = get_cart(user_id)
    keyboard = []
    for item_key, (name, price) in cat["items"].items():
        qty = cart.get(item_key, 0)
        if qty > 0:
            btn_text = f"✅ {name} — {format_price(price)} сўм  [{qty}]"
        else:
            btn_text = f"{name} — {format_price(price)} сўм"
        keyboard.append([InlineKeyboardButton(btn_text, callback_data=f"add_{item_key}")])
    keyboard.append([InlineKeyboardButton("🛒 Саватча", callback_data="cart")])
    keyboard.append([InlineKeyboardButton("🔙 Асосий меню", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

def cart_keyboard(user_id):
    cart = get_cart(user_id)
    keyboard = []
    for item_key, qty in cart.items():
        if qty > 0:
            item = ALL_ITEMS[item_key]
            keyboard.append([
                InlineKeyboardButton(f"➖", callback_data=f"minus_{item_key}"),
                InlineKeyboardButton(f"{item['name']} x{qty}", callback_data="noop"),
                InlineKeyboardButton(f"➕", callback_data=f"add_{item_key}"),
            ])
    if cart and any(v > 0 for v in cart.values()):
        keyboard.append([InlineKeyboardButton("✅ Буюртма бериш", callback_data="order")])
    keyboard.append([InlineKeyboardButton("🔙 Асосий меню", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

def cart_text(user_id):
    cart = get_cart(user_id)
    items = {k: v for k, v in cart.items() if v > 0}
    if not items:
        return "🛒 Саватча бўш\n\nМаҳсулот қўшиш учун менюдан танланг:"
    
    lines = ["🛒 *Сизнинг буюртмангиз:*\n"]
    total = 0
    for item_key, qty in items.items():
        item = ALL_ITEMS[item_key]
        subtotal = item["price"] * qty
        total += subtotal
        lines.append(f"• {item['name']} x{qty} = *{format_price(subtotal)} сўм*")
    lines.append(f"\n💰 *Жами: {format_price(total)} сўм*")
    return "\n".join(lines)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    carts[user_id] = {}
    text = "🍽 *БАЙТЕРЕК — МИЛЛИЙ ТАОМЛАР МАСКАНИ* ✨\n\nХуш келибсиз! Маҳсулот танланг:"
    await update.message.reply_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    cart = get_cart(user_id)

    if data == "main":
        text = "🍽 *БАЙТЕРЕК* ✨\n\nМаҳсулот танланг:"
        await query.edit_message_text(text, reply_markup=main_keyboard(), parse_mode="Markdown")

    elif data.startswith("cat_"):
        cat_key = data[4:]
        cat = MENU[cat_key]
        text = f"*{cat['title']}*\n\nМаҳсулот танлаш учун босинг:"
        await query.edit_message_text(text, reply_markup=category_keyboard(cat_key, user_id), parse_mode="Markdown")

    elif data.startswith("add_"):
        item_key = data[4:]
        cart[item_key] = cart.get(item_key, 0) + 1
        item = ALL_ITEMS[item_key]
        cat_key = item["cat"]
        cat = MENU[cat_key]
        text = f"*{cat['title']}*\n\n✅ {item['name']} саватчага қўшилди!"
        await query.edit_message_text(text, reply_markup=category_keyboard(cat_key, user_id), parse_mode="Markdown")

    elif data.startswith("minus_"):
        item_key = data[6:]
        if cart.get(item_key, 0) > 0:
            cart[item_key] -= 1
        text = cart_text(user_id)
        await query.edit_message_text(text, reply_markup=cart_keyboard(user_id), parse_mode="Markdown")

    elif data == "cart":
        text = cart_text(user_id)
        await query.edit_message_text(text, reply_markup=cart_keyboard(user_id), parse_mode="Markdown")

    elif data == "order":
        items = {k: v for k, v in cart.items() if v > 0}
        if not items:
            await query.answer("Саватча бўш!", show_alert=True)
            return
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚗 Етказиб бериш", callback_data="delivery")],
            [InlineKeyboardButton("🏃 Ўзим оламан", callback_data="pickup")],
            [InlineKeyboardButton("🔙 Орқага", callback_data="cart")],
        ])
        text = cart_text(user_id) + "\n\n*Қандай оласиз?*"
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

    elif data in ["delivery", "pickup"]:
        delivery_type = "🚗 Етказиб бериш" if data == "delivery" else "🏃 Ўзим оламан"
        order_text = cart_text(user_id)
        total_line = [l for l in order_text.split("\n") if "Жами" in l]
        total = total_line[0] if total_line else ""
        
        confirm_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Тасдиқлаш", callback_data=f"confirm_{data}")],
            [InlineKeyboardButton("🔙 Орқага", callback_data="order")],
        ])
        text = order_text + f"\n\n📦 *{delivery_type}*\n\nБуюртмани тасдиқлайсизми?"
        await query.edit_message_text(text, reply_markup=confirm_keyboard, parse_mode="Markdown")

    elif data.startswith("confirm_"):
        dtype = data[8:]
        delivery_type = "🚗 Етказиб бериш" if dtype == "delivery" else "🏃 Ўзим оламан"
        
        # Buyurtma matnini tuzish
        items = {k: v for k, v in cart.items() if v > 0}
        total = sum(ALL_ITEMS[k]["price"] * v for k, v in items.items())
        
        order_lines = ["✅ *Буюртмангиз қабул қилинди!*\n"]
        for item_key, qty in items.items():
            item = ALL_ITEMS[item_key]
            order_lines.append(f"• {item['name']} x{qty} = {format_price(item['price'] * qty)} сўм")
        order_lines.append(f"\n💰 *Жами: {format_price(total)} сўм*")
        order_lines.append(f"📦 *{delivery_type}*")
        order_lines.append(f"\n📞 Оператор сиз билан боғланади:\n+998 99 788-60-67")
        
        # Savatchani tozalash
        carts[user_id] = {}
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Бош меню", callback_data="main")]
        ])
        await query.edit_message_text("\n".join(order_lines), reply_markup=keyboard, parse_mode="Markdown")

    elif data == "manzil":
        text = "📍 *Манзилимиз:*\n\nҚибрай тумани, Уймоут,\nСоҳибкор кўчаси, 156-уй\n\n📱 +998 99 788-60-67\n\n🕐 Ҳар куни очиқ"
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Асосий меню", callback_data="main")]])
        await query.edit_message_text(text, reply_markup=keyboard, parse_mode="Markdown")

    elif data == "noop":
        pass

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bayterek bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)
