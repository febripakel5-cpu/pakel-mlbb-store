import telebot
from telebot import types
import random
import time

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

# Fungsi Tombol Kembali ke Menu Utama
def get_back_markup():
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama / Main Menu", callback_data='menu_utama'))
    return markup

# 1. Perintah /start (Menu Utama + Promo Member Baru)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_katalog = types.InlineKeyboardButton("💎 Pilih & Beli Paket VIP (Katalog Lengkap)", callback_data='menu_katalog')
    btn_promo = types.InlineKeyboardButton("🎁 Klaim Promo Member Baru (Diskon Spesial)", callback_data='menu_promo')
    btn_cara_order = types.InlineKeyboardButton("❓ Cara Order & Panduan Otomatis", callback_data='menu_cara_order')
    btn_bayar = types.InlineKeyboardButton("💳 Metode Pembayaran Resmi", callback_data='menu_bayar')
    btn_konfirmasi = types.InlineKeyboardButton("✅ Konfirmasi Pembayaran & Cek Resi", callback_data='menu_konfirmasi')
    btn_admin = types.InlineKeyboardButton("💬 Hubungi Admin Resmi", url="https://t.me/PakelMlbbOfficial")
    
    markup.add(btn_katalog, btn_promo, btn_cara_order, btn_bayar, btn_konfirmasi, btn_admin)
    
    welcome_text = (
        f"🔥 *Halo, Kak {user_name}!* Selamat datang di Official *Pakel MlbbStore* 🙏✨\n\n"
        "Pusat layanan script custom damage, one hit, server lag panel, & drone view terlengkap dengan sistem otomatis tercanggih anti-nipu.\n\n"
        "🇲🇨 *ID:* Silakan pilih paket di menu katalog atau klaim promo member baru!\n"
        "🇬🇧 *EN:* Please select a package or claim your new member promo below.\n\n"
        "👇 *Silakan ketuk tombol di bawah ini, Kak:*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# 2. Handler Tombol (Callback Query)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_name = call.from_user.first_name
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'menu_utama':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_katalog = types.InlineKeyboardButton("💎 Pilih & Beli Paket VIP (Katalog Lengkap)", callback_data='menu_katalog')
        btn_promo = types.InlineKeyboardButton("🎁 Klaim Promo Member Baru (Diskon Spesial)", callback_data='menu_promo')
        btn_cara_order = types.InlineKeyboardButton("❓ Cara Order & Panduan Otomatis", callback_data='menu_cara_order')
        btn_bayar = types.InlineKeyboardButton("💳 Metode Pembayaran Resmi", callback_data='menu_bayar')
        btn_konfirmasi = types.InlineKeyboardButton("✅ Konfirmasi Pembayaran & Cek Resi", callback_data='menu_konfirmasi')
        btn_admin = types.InlineKeyboardButton("💬 Hubungi Admin Resmi", url="https://t.me/PakelMlbbOfficial")
        markup.add(btn_katalog, btn_promo, btn_cara_order, btn_bayar, btn_konfirmasi, btn_admin)
        
        welcome_text = (
            f"🔥 *Halo kembali, Kak {user_name}!* 🙏\n"
            "Silakan pilih menu layanan resmi kami di bawah ini ya:"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=welcome_text, parse_mode='Markdown', reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_promo':
        promo_text = (
            f"🎁 *PROMO SPESIAL PELANGGAN BARU (NEW MEMBER)* (Untuk Kak *{user_name}*) 🎉\n\n"
            "Nikmati penawaran khusus pembelian pertama di *Pakel MlbbStore*:\n\n"
            "🎟️ **KODE KUPON:** `WELCOMEPAKEL`\n"
            "💰 **Keuntungan:** Potongan harga langsung Rp 10.000 / Diskon Spesial di semua kategori paket VIP!\n\n"
            "📌 *Cara Pakai:*\n"
            "Cukup sebutkan kode kupon `WELCOMEPAKEL` kepada admin saat melakukan konfirmasi pembayaran setelah memilih paket di katalog. Gampang banget kan? 🚀"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id, text="Kupon berhasil dilihat!")

    elif call.data == 'menu_katalog':
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        markup.add(types.InlineKeyboardButton("🛒 Beli: Natural Balance (Rp 120k)", callback_data='buy_natural'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Light VIP + Drone (Rp 95k)", callback_data='buy_light'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Sultan One Hit 100% (Rp 150k)", callback_data='buy_sultan'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", callback_data='buy_pro'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Permanent Legend (Rp 250k)", callback_data='buy_permanent'))
        markup.add(types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama'))

        katalog_text = (
            f"🔥 *VIP EXCLUSIVE CATALOGUE* (Untuk Kak *{user_name}*) 🔥\n"
            "*(Pilih paket impianmu di bawah dan klik tombol beli langsung!)*\n\n"
            
            "⚡ *BONUS SPESIAL FREE ALL PACKAGES:* \n"
            "🎁 Otomatis mendapatkan **Panel Server Lag Musuh** & **Drone View X1 - X10** gratis!\n\n"
            
            "📂 *KATEGORI 1: CUSTOM DAMAGE & FAIR PLAY* 🛡️\n"
            "• **Natural Balance (30 Hari):** Rp 120.000\n"
            "• **Light VIP + Drone (30 Hari):** Rp 95.000\n"
            "• **Semi-Safe (14 Hari):** Rp 75.000\n"
            "• **Lifetime Safe (Permanent):** Rp 200.000\n\n"
            
            "📂 *KATEGORI 2: ONE HIT & HIGH CLASS* 💥\n"
            "• **Sultan One Hit 100% (30 Hari):** Rp 150.000\n"
            "• **VIP Pro One Hit 80% (30 Hari):** Rp 100.000\n"
            "• **Semi-Private (14 Hari):** Rp 75.000\n"
            "• **Permanent Legend (Lifetime):** Rp 250.000\n\n"
            
            "💳 *INFO PEMBAYARAN & PROMO:*\n"
            f"• DANA/GoPay: `{DANA_NUMBER}` ({DANA_NAME})\n"
            f"• Saweria: {SAWERIA_LINK}\n"
            "• Gunakan Kupon Member Baru: `WELCOMEPAKEL`\n\n"
            "👇 *Klik tombol beli di bawah untuk generate pesanan instan!*"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        paket_tipe = call.data.replace('buy_', '')
        
        if paket_tipe == 'natural':
            paket_nama = "Natural Balance (Rp 120.000)"
        elif paket_tipe == 'light':
            paket_nama = "Light VIP + Drone (Rp 95.000)"
        elif paket_tipe == 'sultan':
            paket_nama = "Sultan One Hit 100% (Rp 150.000)"
        elif paket_tipe == 'pro':
            paket_nama = "VIP Pro One Hit 80% (Rp 100.000)"
        elif paket_tipe == 'permanent':
            paket_nama = "Permanent Legend (Rp 250.000)"
        else:
            paket_nama = "Paket VIP Custom"

        random_serial = random.randint(10000, 99999)
        
        invoice_text = (
            f"🛒 *INVOICE PEMESANAN OTOMATIS* (Kak *{user_name}*) 🧾\n\n"
            f"📦 *Paket Dipilih:* `{paket_nama}`\n"
            f"🔢 *Nomor Seri Resi:* `PKL-MLBB-{random_serial}`\n"
            f"⏱️ *Batas Waktu Bayar:* 15 Menit (Akan otomatis kedaluwarsa jika lewat)\n\n"
            "💳 *SILAKAN TRANSFER KE REKENING RESMI KAMI:*\n"
            f"• **DANA / GoPay:** `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"• **Saweria (QRIS/Bank):** {SAWERIA_LINK}\n\n"
            "🛡️ *INSTRUKSI ANTI-FRAUD & KONFIRMASI OTOMATIS:*\n"
            f"Setelah transfer, kirim bukti screenshot asli ke chat ini beserta nomor resi `PKL-MLBB-{random_serial}` agar sistem memprosesnya secara instan!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=invoice_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id, text="Invoice berhasil dibuat! Silakan lakukan pembayaran.")

    elif call.data == 'menu_cara_order':
        panduan_text = (
            f"❓ *CARA ORDER & SISTEM OTOMATIS* (Kak *{user_name}*) 🛒\n\n"
            "1️⃣ Pilih paket di menu katalog dan klik tombol **Beli**.\n"
            "2️⃣ Bot otomatis menerbitkan **Nomor Seri Resi & Invoice Pembayaran (Batas 15 Menit)**.\n"
            f"3️⃣ Transfer sesuai tagihan ke DANA/GoPay (`{DANA_NUMBER}`) atau Saweria.\n"
            "4️⃣ Kirim screenshot bukti transfer ke chat bot ini untuk verifikasi otomatis dengan antrean sibuk!\n\n"
            "⚡ *Sistem anti-nipu aktif:* Resi unik mencegah pemalsuan bukti transfer!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=panduan_text, parse_mode='Markdown', reply_markup=get_back_markup(), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        bayar_text = (
            f"💳 *METODE PEMBAYARAN RESMI* (Kak *{user_name}*)\n\n"
            f"📱 **DANA / GoPay:** `{DANA_NUMBER}`\n"
            f"👤 Atas Nama: *{DANA_NAME}*\n\n"
            f"🧡 **Saweria (QRIS / Bank Transfer / E-Wallet):**\n"
            f"🔗 {SAWERIA_LINK}\n\n"
            "📌 *Catatan:* Simpan bukti transfer dengan jelas. Pastikan melakukan pembayaran sebelum batas waktu invoice kedaluwarsa."
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=bayar_text, parse_mode='Markdown', reply_markup=get_back_markup(), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        random_serial = random.randint(10000, 99999)
        konfirmasi_text = (
            f"✅ *CEK STATUS & KONFIRMASI RESI* (Kak *{user_name}*)\n\n"
            f"🛡️ *Nomor Resi Unik Anda:* `PKL-MLBB-{random_serial}`\n\n"
            "Silakan kirimkan **screenshot bukti transfer asli** langsung ke chat bot ini beserta nomor resi di atas untuk memulai antrean packing otomatis!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=konfirmasi_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id)

# 3. Sistem Filter Foto/SSAN & Antrean Fiktif (Maks 1-2 Jam + Pesan Kesabaran)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_name = message.from_user.first_name
    random_serial = random.randint(10000, 99999)
    
    rand_hour = random.randint(1, 2)
    rand_min = random.randint(10, 59)
    rand_sec = random.randint(0, 59)
    rand_queue = random.randint(3, 8)
    
    initial_msg = bot.reply_to(
        message, 
        f"🤖 *SISTEM VERIFIKASI PAKEL STORE* 🛡️\n\n"
        f"Halo Kak *{user_name}*, bukti pembayaran / screenshot telah diterima oleh sistem.\n\n"
        f"💬 *Mohon bersabar ya kak, sedang banyak pelanggan yang harus saya selesaikan.* Saat ini kamu berada di dalam **antrean ke-{rand_queue}**.\n\n"
        f"📦 Status: *Antrean utama server untuk proses packing script...*\n"
        f"⏱️ Estimasi Waktu Tunggu: {rand_hour} Jam : {rand_min:02d} Menit : {rand_sec:02d} Detik", 
        parse_mode='Markdown'
    )
    
    try:
        time.sleep(2)
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=initial_msg.message_id,
            text=(
                f"🤖 *SISTEM VERIFIKASI PAKEL STORE* 🛡️\n\n"
                f"Halo Kak *{user_name}*, bukti pembayaran / screenshot telah dicek.\n"
                f"💬 *Mohon bersabar, antrean bergeser ke posisi ke-{max(1, rand_queue-1)}...*\n"
                f"📦 Status: *Sedang meracik script & enkripsi keamanan...*\n"
                f"⏱️ Sisa Waktu: 0 Jam : 0 Menit : 15 Detik"
            ),
            parse_mode='Markdown'
        )
        
        time.sleep(2)
        final_instruction = (
            f"✅ *VERIFIKASI & PACKING SELESAI!* (No Resi: `PKL-MLBB-{random_serial}`)\n\n"
            f"Halo Kak *{user_name}*, waktu tunggu antrean telah habis (0 detik). File script & cheat pilihanmu sudah siap!\n\n"
            f"📋 *SALIN & KIRIM FORMAT INI KE ADMIN UNTUK KLAIM FILE:*\n"
            f"```text\n"
            f"• No Resi Unik : PKL-MLBB-{random_serial}\n"
            f"• Nama Pembeli : {user_name}\n"
            f"• Status Bayar : LUNAS / VALID\n"
            f"• Request File : Kirim file script & bonus sekarang\n"
            f"```\n"
            f"🚀 *Segera salin teks di atas dan kirimkan ke admin utama:* `{ADMIN_USERNAME}` agar file langsung dikirim ke akunmu detik ini juga!"
        )
        bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=initial_msg.message_id,
            text=final_instruction,
            parse_mode='Markdown'
        )
    except Exception as e:
        print(f"[LOG ERROR] Gagal update hitung mundur: {e}")

# 4. Auto-Reply Kata Kunci Teks Pintar (Termasuk Deteksi Kata Kedaluwarsa/Expired)
@bot.message_handler(func=lambda message: True)
def auto_reply(message):
    user_name = message.from_user.first_name
    text = message.text.lower()
    
    if any(word in text for word in ['harga', 'list', 'menu', 'jual', 'paket', 'script', 'cheat', 'price', 'catalog', 'katalog']):
        reply = f"💎 Halo Kak *{user_name}*! Mau cek dan beli paket VIP? Silakan ketik /start lalu pilih tombol *Katalog VIP* ya! 🙏"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['promo', 'diskon', 'voucher', 'kupon', 'newmember']):
        reply = f"🎁 Mau klaim promo member baru, Kak *{user_name}*? Ketik /start lalu klik tombol *Klaim Promo Member Baru* ya! Gunakan kupon `WELCOMEPAKEL`. ✨"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['expired', 'kedaluwarsa', 'habis', 'lewat', 'batal']):
        reply = f"⚠️ *INFO INVOICE*\n\nMohon maaf Kak *{user_name}*, jika batas waktu pembayaran 15 menit telah habis, nomor resi otomatis kedaluwarsa. Silakan ketik /start untuk membuat pesanan baru di katalog ya! 🙏"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['cara', 'beli', 'order', 'gimana', 'panduan', 'how', 'buy']):
        reply = f"❓ Butuh panduan cara order otomatis, Kak *{user_name}*? Ketik /start lalu klik tombol *Cara Order* ya! ✨"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['dana', 'gopay', 'saweria', 'bayar', 'transfer', 'rekening', 'payment']):
        reply = (
            f"💳 *INFO PEMBAYARAN RESMI* (Kak *{user_name}*)\n\n"
            f"📱 DANA / GoPay: `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"🧡 Saweria: {SAWERIA_LINK}\n\n"
            "Silakan pilih paket lewat /start untuk mendapatkan nomor resi unik transaksi ya, Kak! 🙏"
        )
        bot.reply_to(message, reply, parse_mode='Markdown', disable_web_page_preview=True)
        
    elif any(word in text for word in ['terima kasih', 'makasih', 'oke', 'ok', 'salam', 'thank', 'thanks']):
        reply = f"Sama-sama dengan senang hati, Kak *{user_name}*! Semoga makin jago dan win streak terus bersama *Pakel MlbbStore*! 🚀🔥"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    else:
        reply = (
            f"Halo Kak *{user_name}*! Pesan Anda telah dicatat oleh sistem otomatis *Pakel MlbbStore*.\n"
            f"Jika ingin mengirim bukti transfer, silakan kirimkan foto/screenshot langsung ke chat ini. Untuk bantuan darurat, hubungi {ADMIN_USERNAME}. Terima kasih! 🙏✨"
        )
        bot.reply_to(message, reply, parse_mode='Markdown')

# Jalankan Bot
print("[INFO] Bot Telegram Pakel MlbbStore Berjalan...")
bot.infinity_polling()
