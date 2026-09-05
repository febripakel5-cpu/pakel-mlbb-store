import telebot
from telebot import types
import random
from datetime import datetime, timezone, timedelta

# Token bot lu yang aktif
TOKEN = '8637403539:AAFyKck7U8POV3hzSw9UcF_sDDp0d_hKat0'
bot = telebot.TeleBot(TOKEN)

# Data Kontak Admin & Info Pembayaran Resmi
ADMIN_USERNAME = "@PakelMlbbOfficial"
ADMIN_LINK = "https://t.me/PakelMlbbOfficial"
DANA_NUMBER = "089526466512"
DANA_NAME = "PakelMlbb"
GOPAY_NUMBER = "089526466512"
GOPAY_NAME = "PakelMlbb"
SAWERIA_LINK = "https://saweria.co/PakelMlbb"

# ==================== MASTER GLOBAL TRANSLATION ENGINE ====================
TRANSLATIONS = {
    'id': {
        'wel': "🔥 *Halo, Kak {name}!* Selamat datang di Official *Pakel MlbbStore* 🙏✨\n\nPusat layanan script custom damage, one hit, server lag panel, & drone view terlengkap.\n\n👇 *Silakan pilih menu di bawah ini:*",
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_promo': "🎁 Klaim Promo Member Baru",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Resmi",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 *VIP EXCLUSIVE CATALOGUE - BAGIAN 1* (Kak *{name}*) 🔥\n*(Kategori: Custom Damage & Fair Play)*",
        'cat_title_2': "🔥 *VIP EXCLUSIVE CATALOGUE - BAGIAN 2* (Kak *{name}*) 🔥\n*(Kategori: One Hit & High Class)*",
        'bonus_txt': "⚡ *BONUS SPESIAL FREE ALL PACKAGES:* \n🎁 Otomatis mendapatkan **Panel Server Lag Musuh** & **Drone View X1 - X10** gratis!\n\n📂 *DETAIL & FUNGSI PAKET UTAMA:*",
        'p1': [
            ("🛒 Beli: Natural Balance (Rp 120k)", "buy_natural", "• 💎 *Natural Balance (30 Hari)* — Rp 120.000\n  └ 🎯 *Fungsi:* Penyesuaian damage seimbang & stabil tanpa curiga."),
            ("🛒 Beli: Light VIP + Drone (Rp 95k)", "buy_light", "• ⚡ *Light VIP + Drone (30 Hari)* — Rp 95.000\n  └ 🎯 *Fungsi:* Damage ringan + bonus luas pandang map (drone view)."),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", "buy_semisafe", "• 🛡️ *Semi-Safe (14 Hari)* — Rp 75.000\n  └ 🎯 *Fungsi:* Durasi singkat performa boost optimal buat push rank."),
            ("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", "buy_lifetimesafe", "• 👑 *Lifetime Safe (Permanent)* — Rp 200.000\n  └ 🎯 *Fungsi:* Akses permanen selamanya proteksi anti-detect tinggi.")
        ],
        'p2': [
            ("🛒 Beli: Sultan One Hit 100% (Rp 150k)", "buy_sultan", "• 💥 *Sultan One Hit 100% (30 Hari)* — Rp 150.000\n  └ 🎯 *Fungsi:* Efek kill instan maksimal dominasi total."),
            ("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", "buy_pro", "• ⚡ *VIP Pro One Hit 80% (30 Hari)* — Rp 100.000\n  └ 🎯 *Fungsi:* Power one hit pro 80% stabil di mode ranked."),
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", "buy_semiprivate", "• 🔒 *Semi-Private (14 Hari)* — Rp 75.000\n  └ 🎯 *Fungsi:* Script privat khusus durasi 2 minggu eksklusif."),
            ("🛒 Beli: Permanent Legend (Rp 250k)", "buy_permanent", "• 🏆 *Permanent Legend (Lifetime)* — Rp 250.000\n  └ 🎯 *Fungsi:* Status legend lifetime bebas update selamanya.")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2 (One Hit)",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 *INVOICE PEMESANAN OTOMATIS* (Kak *{name}*) 🧾",
        'pay_info': "💳 *SILAKAN TRANSFER KE REKENING RESMI:*",
        'confirm_instr': "🛡️ *INSTRUKSI KONFIRMASI:*",
        'photo_rec': "✅ *BUKTI PEMBAYARAN DITERIMA & DICATAT* (Kak *{name}*)"
    },
    'tl': { # Filipina (Tagalog)
        'wel': "🔥 *Hello, {name}!* Maligayang pagdating sa Official *Pakel MlbbStore* 🙏✨\n\nAng sentro para sa custom damage scripts, one hit, server lag panel, at drone view.\n\n👇 *Mangyaring piliin ang menu sa ibaba:*",
        'btn_katalog': "💎 VIP Catalogue & Presyo",
        'btn_promo': "🎁 Kunin ang New Member Promo",
        'btn_cara_order': "❓ Gabay sa Pag-order",
        'btn_bayar': "💳 Opisyal na Paraan ng Bayad",
        'btn_faq': "💡 Mga Madalas Itanong (FAQ)",
        'btn_konfirmasi': "✅ Suriin ang Katayuan ng Resibo",
        'btn_admin': "💬 Makipag-ugnayan sa Admin",
        'back': "⬅️ Bumalik sa Main Menu",
        'cat_title_1': "🔥 *VIP EXCLUSIVE CATALOGUE - PART 1* ( *{name}*) 🔥\n*(Category: Custom Damage & Fair Play)*",
        'cat_title_2': "🔥 *VIP EXCLUSIVE CATALOGUE - PART 2* ( *{name}*) 🔥\n*(Category: One Hit & High Class)*",
        'bonus_txt': "⚡ *SPECIAL BONUS (FREE ALL PACKAGES):* \n🎁 Get **Enemy Server Lag Panel** & **Drone View X1 - X10** for FREE!\n\n📂 *PACKAGE DETAILS & FUNCTIONS:*",
        'p1': [
            ("🛒 Buy: Natural Balance ($8 / Rp 120k)", "buy_natural", "• 💎 *Natural Balance (30 Days)* — $8 / Rp 120k\n  └ 🎯 *Function:* Balanced & stable damage adjustment."),
            ("🛒 Buy: Light VIP + Drone ($6 / Rp 95k)", "buy_light", "• ⚡ *Light VIP + Drone (30 Days)* — $6 / Rp 95k\n  └ 🎯 *Function:* Light damage + map vision bonus (drone view)."),
            ("🛒 Buy: Semi-Safe 14 Days ($5 / Rp 75k)", "buy_semisafe", "• 🛡️ *Semi-Safe (14 Days)* — $5 / Rp 75k\n  └ 🎯 *Function:* Short duration optimal boost for rank push."),
            ("🛒 Buy: Lifetime Permanent ($13 / Rp 200k)", "buy_lifetimesafe", "• 👑 *Lifetime Permanent* — $13 / Rp 200k\n  └ 🎯 *Function:* Permanent access with high anti-detect protection.")
        ],
        'p2': [
            ("🛒 Buy: Sultan One Hit 100% ($10 / Rp 150k)", "buy_sultan", "• 💥 *Sultan One Hit 100%* — $10 / Rp 150k\n  └ 🎯 *Function:* Instant kill effect for total domination."),
            ("🛒 Buy: VIP Pro One Hit 80% ($7 / Rp 100k)", "buy_pro", "• ⚡ *VIP Pro One Hit 80%* — $7 / Rp 100k\n  └ 🎯 *Function:* Stable pro one hit power for ranked mode."),
            ("🛒 Buy: Semi-Private 14 Days ($5 / Rp 75k)", "buy_semiprivate", "• 🔒 *Semi-Private (14 Days)* — $5 / Rp 75k\n  └ 🎯 *Function:* Exclusive 2-week private script."),
            ("🛒 Buy: Permanent Legend ($16 / Rp 250k)", "buy_permanent", "• 🏆 *Permanent Legend* — $16 / Rp 250k\n  └ 🎯 *Function:* Lifetime status with free updates forever.")
        ],
        'next_1': "▶️ Next: Catalog Part 2 (One Hit)",
        'prev_2': "◀️ Back to Catalog Part 1",
        'inv_title': "🛒 *AUTOMATED ORDER INVOICE* ( *{name}*) 🧾",
        'pay_info': "💳 *PLEASE TRANSFER TO OFFICIAL PAYMENT:*\n• **Local (Indonesia):** DANA/GoPay `089526466512`\n• **Global (International / PH / India):**",
        'confirm_instr': "🛡️ *CONFIRMATION INSTRUCTION:*",
        'photo_rec': "✅ *PAYMENT PROOF RECEIVED* ( *{name}*)"
    },
    'en': { # Global / Universal Fallback
        'wel': "🔥 *Hello, {name}!* Welcome to Official *Pakel MlbbStore* 🙏✨\n\nThe ultimate global provider for custom damage scripts, one hit, server lag panel, & drone view.\n\n👇 *Please select a menu below:*",
        'btn_katalog': "💎 VIP Catalogue & Pricing",
        'btn_promo': "🎁 Claim New Member Promo",
        'btn_cara_order': "❓ How to Order Guide",
        'btn_bayar': "💳 Official Payment Methods",
        'btn_faq': "💡 FAQ / General Questions",
        'btn_konfirmasi': "✅ Check Status & Receipt",
        'btn_admin': "💬 Contact Official Admin",
        'back': "⬅️ Back to Main Menu",
        'cat_title_1': "🔥 *VIP EXCLUSIVE CATALOGUE - PART 1* ( *{name}*) 🔥\n*(Category: Custom Damage & Fair Play)*",
        'cat_title_2': "🔥 *VIP EXCLUSIVE CATALOGUE - PART 2* ( *{name}*) 🔥\n*(Category: One Hit & High Class)*",
        'bonus_txt': "⚡ *SPECIAL BONUS (FREE ALL PACKAGES):* \n🎁 Get **Enemy Server Lag Panel** & **Drone View X1 - X10** for FREE!\n\n📂 *PACKAGE DETAILS & FUNCTIONS:*",
        'p1': [
            ("🛒 Buy: Natural Balance ($8 / Rp 120k)", "buy_natural", "• 💎 *Natural Balance (30 Days)* — $8 / Rp 120k\n  └ 🎯 *Function:* Balanced & stable damage adjustment."),
            ("🛒 Buy: Light VIP + Drone ($6 / Rp 95k)", "buy_light", "• ⚡ *Light VIP + Drone (30 Days)* — $6 / Rp 95k\n  └ 🎯 *Function:* Light damage + map vision bonus (drone view)."),
            ("🛒 Buy: Semi-Safe 14 Days ($5 / Rp 75k)", "buy_semisafe", "• 🛡️ *Semi-Safe (14 Days)* — $5 / Rp 75k\n  └ 🎯 *Function:* Short duration optimal boost for rank push."),
            ("🛒 Buy: Lifetime Permanent ($13 / Rp 200k)", "buy_lifetimesafe", "• 👑 *Lifetime Permanent* — $13 / Rp 200k\n  └ 🎯 *Function:* Permanent access with high anti-detect protection.")
        ],
        'p2': [
            ("🛒 Buy: Sultan One Hit 100% ($10 / Rp 150k)", "buy_sultan", "• 💥 *Sultan One Hit 100%* — $10 / Rp 150k\n  └ 🎯 *Function:* Instant kill effect for total domination."),
            ("🛒 Buy: VIP Pro One Hit 80% ($7 / Rp 100k)", "buy_pro", "• ⚡ *VIP Pro One Hit 80%* — $7 / Rp 100k\n  └ 🎯 *Function:* Stable pro one hit power for ranked mode."),
            ("🛒 Buy: Semi-Private 14 Days ($5 / Rp 75k)", "buy_semiprivate", "• 🔒 *Semi-Private (14 Days)* — $5 / Rp 75k\n  └ 🎯 *Function:* Exclusive 2-week private script."),
            ("🛒 Buy: Permanent Legend ($16 / Rp 250k)", "buy_permanent", "• 🏆 *Permanent Legend* — $16 / Rp 250k\n  └ 🎯 *Function:* Lifetime status with free updates forever.")
        ],
        'next_1': "▶️ Next: Catalog Part 2 (One Hit)",
        'prev_2': "◀️ Back to Catalog Part 1",
        'inv_title': "🛒 *AUTOMATED ORDER INVOICE* ( *{name}*) 🧾",
        'pay_info': "💳 *PLEASE TRANSFER TO OFFICIAL PAYMENT:*\n• **Local (Indonesia):** DANA/GoPay `089526466512`\n• **Global (International / PayPal / Cards):**",
        'confirm_instr': "🛡️ *CONFIRMATION INSTRUCTION:*",
        'photo_rec': "✅ *PAYMENT PROOF RECEIVED* ( *{name}*)"
    }
}

def get_lang(user):
    code = getattr(user, 'language_code', 'en')
    if code:
        code = code.lower()
        if code.startswith('id'):
            return 'id'
        elif code.startswith('tl') or code.startswith('fil'):
            return 'tl'
    return 'en' # Universal fallback untuk seluruh negara di dunia (India, Amerika, Eropa, dll.)

def get_back_markup(l):
    markup = types.InlineKeyboardMarkup()
    text = TRANSLATIONS.get(l, TRANSLATIONS['en'])['back']
    markup.add(types.InlineKeyboardButton(text, callback_data='menu_utama'))
    return markup
# ======================================================================

# 1. Perintah /start & /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
        types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
        types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
        types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
        types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
        types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
        types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
    )
    
    welcome_text = t['wel'].format(name=user.first_name)
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# Command Tambahan: /cekresi
@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    user = message.from_user
    l = get_lang(user)
    if l == 'id':
        text = f"🔍 *CEK STATUS RESI PEMBELIAN* (Kak *{user.first_name}*)\n\nKirimkan **Nomor Resi Unik** (`PKL-MLBB-12345`) atau bukti transfer.\n\n💬 Admin: [{ADMIN_USERNAME}]({ADMIN_LINK})"
    else:
        text = f"🔍 *CHECK RECEIPT STATUS* ( *{user.first_name}*)\n\nPlease send your **Unique Receipt Number** or payment proof.\n\n💬 Admin: [{ADMIN_USERNAME}]({ADMIN_LINK})"
    bot.reply_to(message, text, parse_mode='Markdown', disable_web_page_preview=True)

# Command Tambahan: /katalog
@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn_text, callback_val, _ in t['p1']:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
    markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
    markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

    katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n" + "\n".join([desc for _, _, desc in t['p1']])
    bot.send_message(message.chat.id, katalog_text, parse_mode='Markdown', reply_markup=markup)

# 2. Handler Tombol (Callback Query Multi-Negara)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'menu_utama':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
            types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
            types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
            types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
            types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
            types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
            types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
        )
        text = "🔥 *Main Menu:*" if l != 'id' else "🔥 *Menu Utama:*"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_promo':
        promo_text = f"🎁 *PROMO* ( *{user.first_name}*)\n\n🎟️ **COUPON:** `WELCOMEPAKEL`\n💰 Special discount on all VIP packages!" if l != 'id' else f"🎁 *PROMO PELANGGAN BARU* (Kak *{user.first_name}*)\n\n🎟️ **KODE KUPON:** `WELCOMEPAKEL`\n💰 Diskon spesial di semua paket VIP!"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, parse_mode='Markdown', reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        faq_text = f"💡 *FAQ*\n\n❓ *Safe from ban?* 💬 A: High-level anti-detect encryption.\n❓ *How to install?* 💬 A: Script sent by admin after payment." if l != 'id' else f"💡 *FAQ*\n\n❓ *Aman dari banned?* 💬 A: Enkripsi anti-detect tinggi.\n❓ *Cara pasang?* 💬 A: File dikirim admin setelah pembayaran."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=faq_text, parse_mode='Markdown', reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in t['p1']:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n" + "\n".join([desc for _, _, desc in t['p1']])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'katalog_part2':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in t['p2']:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['prev_2'], callback_data='katalog_part1'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_2'].format(name=user.first_name)}\n\n" + "\n".join([desc for _, _, desc in t['p2']])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        paket_tipe = call.data.replace('buy_', '')
        all_items = t['p1'] + t['p2']
        paket_nama = "VIP Package"
        for btn_txt, cb_val, _ in all_items:
            if cb_val == call.data:
                paket_nama = btn_txt.replace("🛒 Buy: ", "").replace("🛒 Beli: ", "")
                
        random_serial = random.randint(10000, 99999)
        
        invoice_text = (
            f"{t['inv_title']}\n\n"
            f"📦 *Package:* `{paket_nama}`\n"
            f"🔢 *Receipt No:* `PKL-MLBB-{random_serial}`\n"
            f"⏱️ *Payment Limit:* 15 Minutes\n\n"
            f"{t['pay_info']}\n"
            f"• **DANA/GoPay:** `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"• **Saweria (Global/QRIS/Cards):** {SAWERIA_LINK}\n\n"
            f"{t['confirm_instr']}\n"
            f"Send payment proof & receipt to admin: [{ADMIN_USERNAME}]({ADMIN_LINK})"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=invoice_text, parse_mode='Markdown', reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Invoice generated!")

    elif call.data == 'menu_cara_order':
        text = "❓ *HOW TO ORDER*\n1️⃣ Select package & click Buy.\n2️⃣ Get Invoice & Receipt.\n3️⃣ Transfer via DANA/Saweria.\n4️⃣ Send proof to admin." if l != 'id' else "❓ *CARA ORDER*\n1️⃣ Pilih paket & klik Beli.\n2️⃣ Dapatkan Resi.\n3️⃣ Transfer.\n4️⃣ Kirim bukti ke admin."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        text = f"💳 *PAYMENT METHODS*\n\n📱 **DANA/GoPay:** `{DANA_NUMBER}`\n🧡 **Saweria (Global):** {SAWERIA_LINK}\n\n📌 Confirm to [{ADMIN_USERNAME}]({ADMIN_LINK})." if l != 'id' else f"💳 *METODE PEMBAYARAN*\n\n📱 **DANA/GoPay:** `{DANA_NUMBER}`\n🧡 **Saweria:** {SAWERIA_LINK}\n\n📌 Konfirmasi ke [{ADMIN_USERNAME}]({ADMIN_LINK})."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        rs = random.randint(10000, 99999)
        text = f"✅ *PAYMENT CONFIRMATION*\nExample Receipt: `PKL-MLBB-{rs}`\nSend transfer screenshot to admin." if l != 'id' else f"✅ *KONFIRMASI PEMBAYARAN*\nContoh Resi: `PKL-MLBB-{rs}`\nKirim screenshot ke admin."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, parse_mode='Markdown', reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

# 3. Handler Foto Resi Universal
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    rs = random.randint(10000, 99999)
    
    WIB = timezone(timedelta(hours=7))
    now = datetime.now(WIB)
    dt_str = now.strftime("%d-%m-%Y")
    tm_str = now.strftime("%H:%M:%S WIB")
    
    res = (
        f"{t['photo_rec']}\n\n"
        f"🛡️ *Receipt No:* `PKL-MLBB-{rs}`\n"
        f"⏱️ *Time:* {dt_str} - {tm_str}\n\n"
        f"📋 *COPY & SEND THIS TO ADMIN:*\n"
        f"```text\n"
        f"• Receipt No   : PKL-MLBB-{rs}\n"
        f"• Buyer Name   : {user.first_name}\n"
        f"• Date/Time    : {dt_str} - {tm_str}\n"
        f"• Status       : PAID\n"
        f"• Admin Link   : {ADMIN_LINK}\n"
        f"```\n"
        f"🚀 Send to admin: [{ADMIN_USERNAME}]({ADMIN_LINK})"
    )
    bot.reply_to(message, res, parse_mode='Markdown', disable_web_page_preview=True)

# 4. Auto-Reply Cerdas Lintas Bahasa
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    user = message.from_user
    l = get_lang(user)
    txt = message.text.lower()
    
    if any(w in txt for w in ['price', 'harga', 'list', 'menu', 'catalog', 'katalog']):
        rep = "💎 Type /start to view the VIP Catalogue!" if l != 'id' else "💎 Ketik /start untuk melihat Katalog VIP!"
    elif any(w in txt for w in ['pay', 'bayar', 'dana', 'saweria']):
        rep = f"💳 Official Payment: DANA/GoPay `{DANA_NUMBER}` or Saweria {SAWERIA_LINK}" if l != 'id' else f"💳 Pembayaran: DANA/GoPay `{DANA_NUMBER}` atau Saweria {SAWERIA_LINK}"
    else:
        rep = f"Hello *{user.first_name}*! Contact our admin at [{ADMIN_USERNAME}]({ADMIN_LINK})." if l != 'id' else f"Halo Kak *{user.first_name}*! Hubungi admin kami di [{ADMIN_USERNAME}]({ADMIN_LINK})."
        
    bot.reply_to(message, rep, parse_mode='Markdown', disable_web_page_preview=True)

# Jalankan Bot
print("[INFO] Ultimate Global Localized Bot Pakel MlbbStore Berjalan...")
bot.infinity_polling()