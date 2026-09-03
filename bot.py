import telebot
from telebot import types
import random
from datetime import datetime

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
    markup.add(types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama'))
    return markup

# 1. Perintah /start & /help (Menu Utama Rapi & Profesional)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user_name = message.from_user.first_name
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_katalog = types.InlineKeyboardButton("💎 Katalog VIP & Harga Paket", callback_data='menu_katalog')
    btn_promo = types.InlineKeyboardButton("🎁 Klaim Promo Member Baru", callback_data='menu_promo')
    btn_cara_order = types.InlineKeyboardButton("❓ Panduan Cara Order", callback_data='menu_cara_order')
    btn_bayar = types.InlineKeyboardButton("💳 Metode Pembayaran Resmi", callback_data='menu_bayar')
    btn_faq = types.InlineKeyboardButton("💡 FAQ / Pertanyaan Umum", callback_data='menu_faq')
    btn_konfirmasi = types.InlineKeyboardButton("✅ Cek Status & Konfirmasi Resi", callback_data='menu_konfirmasi')
    btn_admin = types.InlineKeyboardButton("💬 Hubungi Admin Resmi", url="https://t.me/PakelMlbbOfficial")
    
    markup.add(btn_katalog, btn_promo, btn_cara_order, btn_bayar, btn_faq, btn_konfirmasi, btn_admin)
    
    welcome_text = (
        f"🔥 *Halo, Kak {user_name}!* Selamat datang di Official *Pakel MlbbStore* 🙏✨\n\n"
        "Pusat layanan script custom damage, one hit, server lag panel, & drone view terlengkap dengan sistem otomatis tercanggih anti-nipu.\n\n"
        "👇 *Silakan pilih menu di bawah ini untuk mulai bertransaksi:*"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)

# Command Tambahan: /cekresi atau /resi
@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    user_name = message.from_user.first_name
    
    reply_text = (
        f"🔍 *CEK STATUS RESI PEMBELIAN* (Kak *{user_name}*)\n\n"
        "Silakan kirimkan **Nomor Resi Unik** milikmu (Contoh: `PKL-MLBB-12345`) atau kirimkan screenshot bukti transfer langsung ke chat ini.\n\n"
        f"💬 Konfirmasi lebih lanjut bisa langsung ke admin: {ADMIN_USERNAME}"
    )
    bot.reply_to(message, reply_text, parse_mode='Markdown')

# 2. Handler Tombol (Callback Query)
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_name = call.from_user.first_name
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'menu_utama':
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_katalog = types.InlineKeyboardButton("💎 Katalog VIP & Harga Paket", callback_data='menu_katalog')
        btn_promo = types.InlineKeyboardButton("🎁 Klaim Promo Member Baru", callback_data='menu_promo')
        btn_cara_order = types.InlineKeyboardButton("❓ Panduan Cara Order", callback_data='menu_cara_order')
        btn_bayar = types.InlineKeyboardButton("💳 Metode Pembayaran Resmi", callback_data='menu_bayar')
        btn_faq = types.InlineKeyboardButton("💡 FAQ / Pertanyaan Umum", callback_data='menu_faq')
        btn_konfirmasi = types.InlineKeyboardButton("✅ Cek Status & Konfirmasi Resi", callback_data='menu_konfirmasi')
        btn_admin = types.InlineKeyboardButton("💬 Hubungi Admin Resmi", url="https://t.me/PakelMlbbOfficial")
        markup.add(btn_katalog, btn_promo, btn_cara_order, btn_bayar, btn_faq, btn_konfirmasi, btn_admin)
        
        welcome_text = (
            f"🔥 *Halo kembali, Kak {user_name}!* 🙏\n"
            "Silakan pilih menu layanan resmi kami di bawah ini ya:"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=welcome_text, parse_mode='Markdown', reply_markup=markup)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_promo':
        promo_text = (
            f"🎁 *PROMO PELANGGAN BARU (NEW MEMBER)* (Kak *{user_name}*) 🎉\n\n"
            "Nikmati penawaran khusus pembelian pertama di *Pakel MlbbStore*:\n\n"
            "🎟️ **KODE KUPON:** `WELCOMEPAKEL`\n"
            "💰 **Keuntungan:** Potongan harga langsung / Diskon spesial di semua kategori paket VIP!\n\n"
            "📌 *Cara Pakai:*\n"
            "Sebutkan kode kupon `WELCOMEPAKEL` kepada admin saat konfirmasi pembayaran setelah memilih paket di katalog. Gampang banget! 🚀"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id, text="Kupon berhasil dilihat!")

    elif call.data == 'menu_faq':
        faq_text = (
            f"💡 *FAQ / PERTANYAAN UMUM* (Kak *{user_name}*)\n\n"
            "❓ *Q: Apakah script aman dari banned?*\n"
            "💬 A: Paket VIP kami dilengkapi enkripsi anti-detect tingkat tinggi, sangat aman digunakan jika mengikuti petunjuk.\n\n"
            "❓ *Q: Bagaimana cara pasang script-nya?*\n"
            "💬 A: Setelah pembayaran divalidasi admin, file script & panduan pemasangan lengkap akan langsung dikirim ke chat kamu.\n\n"
            "❓ *Q: Apakah dapat bonus tambahan?*\n"
            "💬 A: Ya! Setiap pembelian paket sudah otomatis mendapatkan bonus Panel Server Lag Musuh & Drone View X1-X10 gratis!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=faq_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        markup.add(types.InlineKeyboardButton("🛒 Beli: Natural Balance (Rp 120k)", callback_data='buy_natural'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Light VIP + Drone (Rp 95k)", callback_data='buy_light'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Semi-Safe 14 Hari (Rp 75k)", callback_data='buy_semisafe'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Lifetime Safe Permanent (Rp 200k)", callback_data='buy_lifetimesafe'))
        markup.add(types.InlineKeyboardButton("▶️ Lanjut ke Katalog Bagian 2 (One Hit)", callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama'))

        katalog_text = (
            f"🔥 *VIP EXCLUSIVE CATALOGUE - BAGIAN 1* (Kak *{user_name}*) 🔥\n"
            "*(Kategori: Custom Damage & Fair Play)*\n\n"
            
            "⚡ *BONUS SPESIAL FREE ALL PACKAGES:* \n"
            "🎁 Otomatis mendapatkan **Panel Server Lag Musuh** & **Drone View X1 - X10** gratis!\n\n"
            
            "📂 *KATEGORI 1: CUSTOM DAMAGE & FAIR PLAY* 🛡️\n"
            "• **Natural Balance (30 Hari):** Rp 120.000\n"
            "• **Light VIP + Drone (30 Hari):** Rp 95.000\n"
            "• **Semi-Safe (14 Hari):** Rp 75.000\n"
            "• **Lifetime Safe (Permanent):** Rp 200.000\n\n"
            "👇 *Pilih paket di bawah atau lanjut ke Bagian 2:*"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'katalog_part2':
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        markup.add(types.InlineKeyboardButton("🛒 Beli: Sultan One Hit 100% (Rp 150k)", callback_data='buy_sultan'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: VIP Pro One Hit 80% (Rp 100k)", callback_data='buy_pro'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Semi-Private 14 Hari (Rp 75k)", callback_data='buy_semiprivate'))
        markup.add(types.InlineKeyboardButton("🛒 Beli: Permanent Legend (Rp 250k)", callback_data='buy_permanent'))
        markup.add(types.InlineKeyboardButton("◀️ Kembali ke Katalog Bagian 1", callback_data='katalog_part1'))
        markup.add(types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama'))

        katalog_text = (
            f"🔥 *VIP EXCLUSIVE CATALOGUE - BAGIAN 2* (Kak *{user_name}*) 🔥\n"
            "*(Kategori: One Hit & High Class)*\n\n"
            
            "📂 *KATEGORI 2: ONE HIT & HIGH CLASS* 💥\n"
            "• **Sultan One Hit 100% (30 Hari):** Rp 150.000\n"
            "• **VIP Pro One Hit 80% (30 Hari):** Rp 100.000\n"
            "• **Semi-Private (14 Hari):** Rp 75.000\n"
            "• **Permanent Legend (Lifetime):** Rp 250.000\n\n"
            f"💳 *INFO PEMBAYARAN:* DANA/GoPay: `{DANA_NUMBER}`\n\n"
            "👇 *Pilih paket atau kembali ke Bagian 1:*"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, parse_mode='Markdown', reply_markup=markup, disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        paket_tipe = call.data.replace('buy_', '')
        
        if paket_tipe == 'natural':
            paket_nama = "Natural Balance (Rp 120.000)"
        elif paket_tipe == 'light':
            paket_nama = "Light VIP + Drone (Rp 95.000)"
        elif paket_tipe == 'semisafe':
            paket_nama = "Semi-Safe 14 Hari (Rp 75.000)"
        elif paket_tipe == 'lifetimesafe':
            paket_nama = "Lifetime Safe Permanent (Rp 200.000)"
        elif paket_tipe == 'sultan':
            paket_nama = "Sultan One Hit 100% (Rp 150.000)"
        elif paket_tipe == 'pro':
            paket_nama = "VIP Pro One Hit 80% (Rp 100.000)"
        elif paket_tipe == 'semiprivate':
            paket_nama = "Semi-Private 14 Hari (Rp 75.000)"
        elif paket_tipe == 'permanent':
            paket_nama = "Permanent Legend (Rp 250.000)"
        else:
            paket_nama = "Paket VIP Custom"

        random_serial = random.randint(10000, 99999)
        
        invoice_text = (
            f"🛒 *INVOICE PEMESANAN OTOMATIS* (Kak *{user_name}*) 🧾\n\n"
            f"📦 *Paket Dipilih:* `{paket_nama}`\n"
            f"🔢 *Nomor Seri Resi:* `PKL-MLBB-{random_serial}`\n"
            f"⏱️ *Batas Waktu Bayar:* 15 Menit\n\n"
            "💳 *SILAKAN TRANSFER KE REKENING RESMI KAMI:*\n"
            f"• **DANA / GoPay:** `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"• **Saweria (QRIS/Bank):** {SAWERIA_LINK}\n\n"
            "🛡️ *INSTRUKSI KONFIRMASI:*\n"
            f"Setelah melakukan pembayaran, silakan kirim bukti screenshot/foto transaksi beserta nomor resi di atas langsung ke admin utama: `{ADMIN_USERNAME}` agar pesananmu segera diproses!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=invoice_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id, text="Invoice berhasil dibuat! Silakan lakukan pembayaran.")

    elif call.data == 'menu_cara_order':
        panduan_text = (
            f"❓ *CARA ORDER & PANDUAN* (Kak *{user_name}*) 🛒\n\n"
            "1️⃣ Pilih paket di menu katalog dan klik tombol **Beli**.\n"
            "2️⃣ Bot otomatis menerbitkan **Nomor Seri Resi & Invoice Pembayaran**.\n"
            f"3️⃣ Transfer sesuai tagihan ke DANA/GoPay (`{DANA_NUMBER}`) atau Saweria.\n"
            f"4️⃣ Kirim screenshot bukti transfer & nomor resi langsung ke admin utama: `{ADMIN_USERNAME}`.\n\n"
            "⚡ *Aman & Terpercaya!*"
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
            f"📌 *Konfirmasi Pembayaran:* Kirim bukti transfer ke `{ADMIN_USERNAME}`."
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=bayar_text, parse_mode='Markdown', reply_markup=get_back_markup(), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        random_serial = random.randint(10000, 99999)
        konfirmasi_text = (
            f"✅ *KONFIRMASI PEMBAYARAN & RESI* (Kak *{user_name}*)\n\n"
            f"🛡️ *Contoh Nomor Resi:* `PKL-MLBB-{random_serial}`\n\n"
            f"Silakan kirimkan **screenshot bukti transfer asli** beserta nomor resi pesananmu langsung ke admin utama: `{ADMIN_USERNAME}` untuk diverifikasi dan dikirim filenya!"
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=konfirmasi_text, parse_mode='Markdown', reply_markup=get_back_markup())
        bot.answer_callback_query(call.id)

# 3. Handler Foto (Generate Resi, Waktu Real-Time, & Format Copy Text Siap Salin)
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_name = message.from_user.first_name
    random_serial = random.randint(10000, 99999)
    
    now = datetime.now()
    tanggal_str = now.strftime("%d-%m-%Y")
    jam_str = now.strftime("%H:%M:%S WIB")
    
    response_text = (
        f"✅ *BUKTI PEMBAYARAN DITERIMA & DICATAT* (Kak *{user_name}*)\n\n"
        f"🛡️ *No Resi Unik:* `PKL-MLBB-{random_serial}`\n"
        f"📅 *Tanggal:* {tanggal_str}\n"
        f"⏱️ *Jam:* {jam_str}\n\n"
        f"📋 *SALIN FORMAT DI BAWAH INI DAN KIRIM KE ADMIN:*\n"
        f"```text\n"
        f"• No Resi Unik : PKL-MLBB-{random_serial}\n"
        f"• Nama Pembeli : {user_name}\n"
        f"• Tanggal/Jam  : {tanggal_str} - {jam_str}\n"
        f"• Status Bayar : LUNAS / MENUNGGU CEK\n"
        f"• Request File : Kirim file script & bonus sekarang\n"
        f"```\n"
        f"🚀 *Segera salin teks dalam kotak di atas dan kirimkan langsung ke admin utama:* `{ADMIN_USERNAME}` agar file pesananmu langsung diproses!"
    )
    bot.reply_to(message, response_text, parse_mode='Markdown')

# 4. Auto-Reply Kata Kunci Teks Pintar
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
        
    elif any(word in text for word in ['cara', 'beli', 'order', 'gimana', 'panduan', 'how', 'buy']):
        reply = f"❓ Butuh panduan cara order, Kak *{user_name}*? Ketik /start lalu klik tombol *Cara Order* ya! ✨"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    elif any(word in text for word in ['dana', 'gopay', 'saweria', 'bayar', 'transfer', 'rekening', 'payment']):
        reply = (
            f"💳 *INFO PEMBAYARAN RESMI* (Kak *{user_name}*)\n\n"
            f"📱 DANA / GoPay: `{DANA_NUMBER}` (A/N: {DANA_NAME})\n"
            f"🧡 Saweria: {SAWERIA_LINK}\n\n"
            f"Silakan konfirmasi pembayaran ke admin: {ADMIN_USERNAME} ya, Kak! 🙏"
        )
        bot.reply_to(message, reply, parse_mode='Markdown', disable_web_page_preview=True)
        
    elif any(word in text for word in ['terima kasih', 'makasih', 'oke', 'ok', 'salam', 'thank', 'thanks']):
        reply = f"Sama-sama dengan senang hati, Kak *{user_name}*! Semoga makin jago dan win streak terus bersama *Pakel MlbbStore*! 🚀🔥"
        bot.reply_to(message, reply, parse_mode='Markdown')
        
    else:
        reply = (
            f"Halo Kak *{user_name}*! Pesan Anda telah diterima oleh sistem *Pakel MlbbStore*.\n"
            f"Untuk bantuan, pemesanan, atau konfirmasi bukti pembayaran, silakan langsung hubungi admin utama kami di: {ADMIN_USERNAME}. Terima kasih! 🙏✨"
        )
        bot.reply_to(message, reply, parse_mode='Markdown')

# Jalankan Bot
print("[INFO] Bot Telegram Pakel MlbbStore Berjalan...")
bot.infinity_polling()
