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
INFO_SAWERIA = "https://saweria.co/pakelmlbbstore"

# ==================== FUNGSI DATABASE USER & BROADCAST ====================
def save_user(chat_id):
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
        if str(chat_id) not in users:
            with open("users.txt", "a") as f:
                f.write(str(chat_id) + "\n")
    except FileNotFoundError:
        with open("users.txt", "w") as f:
            f.write(str(chat_id) + "\n")

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
# ==================== BACKGROUND WORKER (AUTO-POST) ====================
def background_auto_poster():
    time.sleep(30)
    while True:
        try:
            sleep_time = random.randint(600, 1500)
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

# ==================== ROBLOX-STYLE ADMIN PANEL ENGINE (/sc & /panel) ====================
admin_panel_sessions = {}

@bot.message_handler(commands=['sc', 'panel'])
def cmd_roblox_admin_panel(message):
    save_user(message.chat.id)
    text_clean = message.text.replace('/sc', '').replace('/panel', '').strip()
    
    if not text_clean:
        target_buyer = f"@{message.from_user.username}" if message.from_user.username else f"@{message.from_user.first_name}"
    else:
        target_buyer = text_clean if text_clean.startswith('@') else f"@{text_clean}"
        
    chat_id = message.chat.id
    
    admin_panel_sessions[chat_id] = {
        'buyer': target_buyer,
        'package': None,
        'price': None,
        'key': None
    }
    
    render_roblox_panel(chat_id, message.message_id, is_new=True)

def render_roblox_panel(chat_id, message_id, is_new=False):
    session = admin_panel_sessions.get(chat_id, {'buyer': '@Customer', 'package': 'Belum Dipilih', 'price': '-'})
    
    buyer = session['buyer']
    pkg = session['package'] if session['package'] else "❌ Belum Dipilih (Silakan Pilih di Bawah)"
    prc = session['price'] if session['price'] else "-"
    
    panel_text = (
        "🖥️ ━━━━━━━━━━━━━━━━━━━━━ 🖥️\n"
        "     <b>[ PAKEL ROBLOX ADMIN STUDIO ]</b>\n"
        "🖥️ ━━━━━━━━━━━━━━━━━━━━━ 🖥️\n\n"
        f"👤 <b>Target Buyer :</b> <code>{buyer}</code>\n"
        f"📦 <b>Selected Item:</b> <b>{pkg}</b>\n"
        f"💵 <b>Price Value  :</b> <code>{prc}</code>\n"
        f"⚙️ <b>Panel Status :</b> <code>READY TO DISPATCH</code>\n\n"
        "👇 <i>Gunakan Scrolling Frame di bawah untuk memilih paket, lalu tekan tombol Kirim:</i>"
    )
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    packages_btn = [
        ("💎 Natural Balance (30 Hari) [120k]", "rbx_pkg|natural|Natural Balance (30 Hari)|Rp 120.000"),
        ("⚡ Light VIP + Drone (30 Hari) [95k]", "rbx_pkg|light|Light VIP + Drone (30 Hari)|Rp 95.000"),
        ("🛡️ Semi-Safe 14 Hari [75k]", "rbx_pkg|semisafe|Semi-Safe 14 Hari|Rp 75.000"),
        ("👑 Lifetime Safe Permanent [200k]", "rbx_pkg|lifetimesafe|Lifetime Safe Permanent|Rp 200.000"),
        ("💥 Sultan One Hit 100% (30 Hari) [150k]", "rbx_pkg|sultan|Sultan One Hit 100% (30 Hari)|Rp 150.000"),
        ("⚡ VIP Pro One Hit 80% (30 Hari) [100k]", "rbx_pkg|pro|VIP Pro One Hit 80% (30 Hari)|Rp 100.000"),
        ("🔒 Semi-Private 14 Hari [75k]", "rbx_pkg|semiprivate|Semi-Private 14 Hari|Rp 75.000"),
        ("🏆 Permanent Legend (Lifetime) [250k]", "rbx_pkg|permanent|Permanent Legend (Lifetime)|Rp 250.000")
    ]
    
    for text_b, cb_b in packages_btn:
        active_mark = " ✅" if session['key'] in cb_b else ""
        markup.add(types.InlineKeyboardButton(text_b + active_mark, callback_data=cb_b))
        
    markup.row(
        types.InlineKeyboardButton("🚀 Kirim Testi / Done", callback_data="rbx_action|send"),
        types.InlineKeyboardButton("🔄 Reset", callback_data="rbx_action|reset")
    )
    
    if is_new:
        bot.send_message(chat_id, panel_text, reply_markup=markup, parse_mode="HTML")
    else:
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=panel_text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            pass

@bot.callback_query_handler(func=lambda call: call.data.startswith('rbx_'))
def callback_roblox_panel(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    
    if chat_id not in admin_panel_sessions:
        admin_panel_sessions[chat_id] = {'buyer': '@Customer', 'package': None, 'price': None, 'key': None}
        
    data_split = call.data.split('|')
    action_type = data_split[0]
    
    if action_type == 'rbx_pkg':
        pkg_key = data_split[1]
        pkg_name = data_split[2]
        pkg_price = data_split[3]
        
        admin_panel_sessions[chat_id]['key'] = pkg_key
        admin_panel_sessions[chat_id]['package'] = pkg_name
        admin_panel_sessions[chat_id]['price'] = pkg_price
        
        render_roblox_panel(chat_id, message_id, is_new=False)
        bot.answer_callback_query(call.id, text=f"Dipilih: {pkg_name}")
        
    elif action_type == 'rbx_action':
        sub_action = data_split[1]
        
        if sub_action == 'reset':
            admin_panel_sessions[chat_id]['package'] = None
            admin_panel_sessions[chat_id]['price'] = None
            admin_panel_sessions[chat_id]['key'] = None
            render_roblox_panel(chat_id, message_id, is_new=False)
            bot.answer_callback_query(call.id, text="Panel direset!")
            
        elif sub_action == 'send':
            session = admin_panel_sessions[chat_id]
            if not session['package']:
                bot.answer_callback_query(call.id, text="⚠️ Pilih dulu paket script-nya di scrolling frame!", show_alert=True)
                return
                
            buyer_name = session['buyer']
            paket_nama = session['package']
            harga = session['price']
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
                text=(
                    "🖥️ ━━━━━━━━━━━━━━━━━━━━━ 🖥️\n"
                    "     <b>[ ROBLOX PANEL: SUCCESS ]</b>\n"
                    "🖥️ ━━━━━━━━━━━━━━━━━━━━━ 🖥️\n\n"
                    f"✅ <b>BERHASIL DIKIRIM KE GRUP!</b>\n"
                    f"• Pembeli: <code>{buyer_name}</code>\n"
                    f"• Paket: <b>{paket_nama}</b>\n"
                    f"• Harga: <code>{harga}</code>"
                ),
                parse_mode="HTML"
            )
            bot.answer_callback_query(call.id, text="Testimoni sukses dikirim ke grup!")
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
            ("🛒 Beli: Natural Balance (Rp 120k)", "buy_natural", "• 💎 Natural Balance (30 Hari) — Rp 120.000\n  └ 🎯 Fungsi: Damage halus, stabil, aman dari ban, cocok untuk Mythic ke atas."),
            ("🛒 Beli: Light VIP + Drone (Rp 95k)", "buy_light", "• ⚡ Light VIP + Drone (30 Hari) — Rp 95.000\n  └ 🎯 Fungsi: Boost damage ringan + luas pandang map (drone view)."),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", "buy_semisafe", "• 🛡️ Semi-Safe (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Durasi singkat optimal buat ngebut push star akhir season."),
            ("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", "buy_lifetimesafe", "• 👑 Lifetime Safe (Permanent) — Rp 200.000\n  └ 🎯 Fungsi: Akses seumur hidup + update gratis setiap patch baru.")
        ],
        'p2': [
            ("🛒 Beli: Sultan One Hit 100% (Rp 150k)", "buy_sultan", "• 💥 Sultan One Hit 100% (30 Hari) — Rp 150.000\n  └ 🎯 Fungsi: Kill instan mutlak tanpa ampun di setiap pertarungan."),
            ("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", "buy_pro", "• ⚡ VIP Pro One Hit 80% (30 Hari) — Rp 100.000\n  └ 🎯 Fungsi: Kombinasi power one hit stabil dan aman dilaporkan."),
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", "buy_semiprivate", "• 🔒 Semi-Private (14 Hari) — Rp 75.000\n  └ 🎯 Fungsi: Script privat eksklusif distribusi terbatas."),
            ("🛒 Beli: Permanent Legend (Rp 250k)", "buy_permanent", "• 🏆 Permanent Legend (Lifetime) — Rp 250.000\n  └ 🎯 Fungsi: Status sultan tertinggi selamanya.")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': f"💳 TRANSFER DANA/GOPAY: {INFO_DANA}\n🌐 SAWERIA: {INFO_SAWERIA}",
        'confirm_instr': "🛡️ Kirim bukti transfer ke bot ini untuk dapat Resi Unik.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue",
        'btn_testi': "🌟 Live Testimonials",
        'btn_promo': "🎁 Promo",
        'btn_cara_order': "❓ How to Order",
        'btn_bayar': "💳 Payments",
        'btn_faq': "💡 FAQ",
        'btn_konfirmasi': "✅ Receipt",
        'btn_admin': "💬 Admin",
        'back': "⬅️ Back",
        'cat_title_1': "🔥 CATALOGUE PART 1 ({name})",
        'cat_title_2': "🔥 CATALOGUE PART 2 ({name})",
        'bonus_txt': "⚡ BONUS FREE ALL PACKAGES",
        'p1': [("🛒 Buy: Natural Balance", "buy_natural", "• Natural Balance")],
        'p2': [("🛒 Buy: Sultan One Hit", "buy_sultan", "• Sultan One Hit")],
        'next_1': "▶️ Next",
        'prev_2': "◀️ Back",
        'inv_title': "🛒 INVOICE",
        'pay_info': "💳 Payment Info",
        'confirm_instr': "Send proof.",
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

@bot.message_handler(commands=['bc', 'broadcast'])
def broadcast_message(message):
    pesan_bc = message.text.replace('/bc', '').replace('/broadcast', '').strip()
    if not pesan_bc:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /bc Halo semua")
        return
    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Belum ada user.")
        return
    success = sum(1 for cid in users if bot.send_message(cid, f"📢 PENGUMUMAN:\n\n{pesan_bc}") or True)
    bot.reply_to(message, f"✅ Broadcast Selesai ke {success} user!")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    save_user(message.chat.id)
    user = message.from_user
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
    bot.send_message(message.chat.id, f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n👇 Silakan pilih menu di bawah:", reply_markup=markup)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    save_user(message.chat.id)
    user = message.from_user
    bot.reply_to(message, f"🔍 CEK STATUS RESI (Kak {user.first_name})\nKirimkan No Resi / bukti transfer ke sini.\n💬 Admin: {ADMIN_USERNAME}", disable_web_page_preview=True)

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
        text = f"🔥 {greeting}! Silakan pilih menu utama Pakel MlbbStore:"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup)
        except Exception:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_testi':
        fake_data = generate_fake_testimonials_list()
        testi_text = f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n\n{fake_data}"
        markup_testi = types.InlineKeyboardMarkup(row_width=1)
        markup_testi.add(types.InlineKeyboardButton("🔄 Refresh Testimoni", callback_data='menu_testi'))
        markup_testi.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text, reply_markup=markup_testi, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Testimoni diperbarui!")

    elif call.data == 'menu_promo':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"🎁 PROMO KUPON: WELCOMEPAKEL", reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💡 FAQ: Script dijamin aman & anti-detect.", reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in t['p1']:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n" + "\n\n".join([desc for _, _, desc in t['p1']])
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
        random_serial = random.randint(10000, 99999)
        invoice_text = f"🛒 INVOICE (PKL-MLBB-{random_serial})\n\n{t['pay_info']}\n\n{t['confirm_instr']}"
        try:
            bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception:
            pass
        bot.send_message(chat_id, invoice_text, reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_cara_order':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❓ CARA ORDER:\n1. Pilih paket\n2. Bayar\n3. Kirim bukti", reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=t['pay_info'], reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ Kirim screenshot bukti transfer ke chat ini.", reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    save_user(message.chat.id)
    rs = random.randint(10000, 99999)
    bot.reply_to(message, f"✅ Bukti diterima! No Resi Unik: PKL-MLBB-{rs}\nKirim format ini ke {ADMIN_USERNAME}")

@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    save_user(message.chat.id)
    bot.reply_to(message, f"Halo! Ketik /start untuk menu utama atau /panel @Username untuk buka Roblox Admin Panel.")

print("[INFO] Pakel MlbbStore Final Fixed Edition Berhasil Dijalankan...")
bot.infinity_polling()
