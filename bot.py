import telebot
from telebot import types
import random
import time
import threading
from datetime import datetime, timezone, timedelta

# Token bot lu yang aktif dan siap tempur
TOKEN = '8637403539:AAFyKck7U8POV3hzSw9UcF_sDDp0d_hKat0'
bot = telebot.TeleBot(TOKEN)

# Identitas Toko Resmi & Link Grup Beserta ID Topik Khusus Testimoni
ADMIN_USERNAME = "@PakelMlbbOfficial"
ADMIN_LINK = "https://t.me/PakelMlbbOfficial"
GROUP_CHAT_ID = "@PakelMlbb"  # Username grup utama lu
GROUP_TOPIC_ID = 368          # ID Topik khusus di dalam grup untuk auto-post testi

# Informasi Nomor Pembayaran Resmi (Tanpa QRIS)
INFO_DANA = "089526466512"
INFO_GOPAY = "089526466512"
INFO_SAWERIA = "https://saweria.co/PakelMlbb"

# ==================== FUNGSI DATABASE USER & BROADCAST ====================
def save_user(chat_id):
    try:
        chat_id_str = str(chat_id).strip()
        if not chat_id_str:
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

# ==================== WAKTU & SAPAAN OTOMATIS ====================
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

# ==================== LIST NAMA TELEGRAM SENSOR BINTANG ====================
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
        "@Farhan***", "@Fauzi***", "@Febri***", "@Firman",
        "@Fuat***", "@Gani***", "@Gerry***", "@Hadi***",
        "@R.Zky***", "@Alvin.ID***", "@Dimas.Xyz***", "@Reza.Gaming***",
        "@Bayu.Pratama***", "@Farel.Official***", "@Yoga.Ganz***", "@Dicky.Dev***",
        "@Surya.ID***", "@Rama.ID***", "@Gilang.Mlg***", "@Bagas.X***",
        "@Arif.Prat***", "@Dani.Gmr***", "@Hendra.Sultan***", "@Rian.Wicak***",
        "@Aldi.Pro***", "@Bintang.Gz***", "@Candra.07***", "@Dika.Wahyudi***",
        "@Fajar.Sltn***", "@Galih.Xtrem***", "@Iqbal.Farel***", "@Joko.Santoso***",
        "@Kevin.Bagas***", "@Lukman.Rizky***", "@Maulana.Dwi***", "@Naufal.Akbar***",
        "@Pratama.Putra***", "@Rafli.Maulana***", "@Satria.angga***", "@Tegar.Aditya***",
        "@Vian.Saputra***", "@Wahyu.Hidayat***", "@Yuda.Kurniawan***", "@Zaki.Mubarok***",
        "@Rizal_Ganz***", "@Maulana_ID***", "@Fikri_Ramadhan***", "@Ilham_Saputra***",
        "@Rezky_Pratama***", "@Rizky_Maulana***", "@Fauzan_Azima***", "@Zidan_Alfarizi***",
        "@Rafi_Ahmad***", "@Zaki_Mubarok***", "@Fathan_Haikal***", "@Rifki_Ananda***",
        "@Aditya_Pratama***", "@Bayu_Pamungkas***", "@Yoga_Prasetyo***", "@Dimas_Mahendra***",
        "@R_Zky2026***", "@Alvinn123***", "@Dimas777***", "@Reza888***", 
        "@Bayu555***", "@Farel444***", "@Yoga333***", "@Dicky222***", 
        "@Surya111***", "@Rama999***", "@Gilang000***", "@Bagas777***"
    ]
    return random.choice(list_nama_tele)

# ==================== GENERATOR TESTIMONI LIVE (8 PAKET) ====================
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
# ==================== BACKGROUND WORKER (AUTO-POST JEDA ACAK) ====================
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

# ==================== COMMAND PUSH TESTI INSTAN ====================
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
        bot.reply_to(message, "✅ Berhasil! Testimoni real-time baru saja dikirim ke topik grup.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal mengirim testimoni: {e}")

# ==================== FITUR INTERAKTIF MANUAL /SC (8 PAKET LENGKAP) ====================
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
# ==================== MASTER GLOBAL TRANSLATION ENGINE ====================
TRANSLATIONS = {
    'id': {
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_testi': "🌟 Testimoni & Real-Time Bukti Order",
        'btn_promo': "🎁 Klaim Promo Member Baru",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Lengkap",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥\n*(Kategori: Custom Damage High-Tier & Fair Play Anti-Detect)*",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥\n*(Kategori: Sultan One Hit Instan & Dominasi Mutlak)*",
        'bonus_txt': "⚡ BONUS SPESIAL FREE ALL PACKAGES (TANPA BIAYA TAMBAHAN): \n🎁 Setiap pembelian paket apa saja, otomatis mendapatkan:\n  • Panel Server Lag Musuh (Global Ping Spikes)\n  • Drone View Eksklusif X1 sampai X10 (Ultra Wide View)\n\n📂 SILAKAN PILIH SCRIPT & PELAJARI DETAIL FITUR DI BAWAH INI:",
        'p1': [
            ("🛒 Beli: Natural Balance (Rp 120k)", "buy_natural", 
             "• 💎 Natural Balance (30 Hari) — Rp 120.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Script dirancang khusus untuk menyetarakan damage hero secara halus, natural, dan sangat stabil tanpa menimbulkan kecurigaan sistem ban. Sangat cocok bagi player yang ingin mendominasi ranked match secara konsisten, tidak mencolok, namun tetap mematikan di setiap teamfight. Aman untuk akun utama tier Mythic ke atas."),
            
            ("🛒 Beli: Light VIP + Drone (Rp 95k)", "buy_light", 
             "• ⚡ Light VIP + Drone (30 Hari) — Rp 95.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Memberikan boost damage ringan yang presisi dipadukan dengan fitur luas pandang map (drone view). Memungkinkan Anda melihat posisi musuh dari kejauhan sebelum mereka menyergap, mengamankan objective lord/turtle dengan mudah, serta memenangkan pertempuran kecil di early game tanpa terdeteksi sistem keamanan game."),
            
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", "buy_semisafe", 
             "• 🛡️ Semi-Safe (14 Hari) — Rp 75.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Solusi cepat dan bertenaga untuk durasi singkat bagi Anda yang sedang terburu-buru mengejar target star/winrate di akhir season. Performa script digenjot secara maksimal untuk memberikan keunggulan instan dalam duel 1vs1 maupun war besar."),
            
            ("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", "buy_lifetimesafe", 
             "• 👑 Lifetime Safe (Permanent) — Rp 200.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Investasi jangka panjang terbaik! Akses permanen selamanya dengan enkripsi tingkat tinggi berlapis anti-detect system. Dapatkan pembaruan (update) otomatis setiap patch patch terbaru tanpa perlu bayar ulang. Kualitas sultan, performa stabil seumur hidup.")
        ],
        'p2': [
            ("🛒 Beli: Sultan One Hit 100% (Rp 150k)", "buy_sultan", 
             "• 💥 Sultan One Hit 100% (30 Hari) — Rp 150.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Kasta tertinggi script mematikan! Memberikan efek eliminasi instan (one hit kill) secara mutlak pada monster, minion, dan hero lawan. Musuh dijamin tidak akan sempat menggunakan skill atau spell ketika berhadapan dengan Anda. Sensasi dominasi total tanpa tanding di setiap pertandingan."),
            
            ("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", "buy_pro", 
             "• ⚡ VIP Pro One Hit 80% (30 Hari) — Rp 100.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Keseimbangan sempurna antara kekuatan destruktif dan keamanan akun. Power one hit sebesar 80% disetel agar tetap terlihat natural oleh sistem laporan musuh, namun sangat mematikan saat Anda melakukan eksekusi di mode ranked kompetitif."),
            
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", "buy_semiprivate", 
             "• 🔒 Semi-Private (14 Hari) — Rp 75.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Script privat eksklusif dengan distribusi terbatas untuk menjaga kerahasiaan performa. Durasi 2 minggu penuh untuk memaksimalkan push rank tanpa hambatan berarti."),
            
            ("🛒 Beli: Permanent Legend (Rp 250k)", "buy_permanent", 
             "• 🏆 Permanent Legend (Lifetime) — Rp 250.000\n"
             "  └ 🎯 Fungsi & Keunggulan: Paket paling elit di Pakel MlbbStore. Status permanen seumur hidup dengan prioritas update script tercepat di setiap patch baru. Kebebasan mutlak menguasai permainan selamanya.")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2 (Sultan One Hit)",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': (
            "💳 SILAKAN PILIH METODE TRANSFER DI BAWAH INI:\n\n"
            "1️⃣ TRANSFER DANA / GOPAY:\n"
            f"   • Nomor DANA: {INFO_DANA}\n"
            f"   • Nomor GoPay: {INFO_GOPAY}\n\n"
            "2️⃣ SAWERIA (Support Kartu, QRIS, E-Wallet):\n"
            f"   • Link Pembayaran: {INFO_SAWERIA}\n"
        ),
        'confirm_instr': "🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\nSetelah sukses melakukan pembayaran via metode apapun, silakan kirim Screenshot Bukti Transfer ke bot ini untuk mendapatkan Nomor Resi Unik Anda.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue & Pricing",
        'btn_testi': "🌟 Live Testimonials",
        'btn_promo': "🎁 Claim New Member Promo",
        'btn_cara_order': "❓ How to Order Guide",
        'btn_bayar': "💳 All Payment Methods",
        'btn_faq': "💡 FAQ / General Questions",
        'btn_konfirmasi': "✅ Check Status & Receipt",
        'btn_admin': "💬 Contact Official Admin",
        'back': "⬅️ Back to Main Menu",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS (FREE ALL PACKAGES): \n🎁 Get for FREE:\n  • Enemy Server Lag Panel\n  • Drone View X1 - X10 (Ultra Wide)\n\n📂 PACKAGE DETAILS & FUNCTIONS:",
        'p1': [
            ("🛒 Buy: Natural Balance ($8 / Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Days) — $8 / Rp 120k\n  └ 🎯 Function: Balanced & smooth damage adjustment without suspicion."),
            ("🛒 Buy: Light VIP + Drone ($6 / Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Days) — $6 / Rp 95k\n  └ 🎯 Function: Precision damage boost + wide map vision bonus."),
            ("🛒 Buy: Semi-Safe 14 Days ($5 / Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Days) — $5 / Rp 75k\n  └ 🎯 Function: Short duration optimal boost for rank push."),
            ("🛒 Buy: Lifetime Permanent ($13 / Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Permanent — $13 / Rp 200k\n  └ 🎯 Function: Permanent access with high anti-detect protection & free updates.")
        ],
        'p2': [
            ("🛒 Buy: Sultan One Hit 100% ($10 / Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% — $10 / Rp 150k\n  └ 🎯 Function: Instant kill effect for total absolute domination."),
            ("🛒 Buy: VIP Pro One Hit 80% ($7 / Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% — $7 / Rp 100k\n  └ 🎯 Function: Stable pro one hit power for ranked mode."),
            ("🛒 Buy: Semi-Private 14 Days ($5 / Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Days) — $5 / Rp 75k\n  └ 🎯 Function: Exclusive 2-week private script."),
            ("🛒 Buy: Permanent Legend ($16 / Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend — $16 / Rp 250k\n  └ 🎯 Function: Lifetime status with free updates forever.")
        ],
        'next_1': "▶️ Next: Catalog Part 2 (One Hit)",
        'prev_2': "◀️ Back to Catalog Part 1",
        'inv_title': "🛒 AUTOMATED VIP ORDER INVOICE ({name}) 🧾",
        'pay_info': "💳 CHOOSE YOUR PAYMENT METHOD:\n1. DANA / GoPay\n2. Saweria",
        'confirm_instr': "🛡️ CONFIRMATION INSTRUCTION:\nAfter successful payment, send your Transfer Proof Screenshot to this bot.",
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

# ==================== FITUR BROADCAST ADMIN (KIRIM KE DM SEMUA MEMBER) ====================
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
        bot.reply_to(message, "⚠️ Belum ada user yang tercatat di database (users.txt kosong).")
        return
        
    if not users:
        bot.reply_to(message, "⚠️ Database kosong, belum ada user yang berinteraksi.")
        return

    users = list(set(users))
    
    success = 0
    failed = 0
    
    bot.reply_to(message, f"🚀 Memulai broadcast pengumuman ke {len(users)} member via DM...")
    
    for chat_id in users:
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI PAKEL MLBBSTORE</b>\n\n{pesan_bc}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception as e:
            print(f"[BROADCAST FAIL TO {chat_id}]: {e}")
            failed += 1
            
    bot.send_message(message.chat.id, f"✅ Broadcast Selesai!\n- Berhasil dikirim ke DM: {success} member\n- Gagal/Diblokir: {failed} member")

# ==================== HANDLER UTAMA BOT ====================
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
        types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
        types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
        types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
        types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
        types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
        types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
    )
    
    if l == 'id':
        welcome_text = (
            f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n"
            "Pusat layanan script cheat Mobile Legends premium terpercaya, anti-detect kelas atas, server lag panel, & drone view paling stabil se-Indonesia.\n\n"
            "👇 Silakan pilih menu di bawah ini untuk mulai berbelanja:"
        )
    else:
        welcome_text = (
            f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n"
            "The ultimate trusted provider for high-tier MLBB scripts, anti-detect protection, & premium features.\n\n"
            "👇 Please select a menu below to start:"
        )
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    if l == 'id':
        text = f"🔍 CEK STATUS RESI PEMBELIAN VIP (Kak {user.first_name})\n\nKirimkan Nomor Resi Unik (PKL-MLBB-12345) atau screenshot bukti transfer Anda ke sini.\n\n💬 Admin Utama: {ADMIN_USERNAME}"
    else:
        text = f"🔍 CHECK RECEIPT STATUS ({user.first_name})\n\nPlease send your Unique Receipt Number or payment proof.\n\n💬 Admin: {ADMIN_USERNAME}"
    bot.reply_to(message, text, disable_web_page_preview=True)

@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    for btn_text, callback_val, _ in t['p1']:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
    markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
    markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

    katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([desc for _, _, desc in t['p1']])
    bot.send_message(message.chat.id, katalog_text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    save_user(call.message.chat.id)
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    greeting = get_time_greeting()

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
            if 4 <= current_hour < 11:
                waktu_ket = "pagi ini"
            elif 11 <= current_hour < 15:
                waktu_ket = "siang ini"
            elif 15 <= current_hour < 18:
                waktu_ket = "sore ini"
            else:
                waktu_ket = "malam ini"
                
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
            
            bot.send_message(
                chat_id=GROUP_CHAT_ID, 
                text=post_text, 
                message_thread_id=GROUP_TOPIC_ID, 
                disable_web_page_preview=True
            )
            
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"✅ **BERHASIL DIKIRIM KE GRUP!**\n\n• Pembeli: {buyer_name}\n• Paket: {paket_nama} ({harga})"
            )
            bot.answer_callback_query(call.id, text="Testimoni sukses terkirim ke grup!")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
        return

    if call.data == 'menu_utama':
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
            types.InlineKeyboardButton(t['btn_testi'], callback_data='menu_testi'),
            types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
            types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
            types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
            types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
            types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
            types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK)
        )
        text = f"🔥 {greeting}! Silakan pilih menu utama Pakel MlbbStore:" if l == 'id' else f"🔥 {greeting}! Main Menu:"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)
        except Exception:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_testi':
        fake_data = generate_fake_testimonials_list()
        if l == 'id':
            testi_text = (
                f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n"
                "Berikut adalah daftar pembeli yang baru saja sukses melakukan checkout script VIP di Pakel MlbbStore secara real-time:\n\n"
                f"{fake_data}"
                "💡 Catatan: Data di atas diperbarui secara otomatis setiap kali Anda membuka menu testimoni. Toko terpercaya & 100% amanah! 🚀"
            )
        else:
            testi_text = f"🌟 LIVE TESTIMONIALS\n\n{fake_data}"
        
        markup_testi = types.InlineKeyboardMarkup(row_width=1)
        markup_testi.add(types.InlineKeyboardButton("🔄 Refresh Testimoni Terbaru", callback_data='menu_testi'))
        markup_testi.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text, reply_markup=markup_testi, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Testimoni berhasil diperbarui!")

    elif call.data == 'menu_promo':
        if l == 'id':
            promo_text = f"🎁 PROMO EKSKLUSIF PELANGGAN BARU (Kak {user.first_name})\n\n🎟️ KODE KUPON: WELCOMEPAKEL\n💰 Nikmati potongan harga spesial untuk pembelian paket VIP pertama Anda hari ini! Klaim sekarang sebelum kuota promo habis."
        else:
            promo_text = f"🎁 NEW MEMBER PROMO ({user.first_name})\n\n🎟️ COUPON: WELCOMEPAKEL\n💰 Special discount for your first VIP package purchase!"
        
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        if l == 'id':
            faq_text = (
                "💡 FAQ / PERTANYAAN UMUM PAKEL MLBBSTORE\n\n"
                "❓ Q: Apakah script ini aman dari banned akun utama?\n"
                "💬 A: Sangat aman! Setiap script kami dilengkapi enkripsi anti-detect tingkat tinggi dan sistem bypass pengaman game terbaru.\n\n"
                "❓ Q: Bagaimana cara instalasi filenya setelah dibeli?\n"
                "💬 A: File script lengkap beserta tutorial video panduan pemasangan yang sangat mudah akan langsung dikirimkan oleh Admin setelah pembayaran dikonfirmasi.\n\n"
                "❓ Q: Apakah ada garansi jika patch game berubah?\n"
                "💬 A: Tentu! Setiap pembelian paket mendapatkan update gratis sesuai masa aktif paket Anda."
            )
        else:
            faq_text = (
                "💡 FAQ\n\n"
                "❓ Safe from ban? 💬 A: High-level anti-detect encryption.\n"
                "❓ How to install? 💬 A: Script & tutorial sent by admin after payment."
            )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=faq_text, reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in t['p1']:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([desc for _, _, desc in t['p1']])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'katalog_part2':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in t['p2']:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['prev_2'], callback_data='katalog_part1'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        katalog_text = f"{t['cat_title_2'].format(name=user.first_name)}\n\n" + "\n\n".join([desc for _, _, desc in t['p2']])
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        all_items = t['p1'] + t['p2']
        paket_nama = "VIP Package"
        for btn_txt, cb_val, _ in all_items:
            if cb_val == call.data:
                paket_nama = btn_txt.replace("🛒 Buy: ", "").replace("🛒 Beli: ", "")
                
        random_serial = random.randint(10000, 99999)
        
        invoice_text = (
            f"{t['inv_title']}\n\n"
            f"📦 Paket Dipilih: {paket_nama}\n"
            f"🔢 Nomor Resi Unik: PKL-MLBB-{random_serial}\n"
            f"⏱️ Batas Waktu Pembayaran: 15 Menit\n\n"
            f"{t['pay_info']}\n\n"
            f"{t['confirm_instr']}\n"
            f"👉 Kirim bukti transfer & resi ke admin: {ADMIN_USERNAME}"
        )
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
            
        markup_inv = get_back_markup(l)
        bot.send_message(chat_id, invoice_text, reply_markup=markup_inv, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Invoice Generated!")

    elif call.data == 'menu_cara_order':
        if l == 'id':
            text = (
                "❓ PANDUAN CARA ORDER DI PAKEL MLBBSTORE\n\n"
                "1️⃣ Pilih paket script VIP impian Anda melalui menu Katalog.\n"
                "2️⃣ Klik tombol beli pada paket yang diinginkan untuk mendapatkan Nomor Resi Unik & daftar metode pembayaran.\n"
                "3️⃣ Lakukan pembayaran via metode pilihan Anda: DANA, GoPay, atau Saweria.\n"
                "4️⃣ Kirimkan screenshot bukti transfer beserta Nomor Resi ke bot ini atau langsung ke Admin utama.\n"
                "5️⃣ Admin akan memverifikasi dan mengirimkan file script beserta panduan lengkapnya detik itu juga!"
            )
        else:
            text = "❓ HOW TO ORDER\n1️⃣ Select package & click Buy.\n2️⃣ Choose payment (DANA, GoPay, Saweria).\n3️⃣ Pay & send proof to admin."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        if l == 'id':
            text = (
                "💳 METODE PEMBAYARAN LENGKAP PAKEL MLBBSTORE\n\n"
                "Bebas pilih metode pembayaran yang paling nyaman untuk Anda:\n\n"
                "1️⃣ TRANSFER DANA / GOPAY:\n"
                f"   • Nomor DANA: {INFO_DANA}\n"
                f"   • Nomor GoPay: {INFO_GOPAY}\n\n"
                "2️⃣ SAWERIA (Dukungan Donasi / Kartu / E-Wallet):\n"
                f"   • Link Pembayaran: {INFO_SAWERIA}\n\n"
                "📌 Catatan: Silakan pilih paket di katalog lalu klik beli untuk memunculkan instruksi pembayaran lengkap, atau langsung hubungi {ADMIN_USERNAME}."
            )
        else:
            text = f"💳 ALL PAYMENT METHODS\n\n1. DANA / GoPay\n2. Saweria\n📌 Confirm to {ADMIN_USERNAME}."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        rs = random.randint(10000, 99999)
        if l == 'id':
            text = (
                "✅ KONFIRMASI PEMBAYARAN & KLAIM SCRIPT\n\n"
                f"Contoh Format Resi Anda: PKL-MLBB-{rs}\n\n"
                "Silakan kirim screenshot bukti transfer pembayaran Anda (baik dari DANA, GoPay, maupun Saweria) ke chat ini atau langsung ke Admin untuk segera diproses."
            )
        else:
            text = f"✅ PAYMENT CONFIRMATION\nExample Receipt: PKL-MLBB-{rs}\nSend transfer screenshot to admin."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    save_user(message.chat.id)
    user = message.from_user
    rs = random.randint(10000, 99999)
    
    WIB = timezone(timedelta(hours=7))
    now = datetime.now(WIB)
    dt_str = now.strftime("%d-%m-%Y")
    tm_str = now.strftime("%H:%M:%S WIB")
    
    res = (
        "✅ BUKTI PEMBAYARAN BERHASIL DIUNGGAH!\n"
        f"Terima kasih banyak Kak {user.first_name} atas kepercayaannya berbelanja di Pakel MlbbStore 🙏✨\n\n"
        f"🛡️ Nomor Resi Unik Anda: PKL-MLBB-{rs}\n"
        f"⏱️ Waktu Transaksi: {dt_str} - {tm_str}\n\n"
        "📋 SALIN FORMAT DI BAWAH INI DAN KIRIM KE ADMIN:\n"
        "----------------------------------------\n"
        f"• No Resi      : PKL-MLBB-{rs}\n"
        f"• Nama Pembeli : {user.first_name}\n"
        "• Status       : LUNAS / MENUNGGU SCRIPT\n"
        "----------------------------------------\n"
        f"🚀 Hubungi Admin sekarang: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, res, disable_web_page_preview=True)

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    txt = message.text.lower()
    
    if any(w in txt for w in ['price', 'harga', 'list', 'menu', 'catalog', 'katalog']):
        res_msg = "💎 Ketik /start untuk membuka Katalog VIP eksklusif Pakel MlbbStore!" if l == 'id' else "💎 Type /start to view the VIP Catalogue!"
    elif any(w in txt for w in ['pay', 'bayar', 'dana', 'gopay', 'saweria', 'testi', 'testimoni']):
        res_msg = "🌟 Cek menu /start untuk melihat Katalog VIP, Metode Pembayaran Lengkap, hingga Live Testimoni real-time pembeli!" if l == 'id' else "🌟 Type /start to view catalogue, payments, and live testimonials."
    else:
        res_msg = f"Halo {user.first_name}! Silakan ketik /start untuk mengakses menu utama atau hubungi admin kami di {ADMIN_USERNAME}." if l == 'id' else f"Hello {user.first_name}! Contact our admin at {ADMIN_USERNAME}."
        
    bot.reply_to(message, res_msg, disable_web_page_preview=True)

print("[INFO] Pakel MlbbStore Master Ultimate Edition Berhasil Dijalankan...")
bot.infinity_polling()

