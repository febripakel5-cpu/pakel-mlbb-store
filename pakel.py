import telebot
from telebot import types
import random
import time
import threading
from datetime import datetime, timezone, timedelta
import os

TOKEN = '8614166487:AAFt6SzB6mP6sA31fXU7QUsz9uH8KdIEiFo'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

ADMIN_USERNAME = "@PakelMlbbOfficial"
ADMIN_LINK = "https://t.me/PakelMlbbOfficial"
CHANNEL_TESTI_LINK = "https://t.me/PakelMlbb/368"

GROUP_CHAT_ID = "@PakelMlbb"
GROUP_TOPIC_ID = 368

GROUP_PAY_ID = "@Paysukses"
GROUP_PAY_TOPIC_ID = 5

INFO_DANA = "085188371150"
INFO_GOPAY = "085188371150"
INFO_SAWERIA = "https://saweria.co/PakelMlbb"
QRIS_WEB_LINK = "https://ibb.co.com/cX2J28kj"

def save_user(chat_id):
    try:
        chat_id_str = str(chat_id).strip()
        if not chat_id_str or chat_id_str.startswith('-'):
            return
        users = []
        try:
            with open("users.txt", "r") as f:
                users = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            pass
        if chat_id_str not in users:
            with open("users.txt", "a") as f:
                f.write(chat_id_str + "\n")
    except Exception as e:
        print(f"[SAVE USER ERROR]: {e}")

def get_user_coupon_status(chat_id):
    try:
        with open("coupons.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == str(chat_id):
                    return parts[1]
    except FileNotFoundError:
        pass
    return "AVAILABLE"

def set_user_coupon_status(chat_id, status_baru):
    try:
        rows = []
        updated = False
        chat_id_str = str(chat_id)
        try:
            with open("coupons.txt", "r") as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        c_id, status = parts
                        if c_id == chat_id_str:
                            status = status_baru
                            updated = True
                        rows.append(f"{c_id}|{status}\n")
        except FileNotFoundError:
            pass
        if not updated:
            rows.append(f"{chat_id_str}|{status_baru}\n")
        with open("coupons.txt", "w") as f:
            f.writelines(rows)
    except Exception as e:
        print(f"[COUPON ERROR]: {e}")

def get_user_points(chat_id):
    try:
        with open("points.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == str(chat_id):
                    return int(parts[1])
    except FileNotFoundError:
        pass
    return 0

def add_user_points(chat_id, amount):
    try:
        current = get_user_points(chat_id)
        new_total = current + amount
        rows = []
        updated = False
        chat_id_str = str(chat_id)
        try:
            with open("points.txt", "r") as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) == 2:
                        c_id, pts = parts
                        if c_id == chat_id_str:
                            pts = str(new_total)
                            updated = True
                        rows.append(f"{c_id}|{pts}\n")
        except FileNotFoundError:
            pass
        if not updated:
            rows.append(f"{chat_id_str}|{new_total}\n")
        with open("points.txt", "w") as f:
            f.writelines(rows)
    except Exception as e:
        print(f"[ADD POINTS ERROR]: {e}")

def reduce_user_points(chat_id, amount):
    current = get_user_points(chat_id)
    new_total = max(0, current - amount)
    rows = []
    chat_id_str = str(chat_id)
    try:
        with open("points.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    c_id, pts = parts
                    if c_id == chat_id_str:
                        pts = str(new_total)
                    rows.append(f"{c_id}|{pts}\n")
    except FileNotFoundError:
        pass
    with open("points.txt", "w") as f:
        f.writelines(rows)

def save_user_review(chat_id, rating, text_review):
    try:
        WIB = timezone(timedelta(hours=7))
        now = datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S')
        review_line = f"{chat_id}|{now}|{rating}|{text_review.replace('|', '-')}\n"
        with open("reviews.txt", "a") as f:
            f.write(review_line)
    except Exception as e:
        print(f"[SAVE REVIEW ERROR]: {e}")
def save_order(chat_id, paket_nama, harga, resi, payment_method="TRANSFER", point_cost=0, admin_msg_id=0):
    try:
        WIB = timezone(timedelta(hours=7))
        now = datetime.now(WIB)
        tanggal_str = now.strftime('%d-%m-%Y')
        jam_str = now.strftime('%H:%M:%S WIB')
        timestamp_epoch = int(now.timestamp())
        
        days_indo = {
            'Mon': 'Senin', 'Tue': 'Selasa', 'Wed': 'Rabu', 
            'Thu': 'Kamis', 'Fri': 'Jumat', 'Sat': 'Sabtu', 'Sun': 'Minggu'
        }
        hari_str = days_indo.get(now.strftime('%a'), 'Senin')
        
        order_line = f"{chat_id}|{tanggal_str}|{hari_str}|{jam_str}|{paket_nama}|{harga}|{resi}|PENDING|{timestamp_epoch}|{payment_method}|{point_cost}|{admin_msg_id}\n"
        
        with open("orders.txt", "a") as f:
            f.write(order_line)
    except Exception as e:
        print(f"[SAVE ORDER ERROR]: {e}")

def update_order_status_by_resi(resi_target, status_baru):
    try:
        updated = False
        target_chat_id = None
        target_payment = "TRANSFER"
        target_points_cost = 0
        current_status = ""
        rows = []
        
        try:
            with open("orders.txt", "r") as f:
                for line in f:
                    parts = line.strip().split('|')
                    if len(parts) >= 8:
                        chat_id = parts[0]
                        tanggal = parts[1]
                        hari = parts[2]
                        jam = parts[3]
                        paket = parts[4]
                        harga = parts[5]
                        resi = parts[6]
                        status = parts[7]
                        timestamp_epoch = parts[8] if len(parts) > 8 else "0"
                        pay_method = parts[9] if len(parts) > 9 else "TRANSFER"
                        p_cost = int(parts[10]) if len(parts) > 10 and parts[10].isdigit() else 0
                        adm_msg_id = parts[11] if len(parts) > 11 else "0"

                        if resi.strip() == resi_target.strip():
                            target_chat_id = chat_id
                            target_payment = pay_method
                            target_points_cost = p_cost
                            current_status = status
                            
                            if status in ["BERHASIL", "DITOLAK", "CANCELLED", "EXPIRED"] and status_baru in ["BERHASIL", "DITOLAK"]:
                                rows.append(line)
                                continue
                                
                            status = status_baru
                            updated = True
                            
                        rows.append(f"{chat_id}|{tanggal}|{hari}|{jam}|{paket}|{harga}|{resi}|{status}|{timestamp_epoch}|{pay_method}|{p_cost}|{adm_msg_id}\n")
        except FileNotFoundError:
            return False

        if updated:
            with open("orders.txt", "w") as f:
                f.writelines(rows)
            
            if target_chat_id and current_status not in ["BERHASIL", "DITOLAK", "CANCELLED", "EXPIRED"]:
                if status_baru == "BERHASIL":
                    set_user_coupon_status(target_chat_id, "USED")
                    if target_payment != "POIN":
                        add_user_points(target_chat_id, 10)
                elif status_baru in ["DITOLAK", "EXPIRED", "CANCELLED"]:
                    set_user_coupon_status(target_chat_id, "AVAILABLE")
                    if target_payment == "POIN" and target_points_cost > 0:
                        add_user_points(target_chat_id, target_points_cost)
                    
            return True
    except Exception as e:
        print(f"[UPDATE ORDER ERROR]: {e}")
    return False

def get_user_orders(chat_id):
    orders = []
    try:
        with open("orders.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8 and parts[0] == str(chat_id):
                    orders.append({
                        'tanggal': parts[1], 'hari': parts[2], 'jam': parts[3],
                        'paket': parts[4], 'harga': parts[5], 'resi': parts[6],
                        'status': parts[7], 'pay_method': parts[9] if len(parts) > 9 else "TRANSFER"
                    })
    except FileNotFoundError:
        pass
    return orders

def get_latest_user_order_data(chat_id):
    try:
        WIB = timezone(timedelta(hours=7))
        current_time = int(datetime.now(WIB).timestamp())
        last_order = None
        with open("orders.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8 and parts[0] == str(chat_id):
                    last_order = parts
        if last_order:
            resi = last_order[6]
            status = last_order[7]
            timestamp_epoch = int(last_order[8]) if len(last_order) > 8 else current_time
            if status == "PENDING" and (current_time - timestamp_epoch > 900):
                update_order_status_by_resi(resi, "EXPIRED")
                return resi, "EXPIRED"
            return resi, status
    except Exception as e:
        print(f"[LATEST ORDER ERROR]: {e}")
    return f"PKL-MLBB-{random.randint(10000, 99999)}", "PENDING"

def get_time_greeting():
    WIB = timezone(timedelta(hours=7))
    hour = datetime.now(WIB).hour
    if 4 <= hour < 11:
        return "Selamat Pagi 🌅"
    elif 11 <= hour < 15:
        return "Selamat Siang ☀️"
    elif 15 <= hour < 18:
        return "Selamat Sore 🌇"
    else:
        return "Selamat Malam 🌙"

def check_store_status():
    WIB = timezone(timedelta(hours=7))
    hour = datetime.now(WIB).hour
    if 0 <= hour < 7:
        return False, "⚠️ <b>INFO OPERASIONAL TOKO:</b>\nHalo Kak! Saat ini toko sedang istirahat (Offline) jam 00:00 - 07:00 WIB. Pesanan dan pembayaran tetap bisa dilakukan lewat bot, namun proses pengiriman script dan verifikasi resi akan dilanjutkan pagi ini mulai pukul 07:00 WIB ya! 🙏✨"
    return True, ""
def get_random_masked_name():
    list_nama_tele = [
        "@R_Zky***", "@Alvinn_***", "@Dimas_99***", "@RezaPrat_***", 
        "@Bayu_Official***", "@Farel_X***", "@Yoga_Mlg***", "@DickyGez_***", 
        "@SuryaPratama***", "@RamaWicak***", "@Gilang_ID***", "@BagasKusn***",
        "@Arif_Wd***", "@DaniPratama***", "@Hendra_99***", "@Rian_Xyz***",
        "@Aldi_07***", "@Bintang_ID***", "@CandraPras***", "@DikaPrast_***",
        "@Fajar_01***", "@GalihGmr***", "@IqbalID***", "@JokoPrasetyo***",
        "@KevinWdj***", "@LukmanHkm***", "@MaulanaID***", "@NaufalXyz***",
        "@Pratama99***", "@RafliSultan***", "@SatriaGaming***", "@TegarGanz***",
        "@VianID***", "@WahyuPrat***", "@YudaDev***", "@ZakiMlf***",
        "@Amirul_My***", "@Haikal_Iskandar***", "@Farhan_Zul***", "@Aiman_Badri***",
        "@Aqil_Danial***", "@Syahmi_Zain***", "@Luqman_Hakim***", "@Zulhelmi_My***",
        "@Alex_Walker***", "@Liam_Smith***", "@Noah_Miller***", "@Oliver_Davis***",
        "@Sultan_Mlbb***", "@Anjay_Mabar***", "@Gacor_Gaming***", "@TopGlobal_1***"
    ]
    return random.choice(list_nama_tele)

def generate_single_testimonial():
    list_paket = [
        ("Natural Balance (30 Hari)", "Rp 120.000"),
        ("Light VIP + Drone (30 Hari)", "Rp 95.000"),
        ("Semi-Safe 14 Hari", "Rp 75.000"),
        ("Lifetime Safe Permanent", "Rp 200.000"),
        ("Sultan One Hit 100% (30 Hari)", "Rp 150.000"),
        ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000"),
        ("Semi-Private 14 Hari", "Rp 75.000"),
        ("Permanent Legend (Lifetime)", "Rp 250.000")
    ]
    nama = get_random_masked_name()
    paket, harga = random.choice(list_paket)
    menit_lalu = random.randint(2, 45)
    current_hour = datetime.now(timezone(timedelta(hours=7))).hour
    waktu_ket = "pagi ini" if 4 <= current_hour < 11 else ("siang ini" if 11 <= current_hour < 15 else ("sore ini" if 15 <= current_hour < 18 else "malam ini"))
    
    return (
        "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
        f"✅ Buyer ID: {nama}\n"
        f"📦 Item Purchased: {paket}\n"
        f"💵 Price: {harga}\n"
        f"⏱️ Time: {menit_lalu} menit yang lalu ({waktu_ket})\n"
        f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
        "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
        f"🤖 Bot Store: @{bot.get_me().username}"
    )

def generate_fake_testimonials_list():
    list_paket = [
        ("Natural Balance", "Rp 120.000"), ("Light VIP + Drone", "Rp 95.000"),
        ("Semi-Safe 14 Hari", "Rp 75.000"), ("Lifetime Safe Permanent", "Rp 200.000"),
        ("Sultan One Hit 100%", "Rp 150.000"), ("VIP Pro One Hit 80%", "Rp 100.000")
    ]
    testi_output = ""
    for i in range(1, 6):
        nama = get_random_masked_name()
        paket, harga = random.choice(list_paket)
        menit_lalu = random.randint(2, 45)
        testi_output += f"✅ {i}. Buyer ID: {nama}\n   • Dibeli: {paket} ({harga})\n   • Status: LUNAS & SCRIPT TERKIRIM\n\n"
    return testi_output

def background_auto_poster():
    time.sleep(60) 
    while True:
        try:
            time.sleep(random.choice([1500, 3600, 7200, 10800]))
            bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(), message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        except Exception:
            time.sleep(60)

threading.Thread(target=background_auto_poster, daemon=True).start()

def background_auto_broadcast():
    time.sleep(300)
    broadcast_templates = [
        ("📢 <b>INFO PROMO SPESIAL HARI INI!</b> 🔥\n\nBuruan sikat script VIP kita sekarang!\n🛒 Cek katalog di bot: @{bot_username}",),
        ("🛡️ <b>KENAPA HARUS PAKAI SCRIPT PAKEL MLBBSTORE?</b> ⚡\n\nEnkripsi high-tier anti-detect paling stabil se-Indonesia.\n📦 Pilih paket di: @{bot_username}",)
    ]
    while True:
        try:
            time.sleep(random.randint(14400, 28800))
            try:
                with open("users.txt", "r") as f:
                    users = [line.strip() for line in f.read().splitlines() if line.strip()]
            except FileNotFoundError:
                continue
            if not users:
                continue
            pesan_final = random.choice(broadcast_templates)[0].format(bot_username=bot.get_me().username)
            for chat_id in set(users):
                try:
                    bot.send_message(chat_id=chat_id, text=f"📢 <b>PENGUMUMAN OTOMATIS</b>\n\n{pesan_final}", parse_mode="HTML")
                    time.sleep(0.05)
                except Exception:
                    pass
        except Exception:
            time.sleep(300)

threading.Thread(target=background_auto_broadcast, daemon=True).start()

TRANSLATIONS = {
    'id': {
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_testi': "🌟 Testimoni & Real-Time Bukti Order",
        'btn_riwayat': "📦 Cek Riwayat & Status Pesanan Saya",
        'btn_promo': "🎁 Klaim Kupon & Poin Loyalitas",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Lengkap",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥",
        'bonus_txt': "⚡ BONUS SPESIAL FREE ALL PACKAGES:\n  • Panel Server Lag Musuh\n  • Drone View X1 - X10",
        'p1_normal': [
            ("🛒 Beli: Natural Balance (Rp 120k / 30 Poin)", "buy_natural", "• 💎 Natural Balance — Rp 120.000 / 30 Poin"),
            ("🛒 Beli: Light VIP + Drone (Rp 95k / 25 Poin)", "buy_light", "• ⚡ Light VIP + Drone — Rp 95.000 / 25 Poin"),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k / 20 Poin)", "buy_semisafe", "• 🛡️ Semi-Safe — Rp 75.000 / 20 Poin"),
            ("🛒 Beli: Lifetime Safe (Rp 200k / 50 Poin)", "buy_lifetimesafe", "• 👑 Lifetime — Rp 200.000 / 50 Poin")
        ],
        'p1_promo': [
            ("🛒 Natural Balance (Hemat 10k / 30 Poin)", "buy_natural", "• 💎 Natural Balance — <s>Rp 120.000</s> <b>Rp 110.000</b> (Promo Member Baru!)"),
            ("🛒 Light VIP + Drone (Hemat 10k / 25 Poin)", "buy_light", "• ⚡ Light VIP + Drone — <s>Rp 95.000</s> <b>Rp 85.000</b> (Promo Member Baru!)"),
            ("🛒 Semi-Safe 14 Hari (Hemat 10k / 20 Poin)", "buy_semisafe", "• 🛡️ Semi-Safe — <s>Rp 75.000</s> <b>Rp 65.000</b> (Promo Member Baru!)"),
            ("🛒 Lifetime Safe (Hemat 10k / 50 Poin)", "buy_lifetimesafe", "• 👑 Lifetime — <s>Rp 200.000</s> <b>Rp 190.000</b> (Promo Member Baru!)")
        ],
        'p2_normal': [
            ("🛒 Beli: Sultan One Hit (Rp 150k / 40 Poin)", "buy_sultan", "• 💥 Sultan One Hit — Rp 150.000 / 40 Poin"),
            ("🛒 Beli: VIP Pro One Hit (Rp 100k / 30 Poin)", "buy_pro", "• ⚡ VIP Pro — Rp 100.000 / 30 Poin")
        ],
        'p2_promo': [
            ("🛒 Sultan One Hit (Hemat 10k / 40 Poin)", "buy_sultan", "• 💥 Sultan One Hit — <s>Rp 150.000</s> <b>Rp 140.000</b> (Promo Member Baru!)"),
            ("🛒 VIP Pro One Hit (Hemat 10k / 30 Poin)", "buy_pro", "• ⚡ VIP Pro — <s>Rp 100.000</s> <b>Rp 90.000</b> (Promo Member Baru!)")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': f"💳 DANA / GoPay: <code>{INFO_DANA}</code> (a.n. PakelMlbb)",
        'confirm_instr': "🛡️ Kirim screenshot bukti transfer untuk verifikasi resi.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue", 'btn_testi': "🌟 Live Testimonials",
        'btn_riwayat': "📦 My Orders", 'btn_promo': "🎁 Claim Promo & Points",
        'btn_cara_order': "❓ How to Order", 'btn_bayar': "💳 Payments",
        'btn_faq': "💡 FAQ", 'btn_konfirmasi': "✅ Check Status",
        'btn_admin': "💬 Contact Admin", 'back': "⬅️ Main Menu",
        'cat_title_1': "🔥 CATALOGUE PART 1", 'cat_title_2': "🔥 CATALOGUE PART 2",
        'bonus_txt': "⚡ SPECIAL BONUS:", 'p1_normal': [("🛒 Natural Balance", "buy_natural", "• Natural Balance")],
        'p1_promo': [("🛒 Natural Balance (Promo)", "buy_natural", "• Natural Balance")],
        'p2_normal': [("🛒 Sultan One Hit", "buy_sultan", "• Sultan One Hit")],
        'p2_promo': [("🛒 Sultan One Hit (Promo)", "buy_sultan", "• Sultan One Hit")],
        'next_1': "▶️ Next", 'prev_2': "◀️ Back", 'inv_title': "🛒 INVOICE",
        'pay_info': "💳 Payment Info", 'confirm_instr': "🛡️ Send receipt.",
    }
}

def get_lang(user):
    code = getattr(user, 'language_code', 'en')
    if code and code.lower().startswith('id'):
        return 'id'
    return 'en'

def get_back_markup(l):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(TRANSLATIONS.get(l, TRANSLATIONS['en'])['back'], callback_data='menu_utama'))
    return markup
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    save_user(message.chat.id)
    l = get_lang(user)
    t = TRANSLATIONS[l]
    user_points = get_user_points(message.chat.id)
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
        types.InlineKeyboardButton(t['btn_testi'], callback_data='menu_testi'),
        types.InlineKeyboardButton(t['btn_riwayat'], callback_data='menu_riwayat'),
        types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
        types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
        types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
        types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
        types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
        types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
    )
    is_open, store_msg = check_store_status()
    text = f"🔥 {get_time_greeting()}, Kak {user.first_name}!\n🪙 Saldo Poin Anda: <b>{user_points} Poin</b>\n\nPusat layanan script VIP Mobile Legends terpercaya.\n\n"
    if not is_open:
        text += f"{store_msg}\n\n"
    text += "👇 Silakan pilih menu di bawah:"
    bot.send_message(message.chat.id, text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['riwayat', 'history'])
def cmd_riwayat(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    get_latest_user_order_data(message.chat.id)
    orders = get_user_orders(message.chat.id)
    
    if not orders:
        text = f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n❌ Belum ada riwayat pesanan tercatat."
    else:
        text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
        for idx, o in enumerate(orders[-5:], 1):
            st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK", "CANCELLED": "❌ DIBATALKAN", "EXPIRED": "⌛ EXPIRED"}.get(o['status'], "⏳ PENDING")
            text += f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n   • Resi: <code>{o['resi']}</code>\n   • Status: {st}\n\n"
    bot.reply_to(message, text, reply_markup=get_back_markup(l), parse_mode="HTML")

@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    coupon_status = get_user_coupon_status(message.chat.id)
    items = t['p1_promo'] if coupon_status == "AVAILABLE" else t['p1_normal']
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn_text, cb_val, _ in items:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=cb_val))
    markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
    markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

    txt = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([d for _, _, d in items])
    txt += f"\n\n🪙 Saldo Poin Anda: <b>{get_user_points(message.chat.id)} Poin</b>"
    bot.send_message(message.chat.id, txt, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['testi', 'push'])
def admin_push_testi(message):
    try:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(), message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        bot.reply_to(message, "✅ Berhasil mengirim testimoni!")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal: {e}")

@bot.message_handler(commands=['sc'])
def cmd_sc_interactive(message):
    save_user(message.chat.id)
    args = message.text.replace('/sc', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /sc @UsernamePembeli")
        return
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn_text, cb_data in [
        ("💎 Natural Balance (30 Hari)", "sc_buy_natural"),
        ("⚡ Light VIP + Drone (30 Hari)", "sc_buy_light"),
        ("🛡️ Semi-Safe 14 Hari", "sc_buy_semisafe"),
        ("👑 Lifetime Safe Permanent", "sc_buy_lifetimesafe")
    ]:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"{cb_data}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target: <b>{target_buyer}</b>\nPilih paket:", reply_markup=markup, parse_mode="HTML")
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    save_user(call.message.chat.id)
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data.startswith('cancel_'):
        resi_target = call.data.replace('cancel_', '')
        admin_msg_id = None
        try:
            with open("orders.txt", "r") as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) >= 12 and p[6].strip() == resi_target.strip():
                        if p[7].strip() != "PENDING":
                            bot.answer_callback_query(call.id, text="Pesanan sudah diproses atau kedaluwarsa.", show_alert=True)
                            return
                        admin_msg_id = int(p[11]) if p[11].isdigit() else None
                        break
        except Exception:
            pass

        success = update_order_status_by_resi(resi_target, "CANCELLED")
        if success:
            if admin_msg_id:
                try:
                    old_caption = call.message.caption or "Laporan Pembayaran Poin"
                    new_admin_caption = f"❌ <b>[DIBATALKAN OLEH PEMBELI]</b>\n\n{old_caption}\n\n<b>STATUS: ❌ DIBATALKAN USER (Poin Dikembalikan)</b>"
                    bot.edit_message_caption(chat_id=GROUP_PAY_ID, message_id=admin_msg_id, caption=new_admin_caption, parse_mode="HTML", reply_markup=None)
                except Exception as e:
                    print(f"[EDIT ADMIN MSG CANCEL ERROR]: {e}")

            cancel_text = (
                f"❌ <b>PESANAN BERHASIL DIBATALKAN</b> ❌\n\n"
                f"🔑 No Resi: <code>{resi_target}</code>\n"
                "Pesanan dibatalkan atas permintaan Anda.\n"
                "💡 Kupon diskon dan saldo poin Anda telah dikembalikan dengan aman tanpa duplikasi!"
            )
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=cancel_text, parse_mode="HTML", reply_markup=get_back_markup(l))
            except Exception:
                bot.send_message(chat_id, cancel_text, parse_mode="HTML", reply_markup=get_back_markup(l))
            bot.answer_callback_query(call.id, text="Pesanan dibatalkan & poin dikembalikan!")
        else:
            bot.answer_callback_query(call.id, text="Gagal membatalkan pesanan.", show_alert=True)
        return

    if call.data.startswith('paymode_'):
        parts = call.data.split('|')
        if len(parts) < 3:
            return
        action_type, paket_code = parts[1], parts[2]
        
        paket_dict = {
            'buy_natural': ("Natural Balance (30 Hari)", "Rp 120.000", 30),
            'buy_light': ("Light VIP + Drone (30 Hari)", "Rp 95.000", 25),
            'buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000", 20),
            'buy_lifetimesafe': ("Lifetime Safe Permanent", "Rp 200.000", 50),
            'buy_sultan': ("Sultan One Hit 100% (30 Hari)", "Rp 150.000", 40),
            'buy_pro': ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000", 30)
        }
        p_name, p_price, p_points = paket_dict.get(paket_code, ("VIP Package", "Rp 100.000", 30))
        resi_unik = f"PKL-MLBB-{random.randint(10000, 99999)}"
        
        if action_type == 'poin':
            user_pts = get_user_points(chat_id)
            if user_pts >= p_points:
                if get_user_coupon_status(chat_id) == "AVAILABLE":
                    set_user_coupon_status(chat_id, "PENDING")

                pending_poin_text = (
                    f"🪙 <b>INVOICE PEMBAYARAN VIA POIN (PENDING)</b> 🪙\n\n"
                    f"📦 Paket: {p_name}\n"
                    f"🪙 Poin yang Akan Dipotong: <b>{p_points} Poin</b> (Sisa Poin: {user_pts} Poin)\n"
                    f"🔑 No Resi: <code>{resi_unik}</code>\n"
                    f"⏱️ Status: Menunggu Verifikasi Admin.\n\n"
                    "💡 <i>Poin baru akan dipotong setelah di-ACC admin!</i>"
                )
                
                markup_poin_inv = types.InlineKeyboardMarkup(row_width=1)
                markup_poin_inv.add(
                    types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                    types.InlineKeyboardButton("📦 Cek Riwayat Pesanan", callback_data='menu_riwayat'),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )
                
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    pass
                
                bot.send_message(chat_id, pending_poin_text, reply_markup=markup_poin_inv, parse_mode="HTML")
                
                try:
                    report_admin_poin = (
                        "🪙 <b>KLAIM PEMBAYARAN VIA POIN MASUK!</b> 🪙\n\n"
                        f"👤 User: @{user.username if user.username else user.first_name} (ID: <code>{chat_id}</code>)\n"
                        f"📦 Paket: {p_name}\n"
                        f"🪙 Nominal Poin: <b>{p_points} Poin</b>\n"
                        f"🔑 No Resi: <code>{resi_unik}</code>\n\n"
                        "👇 <i>Klik ACC untuk potong poin, atau TOLAK!</i>"
                    )
                    markup_admin_poin = types.InlineKeyboardMarkup(row_width=2)
                    markup_admin_poin.add(
                        types.InlineKeyboardButton("✅ ACC POIN", callback_data=f"apoin|{resi_unik}"),
                        types.InlineKeyboardButton("❌ TOLAK POIN", callback_data=f"tpoin|{resi_unik}")
                    )
                    admin_sent = bot.send_message(GROUP_PAY_ID, report_admin_poin, message_thread_id=GROUP_PAY_TOPIC_ID, parse_mode="HTML", reply_markup=markup_admin_poin)
                    save_order(chat_id, p_name, f"{p_points} Poin", resi_unik, payment_method="POIN", point_cost=p_points, admin_msg_id=admin_sent.message_id)
                except Exception as e:
                    print(f"[REPORT ADMIN POIN ERROR]: {e}")
                    save_order(chat_id, p_name, f"{p_points} Poin", resi_unik, payment_method="POIN", point_cost=p_points, admin_msg_id=0)
                    
                bot.answer_callback_query(call.id, text="Invoice poin diterbitkan!")
                return
            else:
                bot.answer_callback_query(call.id, text="Poin Anda tidak mencukupi!", show_alert=True)
                return

        elif action_type == 'transfer':
            if get_user_coupon_status(chat_id) == "AVAILABLE":
                set_user_coupon_status(chat_id, "PENDING")
            
            save_order(chat_id, p_name, p_price, resi_unik, payment_method="TRANSFER", point_cost=0, admin_msg_id=0)
            
            invoice_text = (
                f"{t['inv_title'].format(name=user.first_name)}\n\n"
                f"📦 Paket: {p_name}\n💵 Harga: {p_price}\n"
                f"🔢 Resi: <code>{resi_unik}</code>\n\n"
                f"{t['pay_info']}\n\n{t['confirm_instr']}"
            )
            markup_inv = types.InlineKeyboardMarkup(row_width=1)
            markup_inv.add(
                types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
            )
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            bot.send_message(chat_id, invoice_text, reply_markup=markup_inv, parse_mode="HTML")
            bot.answer_callback_query(call.id)
            return
    if call.data.startswith('acc_') or call.data.startswith('tolak_') or call.data.startswith('acc|') or call.data.startswith('tolak|') or call.data.startswith('apoin|') or call.data.startswith('tpoin|'):
        try:
            sep = '|' if '|' in call.data else '_'
            parts = call.data.split(sep)
            action = parts[0].replace('_', '')
            resi_code = parts[1] if action in ['apoin', 'tpoin'] else parts[2]
            target_user_id = parts[1] if action not in ['apoin', 'tpoin'] else None

            order_status_db = "PENDING"
            p_points_val = 0
            if action in ['apoin', 'tpoin']:
                try:
                    with open("orders.txt", "r") as f:
                        for line in f:
                            p = line.strip().split('|')
                            if len(p) >= 11 and p[6].strip() == resi_code.strip():
                                target_user_id = p[0]
                                order_status_db = p[7]
                                p_points_val = int(p[10]) if p[10].isdigit() else 0
                                break
                except Exception:
                    pass

            if not target_user_id:
                bot.answer_callback_query(call.id, text="Gagal: Data resi tidak ditemukan!", show_alert=True)
                return

            if order_status_db in ["CANCELLED", "EXPIRED", "BERHASIL", "DITOLAK"]:
                bot.answer_callback_query(call.id, text=f"Peringatan: Pesanan ini sudah berstatus {order_status_db}!", show_alert=True)
                return

            original_text = call.message.caption or call.message.text or ""

            if action == 'acc' or action == 'apoin':
                if action == 'apoin':
                    if get_user_points(target_user_id) >= p_points_val:
                        reduce_user_points(target_user_id, p_points_val)
                    else:
                        bot.answer_callback_query(call.id, text="Gagal ACC: Saldo poin pembeli tidak cukup!", show_alert=True)
                        return

                update_order_status_by_resi(resi_code, "BERHASIL")
                
                new_admin_text = original_text + f"\n\n<b>STATUS: ✅ DI-ACC ADMIN (Sukses)</b>"
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)

                bot.send_message(target_user_id, f"🎉 <b>PEMBAYARAN ANDA TELAH DI-ACC ADMIN!</b> 🎉\nResi: <code>{resi_code}</code>", parse_mode="HTML")
                
                markup_rating = types.InlineKeyboardMarkup(row_width=5)
                markup_rating.add(
                    types.InlineKeyboardButton("⭐ 1", callback_data=f"rate|1|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 2", callback_data=f"rate|2|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 3", callback_data=f"rate|3|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 4", callback_data=f"rate|4|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 5", callback_data=f"rate|5|{resi_code}")
                )
                bot.send_message(target_user_id, "⭐ Berikan rating pelayanan kami:", reply_markup=markup_rating, parse_mode="HTML")
                bot.answer_callback_query(call.id, text="Berhasil di-ACC!")

            elif action == 'tolak' or action == 'tpoin':
                update_order_status_by_resi(resi_code, "DITOLAK")
                new_admin_text = original_text + "\n\n<b>STATUS: ❌ DITOLAK ADMIN</b>"
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)
                bot.send_message(target_user_id, f"❌ Pembayaran ditolak admin untuk resi <code>{resi_code}</code>.", parse_mode="HTML")
                bot.answer_callback_query(call.id, text="Pesanan ditolak.")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Error: {e}", show_alert=True)
        return

    if call.data.startswith('sc_buy_'):
        try:
            data_split = call.data.split('|')
            action, buyer_name = data_split[0], data_split[1]
            paket_map = {
                'sc_buy_natural': ("Natural Balance", "Rp 120.000"),
                'sc_buy_light': ("Light VIP + Drone", "Rp 95.000"),
                'sc_buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000"),
                'sc_buy_lifetimesafe': ("Lifetime Safe", "Rp 200.000")
            }
            p_nama, p_hrg = paket_map.get(action, ("VIP Package", "Rp 100.000"))
            post_text = (
                "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                f"✅ Buyer ID: {buyer_name}\n"
                f"📦 Item Purchased: {p_nama}\n"
                f"💵 Price: {p_hrg}\n"
                f"⏱️ Time: {random.randint(1, 5)} menit yang lalu\n"
                f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
                f"🤖 Bot Store: @{bot.get_me().username}"
            )
            bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text, message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"✅ <b>BERHASIL DIKIRIM KE GRUP!</b>\n• Buyer: {buyer_name}\n• Paket: {p_nama}", parse_mode="HTML")
            bot.answer_callback_query(call.id, text="Terkirim ke grup!")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
        return
    if call.data == 'menu_utama':
        user_points = get_user_points(chat_id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
            types.InlineKeyboardButton(t['btn_testi'], callback_data='menu_testi'),
            types.InlineKeyboardButton(t['btn_riwayat'], callback_data='menu_riwayat'),
            types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
            types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
            types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
            types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
            types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
            types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
        )
        text = f"🔥 {get_time_greeting()}, Kak {user.first_name}!\n🪙 Saldo Poin Anda: <b>{user_points} Poin</b>\n\nPilih menu utama:"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id, text=text, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        coupon_status = get_user_coupon_status(chat_id)
        items = t['p1_promo'] if coupon_status == "AVAILABLE" else t['p1_normal']
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, cb_val, _ in items:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=cb_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        txt = f"{t['cat_title_1'].format(name=user.first_name)}\n\n" + "\n\n".join([d for _, _, d in items]) + f"\n\n🪙 Saldo Poin: {get_user_points(chat_id)}"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'katalog_part2':
        coupon_status = get_user_coupon_status(chat_id)
        items = t['p2_promo'] if coupon_status == "AVAILABLE" else t['p2_normal']
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, cb_val, _ in items:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=cb_val))
        markup.add(types.InlineKeyboardButton(t['prev_2'], callback_data='katalog_part1'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        txt = f"{t['cat_title_2'].format(name=user.first_name)}\n\n" + "\n\n".join([d for _, _, d in items]) + f"\n\n🪙 Saldo Poin: {get_user_points(chat_id)}"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=txt, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        paket_code = call.data
        paket_dict = {
            'buy_natural': ("Natural Balance (30 Hari)", "Rp 120.000", 30),
            'buy_light': ("Light VIP + Drone (30 Hari)", "Rp 95.000", 25),
            'buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000", 20),
            'buy_lifetimesafe': ("Lifetime Safe Permanent", "Rp 200.000", 50),
            'buy_sultan': ("Sultan One Hit 100% (30 Hari)", "Rp 150.000", 40),
            'buy_pro': ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000", 30)
        }
        p_name, p_price, p_points = paket_dict.get(paket_code, ("VIP Package", "Rp 100.000", 30))
        
        choice_text = f"🛒 <b>PILIH PEMBAYARAN</b>\nPaket: {p_name}\n Harga: {p_price} | Poin: {p_points}"
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(f"🪙 Bayar Pakai Saldo Poin ({p_points} Poin)", callback_data=f"paymode_|poin|{paket_code}"),
            types.InlineKeyboardButton(f"💳 Bayar Transfer ({p_price})", callback_data=f"paymode_|transfer|{paket_code}"),
            types.InlineKeyboardButton(t['back'], callback_data='menu_katalog')
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=choice_text, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data.startswith('rate|'):
        parts = call.data.split('|')
        if len(parts) < 3:
            return
        rating_val, resi_code = parts[1], parts[2]
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(types.InlineKeyboardButton("🔥 Super Bagus & Mantap!", callback_data=f"textrev|{resi_code}|{rating_val}|Super bagus"))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"⭐ Rating {rating_val} bintang dicatat! Pilih ulasan cepat atau ketik manual:", reply_markup=markup)
        with open(f"pending_review_{chat_id}.txt", "w") as f:
            f.write(f"{resi_code}|{rating_val}")
        bot.answer_callback_query(call.id)

    elif call.data.startswith('textrev|'):
        parts = call.data.split('|', 3)
        if len(parts) < 4:
            return
        resi_c, rating_c, quick_text = parts[1], parts[2], parts[3]
        save_user_review(chat_id, rating_c, quick_text)
        try:
            if os.path.exists(f"pending_review_{chat_id}.txt"):
                os.remove(f"pending_review_{chat_id}.txt")
        except Exception:
            pass
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎉 Terima kasih ulasannya!", parse_mode="HTML")
        bot.answer_callback_query(call.id, text="Terkirim!")
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_and_reviews(message):
    chat_id = message.chat.id
    if message.chat.type != 'private':
        return
    save_user(chat_id)
    user = message.from_user
    txt = message.text.strip()
    
    review_flag_file = f"pending_review_{chat_id}.txt"
    try:
        if os.path.exists(review_flag_file):
            with open(review_flag_file, "r") as f:
                data_rev = f.read().strip().split('|')
            if len(data_rev) == 2:
                resi_c, rating_c = data_rev
                save_user_review(chat_id, rating_c, txt)
                try:
                    os.remove(review_flag_file)
                except Exception:
                    pass
                bot.reply_to(message, "🎉 Terima kasih atas ulasan terbaikmu!", reply_markup=get_back_markup(get_lang(user)), parse_mode="HTML")
                return
    except Exception:
        pass

    bot.reply_to(message, f"Halo {user.first_name}! Ketik /start untuk membuka menu utama.", disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    save_user(message.chat.id)
    user = message.from_user
    resi_unik, order_status = get_latest_user_order_data(message.chat.id)
    
    if order_status == "EXPIRED":
        bot.reply_to(message, "❌ Waktu konfirmasi habis (15 menit).", parse_mode="HTML")
        return

    user_caption = message.caption if message.caption else "Tidak ada pesan"
    bot.reply_to(message, f"✅ Bukti pembayaran diterima!\nResi: {resi_unik}", disable_web_page_preview=True)
    
    try:
        caption_admin = f"🚨 <b>BUKTI TRANSFER MASUK!</b>\n👤 @{user.username or user.first_name}\nResi: <code>{resi_unik}</code>"
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ ACC", callback_data=f"acc|{user.id}|{resi_unik}"),
            types.InlineKeyboardButton("❌ TOLAK", callback_data=f"tolak|{user.id}|{resi_unik}")
        )
        bot.send_photo(chat_id=GROUP_PAY_ID, photo=message.photo[-1].file_id, caption=caption_admin, message_thread_id=GROUP_PAY_TOPIC_ID, parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        print(f"[FORWARD PHOTO ERROR]: {e}")

print("[INFO] Pakel MlbbStore Master Ultimate Edition 8 Bagian Berhasil Dijalankan...")
bot.infinity_polling()
