import telebot
from telebot import types
import random
import time
import threading
from datetime import datetime, timezone, timedelta

# Token bot lu yang aktif dan siap tempur
TOKEN = '8637403539:AAFyKck7U8POV3hzSw9UcF_sDDp0d_hKat0'
bot = telebot.TeleBot(TOKEN)

# Identitas Toko Resmi & Link QRIS Imgbb Lu
ADMIN_USERNAME = "@PakelMlbbOfficial"
ADMIN_LINK = "https://t.me/PakelMlbbOfficial"
GROUP_CHAT_ID = "@PakelMlbb"
GROUP_TOPIC_ID = 368

# Informasi Nomor Pembayaran Resmi & Link QRIS Web
INFO_DANA = "089526466512"
INFO_GOPAY = "089526466512"
INFO_SAWERIA = "https://saweria.co/PakelMlbb"
QRIS_WEB_LINK = "https://ibb.co.com/cX2J28kj"  # Link QRIS lu yang otomatis kebuka

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

def get_random_masked_name():
    list_nama_tele = [
        # --- INDONESIA ---
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
        "@Bayu_Pratama***", "@Farel_Official***", "@Yoga_Ganz***", "@Dicky_Dev***",
        "@Surya_ID***", "@Rama_ID***", "@Gilang_Mlg***", "@Bagas_X***",
        "@Arif_Prat***", "@Dani_Gmr***", "@Hendra_Sultan***", "@Rian_Wicak***",
        "@Aldi_Pro***", "@Bintang_Gz***", "@Candra_07***", "@Dika_Wahyudi***",
        "@Fajar_Sltn***", "@Galih_Xtrem***", "@Iqbal_Farel***", "@Joko_Santoso***",
        "@Kevin_Bagas***", "@Lukman_Rizky***", "@Maulana_Dwi***", "@Naufal_Akbar***",
        "@Pratama_Putra***", "@Rafli_Maulana***", "@Satria_angga***", "@Tegar_Aditya***",
        "@Vian_Saputra***", "@Wahyu_Hidayat***", "@Yuda_Kurniawan***", "@Zaki_Mubarok***",
        "@Rizal_Ganz***", "@Maulana_ID***", "@Fikri_Ramadhan***", "@Ilham_Saputra***",
        "@Rezky_Pratama***", "@Rizky_Maulana***", "@Fauzan_Azima***", "@Zidan_Alfarizi***",
        "@Rafi_Ahmad***", "@Zaki_Mubarok***", "@Fathan_Haikal***", "@Rifki_Ananda***",
        "@Aditya_Pratama***", "@Bayu_Pamungkas***", "@Yoga_Prasetyo***", "@Dimas_Mahendra***",
        "@R_Zky2026***", "@Alvinn123***", "@Dimas777***", "@Reza888***", 
        "@Bayu555***", "@Farel444***", "@Yoga333***", "@Dicky222***", 
        "@Surya111***", "@Rama999***", "@Gilang000***", "@Bagas777***",
        "@Den_Bagusk***", "@Reyhan_X***", "@Akmal_Store***", "@Zul_Fikar***",
        "@Pandu_Gans***", "@Radit_Pratama***", "@Gibran_ID***", "@Baim_Wong***",
        "@Ibnu_Sina***", "@Fahru_Nzi***", "@Nabil_Store***", "@Wildan_Xyz***",
        "@Erlangga_99***", "@Devan_Gmr***", "@Mahesa_Wk***", "@Ary_Satria***",

        # --- MALAYSIA ---
        "@Amirul_My***", "@Haikal_Iskandar***", "@Farhan_Zul***", "@Aiman_Badri***",
        "@Aqil_Danial***", "@Syahmi_Zain***", "@Luqman_Hakim***", "@Zulhelmi_My***",
        "@Azril_Anuar***", "@Izzat_Mukhriz***", "@Faris_Najmi***", "@Hazim_Zikri***",
        "@Nabil_Hakimi***", "@Danial_Fitri***", "@Amir_Syazwan***", "@Firdaus_Rosli***",
        "@Hakim_Azman***", "@Imran_Danish***", "@Khairul_Anwar***", "@Zack_Malaya***",
        "@Syafiq_Amsyar***", "@Aidil_Azhar***", "@Faiz_Mokhtar***", "@Megat_Zul***",
        "@Tarmizi_My***", "@Azlan_Shah***", "@Shahrul_Nizam***", "@Rizman_Azrai***",

        # --- INGGRIS & WESTERN / INTERNASIONAL ---
        "@Alex_Walker***", "@Liam_Smith***", "@Noah_Miller***", "@Oliver_Davis***",
        "@Elijah_Wilson***", "@James_Taylor***", "@William_Anderson***", "@Lucas_Thomas***",
        "@Mason_Moore***", "@Ethan_Jackson***", "@Logan_Martin***", "@Benjamin_Lee***",
        "@Lucas_White***", "@Alexander_Harris***", "@Henry_Clark***", "@Sebastian_Lewis***",
        "@Jack_Robinson***", "@Owen_Walker***", "@Theodore_Perez***", "@Aiden_Hall***",
        "@Samuel_Young***", "@Joseph_King***", "@John_Wright***", "@David_Scott***",
        "@Wyatt_Green***", "@Matthew_Baker***", "@Luke_Adams***", "@Asher_Nelson***",
        "@Carter_Carter***", "@Julian_Mitchell***", "@Grayson_Perez***", "@Leo_Roberts***",
        "@Jayden_Turner***", "@Gabriel_Phillips***", "@Isaac_Campbell***", "@Caleb_Parker***",
        "@Anthony_Evans***", "@Lincoln_Edwards***", "@Jaxon_Collins***", "@Mateo_Stewart***",
        "@Hudson_Sanchez***", "@Theodore_Morris***", "@Thomas_Rogers***", "@Connor_Reed***",
        "@Eli_Cook***", "@Aaron_Morgan***", "@Ezra_Bell***", "@Landon_Murphy***",
        "@Adrian_Bailey***", "@Jonathan_Rivera***", "@Nolan_Cooper***", "@Easton_Richardson***",
        "@Ezekiel_Cox***", "@Milton_Howard***", "@Cole_Ward***", "@Carson_Torres***",

        # --- TAMBAHAN TRENDING GAMER ---
        "@Sultan_Mlbb***", "@Anjay_Mabar***", "@Gacor_Gaming***", "@TopGlobal_1***",
        "@Mythic_Immortal***", "@ProPlayer_Indo***", "@Epep_Bapakmu***", "@Bocil_Kematian***",
        "@Wibu_Gariskeras***", "@Beban_Tim***", "@Jagoan_Emak***", "@Peler_Jawa***",
        "@Raja_Turu***", "@Bapak_Gamer***", "@Anak_Sultan***", "@Wong_Kito***",
        "@Ank_Nongkrong***", "@Wibu_Hunter***", "@Savage_Everyday***", "@Maniac_Lord***"
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
        bot.reply_to(message, "✅ Berhasil! Testimoni real-time baru saja dikirim ke topik grup.")
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
            ("🛒 Beli: Natural Balance (Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Hari) — Rp 120.000\n  └ 🎯 Fungsi: Script penyetara damage halus, aman anti-detect untuk tier Mythic."),
            ("🛒 Beli: Light VIP + Drone (Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Hari) — Rp 95.000\n  └ 🎯 Fungsi: Boost damage ringan + map vision luas (drone view)."),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Solusi cepat push rank akhir season."),
            ("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Safe (Permanent) — Rp 200.000\n  └ 🎯 Fungsi: Akses permanen seumur hidup + update gratis.")
        ],
        'p2': [
            ("🛒 Beli: Sultan One Hit 100% (Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% (30 Hari) — Rp 150.000\n  └ 🎯 Fungsi: One hit kill mutlak untuk dominasi total."),
            ("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% (30 Hari) — Rp 100.000\n  └ 🎯 Fungsi: Keseimbangan kekuatan dan keamanan akun."),
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Script privat eksklusif 2 minggu."),
            ("🛒 Beli: Permanent Legend (Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend (Lifetime) — Rp 250.000\n  └ 🎯 Fungsi: Paket elit permanen seumur hidup.")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2 (Sultan One Hit)",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': (
            "💳 SILAKAN PILIH METODE PEMBAYARAN DI BAWAH INI:\n\n"
            "1️⃣ QRIS (Scan Otomatis Semua Bank / E-Wallet / Cross-Border):\n"
            "   👉 Klik tombol link QRIS di bawah untuk langsung membuka gambar QRIS!\n\n"
            "2️⃣ TRANSFER MANUAL DANA / GOPAY:\n"
            f"   • Nomor DANA: {INFO_DANA}\n"
            f"   • Nomor GoPay: {INFO_GOPAY}\n\n"
            "3️⃣ SAWERIA (Support Kartu & E-Wallet):\n"
            f"   • Link: {INFO_SAWERIA}\n"
        ),
        'confirm_instr': "🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\nSetelah sukses membayar via QRIS atau metode lainnya, silakan kirim Screenshot Bukti Transfer ke bot ini untuk mendapatkan Resi Unik.",
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
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS (FREE ALL PACKAGES): \n🎁 Get for FREE:\n  • Enemy Server Lag Panel\n  • Drone View X1 - X10 (Ultra Wide)\n\n📂 PACKAGE DETAILS & FUNCTIONS:",
        'p1': [
            ("🛒 Buy: Natural Balance ($8 / Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Days) — $8 / Rp 120k"),
            ("🛒 Buy: Light VIP + Drone ($6 / Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Days) — $6 / Rp 95k"),
            ("🛒 Buy: Semi-Safe 14 Days ($5 / Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Days) — $5 / Rp 75k"),
            ("🛒 Buy: Lifetime Permanent ($13 / Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Permanent — $13 / Rp 200k")
        ],
        'p2': [
            ("🛒 Buy: Sultan One Hit 100% ($10 / Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% — $10 / Rp 150k"),
            ("🛒 Buy: VIP Pro One Hit 80% ($7 / Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% — $7 / Rp 100k"),
            ("🛒 Buy: Semi-Private 14 Days ($5 / Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Days) — $5 / Rp 75k"),
            ("🛒 Buy: Permanent Legend ($16 / Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend — $16 / Rp 250k")
        ],
        'next_1': "▶️ Next: Catalog Part 2 (One Hit)",
        'prev_2': "◀️ Back to Catalog Part 1",
        'inv_title': "🛒 AUTOMATED VIP ORDER INVOICE ({name}) 🧾",
        'pay_info': "💳 CHOOSE PAYMENT METHOD:\n1. QRIS (Click link below)\n2. DANA / GoPay\n3. Saweria",
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
    
    bot.reply_to(message, f"🚀 Memulai broadcast ke {len(users)} member...")
    for chat_id in users:
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI PAKEL MLBBSTORE</b>\n\n{pesan_bc}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception as e:
            failed += 1
            
    bot.send_message(message.chat.id, f"✅ Broadcast Selesai!\n- Berhasil: {success}\n- Gagal: {failed}")
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
        welcome_text = f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n👇 Please select a menu below:"
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

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
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"✅ **BERHASIL DIKIRIM KE GRUP!**\n\n• Pembeli: {buyer_name}\n• Paket: {paket_nama} ({harga})")
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
        testi_text = f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n\n{fake_data}💡 Toko 100% amanah! 🚀" if l == 'id' else f"🌟 LIVE TESTIMONIALS\n\n{fake_data}"
        
        markup_testi = types.InlineKeyboardMarkup(row_width=1)
        markup_testi.add(types.InlineKeyboardButton("🔄 Refresh Testimoni Terbaru", callback_data='menu_testi'))
        markup_testi.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text, reply_markup=markup_testi, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Testimoni diperbarui!")

    elif call.data == 'menu_promo':
        promo_text = f"🎁 PROMO EKSKLUSIF (Kak {user.first_name})\n\n🎟️ KODE KUPON: WELCOMEPAKEL\n💰 Potongan harga spesial pembelian pertama!"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        faq_text = "💡 FAQ PAKEL MLBBSTORE\n\n❓ Aman dari banned? 💬 A: Sangat aman, enkripsi anti-detect tinggi."
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
            f"⏱️ Batas Waktu: 15 Menit\n\n"
            f"{t['pay_info']}\n\n"
            f"{t['confirm_instr']}\n"
            f"👉 Admin: {ADMIN_USERNAME}"
        )
        
        # Tombol URL Langsung Membuka Link Gambar QRIS Imgbb
        markup_inv = types.InlineKeyboardMarkup(row_width=1)
        markup_inv.add(types.InlineKeyboardButton("💳 Buka Gambar QRIS Pembayaran", url=QRIS_WEB_LINK))
        markup_inv.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
            
        bot.send_message(chat_id, invoice_text, reply_markup=markup_inv, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Invoice Generated!")

    elif call.data == 'menu_cara_order':
        text = "❓ PANDUAN CARA ORDER\n1. Pilih paket di katalog.\n2. Klik beli untuk dapat nomor resi & tombol link QRIS.\n3. Bayar & kirim bukti transfer."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        markup_bayar = types.InlineKeyboardMarkup(row_width=1)
        markup_bayar.add(types.InlineKeyboardButton("💳 Buka Gambar QRIS", url=QRIS_WEB_LINK))
        markup_bayar.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))

        text = f"💳 METODE PEMBAYARAN\n\n1. QRIS (Klik tombol di bawah untuk buka gambar)\n2. DANA/GoPay: {INFO_DANA}\n3. Saweria: {INFO_SAWERIA}"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup_bayar, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        rs = random.randint(10000, 99999)
        text = f"✅ KONFIRMASI PEMBAYARAN\n\nKirim screenshot bukti transfer Anda dengan menyertakan Nomor Resi (misal: PKL-MLBB-{rs}) ke admin."
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    save_user(message.chat.id)
    user = message.from_user
    rs = random.randint(10000, 99999)
    WIB = timezone(timedelta(hours=7))
    now = datetime.now(WIB)
    
    res = (
        "✅ BUKTI PEMBAYARAN BERHASIL DIUNGGAH!\n"
        f"Terima kasih Kak {user.first_name} 🙏\n\n"
        f"🛡️ No Resi Unik: PKL-MLBB-{rs}\n"
        f"⏱️ Waktu: {now.strftime('%d-%m-%Y %H:%M:%S WIB')}\n\n"
        f"📋 Kirim format ini ke Admin: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, res, disable_web_page_preview=True)

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    txt = message.text.lower()
    
    if any(w in txt for w in ['price', 'harga', 'list', 'menu', 'catalog', 'katalog']):
        res_msg = "💎 Ketik /start untuk membuka Katalog VIP!"
    elif any(w in txt for w in ['pay', 'bayar', 'dana', 'gopay', 'saweria', 'qris', 'testi']):
        res_msg = "🌟 Cek menu /start untuk melihat metode pembayaran QRIS & katalog lengkap!"
    else:
        res_msg = f"Halo {user.first_name}! Ketik /start untuk membuka menu utama atau hubungi {ADMIN_USERNAME}."
        
    bot.reply_to(message, res_msg, disable_web_page_preview=True)

print("[INFO] Pakel MlbbStore Imgbb QRIS Edition Berhasil Dijalankan...")
bot.infinity_polling()
