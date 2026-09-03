import telebot
from telebot import types

# Token bot lu yang aktif
TOKEN = '8637403539:AAExQXPSnm8_eNoMyjCzA2Ldl1sOXRAVzcM'
bot = telebot.TeleBot(TOKEN)

# Data Kontak Admin & Info Pembayaran Resmi
ADMIN_USERNAME = "@PakelMlbbOfficial"
DANA_NUMBER = "089526466512"
DANA_NAME = "PakelMlbb"
GOPAY_NUMBER = "089526466512"
GOPAY_NAME = "PakelMlbb"
SAWERIA_LINK = "https://saweria.co/PakelMlbb"

# 1. Perintah /start (Menu Utama)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_katalog = types.InlineKeyboardButton("💎 Lihat Katalog VIP (2 Kategori Pilihan)", callback_data='menu_katalog')
    btn_cara_order = types.InlineKeyboardButton("❓ Cara Order & Panduan Belanja", callback_data='menu_cara_order')
    btn_bayar = types.InlineKeyboardButton("💳 Metode Pembayaran (DANA / GoPay / Saweria)", callback_data='menu_bayar')
    btn_konfirmasi = types.InlineKeyboardButton("✅ Konfirmasi Pembayaran Selesai", callback_data='menu_konfirmasi')
    btn_admin = types.InlineKeyboardButton("💬 Hubungi Admin Resmi", url="https://t.me/PakelMlbbOfficial")
    
    markup.add(btn_katalog, btn_cara_order, btn_bayar, btn_konfirmasi, btn_admin)
    
    welcome_text = (
        f"🔥 Halo, Kak *{user_name}*! Selamat datang di Bot Resmi *Pakel MlbbStore* 🚀\n\n"
        "Pusat script custom damage fair play, one hit, panel server lag, & drone view X1-X10 terlengkap. Silakan pilih menu di bawah untuk melihat katalog!"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# 2. Handler Tombol (Callback Query)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == 'menu_katalog':
        katalog_text = (
            "🔥 *KATALOG EKSKLUSIF SCRIPT PAKEL MLBBSTORE* 🔥\n"
            "*(Bebas pilih durasi & kategori sesuai gaya bermainmu!)*\n\n"
            
            "⚡ *BONUS SPESIAL SEMUA PAKET:* \n"
            "Otomatis mendapatkan **Panel Pembuat Jaringan Musuh Lag / Server Lag** serta **Drone View Lengkap dari X1 sampai X10** di setiap pembelian!\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "📂 *KATEGORI 1: CUSTOM DAMAGE & FAIR PLAY* 🛡️\n"
            "*(Cocok untuk pemain yang mengutamakan keamanan akun & damage natural)*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            "👑 *1. Paket Natural Balance • Custom Damage Halus & Fleksibel*\n"
            "👉 Harga: **Rp 120.000** (Durasi 30 Hari / 1 Bulan)\n"
            "📌 Pengaturan damage dapat disesuaikan secara mandiri (seperti 2 hit agar tidak mencolok), performa optimal namun senyap.\n\n"
            
            "⚡ *2. Paket Light VIP • Custom Damage Lembut + Drone View*\n"
            "👉 Harga: **Rp 95.000** (Durasi 30 Hari / 1 Bulan)\n"
            "📌 Kombinasi pas antara damage wajar ditambah pandangan map lebih luas untuk baca pergerakan lawan.\n\n"
            
            "🔥 *3. Paket Semi-Safe • Custom Damage Natural + Anti Lag*\n"
            "👉 Harga: **Rp 75.000** (Durasi 14 Hari / 2 Minggu)\n"
            "📌 Paket harian terjangkau dengan setelan damage terkontrol serta kestabilan koneksi dua minggu penuh.\n\n"
            
            "♾️ *4. Paket Lifetime Safe • Custom Damage Seimbang*\n"
            "👉 Harga: **Rp 200.000** (Akses Seumur Hidup / Permanent)\n"
            "📌 Solusi hemat jangka panjang tanpa biaya langganan, fitur damage fleksibel aman digunakan kapan saja.\n\n"
            
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "📂 *KATEGORI 2: ONE HIT & HIGH CLASS* 💥\n"
            "*(Buat sultan atau player serius yang mau overpower maksimal)*\n"
            "━━━━━━━━━━━━━━━━━━━━━\n\n"
            
            "👑 *5. Paket Sultan • One Hit Ultimate 100%*\n"
            "👉 Harga: **Rp 150.000** (Durasi 30 Hari / 1 Bulan)\n"
            "📌 Damage tembus batas, instant kill musuh dalam sekali hit, bypass anti-cheat paling aman.\n\n"
            
            "⚡ *6. Paket VIP Pro • One Hit 80% + Drone View X1-X10*\n"
            "👉 Harga: **Rp 100.000** (Durasi 30 Hari / 1 Bulan)\n"
            "📌 Damage sakit maksimal + pandangan map sangat luas, komplit jadi satu andalan top global.\n\n"
            
            "🔥 *7. Paket Semi-Private • One Hit 60% + Anti Lag Extreme*\n"
            "👉 Harga: **Rp 75.000** (Durasi 14 Hari / 2 Minggu)\n"
            "📌 Performa stabil, anti patah-patah dijamin lancar jaya buat bantai musuh seharian.\n\n"
            
            "♾️ *8. Paket Permanent • One Hit Legend*\n"
            "👉 Harga: **Rp 250.000** (Akses Seumur Hidup Tanpa Expired)\n"
            "📌 Sekali bayar, nikmati update script one hit seumur hidup tanpa perlu perpanjang tiap bulan.\n\n"
            
            "💳 *METODE PEMBAYARAN RESMI:*\n"
            f"• **DANA:** `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"• **GoPay:** `{GOPAY_NUMBER}` (A/N: {GOPAY_NAME})\n"
            f"• **Saweria:** {SAWERIA_LINK}\n\n"
            "💬 *KONSULTASI & PEMESANAN:*\n"
            "📲 Telegram Admin: https://t.me/PakelMlbbOfficial\n\n"
            "⚠️ *Catatan Penting:* Slot VIP dibatasi setiap hari demi menjaga keamanan akun. Siapa cepat dia dapat, Bosku! 🚀🔥"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, katalog_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'menu_cara_order':
        panduan_text = (
            "❓ *CARA ORDER & PANDUAN BELANJA DI PAKEL MLBBSTORE* 🛒\n\n"
            "Ikuti 3 langkah mudah di bawah ini, Bosku:\n\n"
            "1️⃣ **Pilih Kategori & Paket**\n"
            "Masuk ke menu *Lihat Katalog VIP*, tentukan pilihan paket (Custom Damage atau One Hit) sesuai durasi yang diinginkan.\n\n"
            "2️⃣ **Lakukan Pembayaran**\n"
            f"Transfer sesuai harga paket ke DANA/GoPay (`{DANA_NUMBER}`) atau via Saweria (`{SAWERIA_LINK}`).\n\n"
            "3️⃣ **Konfirmasi & Kirim Bukti**\n"
            "Klik tombol *Konfirmasi Pembayaran Selesai* atau kirim screenshot bukti transfer ke admin resmi di @PakelMlbbOfficial.\n\n"
            "⚡ File script, bonus panel server lag, & drone view X1-X10 akan langsung dikirim admin!"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, panduan_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'menu_bayar':
        bayar_text = (
            f"💳 *METODE PEMBAYARAN RESMI PAKEL MLBBSTORE*\n\n"
            f"📱 **DANA:** `{DANA_NUMBER}`\n"
            f"👤 Atas Nama: *{DANA_NAME}*\n\n"
            f"🟢 **GoPay:** `{GOPAY_NUMBER}`\n"
            f"👤 Atas Nama: *{GOPAY_NAME}*\n\n"
            f"🧡 **Saweria (QRIS / E-Wallet / Bank):**\n"
            f"🔗 {SAWERIA_LINK}\n\n"
            "📌 *Petunjuk Selanjutnya:*\n"
            "1. Transfer sesuai nominal paket pilihanmu.\n"
            "2. Kirim bukti transfer ke chat ini atau admin.\n"
            "3. File script akan segera dikirim!"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, bayar_text, parse_mode='Markdown', disable_web_page_preview=True)

    elif call.data == 'menu_konfirmasi':
        konfirmasi_text = (
            "✅ *KONFIRMASI PEMBAYARAN BERHASIL DIKIRIM*\n\n"
            "Terima kasih, Kak. Silakan kirimkan screenshot bukti transfer Anda ke admin `@PakelMlbbOfficial` agar langsung divalidasi!"
        )
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, konfirmasi_text, parse_mode='Markdown')

# 3. Auto-Reply Berdasarkan Kata Kunci Pesan Teks
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    text = message.text.lower()
    
    if any(word in text for word in ['harga', 'list', 'menu', 'jual', 'paket', 'script', 'cheat', 'one hit', 'lag', 'drone']):
        reply = "💎 Mau lihat katalog VIP yang dibagi jadi 2 kategori (Custom Damage & One Hit), Kak? Ketik /start lalu klik tombol *Lihat Katalog VIP* ya!"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['cara', 'beli', 'order', 'gimana', 'panduan']):
        reply = "❓ Mau tahu cara ordernya, Kak? Ketik /start lalu klik tombol *Cara Order & Panduan Belanja* ya!"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['dana', 'gopay', 'saweria', 'bayar', 'transfer', 'rekening']):
        reply = (
            f"💳 *INFO PEMBAYARAN LENGKAP*\n\n"
            f"📱 DANA / GoPay: `{DANA_NUMBER}` (Atas Nama: {DANA_NAME})\n"
            f"🧡 Saweria: {SAWERIA_LINK}\n\n"
            "Silakan transfer sesuai nominal, lalu kirim buktinya ya, Kak!"
        )
        bot.reply_to(message, reply, parse_mode='Markdown', disable_web_page_preview=True)
        
    elif any(word in text for word in ['terima kasih', 'makasih', 'oke', 'ok', 'salam']):
        reply = "Sama-sama, Kak! Semoga makin lancar win streak-nya bersama *Pakel MlbbStore*! 🚀🔥"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    else:
        reply = (
            f"Halo Kak! Pesan sudah diterima sistem *Pakel MlbbStore*. "
            f"Untuk bantuan cepat, hubungi admin resmi di {ADMIN_USERNAME} atau ketik /start untuk menu utama."
        )
        bot.reply_to(message, reply)

# Jalankan Bot
print("[INFO] Bot Telegram Pakel MlbbStore Berjalan...")
bot.infinity_polling()

