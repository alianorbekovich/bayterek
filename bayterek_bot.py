import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("TOKEN", "8544157950:AAGPPC_acxKZWu7Z6LzX3qFhW03xIAzyXS0")
ADMIN_ID = 1110117109

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

MENU_ITEMS = {
    "b1": {"name": "Бешбармоқ (1 порция)", "price": 110000, "photo": None, "cat": "beshbarmaq"},
    "b2": {"name": "Бешбармоқ (2 порция)", "price": 220000, "photo": None, "cat": "beshbarmaq"},
    "b3": {"name": "Бешбармоқ (3 порция)", "price": 330000, "photo": None, "cat": "beshbarmaq"},
    "b4": {"name": "Бешбармоқ (Кичик)", "price": 65000, "photo": None, "cat": "beshbarmaq"},
    "b5": {"name": "Астау Ассорти", "price": 210000, "photo": None, "cat": "beshbarmaq"},
    "b6": {"name": "Астау Ассорти (Катта)", "price": 320000, "photo": None, "cat": "beshbarmaq"},
    "b7": {"name": "Гўштли Ассорти Байтерек", "price": 155000, "photo": None, "cat": "beshbarmaq"},
    "b8": {"name": "Гўштли Ассорти (Оддий)", "price": 135000, "photo": None, "cat": "beshbarmaq"},
    "b9": {"name": "Қази (Донаси)", "price": 15000, "photo": None, "cat": "beshbarmaq"},
    "b10": {"name": "Қўшимча Хамир (100гр)", "price": 20000, "photo": None, "cat": "beshbarmaq"},
    "b11": {"name": "Хамир устига гўшт (100гр)", "price": 30000, "photo": None, "cat": "beshbarmaq"},
    "i1": {"name": "Қозон кабоб", "price": 60000, "photo": None, "cat": "issiq"},
    "i2": {"name": "Норин (Қазилик)", "price": 45000, "photo": None, "cat": "issiq"},
    "i3": {"name": "Норин (Қазисиз)", "price": 30000, "photo": None, "cat": "issiq"},
    "i4": {"name": "Қовурма Лағмон", "price": 40000, "photo": None, "cat": "issiq"},
    "i5": {"name": "Уйғурча Лағмон", "price": 40000, "photo": None, "cat": "issiq"},
    "i6": {"name": "Тушёнка", "price": 45000, "photo": None, "cat": "issiq"},
    "i7": {"name": "Фаршированный перец", "price": 30000, "photo": None, "cat": "issiq"},
    "i8": {"name": "Пегодя (1 дона)", "price": 10000, "photo": None, "cat": "issiq"},
    "i9": {"name": "Кукси (Катта)", "price": 35000, "photo": None, "cat": "issiq"},
    "i10": {"name": "Кукси (Ўртача)", "price": 30000, "photo": None, "cat": "issiq"},
    "sh1": {"name": "Шўрва қайнатма", "price": 40000, "photo": None, "cat": "shorva"},
    "sh2": {"name": "Фрикаделка шўрва", "price": 30000, "photo": None, "cat": "shorva"},
    "sh3": {"name": "Чучвара шўрва", "price": 30000, "photo": None, "cat": "shorva"},
    "sh4": {"name": "Чучвара (Қуюқ)", "price": 35000, "photo": None, "cat": "shorva"},
    "sh5": {"name": "Ассорти шўрва", "price": 40000, "photo": None, "cat": "shorva"},
    "sh6": {"name": "Қази бульон", "price": 40000, "photo": None, "cat": "shorva"},
    "s1": {"name": "Байтерек фирмий салати", "price": 50000, "photo": None, "cat": "salat"},
    "s2": {"name": "Мимоза", "price": 45000, "photo": None, "cat": "salat"},
    "s3": {"name": "Сельдь под шубой", "price": 45000, "photo": None, "cat": "salat"},
    "s4": {"name": "Оливье", "price": 40000, "photo": None, "cat": "salat"},
    "s5": {"name": "Грекча салат", "price": 45000, "photo": None, "cat": "salat"},
    "s6": {"name": "Цезар", "price": 45000, "photo": None, "cat": "salat"},
    "s7": {"name": "Пикантный", "price": 45000, "photo": None, "cat": "salat"},
    "s8": {"name": "Нежность", "price": 45000, "photo": None, "cat": "salat"},
    "s9": {"name": "Аппетитный", "price": 45000, "photo": None, "cat": "salat"},
    "s10": {"name": "Гурман", "price": 45000, "photo": None, "cat": "salat"},
    "s14": {"name": "Баҳорги салат", "price": 18000, "photo": None, "cat": "salat"},
    "s15": {"name": "Ачиқ-чучук", "price": 18000, "photo": None, "cat": "salat"},
    "g1": {"name": "Балиқли Хе", "price": 45000, "photo": None, "cat": "gazak"},
    "g2": {"name": "Қозоқча Наггетслар", "price": 45000, "photo": None, "cat": "gazak"},
    "g3": {"name": "Кавказча Ассорти", "price": 35000, "photo": None, "cat": "gazak"},
    "g4": {"name": "Русча Сельдь", "price": 30000, "photo": None, "cat": "gazak"},
    "g5": {"name": "Сабзавотли Ассорти", "price": 22000, "photo": None, "cat": "gazak"},
    "g6": {"name": "Тузламалар Ассортиси", "price": 22000, "photo": None, "cat": "gazak"},
    "g7": {"name": "Сузма", "price": 12000, "photo": None, "cat": "gazak"},
    "g8": {"name": "Баурсак (Донаси)", "price": 3000, "photo": None, "cat": "gazak"},
    "g9": {"name": "Лепёшка", "price": 5000, "photo": None, "cat": "gazak"},
    "g10": {"name": "Лимон (Тилимланган)", "price": 6000, "photo": None, "cat": "gazak"},
    "ich1": {"name": "Coca-Cola", "price": 15000, "photo": None, "cat": "ichimlik"},
    "ich2": {"name": "Fanta", "price": 15000, "photo": None, "cat": "ichimlik"},
    "ich3": {"name": "Pepsi", "price": 15000, "photo": None, "cat": "ichimlik"},
    "ich4": {"name": "Сок Сочная долина", "price": 12000, "photo": None, "cat": "ichimlik"},
    "ich5": {"name": "Чортоқ минерал суви", "price": 8000, "photo": None, "cat": "ichimlik"},
    "ich6": {"name": "Biolife минерал суви", "price": 8000, "photo": None, "cat": "ichimlik"},
    "ich7": {"name": "Уй кампоти", "price": 10000, "photo": None, "cat": "ichimlik"},
    "ich8": {"name": "Тоза Қимиз", "price": 20000, "photo": None, "cat": "ichimlik"},
}

CATEGORIES = {
    "beshbarmaq": "🍲 Бешбармоқлар",
    "issiq": "🔥 Иссиқ таомлар",
    "shorva": "🥣 Шўрвалар",
    "salat": "🥗 Салатлар",
    "gazak": "🥒 Газаклар",
    "ichimlik": "🥤 Ичимликлар",
}

carts = {}
admin_state = {}

def get_cart(user_id):
    if user_id not in carts:
        carts[user_id] = {}
    return carts[user_id]

def format_price(p):
    return f"{p:,}".replace(",", " ")

def main_keyboard(user_id):
    cart = get_cart(user_id)
    total_items = sum(cart.values())
    cart_label = f"🛒 Саватча ({total_items} та)" if total_items > 0 else "🛒 Саватча"
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍲 Бешбармоқлар", callback_data="cat_beshbarmaq"),
         InlineKeyboardButton("🔥 Иссиқ таомлар", callback_data="cat_issiq")],
        [InlineKeyboardButton("🥣 Шўрвалар", callback_data="cat_shorva"),
         InlineKeyboardButton("🥗 Салатлар", callback_data="cat_salat")],
        [InlineKeyboardButton("🥒 Газаклар", callback_data="cat_gazak"),
         InlineKeyboardButton("🥤 Ичимликлар", callback_data="cat_ichimlik")],
        [InlineKeyboardButton(cart_label, callback_data="cart")],
        [InlineKeyboardButton("📍 Манзил", callback_data="manzil")],
    ])

def cat_keyboard(cat_key, user_id):
    items = [(k, v) for k, v in MENU_ITEMS.items() if v["cat"] == cat_key]
    cart = get_cart(user_id)
    keyboard = []
    for item_key, item in items:
        qty = cart.get(item_key, 0)
        mark = f" ✅x{qty}" if qty > 0 else ""
        keyboard.append([InlineKeyboardButton(
            f"{item['name']} — {format_price(item['price'])} сўм{mark}",
            callback_data=f"item_{item_key}"
        )])
    total = sum(cart.values())
    cart_label = f"🛒 Саватча ({total} та)" if total > 0 else "🛒 Саватча"
    keyboard.append([InlineKeyboardButton(cart_label, callback_data="cart")])
    keyboard.append([InlineKeyboardButton("🔙 Бош меню", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

def item_keyboard(item_key, user_id):
    cart = get_cart(user_id)
    qty = cart.get(item_key, 0)
    item = MENU_ITEMS[item_key]
    cat_key = item["cat"]
    keyboard = []
    if qty == 0:
        keyboard.append([InlineKeyboardButton("🛒 Саватга қўшиш", callback_data=f"add_{item_key}")])
    else:
        keyboard.append([
            InlineKeyboardButton("➖", callback_data=f"minus_{item_key}"),
            InlineKeyboardButton(f"  {qty} та  ", callback_data="noop"),
            InlineKeyboardButton("➕", callback_data=f"add_{item_key}"),
        ])
    keyboard.append([InlineKeyboardButton("🔙 Рўйхатга қайтиш", callback_data=f"cat_{cat_key}")])
    keyboard.append([InlineKeyboardButton("🛒 Саватча", callback_data="cart")])
    return InlineKeyboardMarkup(keyboard)

def cart_keyboard(user_id):
    cart = {k: v for k, v in get_cart(user_id).items() if v > 0}
    keyboard = []
    for item_key, qty in cart.items():
        item = MENU_ITEMS[item_key]
        name = item['name'][:22]
        keyboard.append([
            InlineKeyboardButton("➖", callback_data=f"cminus_{item_key}"),
            InlineKeyboardButton(f"{name} x{qty}", callback_data="noop"),
            InlineKeyboardButton("➕", callback_data=f"cadd_{item_key}"),
        ])
    if cart:
        keyboard.append([InlineKeyboardButton("✅ Буюртма бериш", callback_data="order")])
    keyboard.append([InlineKeyboardButton("🔙 Бош меню", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

def cart_text(user_id):
    cart = {k: v for k, v in get_cart(user_id).items() if v > 0}
    if not cart:
        return "🛒 *Саватча бўш*\n\nМенюдан таом танланг 👇"
    lines = ["🛒 *Сизнинг буюртмангиз:*\n"]
    total = 0
    for k, v in cart.items():
        item = MENU_ITEMS[k]
        sub = item["price"] * v
        total += sub
        lines.append(f"• {item['name']} x{v} = *{format_price(sub)} сўм*")
    lines.append(f"\n💰 *Жами: {format_price(total)} сўм*")
    return "\n".join(lines)

# Rasmli xabarni o'chirb yangi yuborish
async def send_item(chat_id, item_key, user_id, context, message_id=None):
    item = MENU_ITEMS[item_key]
    caption = f"*{item['name']}*\n💰 {format_price(item['price'])} сўм"
    kb = item_keyboard(item_key, user_id)
    if message_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except:
            pass
    if item["photo"]:
        await context.bot.send_photo(chat_id=chat_id, photo=item["photo"], caption=caption, reply_markup=kb, parse_mode="Markdown")
    else:
        await context.bot.send_message(chat_id=chat_id, text=caption, reply_markup=kb, parse_mode="Markdown")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text(
            "👨‍💼 *ADMIN PANEL — Bayterek*\n\nXush kelibsiz, Alibek!",
            reply_markup=admin_keyboard(), parse_mode="Markdown"
        )
        return
    carts[user_id] = {}
    await update.message.reply_text(
        "🍽 *БАЙТЕРЕК — МИЛЛИЙ ТАОМЛАР МАСКАНИ* ✨\n\nХуш келибсиз! Таом танланг:",
        reply_markup=main_keyboard(user_id), parse_mode="Markdown"
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    msg_id = query.message.message_id
    cart = get_cart(user_id)

    if data == "noop":
        return

    elif data == "main":
        # Eski xabarni o'chir, yangi matn yubor
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_message(
            chat_id=chat_id,
            text="🍽 *БАЙТЕРЕК* ✨\n\nТаом танланг:",
            reply_markup=main_keyboard(user_id), parse_mode="Markdown"
        )

    elif data.startswith("cat_"):
        cat_key = data[4:]
        cat_name = CATEGORIES.get(cat_key, "")
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"*{cat_name}*\n\nТаомни танланг:",
            reply_markup=cat_keyboard(cat_key, user_id), parse_mode="Markdown"
        )

    elif data.startswith("item_"):
        item_key = data[5:]
        await send_item(chat_id, item_key, user_id, context, message_id=msg_id)

    elif data.startswith("add_"):
        item_key = data[4:]
        cart[item_key] = cart.get(item_key, 0) + 1
        await send_item(chat_id, item_key, user_id, context, message_id=msg_id)

    elif data.startswith("minus_"):
        item_key = data[6:]
        if cart.get(item_key, 0) > 0:
            cart[item_key] -= 1
        await send_item(chat_id, item_key, user_id, context, message_id=msg_id)

    elif data.startswith("cadd_"):
        item_key = data[5:]
        cart[item_key] = cart.get(item_key, 0) + 1
        try:
            await query.edit_message_text(cart_text(user_id), reply_markup=cart_keyboard(user_id), parse_mode="Markdown")
        except:
            pass

    elif data.startswith("cminus_"):
        item_key = data[7:]
        if cart.get(item_key, 0) > 0:
            cart[item_key] -= 1
        try:
            await query.edit_message_text(cart_text(user_id), reply_markup=cart_keyboard(user_id), parse_mode="Markdown")
        except:
            pass

    elif data == "cart":
        try:
            await query.message.delete()
        except:
            pass
        await context.bot.send_message(
            chat_id=chat_id,
            text=cart_text(user_id),
            reply_markup=cart_keyboard(user_id), parse_mode="Markdown"
        )

    elif data == "order":
        if not any(v > 0 for v in cart.values()):
            await query.answer("Саватча бўш!", show_alert=True)
            return
        try:
            await query.edit_message_text(
                cart_text(user_id) + "\n\n📦 *Қандай оласиз?*",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🚗 Етказиб бериш", callback_data="delivery")],
                    [InlineKeyboardButton("🏃 Ўзим оламан", callback_data="pickup")],
                    [InlineKeyboardButton("🔙 Орқага", callback_data="cart")],
                ]), parse_mode="Markdown"
            )
        except:
            pass

    elif data in ["delivery", "pickup"]:
        dtype_text = "🚗 Етказиб бериш" if data == "delivery" else "🏃 Ўзим оламан"
        try:
            await query.edit_message_text(
                cart_text(user_id) + f"\n\n📦 *{dtype_text}*\n\nТасдиқлайсизми?",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("✅ Тасдиқлаш", callback_data=f"confirm_{data}")],
                    [InlineKeyboardButton("🔙 Орқага", callback_data="order")],
                ]), parse_mode="Markdown"
            )
        except:
            pass

    elif data.startswith("confirm_"):
        dtype = data[8:]
        dtype_text = "🚗 Етказиб бериш" if dtype == "delivery" else "🏃 Ўзим оламан"
        items = {k: v for k, v in cart.items() if v > 0}
        total = sum(MENU_ITEMS[k]["price"] * v for k, v in items.items())
        user = query.from_user
        username = f"@{user.username}" if user.username else "yo'q"

        # Mijozga
        lines = ["✅ *Буюртмангиз қабул қилинди!*\n"]
        for k, v in items.items():
            item = MENU_ITEMS[k]
            lines.append(f"• {item['name']} x{v} = {format_price(item['price']*v)} сўм")
        lines.append(f"\n💰 *Жами: {format_price(total)} сўм*")
        lines.append(f"📦 *{dtype_text}*")
        lines.append("\n📞 Оператор сиз билан боғланади!")

        # Adminga
        admin_lines = ["🔔 *ЯНГИ БУЮРТМА!*\n"]
        admin_lines.append(f"👤 {user.full_name} ({username})")
        admin_lines.append(f"📱 ID: `{user.id}`\n")
        for k, v in items.items():
            item = MENU_ITEMS[k]
            admin_lines.append(f"• {item['name']} x{v} = {format_price(item['price']*v)} сўм")
        admin_lines.append(f"\n💰 *Жами: {format_price(total)} сўм*")
        admin_lines.append(f"📦 *{dtype_text}*")

        carts[user_id] = {}

        try:
            await query.edit_message_text(
                "\n".join(lines),
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Бош меню", callback_data="main")]]),
                parse_mode="Markdown"
            )
        except:
            pass

        try:
            await context.bot.send_message(ADMIN_ID, "\n".join(admin_lines), parse_mode="Markdown")
        except Exception as e:
            logging.error(f"Admin xabar xato: {e}")

    elif data == "manzil":
        try:
            await query.edit_message_text(
                "📍 *Манзилимиз:*\n\nҚибрай тумани, Уймоут,\nСоҳибкор кўчаси, 156-уй\n\n📱 +998 99 788-60-67",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Бош меню", callback_data="main")]]),
                parse_mode="Markdown"
            )
        except:
            pass

    # ===== ADMIN =====
    elif data == "admin_menu":
        try:
            await query.edit_message_text("👨‍💼 *ADMIN PANEL*", reply_markup=admin_keyboard(), parse_mode="Markdown")
        except:
            pass

    elif data == "admin_list":
        keyboard = []
        for item_key, item in MENU_ITEMS.items():
            mark = "🖼" if item["photo"] else "📷"
            keyboard.append([InlineKeyboardButton(f"{mark} {item['name']}", callback_data=f"admin_edit_{item_key}")])
        keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")])
        try:
            await query.edit_message_text(
                "📋 *Taomlar:*\n🖼 rasm bor | 📷 rasm yo'q",
                reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown"
            )
        except:
            pass

    elif data.startswith("admin_edit_"):
        item_key = data[11:]
        item = MENU_ITEMS[item_key]
        photo_status = "✅ Bor" if item["photo"] else "❌ Yo'q"
        try:
            await query.edit_message_text(
                f"*{item['name']}*\n💰 {format_price(item['price'])} so'm\n🖼 Rasm: {photo_status}",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🖼 Rasm yuklash", callback_data=f"admin_photo_{item_key}")],
                    [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_list")],
                ]), parse_mode="Markdown"
            )
        except:
            pass

    elif data.startswith("admin_photo_"):
        item_key = data[12:]
        admin_state[user_id] = {"step": "waiting_photo", "item_key": item_key}
        item = MENU_ITEMS[item_key]
        try:
            await query.edit_message_text(
                f"🖼 *{item['name']}* uchun rasm yuboring:",
                parse_mode="Markdown"
            )
        except:
            pass

def admin_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🖼 Rasm qo'shish", callback_data="admin_list")],
        [InlineKeyboardButton("🏠 Mijoz menyu", callback_data="main")],
    ])

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        return
    state = admin_state.get(user_id)
    if not state or state["step"] != "waiting_photo":
        return
    item_key = state["item_key"]
    file_id = update.message.photo[-1].file_id
    MENU_ITEMS[item_key]["photo"] = file_id
    admin_state.pop(user_id, None)
    item = MENU_ITEMS[item_key]
    await update.message.reply_photo(
        photo=file_id,
        caption=f"✅ *{item['name']}* uchun rasm saqlandi!",
        parse_mode="Markdown",
        reply_markup=admin_keyboard()
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    print("✅ Bayterek bot ishga tushdi!")
    app.run_polling(drop_pending_updates=True)
