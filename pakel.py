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
        hari_en = now.strftime('%a')
        hari_str = days_indo.get(hari_en, hari_en)
        
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
        current_status_db = ""
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
                            current_status_db = status
                            
                            # PROTEKSI KETAT ANTI DUPLIKASI POIN
                            if status in ["BERHASIL", "DITOLAK", "CANCELLED", "EXPIRED"] and status_baru in ["BERHASIL", "DITOLAK", "CANCELLED"]:
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
            
            if target_chat_id and current_status_db not in ["BERHASIL", "DITOLAK", "CANCELLED", "EXPIRED"]:
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
        ("📢 <b>INFO PROMO SPESIAL HARI INI!</b> 🔥\n\nBuat Kakak yang mau ngebut <i>push rank</i> tanpa takut kena ban, buruan sikat script VIP kita sekarang!\n🎁 Spesial hari ini, ada potongan harga spesial + bonus <i>Server Lag Panel</i> dan <i>Drone View X10</i> gratis tanpa biaya tambahan.\n\n🛒 Langsung cek katalog lengkapnya di bot: @{bot_username}",),
        ("🛡️ <b>KENAPA HARUS PAKAI SCRIPT PAKEL MLBBSTORE?</b> ⚡\n\nJangan pertaruhkan akun sultan Kakak pakai script sembarangan yang gampang terdeteksi sistem Moonton!\nDi sini kita pakai enkripsi <i>high-tier anti-detect</i> paling stabil se-Indonesia, aman buat main di mode <i>Ranked</i> Mythic sekalipun.\n\n📦 Pilih paket andalan Kakak sekarang sebelum kehabisan slot: @{bot_username}",),
        ("⚡ <b>BONUS FREE ALL PACKAGES TANPA SYARAT!</b> 🎁\n\nSetiap pembelian paket apa saja di Official Pakel MlbbStore, Kakak bakal otomatis dapet:\n• Panel Server Lag Musuh (<i>Global Ping Spikes</i>) 🌐\n• Drone View Eksklusif Ultra Wide X1 - X10 🦅\n\n🚀 Yuk dominasi permainan sekarang juga! Order gampang via bot: @{bot_username}",),
        ("🏆 <b>MAU JADI TOP GLOBAL ATAU NYAMPE MYTHIC GLORY DENGAN CEPAT?</b> 🔥\n\nWaktunya buktikan kemampuan terbaikmu di Land of Dawn! Gunakan <i>Custom Damage</i> dan <i>Light VIP</i> dari Pakel MlbbStore biar gameplay makin gampang dan mulus.\n\n💬 Cek riwayat pesanan, klaim kupon, atau pilih paket langsung di: @{bot_username}",),
        ("🌟 <b>PEMBERITAHUAN UPDATE STOK & TESTIMONI HARIAN</b> 🚀\n\nRatusan player sudah membuktikan sendiri kestabilan script kita hari ini tanpa kendala. Giliran Kakak nih buat rasain bedanya pas war!\n💎 Proses cepat, amanah, dan dibimbing sampai beres.\n\n👇 Yuk amankan paket pilihanmu langsung di bot: @{bot_username}",),
        ("💥 <b>SPECIAL EDITION: SULTAN ONE HIT & INSTANT KILL</b> ⚡\n\nMau ngerasain dominasi mutlak di setiap pertandingan? Paket <i>Sultan One Hit</i> siap bikin musuh kewalahan dan rata dalam sekejap!\n🛡️ Dilengkapi sistem pengaman kelas atas agar akun tetap aman sentosa.\n\n🛒 Sikat promonya sekarang lewat bot: @{bot_username}",),
        ("🎁 <b>CEK SALDO POIN & KUPON MEMBER KAMU!</b> 💳\n\nTahukah Kakak? Setiap transaksi sukses di Official Pakel MlbbStore, Kakak bakal otomatis dapet tambahan Poin Loyalitas lho!\n🪙 Poinnya bisa ditukar buat bayar paket script gratis tanpa perlu transfer rupiah lagi. Mantap kan?\n\n✨ Yuk cek poinmu sekarang di bot: @{bot_username}",),
        ("🌐 <b>BASMI LAG & FPS DROP SAAT WAR BERSAMA KITA!</b> 📉➡️📈\n\nKesel banget kan pas lagi momen penting malah patah-patah atau sinyal mendadak merah? Tenang, script kita sudah include fitur *Server Lag Panel* buat stabilin permainan.\n🎯 Main jadi lebih PeDe, mulus, dan bebas hambatan!\n\n📦 Langsung pilih paketnya di sini: @{bot_username}",),
        ("⏰ <b>WAKTU TERBATAS: GASPOL PUSH RANK AKHIR SEASON!</b> ⏳\n\nJangan biarkan bintangmu turun atau stuck di satu tier terus! Maksimalkan performa permainanmu dengan script premium anti-detect terpercaya se-Indonesia.\n⚡ Dijamin ampuh buat bantu naik tier dengan mulus.\n\n🚀 Amankan paketmu sekarang juga via bot: @{bot_username}",),
        ("👋 <b>HALO KAKAK-KAKAK PLAYER MLBB INDONESIA!</b> 🎮✨\n\nMau mabar bareng squad tapi minder sama performa hero? Jangan khawatir, Official Pakel MlbbStore selalu siap jadi solusi terbaik buat naikin performa game kamu hari ini.\n💎 Aman, stabil, dan bergaransi.\n\n👇 Yuk langsung mampir ke katalog bot: @{bot_username}",)
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
            template_pilihan = random.choice(broadcast_templates)[0]
            pesan_final = template_pilihan.format(bot_username=bot.get_me().username)
            for chat_id in set(users):
                try:
                    bot.send_message(chat_id=chat_id, text=f"📢 <b>PENGUMUMAN OTOMATIS</b>\n\n{pesan_final}", parse_mode="HTML", disable_web_page_preview=True)
                    time.sleep(0.05)
                except Exception:
                    pass
        except Exception as e:
            print(f"[AUTO-BROADCAST ERROR]: {e}")
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
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥\n*(Kategori: Custom Damage High-Tier & Fair Play Anti-Detect)*",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥\n*(Kategori: Sultan One Hit Instan & Dominasi Mutlak)*",
        'bonus_txt': "⚡ BONUS SPESIAL FREE ALL PACKAGES (TANPA BIAYA TAMBAHAN): \n🎁 Setiap pembelian paket apa saja, otomatis mendapatkan:\n  • Panel Server Lag Musuh (Global Ping Spikes)\n  • Drone View Eksklusif X1 sampai X10 (Ultra Wide View)\n\n📂 SILAKAN PILIH SCRIPT & PELAJARI DETAIL FITUR DI BAWAH INI:",
        'p1_normal': [
            ("🛒 Beli: Natural Balance (Rp 120k / 30 Poin)", "buy_natural", "• 👑 <b>Paket Natural Balance (30 Hari)</b> — Rp 120.000 (Atau tukar 30 Poin)\n  └ 🎯 <b>Fungsi:</b> Dirancang khusus untuk pemain yang mengutamakan keamanan akun. Pengaturan damage dapat disesuaikan secara mandiri (seperti 2 hit yang tidak mencolok), sehingga performa tetap optimal namun senyap[span_0](start_span)[span_0](end_span)."),
            ("🛒 Beli: Light VIP + Drone (Rp 95k / 25 Poin)", "buy_light", "• ⚡ <b>Paket Light VIP + Drone (30 Hari)</b> — Rp 95.000 (Atau tukar 25 Poin)\n  └ 🎯 <b>Fungsi:</b> Pilihan ekonomis untuk pemakaian bulanan. Kombinasi pas antara damage yang disetel wajar agar tidak terlihat brutal, ditambah pandangan map yang lebih luas untuk membaca pergerakan lawan[span_1](start_span)[span_1](end_span)."),
            ("🛒 Beli: Semi-Safe 14 Hari (Rp 75k / 20 Poin)", "buy_semisafe", "• 🛡️ <b>Paket Semi-Safe (14 Hari)</b> — Rp 75.000 (Atau tukar 20 Poin)\n  └ 🎯 <b>Fungsi:</b> Paket harian yang sangat terjangkau. Menghadirkan setelan damage fleksibel yang terkontrol serta kestabilan koneksi yang terjaga selama dua minggu penuh[span_2](start_span)[span_2](end_span)."),
            ("🛒 Beli: Lifetime Safe (Rp 200k / 50 Poin)", "buy_lifetimesafe", "• 👑 <b>Paket Lifetime Safe (Permanent)</b> — Rp 200.000 (Atau tukar 50 Poin)\n  └ 🎯 <b>Fungsi:</b> Solusi hemat jangka panjang tanpa biaya langganan bulanan. Memberikan akses selamanya dengan fitur damage fleksibel yang aman dan stabil digunakan sewaktu-waktu[span_3](start_span)[span_3](end_span).")
        ],
        'p1_promo': [
            ("🛒 Natural Balance (Hemat 10k / 30 Poin)", "buy_natural", "• 👑 <b>Paket Natural Balance (30 Hari)</b> — <s>Rp 120.000</s> <b>Rp 110.000</b> (Hemat Rp 10.000 / Tukar 30 Poin)\n  └ 🎯 <b>Fungsi:</b> Dirancang khusus untuk pemain yang mengutamakan keamanan akun. Pengaturan damage dapat disesuaikan secara mandiri (seperti 2 hit yang tidak mencolok)[span_4](start_span)[span_4](end_span)."),
            ("🛒 Light VIP + Drone (Hemat 10k / 25 Poin)", "buy_light", "• ⚡ <b>Paket Light VIP + Drone (30 Hari)</b> — <s>Rp 95.000</s> <b>Rp 85.000</b> (Hemat Rp 10.000 / Tukar 25 Poin)\n  └ 🎯 <b>Fungsi:</b> Pilihan ekonomis pemakaian bulanan. Kombinasi damage wajar + pandangan map luas[span_5](start_span)[span_5](end_span)."),
            ("🛒 Semi-Safe 14 Hari (Hemat 10k / 20 Poin)", "buy_semisafe", "• 🛡️ <b>Paket Semi-Safe (14 Hari)</b> — <s>Rp 75.000</s> <b>Rp 65.000</b> (Hemat Rp 10.000 / Tukar 20 Poin)\n  └ 🎯 <b>Fungsi:</b> Paket harian terjangkau dengan setelan damage terkontrol & koneksi stabil[span_6](start_span)[span_6](end_span)."),
            ("🛒 Lifetime Safe (Hemat 10k / 50 Poin)", "buy_lifetimesafe", "• 👑 <b>Paket Lifetime Safe (Permanent)</b> — <s>Rp 200.000</s> <b>Rp 190.000</b> (Hemat Rp 10.000 / Tukar 50 Poin)\n  └ 🎯 <b>Fungsi:</b> Solusi hemat jangka panjang tanpa biaya langganan bulanan[span_7](start_span)[span_7](end_span).")
        ],
        'p2_normal': [
            ("🛒 Beli: Sultan One Hit (Rp 150k / 40 Poin)", "buy_sultan", "• 💥 <b>Paket Sultan One Hit 100% (30 Hari)</b> — Rp 150.000 (Atau tukar 40 Poin)\n  └ 🎯 <b>Fungsi:</b> Damage tembus batas, instant kill musuh dalam sekali hit, bypass anti-cheat paling aman, khusus untuk player serius[span_8](start_span)[span_8](end_span)."),
            ("🛒 Beli: VIP Pro One Hit (Rp 100k / 30 Poin)", "buy_pro", "• ⚡ <b>Paket VIP Pro One Hit 80% (30 Hari)</b> — Rp 100.000 (Atau tukar 30 Poin)\n  └ 🎯 <b>Fungsi:</b> Udah dapet damage sakit, semua skin kebuka, pandangan luas, lengkap jadi satu! Paling dicari para top global[span_9](start_span)[span_9](end_span)."),
            ("🛒 Beli: Semi-Private 14 Hari (Rp 75k / 20 Poin)", "buy_semiprivate", "• 🔒 <b>Paket Semi-Private (14 Hari)</b> — Rp 75.000 (Atau tukar 20 Poin)\n  └ 🎯 <b>Fungsi:</b> Performanya stabil, anti patah-patah dijamin lancar jaya buat bantai musuh seharian[span_10](start_span)[span_10](end_span)."),
            ("🛒 Beli: Permanent Legend (Rp 250k / 60 Poin)", "buy_permanent", "• 🏆 <b>Paket Permanent Legend (Lifetime)</b> — Rp 250.000 (Atau tukar 60 Poin)\n  └ 🎯 <b>Fungsi:</b> Sekali bayar, nikmati update script seumur hidup tanpa perlu perpanjang langganan tiap bulan. Auto untung buat jangka panjang[span_11](start_span)[span_11](end_span)!")
        ],
        'p2_promo': [
            ("🛒 Sultan One Hit (Hemat 10k / 40 Poin)", "buy_sultan", "• 💥 <b>Paket Sultan One Hit 100% (30 Hari)</b> — <s>Rp 150.000</s> <b>Rp 140.000</b> (Hemat Rp 10.000 / Tukar 40 Poin)\n  └ 🎯 <b>Fungsi:</b> Damage tembus batas, instant kill musuh dalam sekali hit[span_12](start_span)[span_12](end_span)."),
            ("🛒 VIP Pro One Hit (Hemat 10k / 30 Poin)", "buy_pro", "• ⚡ <b>Paket VIP Pro One Hit 80% (30 Hari)</b> — <s>Rp 100.000</s> <b>Rp 90.000</b> (Hemat Rp 10.000 / Tukar 30 Poin)\n  └ 🎯 <b>Fungsi:</b> Damage sakit, unlock all skin & drone view lengkap jadi satu[span_13](start_span)[span_13](end_span)."),
            ("🛒 Semi-Private 14 Hari (Hemat 10k / 20 Poin)", "buy_semiprivate", "• 🔒 <b>Paket Semi-Private (14 Hari)</b> — <s>Rp 75.000</s> <b>Rp 65.000</b> (Hemat Rp 10.000 / Tukar 20 Poin)\n  └ 🎯 <b>Fungsi:</b> Performa stabil, anti patah-patah buat bantai musuh seharian[span_14](start_span)[span_14](end_span)."),
            ("🛒 Permanent Legend (Hemat 10k / 60 Poin)", "buy_permanent", "• 🏆 <b>Paket Permanent Legend (Lifetime)</b> — <s>Rp 250.000</s> <b>Rp 240.000</b> (Hemat Rp 10.000 / Tukar 60 Poin)\n  └ 🎯 <b>Fungsi:</b> Sekali bayar untuk update seumur hidup tanpa perpanjang bulanan[span_15](start_span)[span_15](end_span).")
        ],
        'next_1': "▶️ Lanjut ke Katalog Bagian 2 (Sultan One Hit)",
        'prev_2': "◀️ Kembali ke Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': (
            "💳 SILAKAN PILIH METODE PEMBAYARAN DI BAWAH INI:\n\n"
            "1️⃣ QRIS (CROSS-BORDER / ALL E-WALLET):\n"
            "   ⚠️ <b>Mohon Maaf, QRIS Saat Ini Sedang Gangguan / Error!</b>\n\n"
            "2️⃣ TRANSFER MANUAL DANA / GOPAY (RECOMMENDED):\n"
            f"   • Nomor: <code>{INFO_DANA}</code>\n"
            "   • Atas Nama: PakelMlbb\n\n"
            "3️⃣ SAWERIA (Support Kartu & E-Wallet):\n"
            f"   • Link: {INFO_SAWERIA}\n"
        ),
        'confirm_instr': "🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\nSetelah sukses membayar via transfer manual, silakan kirim Screenshot Bukti Transfer ke bot ini untuk mendapatkan Resi Unik.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue & Pricing", 'btn_testi': "🌟 Live Testimonials",
        'btn_riwayat': "📦 My Order History", 'btn_promo': "🎁 Claim Promo & Points",
        'btn_cara_order': "❓ How to Order", 'btn_bayar': "💳 Payments",
        'btn_faq': "💡 FAQ", 'btn_konfirmasi': "✅ Check Status",
        'btn_admin': "💬 Contact Admin", 'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS:", 'p1_normal': [("🛒 Buy: Natural Balance", "buy_natural", "• Natural Balance")],
        'p1_promo': [("🛒 Buy: Natural Balance (Promo)", "buy_natural", "• Natural Balance")],
        'p2_normal': [("🛒 Buy: Sultan One Hit", "buy_sultan", "• Sultan One Hit")],
        'p2_promo': [("🛒 Buy: Sultan One Hit (Promo)", "buy_sultan", "• Sultan One Hit")],
        'next_1': "▶️ Next", 'prev_2': "◀️ Back", 'inv_title': "🛒 INVOICE",
        'pay_info': "💳 Payment Info", 'confirm_instr': "🛡️ Send screenshot.",
    }
}

def get_lang(user):
    code = getattr(user, 'language_code', 'en')
    if code and code.lower().startswith('id'):
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
    success = 0
    for chat_id in set(users):
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI PAKEL MLBBSTORE</b>\n\n{pesan_bc}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ Broadcast Umum Selesai! Berhasil: {success}")

@bot.message_handler(commands=['bcs'])
def broadcast_buyers_only(message):
    pesan_bcs = message.text.replace('/bcs', '').strip()
    if not pesan_bcs:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /bcs Info khusus VIP!")
        return
    buyer_ids = set()
    try:
        with open("orders.txt", "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8 and parts[7].strip() == "BERHASIL":
                    buyer_ids.add(parts[0].strip())
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Belum ada data pesanan sukses.")
        return
    success = 0
    for chat_id in buyer_ids:
        try:
            bot.send_message(chat_id, f"💎 <b>INFO KHUSUS PELANGGAN SETIA PAKEL MLBBSTORE</b>\n\n{pesan_bcs}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ Broadcast Khusus VIP Selesai! Berhasil: {success}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    user = message.from_user
    save_user(message.chat.id)
    l = get_lang(user)
    t = TRANSLATIONS[l]
    greeting = get_time_greeting()
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
    
    if l == 'id':
        welcome_text = (
            f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n"
            f"🪙 Saldo Poin Loyalitas Anda: <b>{user_points} Poin</b>\n\n"
            "Pusat layanan script cheat Mobile Legends premium terpercaya, anti-detect kelas atas, server lag panel, & drone view paling stabil se-Indonesia.\n\n"
        )
        if not is_open:
            welcome_text += f"{store_msg}\n\n"
        welcome_text += "👇 Silakan pilih menu di bawah ini untuk mulai berbelanja:"
    else:
        welcome_text = f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n🪙 Your Loyalty Points: <b>{user_points} Poin</b>\n\n👇 Please select a menu below:"
        
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['riwayat', 'history'])
def cmd_riwayat(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    get_latest_user_order_data(message.chat.id)
    orders = get_user_orders(message.chat.id)
    if not orders:
        text = f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n❌ Belum ada riwayat pesanan tercatat.\n💡 Silakan pilih paket di /katalog untuk melakukan pemesanan baru!"
    else:
        text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
        for idx, o in enumerate(orders[-5:], 1):
            st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK", "CANCELLED": "❌ DIBATALKAN OLEH PEMBELI", "EXPIRED": "⌛ EXPIRED (Waktu 15 Menit Habis)"}.get(o['status'], "⏳ PENDING")
            text += f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n   • No Resi: <code>{o['resi']}</code>\n   • Waktu: {o['hari']}, {o['tanggal']} ({o['jam']})\n   • Status: {st}\n\n"
        text += "💡 <i>Kirim bukti transfer jika belum dikonfirmasi admin!</i>"
    bot.reply_to(message, text, reply_markup=get_back_markup(l), parse_mode="HTML", disable_web_page_preview=True)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    text = f"🔍 CEK STATUS RESI PEMBELIAN VIP (Kak {user.first_name})\n\nKirimkan Nomor Resi Unik atau screenshot bukti transfer ke sini.\n\n💬 Admin: {ADMIN_USERNAME}" if l == 'id' else f"🔍 CHECK RECEIPT STATUS ({user.first_name})"
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
    katalog_text += f"\n\n🪙 Saldo Poin Anda: <b>{get_user_points(message.chat.id)} Poin</b>"
    if coupon_status == "AVAILABLE":
        katalog_text += "\n🎁 <b>INFO PROMO:</b> Anda memiliki hak potong harga spesial member baru otomatis di katalog ini!"
    bot.send_message(message.chat.id, katalog_text, reply_markup=markup, parse_mode="HTML")

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
        ("💎 Natural Balance (30 Hari)", "sc_buy_natural"), ("⚡ Light VIP + Drone (30 Hari)", "sc_buy_light"),
        ("🛡️ Semi-Safe 14 Hari", "sc_buy_semisafe"), ("👑 Lifetime Safe Permanent", "sc_buy_lifetimesafe"),
        ("💥 Sultan One Hit 100% (30 Hari)", "sc_buy_sultan"), ("⚡ VIP Pro One Hit 80% (30 Hari)", "sc_buy_pro"),
        ("🔒 Semi-Private 14 Hari", "sc_buy_semiprivate"), ("🏆 Permanent Legend (Lifetime)", "sc_buy_permanent")
    ]
    for btn_text, cb_data in packages:
        markup.add(types.InlineKeyboardButton(btn_text, callback_data=f"{cb_data}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target Pembeli: <b>{target_buyer}</b>\n👇 Silakan pilih paket script yang dibeli:", reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['testi', 'push'])
def admin_push_testi(message):
    try:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(), message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        bot.reply_to(message, "✅ Berhasil! Testimoni real-time baru saja dikirim ke grup komunitas utama.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal mengirim testimoni: {e}")
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    save_user(call.message.chat.id)
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS[l]
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    greeting = get_time_greeting()

    if call.data.startswith('cancel_'):
        resi_target = call.data.replace('cancel_', '')
        admin_msg_id = None
        try:
            with open("orders.txt", "r") as f:
                for line in f:
                    p = line.strip().split('|')
                    if len(p) >= 12 and p[6].strip() == resi_target.strip():
                        if p[7].strip() != "PENDING":
                            bot.answer_callback_query(call.id, text="Pesanan sudah diproses atau kadaluwarsa.", show_alert=True)
                            return
                        admin_msg_id = int(p[11]) if p[11].isdigit() else None
                        break
        except Exception:
            pass

        success = update_order_status_by_resi(resi_target, "CANCELLED")
        if success:
            if admin_msg_id:
                try:
                    new_admin_caption = f"❌ <b>[DIBATALKAN OLEH PEMBELI]</b>\n\n<b>STATUS: ❌ DIBATALKAN USER (Poin/Kupon Dikembalikan)</b>"
                    bot.edit_message_caption(chat_id=GROUP_PAY_ID, message_id=admin_msg_id, caption=new_admin_caption, parse_mode="HTML", reply_markup=None)
                except Exception as e:
                    print(f"[EDIT ADMIN MSG CANCEL ERROR]: {e}")

            cancel_text = (
                f"❌ <b>PESANAN BERHASIL DIBATALKAN</b> ❌\n\n"
                f"🔑 No Resi: <code>{resi_target}</code>\n"
                "Pesanan ini telah dibatalkan atas permintaan Anda.\n"
                "💡 Hak kupon/diskon member baru serta saldo poin Anda telah dikembalikan secara otomatis. Silakan pilih ulang paket di katalog!"
            )
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=cancel_text, parse_mode="HTML", reply_markup=get_back_markup(l))
            except Exception:
                bot.send_message(chat_id, cancel_text, parse_mode="HTML", reply_markup=get_back_markup(l))
            bot.answer_callback_query(call.id, text="Pesanan berhasil dibatalkan!")
        else:
            bot.answer_callback_query(call.id, text="Gagal membatalkan pesanan atau sudah kadaluwarsa.", show_alert=True)
        return

    if call.data.startswith('paymode_'):
        parts = call.data.split('|')
        if len(parts) < 3:
            bot.answer_callback_query(call.id, text="Data pembayaran tidak valid.", show_alert=True)
            return
            
        action_type, paket_code = parts[1], parts[2]
        paket_dict = {
            'buy_natural': ("Natural Balance (30 Hari)", "Rp 120.000", 30),
            'buy_light': ("Light VIP + Drone (30 Hari)", "Rp 95.000", 25),
            'buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000", 20),
            'buy_lifetimesafe': ("Lifetime Safe Permanent", "Rp 200.000", 50),
            'buy_sultan': ("Sultan One Hit 100% (30 Hari)", "Rp 150.000", 40),
            'buy_pro': ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000", 30),
            'buy_semiprivate': ("Semi-Private 14 Hari", "Rp 75.000", 20),
            'buy_permanent': ("Permanent Legend (Lifetime)", "Rp 250.000", 60)
        }
        p_name, p_price, p_points = paket_dict.get(paket_code, ("VIP Package", "Rp 100.000", 30))
        resi_unik = f"PKL-MLBB-{random.randint(10000, 99999)}"
        
        if action_type == 'poin':
            user_pts = get_user_points(chat_id)
            if user_pts >= p_points:
                coupon_status = get_user_coupon_status(chat_id)
                if coupon_status == "AVAILABLE":
                    set_user_coupon_status(chat_id, "PENDING")

                pending_poin_text = (
                    f"🪙 <b>INVOICE PEMBAYARAN VIA POIN (PENDING)</b> 🪙\n\n"
                    f"📦 Paket: {p_name}\n"
                    f"🪙 Poin yang Akan Dipotong: <b>{p_points} Poin</b> (Sisa Poin Anda: {user_pts} Poin)\n"
                    f"🔑 No Resi: <code>{resi_unik}</code>\n"
                    f"⏱️ Status: Menunggu Verifikasi & ACC dari Admin.\n\n"
                    "💡 <i>Tenang Kak, poin Anda sama sekali belum dipotong sebelum admin meng-ACC pesanan ini!</i>"
                )
                
                markup_poin_inv = types.InlineKeyboardMarkup(row_width=1)
                markup_poin_inv.add(
                    types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                    types.InlineKeyboardButton("📦 Cek Riwayat Pesanan Saya", callback_data='menu_riwayat'),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )

                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    pass
                
                bot.send_message(chat_id, pending_poin_text, reply_markup=markup_poin_inv, parse_mode="HTML")
                
                try:
                    report_admin_poin = (
                        "🪙 <b>ADA KLAIM PEMBAYARAN VIA POIN MASUK!</b> 🪙\n\n"
                        f"👤 Dari User: @{user.username if user.username else user.first_name} (ID: <code>{chat_id}</code>)\n"
                        f"📦 Paket: {p_name}\n"
                        f"🪙 Nominal Poin: <b>{p_points} Poin</b> (Saldo User: {user_pts} Poin)\n"
                        f"🔑 No Resi: <code>{resi_unik}</code>\n\n"
                        "👇 <i>Silakan klik ACC untuk memotong poin & menyetujui, atau TOLAK jika ingin membatalkan!</i>"
                    )
                    markup_admin_poin = types.InlineKeyboardMarkup(row_width=2)
                    markup_admin_poin.add(
                        types.InlineKeyboardButton("✅ ACC POIN", callback_data=f"apoin|{resi_unik}"),
                        types.InlineKeyboardButton("❌ TOLAK POIN", callback_data=f"tpoin|{resi_unik}")
                    )
                    admin_sent = bot.send_message(GROUP_PAY_ID, report_admin_poin, message_thread_id=GROUP_PAY_TOPIC_ID, parse_mode="HTML", reply_markup=markup_admin_poin)
                    
                    # SIMPAN ORDER DENGAN MEREKAM ADMIN_MSG_ID
                    save_order(chat_id, p_name, f"{p_points} Poin", resi_unik, payment_method="POIN", point_cost=p_points, admin_msg_id=admin_sent.message_id)
                except Exception as e:
                    print(f"[REPORT ADMIN POIN ERROR]: {e}")
                    save_order(chat_id, p_name, f"{p_points} Poin", resi_unik, payment_method="POIN", point_cost=p_points, admin_msg_id=0)
                    
                bot.answer_callback_query(call.id, text="Invoice poin diterbitkan, menunggu ACC admin!")
                return
            else:
                markup_fallback = types.InlineKeyboardMarkup(row_width=1)
                markup_fallback.add(
                    types.InlineKeyboardButton(f"💳 Lanjut Bayar Via Transfer Saja ({p_price})", callback_data=f"paymode_|transfer|{paket_code}"),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )
                fail_text = f"❌ <b>MAAF, POIN ANDA BELUM CUKUP!</b>\nPoin Anda: {user_pts} | Butuh: {p_points} Poin"
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=fail_text, parse_mode="HTML", reply_markup=markup_fallback)
                except Exception:
                    bot.send_message(chat_id, fail_text, parse_mode="HTML", reply_markup=markup_fallback)
                bot.answer_callback_query(call.id, text="Poin tidak mencukupi!", show_alert=True)
                return

        elif action_type == 'transfer':
            coupon_status = get_user_coupon_status(chat_id)
            is_promo_used = (coupon_status == "AVAILABLE")
            
            save_order(chat_id, p_name, p_price, resi_unik, payment_method="TRANSFER", point_cost=0, admin_msg_id=0)
            if is_promo_used:
                set_user_coupon_status(chat_id, "PENDING")
                
            invoice_text = (
                f"{t['inv_title'].format(name=user.first_name)}\n\n"
                f"📦 Paket Dipilih: {p_name}\n💵 Harga: {p_price}"
            )
            if is_promo_used:
                invoice_text += " <i>(Sudah termasuk Potongan Promo Member Baru ✨)</i>"
            invoice_text += f"\n🔢 Nomor Resi Unik: <code>{resi_unik}</code>\n⏱️ Batas Waktu: 15 Menit\n\n{t['pay_info']}\n\n{t['confirm_instr']}\n👉 Admin: {ADMIN_USERNAME}"
            
            markup_inv = types.InlineKeyboardMarkup(row_width=1)
            markup_inv.add(
                types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                types.InlineKeyboardButton("📦 Cek Riwayat Pesanan Saya", callback_data='menu_riwayat'),
                types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
            )
            try:
                bot.delete_message(chat_id=chat_id, message_id=message_id)
            except Exception:
                pass
            bot.send_message(chat_id, invoice_text, reply_markup=markup_inv, parse_mode="HTML", disable_web_page_preview=True)
            bot.answer_callback_query(call.id, text="Invoice transfer diterbitkan!")
            return
    if call.data.startswith('acc_') or call.data.startswith('tolak_') or call.data.startswith('acc|') or call.data.startswith('tolak|') or call.data.startswith('apoin|') or call.data.startswith('tpoin|'):
        try:
            sep = '|' if '|' in call.data else '_'
            parts = call.data.split(sep)
            if len(parts) < 2:
                bot.answer_callback_query(call.id, text="Format tombol tidak valid.", show_alert=True)
                return
                
            action = parts[0].replace('_', '')
            resi_code = parts[1] if action in ['apoin', 'tpoin'] else parts[2]
            target_user_id = parts[1] if action not in ['apoin', 'tpoin'] else None

            if action in ['apoin', 'tpoin']:
                try:
                    with open("orders.txt", "r") as f:
                        for line in f:
                            p = line.strip().split('|')
                            if len(p) >= 11 and p[6].strip() == resi_code.strip():
                                target_user_id = p[0]
                                break
                except Exception:
                    pass

            if not target_user_id:
                bot.answer_callback_query(call.id, text="Gagal: Data user dari resi tidak ditemukan di database!", show_alert=True)
                return

            original_text = call.message.caption or call.message.text or ""

            if action == 'acc' or action == 'apoin':
                p_points_val = 0
                if action == 'apoin':
                    try:
                        with open("orders.txt", "r") as f:
                            for line in f:
                                p = line.strip().split('|')
                                if len(p) >= 11 and p[6].strip() == resi_code.strip():
                                    p_points_val = int(p[10]) if p[10].isdigit() else 0
                                    break
                    except Exception:
                        pass
                    
                    current_user_pts = get_user_points(target_user_id)
                    if current_user_pts >= p_points_val:
                        reduce_user_points(target_user_id, p_points_val)
                    else:
                        bot.answer_callback_query(call.id, text="Gagal ACC: Saldo poin pembeli tidak mencukupi!", show_alert=True)
                        return

                update_order_status_by_resi(resi_code, "BERHASIL")
                
                status_label = f"✅ DI-ACC ADMIN (Poin Dipotong {p_points_val} & Kupon Hangus)" if action == 'apoin' else "✅ TELAH DI-ACC OLEH ADMIN (Kupon Hangus & Poin Ditambahkan)"
                new_admin_text = original_text + f"\n\n<b>STATUS: {status_label}</b>"
                
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)

                detail_paket, detail_harga = "VIP Package", "Rp 100.000"
                try:
                    with open("orders.txt", "r") as f:
                        for line in f:
                            p = line.strip().split('|')
                            if len(p) >= 8 and p[6].strip() == resi_code.strip():
                                detail_paket, detail_harga = p[4], p[5]
                                break
                except Exception:
                    pass

                bot.send_message(target_user_id, f"🎉 <b>PEMBAYARAN ANDA TELAH DI-ACC ADMIN!</b> 🎉\nResi: <code>{resi_code}</code>", parse_mode="HTML")
                
                markup_rating = types.InlineKeyboardMarkup(row_width=5)
                markup_rating.add(
                    types.InlineKeyboardButton("⭐ 1", callback_data=f"rate|1|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 2", callback_data=f"rate|2|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 3", callback_data=f"rate|3|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 4", callback_data=f"rate|4|{resi_code}"),
                    types.InlineKeyboardButton("⭐ 5", callback_data=f"rate|5|{resi_code}")
                )
                bot.send_message(target_user_id, "⭐ <b>BAGAIMANA PELAYANAN KAMI, KAK?</b> ⭐\nSilakan berikan penilaian bintang:", reply_markup=markup_rating, parse_mode="HTML")
                bot.answer_callback_query(call.id, text="Pembayaran di-ACC!")

            elif action == 'tolak' or action == 'tpoin':
                update_order_status_by_resi(resi_code, "DITOLAK")
                new_admin_text = original_text + "\n\n<b>STATUS: ❌ DITOLAK OLEH ADMIN (Kupon & Poin Dikembalikan)</b>"
                if call.message.content_type == 'photo':
                    bot.edit_message_caption(chat_id=chat_id, message_id=message_id, caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                else:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=new_admin_text, parse_mode="HTML", reply_markup=None)
                bot.send_message(target_user_id, f"❌ <b>MOHON MAAF, PEMBAYARAN DITOLAK</b>\nResi: <code>{resi_code}</code>", parse_mode="HTML")
                bot.answer_callback_query(call.id, text="Pembayaran ditolak & kupon/poin dikembalikan!")
        except Exception as e:
            bot.answer_callback_query(call.id, text=f"Error: {e}", show_alert=True)
        return

    if call.data.startswith('sc_buy_'):
        try:
            data_split = call.data.split('|')
            if len(data_split) < 2:
                return
            action, buyer_name = data_split[0], data_split[1]
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
            p_nama, p_hrg = paket_map.get(action, ("VIP Package", "Rp 100.000"))
            post_text = (
                "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                f"✅ Buyer ID: {buyer_name}\n📦 Item Purchased: {p_nama}\n💵 Price: {p_hrg}\n"
                f"⏱️ Time: {random.randint(1, 5)} menit yang lalu\n🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
                f"🤖 Bot Store: @{bot.get_me().username}"
            )
            bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text, message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"✅ <b>BERHASIL DIKIRIM KE GRUP UTAMA!</b>\n• Pembeli: {buyer_name}\n• Paket: {p_nama} ({p_hrg})", parse_mode="HTML")
            bot.answer_callback_query(call.id, text="Testimoni sukses terkirim!")
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
        is_open, store_msg = check_store_status()
        text = f"🔥 {greeting}, Kak {user.first_name}!\n🪙 Saldo Poin Anda: <b>{user_points} Poin</b>\n\nSilakan pilih menu utama Pakel MlbbStore:\n\n"
        if not is_open:
            text += f"{store_msg}\n\n"
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_testi':
        fake_data = generate_fake_testimonials_list()
        testi_text = f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n\n{fake_data}💡 Toko 100% amanah & terpercaya! 🚀"
        markup_testi = types.InlineKeyboardMarkup(row_width=1)
        markup_testi.add(
            types.InlineKeyboardButton("🔄 Refresh Testimoni Terbaru", callback_data='menu_testi'),
            types.InlineKeyboardButton("🌟 Lihat Ratusan Testi di Channel", url=CHANNEL_TESTI_LINK),
            types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text, reply_markup=markup_testi, disable_web_page_preview=True)
        bot.answer_callback_query(call.id, text="Testimoni diperbarui!")

    elif call.data == 'menu_riwayat':
        get_latest_user_order_data(chat_id)
        orders = get_user_orders(chat_id)
        if not orders:
            riw_text = f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n❌ Belum ada riwayat pesanan tercatat."
        else:
            riw_text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
            for idx, o in enumerate(orders[-5:], 1):
                st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK", "CANCELLED": "❌ DIBATALKAN", "EXPIRED": "⌛ EXPIRED"}.get(o['status'], "⏳ PENDING")
                riw_text += f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n   • Resi: <code>{o['resi']}</code>\n   • Status: {st}\n\n"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=riw_text, reply_markup=get_back_markup(l), parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_promo':
        status_c = get_user_coupon_status(chat_id)
        promo_text = f"🎁 PROMO & POIN (Kak {user.first_name})\n\n🪙 Saldo Poin: <b>{get_user_points(chat_id)} Poin</b>"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text, reply_markup=get_back_markup(l), parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_faq':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="💡 FAQ PAKEL MLBBSTORE\n\n❓ Aman dari banned? \n💬 A: Sangat aman, enkripsi anti-detect tinggi.", reply_markup=get_back_markup(l))
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_katalog' or call.data == 'katalog_part1':
        coupon_status = get_user_coupon_status(chat_id)
        items_to_use = t['p1_promo'] if coupon_status == "AVAILABLE" else t['p1_normal']
        markup = types.InlineKeyboardMarkup(row_width=1)
        for btn_text, callback_val, _ in items_to_use:
            markup.add(types.InlineKeyboardButton(btn_text, callback_data=callback_val))
        markup.add(types.InlineKeyboardButton(t['next_1'], callback_data='katalog_part2'))
        markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        katalog_text = f"{t['cat_title_1'].format(name=user.first_name)}\n\n{t['bonus_txt']}\n\n" + "\n\n".join([desc for _, _, desc in items_to_use]) + f"\n\n🪙 Saldo Poin Anda: <b>{get_user_points(chat_id)} Poin</b>"
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
        katalog_text = f"{t['cat_title_2'].format(name=user.first_name)}\n\n" + "\n\n".join([desc for _, _, desc in items_to_use]) + f"\n\n🪙 Saldo Poin Anda: <b>{get_user_points(chat_id)} Poin</b>"
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text, reply_markup=markup, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('buy_'):
        paket_code = call.data
        paket_dict = {
            'buy_natural': ("Natural Balance (30 Hari)", "Rp 120.000", 30),
            'buy_light': ("Light VIP + Drone (30 Hari)", "Rp 95.000", 25),
            'buy_semisafe': ("Semi-Safe 14 Hari", "Rp 75.000", 20),
            'buy_lifetimesafe': ("Lifetime Safe Permanent", "Rp 200.000", 50),
            'buy_sultan': ("Sultan One Hit 100% (30 Hari)", "Rp 150.000", 40),
            'buy_pro': ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000", 30),
            'buy_semiprivate': ("Semi-Private 14 Hari", "Rp 75.000", 20),
            'buy_permanent': ("Permanent Legend (Lifetime)", "Rp 250.000", 60)
        }
        p_name, p_price, p_points = paket_dict.get(paket_code, ("VIP Package", "Rp 100.000", 30))
        user_pts = get_user_points(chat_id)
        choice_text = f"🛒 <b>PILIH METODE PEMBAYARAN</b>\nPaket: {p_name}\nHarga: {p_price} | Poin: {p_points}"
        markup_choice = types.InlineKeyboardMarkup(row_width=1)
        markup_choice.add(
            types.InlineKeyboardButton(f"🪙 Bayar Pakai Saldo Poin ({p_points} Poin)", callback_data=f"paymode_|poin|{paket_code}"),
            types.InlineKeyboardButton(f"💳 Bayar Pakai Transfer Manual ({p_price})", callback_data=f"paymode_|transfer|{paket_code}"),
            types.InlineKeyboardButton(t['back'], callback_data='menu_katalog')
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=choice_text, reply_markup=markup_choice, parse_mode="HTML")
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_cara_order':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="❓ PANDUAN CARA ORDER\n1. Pilih paket di katalog.\n2. Pilih metode pembayaran.\n3. Selesaikan pembayaran.", reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_bayar':
        markup_bayar = types.InlineKeyboardMarkup(row_width=1)
        markup_bayar.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"💳 METODE PEMBAYARAN\nDANA/GoPay: <code>{INFO_DANA}</code>", reply_markup=markup_bayar, parse_mode="HTML", disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data == 'menu_konfirmasi':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="✅ Kirim screenshot bukti transfer ke bot ini.", reply_markup=get_back_markup(l), disable_web_page_preview=True)
        bot.answer_callback_query(call.id)

    elif call.data.startswith('rate|'):
        parts = call.data.split('|')
        if len(parts) < 3:
            return
        rating_val, resi_code = parts[1], parts[2]
        markup_ulasan = types.InlineKeyboardMarkup(row_width=1)
        markup_ulasan.add(
            types.InlineKeyboardButton("🔥 Super Bagus & Mantap Banget!", callback_data=f"textrev|{resi_code}|{rating_val}|Super bagus dan mantap"),
            types.InlineKeyboardButton("🚀 Sangat Puas, Pelayanan Gercep!", callback_data=f"textrev|{resi_code}|{rating_val}|Sangat puas, gercep")
        )
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f"⭐ <b>Terima kasih rating {rating_val} bintangnya!</b>\nPilih ulasan cepat:", parse_mode="HTML", reply_markup=markup_ulasan)
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
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="🎉 <b>TERIMA KASIH ATAS ULASANNYA!</b>", parse_mode="HTML")
        bot.answer_callback_query(call.id, text="Ulasan berhasil dikirim!")
        return
@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_and_reviews(message):
    chat_id = message.chat.id
    if message.chat.type != 'private':
        return
    save_user(chat_id)
    user = message.from_user
    l = get_lang(user)
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
                bot.reply_to(message, "🎉 Terima kasih atas ulasan terbaikmu!", reply_markup=get_back_markup(l), parse_mode="HTML")
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
        bot.reply_to(message, "❌ <b>WAKTU KONFIRMASI HABIS (TIMEOUT 15 MENIT)!</b>", parse_mode="HTML")
        return

    user_caption = message.caption if message.caption else "Tidak ada pesan"
    bot.reply_to(message, f"✅ Bukti pembayaran berhasil diunggah!\nResi: {resi_unik}", disable_web_page_preview=True)
    
    try:
        caption_admin = f"🚨 <b>BUKTI TRANSFER MASUK!</b>\n👤 @{user.username or user.first_name} (ID: <code>{user.id}</code>)\nResi: <code>{resi_unik}</code>"
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
