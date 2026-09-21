import telebot
from telebot import types
import random
import time
import threading
from datetime import datetime, timezone, timedelta

# Token bot resmi Pakel MlbbStore
TOKEN = '8614166487:AAFt6SzB6mP6sA31fXU7QUsz9uH8KdIEiFo'

bot = telebot.TeleBot(TOKEN)

# Pembersih webhook otomatis agar terhindar dari Error 409 Conflict
try:
    bot.remove_webhook()
except Exception:
    pass

# --- PENGATURAN IDENTITAS & JALUR GRUP TERPISAH ---
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

# --- MANAJEMEN STATUS KUPON MEMBER BARU ---
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

def save_order(chat_id, paket_nama, harga, resi):
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
        hari_en = now.strftime('%a')
        hari_str = days_indo.get(hari_en, hari_en)
        
        order_line = f"{chat_id}|{tanggal_str}|{hari_str}|{jam_str}|{paket_nama}|{harga}|{resi}|PENDING|{timestamp_epoch}\n"
        
        with open("orders.txt", "a") as f:
            f.write(order_line)
    except Exception as e:
        print(f"[SAVE ORDER ERROR]: {e}")

def update_order_status_by_resi(resi_target, status_baru):
    try:
        updated = False
        target_chat_id = None
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

                        if resi.strip() == resi_target.strip():
                            target_chat_id = chat_id
                            status = status_baru
                            updated = True
                        rows.append(f"{chat_id}|{tanggal}|{hari}|{jam}|{paket}|{harga}|{resi}|{status}|{timestamp_epoch}\n")
        except FileNotFoundError:
            return False

        if updated:
            with open("orders.txt", "w") as f:
                f.writelines(rows)
            
            if target_chat_id:
                if status_baru == "BERHASIL":
                    set_user_coupon_status(target_chat_id, "USED")
                elif status_baru == "DITOLAK" or status_baru == "EXPIRED":
                    set_user_coupon_status(target_chat_id, "AVAILABLE")
                    
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
                        'tanggal': parts[1],
                        'hari': parts[2],
                        'jam': parts[3],
                        'paket': parts[4],
                        'harga': parts[5],
                        'resi': parts[6],
                        'status': parts[7]
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
        "@EkaSltn***", "@DoniGmr***", "@FikriDx***", "@Andi99***",
        "@BudiSt***", "@Coki***", "@Dandi***", "@EkoPrast***",
        "@Fandi***", "@Guntur***", "@Hafiz***", "@Imam***",
        "@Jefri***", "@Kiki***", "@Lutfi***", "@Miko***",
        "@Nanda***", "@Oky***", "@Pandu***", "@Qomar***",
        "@Rahmat***", "@Riki***", "@Roni***", "@Rudi***",
        "@Sandi***", "@Toni***", "@Udin***", "@Vicky***",
        "@Wahid***", "@Yadi***", "@Zainal***", "@Adit***",
        "@Agus***", "@Ahmad***", "@Akbar***", "@Alex***",
        "@Amri***", "@Anang***", "@Angga***", "@Anton***",
        "@Arya***", "@Asep***", "@Azka***", "@Bagus***",
        "@Basri***", "@Beni***", "@Boy***", "@Candra***",
        "@Darma***", "@Dedi***", "@Deny***", "@Diki***",
        "@Egi***", "@Eky***", "@Fahri***", "@Fandi***",
        "@Farhan***", "@Fauzi***", "@Febri***", "@Firman***",
        "@Fuat***", "@Gani***", "@Gerry***", "@Hadi***",
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
    if 4 <= current_hour < 11:
        waktu_ket = "pagi ini"
    elif 11 <= current_hour < 15:
        waktu_ket = "siang ini"
    elif 15 <= current_hour < 18:
        waktu_ket = "sore ini"
    else:
        waktu_ket = "malam ini"
    
    text = (
        "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
        f"✅ Buyer ID: {nama}\n"
        f"📦 Item Purchased: {paket}\n"
        f"💵 Price: {harga}\n"
        f"⏱️ Time: {menit_lalu} menit yang lalu ({waktu_ket})\n"
        f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
        "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
        f"🤖 Bot Store: @{bot.get_me().username}"
    )
    return text

def generate_fake_testimonials_list():
    list_paket = [
        ("Natural Balance", "Rp 120.000"),
        ("Light VIP + Drone", "Rp 95.000"),
        ("Semi-Safe 14 Hari", "Rp 75.000"),
        ("Lifetime Safe Permanent", "Rp 200.000"),
        ("Sultan One Hit 100%", "Rp 150.000"),
        ("VIP Pro One Hit 80%", "Rp 100.000"),
        ("Semi-Private 14 Hari", "Rp 75.000"),
        ("Permanent Legend", "Rp 250.000")
    ]
    testi_output = ""
    for i in range(1, 6):
        nama = get_random_masked_name()
        paket, harga = random.choice(list_paket)
        menit_lalu = random.randint(2, 45)
        testi_output += (
            f"✅ {i}. Buyer ID: {nama}\n"
            f"   • Dibeli: {paket} ({harga})\n"
            f"   • Status: LUNAS & SCRIPT TERKIRIM\n"
            f"   • Waktu: {menit_lalu} menit yang lalu\n\n"
        )
    return testi_output

def background_auto_poster():
    time.sleep(60) 
    while True:
        try:
            pilihan_waktu = [1500, 3600, 7200, 10800]
            sleep_time = random.choice(pilihan_waktu)
            time.sleep(sleep_time)
            post_text = generate_single_testimonial()
            bot.send_message(
                chat_id=GROUP_CHAT_ID, 
                text=post_text, 
                message_thread_id=GROUP_TOPIC_ID, 
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"[AUTO-POST ERROR]: {e}")
            time.sleep(60)

poster_thread = threading.Thread(target=background_auto_poster, daemon=True)
poster_thread.start()

@bot.message_handler(commands=['testi', 'push'])
def admin_push_testi(message):
    try:
        post_text = generate_single_testimonial()
        bot.send_message(
            chat_id=GROUP_CHAT_ID, 
            text=post_text, 
            message_thread_id=GROUP_TOPIC_ID, 
            disable_web_page_preview=True
        )
        bot.reply_to(message, "✅ Berhasil! Testimoni real-time baru saja dikirim ke grup komunitas utama.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal mengirim testimoni: {e}")

@bot.message_handler(commands=['sc'])
def cmd_sc_interactive(message):
    save_user(message.chat.id)
    args = message.text.replace('/sc', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format salah! Gunakan format:\nContoh: /sc @UsernamePembeli")
        return
    
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    packages = [
        ("💎 Natural Balance (30 Hari)", "sc_buy_natural"),
        ("⚡ Light VIP + Drone (30 Hari)", "sc_buy_light"),
        ("🛡️ Semi-Safe 14 Hari", "sc_buy_semisafe"),
        ("👑 Lifetime Safe Permanent", "sc_buy_lifetimesafe"),
        ("💥 Sultan One Hit 100% (30 Hari)", "sc_buy_sultan"),
        ("⚡ VIP Pro One Hit 80% (30 Hari)", "sc_buy_pro"),
        ("🔒 Semi-Private 14 Hari", "sc_buy_semiprivate"),
        ("🏆 Permanent Legend (Lifetime)", "sc_buy_permanent")
    ]
    for btn_text, cb_data in packages:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"{cb_data}|{target_buyer}"))
    
    bot.reply_to(
        message, 
        f"🎯 Target Pembeli: <b>{target_buyer}</b>\n👇 Silakan pilih paket script yang dibeli:", 
        reply_markup=markup, 
        parse_mode="HTML"
    )
TRANSLATIONS = {
    'id': {
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_testi': "🌟 Testimoni & Real-Time Bukti Order",
        'btn_riwayat': "📦 Cek Riwayat & Status Pesanan Saya",
        'btn_promo': "🎁 Klaim Kupon Member Baru",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Lengkap",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥\n*(Kategori: Custom Damage High-Tier & Fair Play Anti-Detect)*",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥\n*(Kategori: Sultan One Hit Instan & Dominasi Mutlak)*",
        'bonus_txt': "⚡ BONUS SPESIAL FREE ALL PACKAGES (TANPA BIAYA TAMBAHAN): \n🎁 Setiap pembelian paket apa saja, otomatis mendapatkan:\n  • Panel Server Lag Musuh (Global Ping Spikes)\n  • Drone View Eksklusif X1 sampai X10 (Ultra Wide View)\n\n📂 SILAKAN PILIH SCRIPT & PELAJARI DETAIL FITUR DI BAWAH INI:",
        'p1_normal': [
            ("🛒 Beli: Natural Balance (Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Hari) — Rp 120.000\n  └ 🎯 Fungsi: Script penyetara damage halus, aman anti-detect untuk tier Mythic."),
            ("🛒 Beli: Light VIP + Drone (Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Hari) — Rp 95.000\n  └ 🎯 Fungsi: Boost damage ringan + map vision luas (drone view)."),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Solusi cepat push rank akhir season."),
            ("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Safe (Permanent) — Rp 200.000\n  └ 🎯 Fungsi: Akses permanen seumur hidup + update gratis.")
        ],
        'p1_promo': [
            ("🛒 Natural Balance (Rp 110k - Hemat 10k)", "buy_natural", "• 💎 Natural Balance (30 Hari) — <s>Rp 120.000</s> <b>Rp 110.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Script penyetara damage halus, aman anti-detect untuk tier Mythic."),
            ("🛒 Light VIP + Drone (Rp 85k - Hemat 10k)", "buy_light", "• ⚡ Light VIP + Drone (30 Hari) — <s>Rp 95.000</s> <b>Rp 85.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Boost damage ringan + map vision luas (drone view)."),
            ("🛒 Semi-Safe 14 Hari (Rp 65k - Hemat 10k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Hari) — <s>Rp 75.000</s> <b>Rp 65.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Solusi cepat push rank akhir season."),
            ("🛒 Lifetime Safe (Rp 190k - Hemat 10k)", "buy_lifetimesafe", "• 👑 Lifetime Safe (Permanent) — <s>Rp 200.000</s> <b>Rp 190.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Akses permanen seumur hidup + update gratis.")
        ],
        'p2_normal': [
            ("🛒 Beli: Sultan One Hit 100% (Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% (30 Hari) — Rp 150.000\n  └ 🎯 Fungsi: One hit kill mutlak untuk dominasi total."),
            ("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% (30 Hari) — Rp 100.000\n  └ 🎯 Fungsi: Keseimbangan kekuatan dan keamanan akun."),
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Script privat eksklusif 2 minggu."),
            ("🛒 Beli: Permanent Legend (Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend (Lifetime) — Rp 250.000\n  └ 🎯 Fungsi: Paket elit permanen seumur hidup.")
        ],
        'p2_promo': [
            ("🛒 Sultan One Hit (Rp 140k - Hemat 10k)", "buy_sultan", "• 💥 Sultan One Hit 100% (30 Hari) — <s>Rp 150.000</s> <b>Rp 140.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: One hit kill mutlak untuk dominasi total."),
            ("🛒 VIP Pro One Hit (Rp 90k - Hemat 10k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% (30 Hari) — <s>Rp 100.000</s> <b>Rp 90.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Keseimbangan kekuatan dan keamanan akun."),
            ("🛒 Semi-Private 14 Hari (Rp 65k - Hemat 10k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Hari) — <s>Rp 75.000</s> <b>Rp 65.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Script privat eksklusif 2 minggu."),
            ("🛒 Permanent Legend (Rp 240k - Hemat 10k)", "buy_permanent", "• 🏆 Permanent Legend (Lifetime) — <s>Rp 250.000</s> <b>Rp 240.000</b> (Hemat Rp 10.000!)\n  └ 🎯 Fungsi: Paket elit permanen seumur hidup.")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2 (Sultan One Hit)",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': (
            "💳 SILAKAN PILIH METODE PEMBAYARAN DI BAWAH INI:\n\n"
            "1️⃣ QRIS (CROSS-BORDER / ALL E-WALLET):\n"
            "   ⚠️ <b>Mohon Maaf, QRIS Saat Ini Sedang Gangguan / Error!</b> Silakan gunakan metode transfer manual di bawah ya.\n\n"
            "2️⃣ TRANSFER MANUAL DANA / GOPAY (RECOMMENDED):\n"
            f"   • Nomor: <code>{INFO_DANA}</code>\n"
            "   • Atas Nama: PakelMlbb\n\n"
            "3️⃣ SAWERIA (Support Kartu & E-Wallet):\n"
            f"   • Link: {INFO_SAWERIA}\n"
        ),
        'confirm_instr': "🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\nSetelah sukses membayar via transfer manual, silakan kirim Screenshot Bukti Transfer ke bot ini untuk mendapatkan Resi Unik.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue & Pricing",
        'btn_testi': "🌟 Live Testimonials",
        'btn_riwayat': "📦 My Order History & Status",
        'btn_promo': "🎁 Claim Member Promo",
        'btn_cara_order': "❓ How to Order Guide",
        'btn_bayar': "💳 All Payment Methods",
        'btn_faq': "💡 FAQ / General Questions",
        'btn_konfirmasi': "✅ Check Status & Receipt",
        'btn_admin': "💬 Contact Official Admin",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS (FREE ALL PACKAGES): \n🎁 Get for FREE:\n  • Enemy Server Lag Panel\n  • Drone View X1 - X10 (Ultra Wide)\n\n📂 PACKAGE DETAILS & FUNCTIONS:",
        'p1_normal': [
            ("🛒 Buy: Natural Balance ($8 / Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Days) — $8 / Rp 120k"),
            ("🛒 Buy: Light VIP + Drone ($6 / Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Days) — $6 / Rp 95k"),
            ("🛒 Buy: Semi-Safe 14 Days ($5 / Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Days) — $5 / Rp 75k"),
            ("🛒 Buy: Lifetime Permanent ($13 / Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Permanent — $13 / Rp 200k")
        ],
        'p1_promo': [
            ("🛒 Buy: Natural Balance ($7.3)", "buy_natural", "• 💎 Natural Balance (30 Days) — <s>$8</s> <b>$7.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: Light VIP + Drone ($5.3)", "buy_light", "• ⚡ Light VIP + Drone (30 Days) — <s>$6</s> <b>$5.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: Semi-Safe 14 Days ($4.3)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Days) — <s>$5</s> <b>$4.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: Lifetime Permanent ($12.3)", "buy_lifetimesafe", "• 👑 Lifetime Permanent — <s>$13</s> <b>$12.3</b> (Promo Member Baru!)")
        ],
        'p2_normal': [
            ("🛒 Buy: Sultan One Hit 100% ($10 / Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% — $10 / Rp 150k"),
            ("🛒 Buy: VIP Pro One Hit 80% ($7 / Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% — $7 / Rp 100k"),
            ("🛒 Buy: Semi-Private 14 Days ($5 / Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Days) — $5 / Rp 75k"),
            ("🛒 Buy: Permanent Legend ($16 / Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend — $16 / Rp 250k")
        ],
        'p2_promo': [
            ("🛒 Buy: Sultan One Hit ($9.3)", "buy_sultan", "• 💥 Sultan One Hit 100% — <s>$10</s> <b>$9.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: VIP Pro One Hit ($6.3)", "buy_pro", "• ⚡ VIP Pro One Hit 80% — <s>$7</s> <b>$6.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: Semi-Private 14 Days ($4.3)", "buy_semiprivate", "• 🔒 Semi-Private (14 Days) — <s>$5</s> <b>$4.3</b> (Promo Member Baru!)"),
            ("🛒 Buy: Permanent Legend ($15.3)", "buy_permanent", "• 🏆 Permanent Legend — <s>$16</s> <b>$15.3</b> (Promo Member Baru!)")
        ],
        'next_1': "▶️ Next: Catalog Part 2 (One Hit)",
        'prev_2': "◀️ Back to Catalog Part 1",
        'inv_title': "🛒 AUTOMATED VIP ORDER INVOICE ({name}) 🧾",
        'pay_info': "💳 CHOOSE PAYMENT METHOD (QRIS is temporarily down, please use DANA/GoPay):",
        'confirm_instr': "🛡️ CONFIRMATION INSTRUCTION:\nSend transfer screenshot after payment.",
    }
}

def get_lang(user):
    code = getattr(user, 'language_code', 'en')
    if code:
        code = code.lower()
        if code.startswith('id'):
            return 'id'
    return 'en'

def get_back_markup(l):
    markup = types.InlineKeyboardMarkup()
    text = TRANSLATIONS.get(l, TRANSLATIONS['en'])['back']
    markup.add(types.InlineKeyboardButton(text, callback_data='menu_utama'))
    return markup
@bot.message_handler(commands=['bc', 'broadcast'])
def broadcast_message(message):
    save_user(message.chat.id)
    pesan_bc = message.text.replace('/bc', '').replace('/broadcast', '').strip()
    if not pesan_bc:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /bc Halo semua, ada promo script VIP baru nih!")
        return
    
    try:
        with open("users.txt", "r") as f:
            users = [line.strip() for line in f.read().splitlines() if line.strip()]
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Belum ada user tercatat.")
        return
        
    if not users:
        bot.reply_to(message, "⚠️ Database kosong.")
        return

    users = list(set(users))
    success = 0
    failed = 0
    
    bot.reply_to(message, f"🚀 Memulai Broadcast Umum ke {len(users)} member...")
    for chat_id in users:
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI PAKEL MLBBSTORE</b>\n\n{pesan_bc}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
            
    bot.send_message(message.chat.id, f"✅ Broadcast Umum Selesai!\n- Berhasil: {success}\n- Gagal: {failed}")

@bot.message_handler(commands=['bcs'])
def broadcast_buyers_only(message):
    pesan_bcs = message.text.replace('/bcs', '').strip()
    if not pesan_bcs:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /bcs Halo Kak, khusus member VIP ada update script terbaru nih!")
        return
    
    buyer_ids = set()
    try:
        with open("orders.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8:
                    chat_id = parts[0]
                    status = parts[7]
                    if status.strip() == "BERHASIL":
                        buyer_ids.add(chat_id.strip())
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Belum ada data pesanan sukses tersimpan.")
        return
        
    if not buyer_ids:
        bot.reply_to(message, "⚠️ Belum ada pembeli yang transaksinya di-ACC.")
        return

    success = 0
    failed = 0
    
    bot.reply_to(message, f"🚀 Memulai Broadcast Khusus VIP (Buyer) ke {len(buyer_ids)} pelanggan...")
    for chat_id in buyer_ids:
        try:
            bot.send_message(chat_id, f"💎 <b>INFO KHUSUS PELANGGAN SETIA PAKEL MLBBSTORE</b>\n\n{pesan_bcs}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            failed += 1
            
    bot.send_message(message.chat.id, f"✅ Broadcast Khusus VIP Selesai!\n- Berhasil: {success}\n- Gagal: {failed}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    save_user(message.chat.id)
    l = get_lang(user)
    t = TRANSLATIONS[l]
    greeting = get_time_greeting()
    
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
    
    if l == 'id':
        welcome_text = (
            f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n"
            "Pusat layanan script cheat Mobile Legends premium terpercaya, anti-detect kelas atas, server lag panel, & drone view paling stabil se-Indonesia.\n\n"
        )
        if not is_open:
            welcome_text += f"{store_msg}\n\n"
        welcome_text += "👇 Silakan pilih menu di bawah ini untuk mulai berbelanja:"
    else:
        welcome_text = f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n👇 Please select a menu below:"
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['riwayat', 'history'])
def cmd_riwayat(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    chat_id = message.chat.id
    
    get_latest_user_order_data(chat_id)
    
    orders = get_user_orders(chat_id)
    if not orders:
        text = f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n❌ Belum ada riwayat pesanan tercatat.\n💡 Silakan pilih paket di /katalog untuk melakukan pemesanan baru!"
    else:
        text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
        for idx, o in enumerate(orders[-5:], 1):
            if o['status'] == "BERHASIL":
                status_emoji = "✅ BERHASIL"
            elif o['status'] == "DITOLAK":
                status_emoji = "❌ DITOLAK"
            elif o['status'] == "EXPIRED":
                status_emoji = "⌛ EXPIRED (Waktu 15 Menit Habis)"
            else:
                status_emoji = "⏳ PENDING"
                
            text += (
                f"<b>{idx}. {o['paket']}</b>\n"
                f"   • Harga: {o['harga']}\n"
                f"   • No Resi: <code>{o['resi']}</code>\n"
                f"   • Waktu: {o['hari']}, {o['tanggal']} ({o['jam']})\n"
                f"   • Status: {status_emoji}\n\n"
            )
        text += "💡 <i>Kirim bukti transfer jika belum dikonfirmasi admin!</i>"

    bot.reply_to(message, text, reply_markup=get_back_markup(l), parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    if l == 'id':
        text = f"🔍 CEK STATUS RESI PEMBELIAN VIP (Kak {user.first_name})\n\nKirimkan Nomor Resi Unik atau screenshot bukti transfer ke sini.\n\n💬 Admin: {ADMIN_USERNAME}"
    else:
        text = f"🔍 CHECK RECEIPT STATUS ({user.first_name})\n\nSend receipt number or payment proof."
    bot.reply_to(message, text, disable_web_page_preview=True)

@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    
    coupon_status = get_user_coupon_status(message.chat.id)
    items_to_use = t['p1_promo'] if coupon_status == "AVAILABLE" else t['p1_normal']
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn_text, callback_val, _ in items_to_use:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
    markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
    markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

    katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([desc for _, _, desc in items_to_use])
    if coupon_status == "AVAILABLE":
        katalog_text += "\n\n🎁 <b>INFO PROMO:</b> Anda memiliki hak potong harga spesial member baru otomatis di katalog ini!"
        
    bot.send_message(message.chat.id, katalog_text, reply_markup=markup, parse_mode="HTML")
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    save_user(call.message.chat.id)
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    greeting = get_time_greeting()

    if call.data.startswith('acc_') or call.data.startswith('tolak_') or call.data.startswith('acc|') or call.data.startswith('tolak|'):
        try:
            sep = '|' if '|' in call.data else '_'
            parts = call.data.split(sep)
            action = parts[0].replace('_', '')
            target_user_id = parts[1]
            resi_code = parts[2]

            original_text = call.message.caption or call.message.text or ""

            if action == 'acc':
                update_order_status_by_resi(resi_code, "BERHASIL")
                
                new_admin_text = original_text + "\n\n<b>STATUS: ✅ TELAH DI-ACC OLEH ADMIN (Kupon Resmi Hangus)</b>"
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)

                detail_paket = "VIP Package"
                detail_harga = "Rp 100.000"
                waktu_beli = datetime.now(timezone(timedelta(hours=7))).strftime('%d-%m-%Y %H:%M:%S WIB')
                try:
                    with open("orders.txt", "r") as f:
                        for line in f:
                            p = line.strip().split('|')
                            if len(p) >= 8 and p[6].strip() == resi_code.strip():
                                detail_paket = p[4]
                                detail_harga = p[5]
                                waktu_beli = f"{p[1]}, {p[3]}"
                                break
                except Exception:
                    pass

                buyer_msg = (
                    "🎉 <b>PEMBAYARAN ANDA TELAH DI-ACC ADMIN!</b> 🎉\n\n"
                    f"🔑 No Resi: <code>{resi_code}</code>\n"
                    "Status transaksi Anda sudah <b>BERHASIL</b> di sistem. Hak promo member baru Anda telah terpakai.\n\n"
                    "📋 <b>SILAKAN SALIN FORMAT PESAN DI BAWAH INI DAN KIRIM KE ADMIN:</b>\n"
                    "👇 (Cukup ketuk/klik teks di bawah untuk menyalin otomatis)"
                )
                bot.send_message(chat_id=target_user_id, text=buyer_msg, parse_mode="HTML")
                
                template_chat_admin = (
                    "🔥 KONFIRMASI KLAIM SCRIPT VIP 🔥\n"
                    f"📦 Paket: {detail_paket}\n"
                    f"💵 Harga: {detail_harga}\n"
                    f"🔑 No Resi: {resi_code}\n"
                    f"⏱️ Waktu Order: {waktu_beli}\n"
                    "Status: Lunas & Sudah di-ACC Bot.\n"
                    "Mohon kirimkan link/file script-nya ya Kak. Terima kasih! 🙏"
                )
                bot.send_message(chat_id=target_user_id, text=f"<code>{template_chat_admin}</code>", parse_mode="HTML")
                
                bot.answer_callback_query(call.id, text="Pembayaran di-ACC, kupon hangus permanen!")

            elif action == 'tolak':
                update_order_status_by_resi(resi_code, "DITOLAK")

                new_admin_text = original_text + "\n\n<b>STATUS: ❌ DITOLAK OLEH ADMIN (Kupon Dikembalikan)</b>"
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)

                buyer_msg = (
                    "❌ <b> MOHON MAAF, PEMBAYARAN DITOLAK </b> ❌\n\n"
                    f"🔑 No Resi: <code>{resi_code}</code>\n"
                    "Bukti pembayaran Anda tidak valid atau mutasi tidak ditemukan.\n"
                    "💡 <i>Tenang Kak, hak diskon/promo member baru Anda telah dikembalikan dan bisa dipakai kembali untuk order ulang!</i>\n\n"
                    f"💬 Silakan hubungi Admin resmi untuk konfirmasi lebih lanjut: {ADMIN_USERNAME}"
                )
                bot.send_message(chat_id=target_user_id, text=buyer_msg, parse_mode="HTML", disable_web_page_preview=True)
                bot.answer_callback_query(call.id, text="Pembayaran ditolak & kupon dikembalikan aktif!")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Error: {e}", show_alert=True)
        return

    if call.data.startswith('sc_buy_'):
        try:
            data_split = call.data.split('|')
            action = data_split[0]
            buyer_name = data_split[1]
            
            paket_map = {
                'sc_buy_natural': ("Natural Balance (30 Hari)", "Rp 120.000"),
                'sc_buy_light': ("Light VIP + Drone (30 Hari)", "Rp 95.000"),
                'sc_buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000"),
                'sc_buy_lifetimesafe': ("Lifetime Safe Permanent", "Rp 200.000"),
                'sc_buy_sultan': ("Sultan One Hit 100% (30 Hari)", "Rp 150.000"),
                'sc_buy_pro': ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000"),
                'sc_buy_semiprivate': ("Semi-Private 14 Hari", "Rp 75.000"),
                'sc_buy_permanent': ("Permanent Legend (Lifetime)", "Rp 250.000")
            }
            paket_nama, harga = paket_map.get(action, ("VIP Package", "Rp 100.000"))
            menit_lalu = random.randint(1, 5)
            
            current_hour = datetime.now(timezone(timedelta(hours=7))).hour
            waktu_ket = "pagi ini" if 4 <= current_hour < 11 else ("siang ini" if 11 <= current_hour < 15 else ("sore ini" if 15 <= current_hour < 18 else "malam ini"))
                
            post_text = (
                "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                f"✅ Buyer ID: {buyer_name}\n"
                f"📦 Item Purchased: {paket_nama}\n"
                f"💵 Price: {harga}\n"
                f"⏱️ Time: {menit_lalu} menit yang lalu ({waktu_ket})\n"
                f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
                "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
                f"🤖 Bot Store: @{bot.get_me().username}"
            )
            bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text, message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"✅ <b>BERHASIL DIKIRIM KE GRUP UTAMA!</b>\n\n• Pembeli: {buyer_name}\n• Paket: {paket_nama} ({harga})", parse_mode="HTML")
            bot.answer_callback_query(call.id, text="Testimoni sukses terkirim ke grup utama!")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
        return

    if call.data == 'menu_utama':
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
        text = f"🔥 {greeting}! Silakan pilih menu utama Pakel MlbbStore:\n\n" if l == 'id' else f"🔥 {greeting}! Main Menu:\n\n"
        if not is_open and l == 'id':
            text += f"{store_msg}\n\n"
            
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_testi':
        fake_data = generate_fake_testimonials_list()
        testi_text = f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n\n{fake_data}💡 Toko 100% amanah & terpercaya! 🚀" if l == 'id' else f"🌟 LIVE TESTIMONIALS\n\n{fake_data}"
        
        markup_testi = types.InlineKeyboardMarkup(row_width=1)
        markup_testi.add(types.InlineKeyboardButton("🔄 Refresh Testimoni Terbaru", callback_data='menu_testi'))
        markup_testi.add(types.InlineKeyboardButton("🌟 Lihat Ratusan Testi di Channel", url=CHANNEL_TESTI_LINK))
        markup_testi.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text, reply_markup=markup_testi, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Testimoni diperbarui!")

    elif call.data == 'menu_riwayat':
        get_latest_user_order_data(chat_id)
        orders = get_user_orders(chat_id)
        if not orders:
            riw_text = f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n❌ Belum ada riwayat pesanan tercatat.\n💡 Silakan pilih paket di katalog untuk membuat pesanan baru!"
        else:
            riw_text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
            for idx, o in enumerate(orders[-5:], 1):
                if o['status'] == "BERHASIL":
                    status_emoji = "✅ BERHASIL"
                elif o['status'] == "DITOLAK":
                    status_emoji = "❌ DITOLAK"
                elif o['status'] == "EXPIRED":
                    status_emoji = "⌛ EXPIRED (Waktu 15 Menit Habis)"
                else:
                    status_emoji = "⏳ PENDING"
                    
                riw_text += (
                    f"<b>{idx}. {o['paket']}</b>\n"
                    f"   • Harga: {o['harga']}\n"
                    f"   • No Resi: <code>{o['resi']}</code>\n"
                    f"   • Waktu: {o['hari']}, {o['tanggal']} ({o['jam']})\n"
                    f"   • Status: {status_emoji}\n\n"
                )
            riw_text += "💡 <i>Kirim bukti transfer jika belum dikonfirmasi admin!</i>"
            
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=riw_text, reply_markup=get_back_markup(l), parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Riwayat dimuat!")

    elif call.data == 'menu_promo':
        status_c = get_user_coupon_status(chat_id)
        if status_c == "AVAILABLE":
            promo_text = f"🎁 PROMO MEMBER BARU (Kak {user.first_name})\n\n✨ Status Kupon: <b>AKTIF & TERSEDIA!</b>\n💰 Nikmati potongan harga otomatis langsung saat Anda memilih paket di menu Katalog VIP."
        elif status_c == "PENDING":
            promo_text = f"🎁 PROMO MEMBER BARU (Kak {user.first_name})\n\n⏳ Status Kupon: <b>DIKUNCI SEMENTARA</b>\nSedang menunggu verifikasi bukti pembayaran oleh admin."
        else:
            promo_text = f"🎁 PROMO MEMBER BARU (Kak {user.first_name})\n\n❌ Status Kupon: <b>SUDAH TERPAKAI / HABIS</b>\nTerima kasih telah menggunakan promo member baru di Pakel MlbbStore!"
            
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, reply_markup=get_back_markup(l), parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        faq_text = "💡 FAQ PAKEL MLBBSTORE\n\n❓ Aman dari banned? 💬 A: Sangat aman, enkripsi anti-detect tinggi."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=faq_text, reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        coupon_status = get_user_coupon_status(chat_id)
        items_to_use = t['p1_promo'] if coupon_status == "AVAILABLE" else t['p1_normal']
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in items_to_use:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([desc for _, _, desc in items_to_use])
        if coupon_status == "AVAILABLE":
            katalog_text += "\n\n🎁 <b>INFO PROMO:</b> Harga coret di atas adalah potongan spesial member baru otomatis!"
            
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'katalog_part2':
        coupon_status = get_user_coupon_status(chat_id)
        items_to_use = t['p2_promo'] if coupon_status == "AVAILABLE" else t['p2_normal']
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in items_to_use:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['prev_2'], callback_data='katalog_part1'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_2'].format(name=user.first_name)}\n\n" + "\n\n".join([desc for _, _, desc in items_to_use])
        if coupon_status == "AVAILABLE":
            katalog_text += "\n\n🎁 <b>INFO PROMO:</b> Harga coret di atas adalah potongan spesial member baru otomatis!"
            
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        coupon_status = get_user_coupon_status(chat_id)
        is_promo_used = (coupon_status == "AVAILABLE")
        
        all_items_normal = t['p1_normal'] + t['p2_normal']
        all_items_promo = t['p1_promo'] + t['p2_promo']
        
        paket_nama = "VIP Package"
        harga_paket = "Rp 100.000"
        
        search_list = all_items_promo if is_promo_used else all_items_normal
        for btn_txt, cb_val, desc_val in search_list:
            if cb_val == call.data:
                paket_nama = btn_txt.replace("🛒 Beli: ", "").replace("🛒 ", "").split(" (Rp")[0]
                if "— " in desc_val:
                    harga_paket = desc_val.split("— ")[1].split("\n")[0]
                break
                
        random_serial = random.randint(10000, 99999)
        resi_unik = f"PKL-MLBB-{random_serial}"
        
        save_order(chat_id, paket_nama, harga_paket, resi_unik)
        
        if is_promo_used:
            set_user_coupon_status(chat_id, "PENDING")
        
        invoice_text = (
            f"{t['inv_title'].format(name=user.first_name)}\n\n"
            f"📦 Paket Dipilih: {paket_nama}\n"
            f"💵 Harga: {harga_paket}"
        )
        if is_promo_used:
            invoice_text += " <i>(Sudah termasuk Potongan Promo Member Baru ✨)</i>"
        invoice_text += (
            f"\n🔢 Nomor Resi Unik: <code>{resi_unik}</code>\n"
            f"⏱️ Batas Waktu: 15 Menit (Sesi Timeout Aktif)\n\n"
            f"{t['pay_info']}\n\n"
            f"{t['confirm_instr']}\n"
            f"👉 Admin: {ADMIN_USERNAME}"
        )
        
        markup_inv = types.InlineKeyboardMarkup(row_width=1)
        markup_inv.add(types.InlineKeyboardButton("📦 Cek Riwayat Pesanan Saya", callback_data='menu_riwayat'))
        markup_inv.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
            
        bot.send_message(chat_id, invoice_text, reply_markup=markup_inv, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Invoice & Riwayat Tercatat Otomatis!")

    elif call.data == 'menu_cara_order':
        text = "❓ PANDUAN CARA ORDER\n1. Pilih paket di katalog.\n2. Klik beli untuk dapat nomor resi.\n3. Transfer ke DANA/GoPay & kirim bukti transfer dalam 15 menit."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        markup_bayar = types.InlineKeyboardMarkup(row_width=1)
        markup_bayar.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        text = f"💳 METODE PEMBAYARAN\n\n1. QRIS: ⚠️ <b>Sedang Gangguan/Error</b>\n2. DANA / GoPay: <code>{INFO_DANA}</code> (a.n. PakelMlbb)\n3. Saweria: {INFO_SAWERIA}"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup_bayar, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        rs = random.randint(10000, 99999)
        text = f"✅ KONFIRMASI PEMBAYARAN\n\nKirim screenshot bukti transfer Anda dengan menyertakan Nomor Resi (misal: PKL-MLBB-{rs}) ke admin sebelum 15 menit."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    save_user(message.chat.id)
    user = message.from_user
    
    resi_unik, order_status = get_latest_user_order_data(message.chat.id)
    
    if order_status == "EXPIRED":
        bot.reply_to(message, "❌ <b>WAKTU KONFIRMASI HABIS (TIMEOUT 15 MENIT)!</b>\n\nMohon maaf Kak, batas waktu pengiriman bukti transfer untuk pesanan ini sudah lewat dari 15 menit sehingga pesanan otomatis kedaluwarsa.\n\n💡 Hak diskon member baru Anda telah dikembalikan. Silakan buat pesanan baru melalui /katalog ya! 🙏", parse_mode="HTML")
        return

    user_caption = message.caption if message.caption else "Tidak ada pesan"
    
    WIB = timezone(timedelta(hours=7))
    now = datetime.now(WIB)
    
    res_to_buyer = (
        "✅ BUKTI PEMBAYARAN BERHASIL DIUNGGAH!\n"
        f"Terima kasih Kak {user.first_name} 🙏\n\n"
        f"🛡️ No Resi Unik: {resi_unik}\n"
        f"⏱️ Waktu: {now.strftime('%d-%m-%Y %H:%M:%S WIB')}\n\n"
        f"📋 Silakan tunggu verifikasi dari Admin: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, res_to_buyer, disable_web_page_preview=True)
    
    try:
        caption_admin = (
            "🚨 <b>ADA BUKTI TRANSFER MASUK!</b> 🚨\n\n"
            f"👤 Dari User: @{user.username if user.username else user.first_name} (ID: <code>{user.id}</code>)\n"
            f"✉️ Pesan Dari User: \"{user_caption}\"\n"
            f"⏱️ Waktu: {now.strftime('%d-%m-%Y %H:%M:%S WIB')}\n"
            f"🔑 No Resi Unik: {resi_unik}\n\n"
            "👇 <i>Silakan cek mutasi e-wallet, lalu klik tombol di bawah untuk ACC atau Tolak!</i>"
        )
        
        markup_admin_action = types.InlineKeyboardMarkup(row_width=2)
        markup_admin_action.add(
            types.InlineKeyboardButton("✅ ACC", callback_data=f"acc|{user.id}|{resi_unik}"),
            types.InlineKeyboardButton("❌ TOLAK", callback_data=f"tolak|{user.id}|{resi_unik}")
        )
        
        bot.send_photo(
            chat_id=GROUP_PAY_ID, 
            photo=message.photo[-1].file_id, 
            caption=caption_admin, 
            message_thread_id=GROUP_PAY_TOPIC_ID, 
            parse_mode="HTML", 
            reply_markup=markup_admin_action
        )
    except Exception as e:
        print(f"[FORWARD PHOTO ERROR]: {e}")

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    if message.chat.type != 'private':
        return

    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    txt = message.text.lower()
    
    if any(w in txt for w in ['price', 'harga', 'list', 'menu', 'catalog', 'katalog']):
        res_msg = "💎 Ketik /start untuk membuka Katalog VIP!"
    elif any(w in txt for w in ['pay', 'bayar', 'dana', 'gopay', 'saweria', 'qris', 'testi', 'riwayat']):
        res_msg = "🌟 Cek menu /start untuk melihat metode pembayaran, riwayat pesanan, & katalog lengkap!"
    else:
        res_msg = f"Halo {user.first_name}! Ketik /start untuk membuka menu utama atau hubungi {ADMIN_USERNAME}."
        
    bot.reply_to(message, res_msg, disable_web_page_preview=True)

print("[INFO] Pakel MlbbStore Master Ultimate Edition Berhasil Dijalankan...")
bot.infinity_polling()