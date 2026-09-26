import telebot
from telebot import types
import random
import time
import threading
import io
import os
from datetime import datetime, timezone, timedelta

# =====================================================================================
#  OFFICIAL PAKEL MLBBSTORE - MASTER ULTIMATE v7 (STABLE + FIXED)
# =====================================================================================

TOKEN = '8614166487:AAFt6SzB6mP6sA31fXU7QUsz9uH8KdIEiFo'
bot = telebot.TeleBot(TOKEN)

try:
    bot.remove_webhook()
except Exception:
    pass

ADMIN_USERNAME = "@PakelMlbbOfficial"
ADMIN_LINK = "https://t.me/PakelMlbbOfficial"
CHANNEL_TESTI_LINK = "https://t.me/PakelMlbb/368"
ADMIN_TELEGRAM_ID = 8772023108

GROUP_CHAT_ID = "@PakelMlbb"
GROUP_TOPIC_ID = 368

GROUP_PAY_ID = "@Paysukses"
GROUP_PAY_TOPIC_ID = 5

INFO_DANA = "085188371150"
INFO_GOPAY = "085188371150"
INFO_SAWERIA = "https://saweria.co/PakelMlbb"

# =====================================================================================
#  KONFIGURASI QRIS — 1 GAMBAR UNTUK SEMUA NOMINAL
# =====================================================================================
QRIS_IMAGE_URL = "AgACAgUAAxkBAAEi68Bqt_3SHsY3CRaJbr-SupeCxbfIuAACFRFrG7kTwFUBoJCavSLOAwEAAwIAA3kAAz0E"

WIB = timezone(timedelta(hours=7))

TRANSAKSI_TIMEOUT_DETIK = 900
PAYMENT_REMINDER_SEBELUM_DETIK = 300
ARCHIVE_UMUR_HARI = 30
AUTO_BACKUP_INTERVAL_DETIK = 6 * 3600

# =====================================================================================
#  KONFIGURASI FITUR BARU
# =====================================================================================
ANTISPAM_CMD_COOLDOWN = 2
ANTISPAM_CALLBACK_COOLDOWN = 1
ANTISPAM_PHOTO_COOLDOWN = 5

LUCKY_DRAW_COOLDOWN_JAM = 24
LUCKY_DRAW_HADIAH = [
    ("🪙 +5 Poin",      "poin",  5,  30),
    ("🪙 +10 Poin",     "poin",  10, 25),
    ("🪙 +15 Poin",     "poin",  15, 20),
    ("🪙 +25 Poin",     "poin",  25, 12),
    ("🪙 +50 Poin",     "poin",  50, 7),
    ("🎁 Diskon 5%",    "diskon", 5,  3),
    ("🎁 Diskon 10%",   "diskon", 10, 2),
    ("💎 Paket Semi-Safe GRATIS", "paket_gratis", 0, 1),
]

TIER_BRONZE   = ("🥉 Bronze",   0,  4,   1.0, 0)
TIER_SILVER   = ("🥈 Silver",   5,  14,  1.2, 5)
TIER_GOLD     = ("🥇 Gold",     15, 29,  1.5, 10)
TIER_PLATINUM = ("💎 Platinum", 30, 9999, 2.0, 15)

STOCK_THRESHOLD_RESTOCK = 20
STOCK_RESTOCK_MIN = 150
STOCK_RESTOCK_MAX = 250
STOCK_FAKE_REDUCE_MIN = 1
STOCK_FAKE_REDUCE_MAX = 3

F_USERS = "users.txt"
F_BANNED = "banned.txt"
F_COUPONS = "coupons.txt"
F_POINTS = "points.txt"
F_POINTLOG = "point_log.txt"
F_REVIEWS = "reviews.txt"
F_ORDERS = "orders.txt"
F_ARCHIVE = "history_archive.txt"
F_REFERRALS = "referrals.txt"
F_PROOFS = "used_proofs.txt"
F_ADMINS = "admins.txt"
F_ERRORLOG = "error.log"
F_SENTMSG = "sent_messages.txt"
F_STOCKS = "stocks.txt"
F_LASTSEEN = "last_seen.txt"
F_SPINLOG = "spin_log.txt"
F_VOUCHERS = "vouchers.txt"
F_USER_VOUCHER = "user_voucher.txt"

processing_lock = set()
pending_flow = {}
last_command_time = {}
last_callback_time = {}
last_photo_time = {}

# =====================================================================================
#  MASTER KATALOG PAKET
# =====================================================================================
MASTER_PAKET = {
    'buy_natural': (
        "Natural Balance (30 Hari)", 120000, "Rp 120.000", 45,
        "🎯 <b>Fungsi:</b> Dirancang khusus untuk pemain yang mengutamakan keamanan akun. "
        "Pengaturan damage dapat disesuaikan secara mandiri (seperti 2 hit yang tidak mencolok), "
        "sehingga performa tetap optimal namun senyap."
    ),
    'buy_light': (
        "Light VIP + Drone (30 Hari)", 95000, "Rp 95.000", 35,
        "🎯 <b>Fungsi:</b> Pilihan ekonomis untuk pemakaian bulanan. Kombinasi pas antara damage "
        "yang disetel wajar agar tidak terlihat brutal, ditambah pandangan map yang lebih luas "
        "untuk membaca pergerakan lawan."
    ),
    'buy_semisafe': (
        "Semi-Safe 14 Hari", 75000, "Rp 75.000", 25,
        "🎯 <b>Fungsi:</b> Paket harian yang sangat terjangkau. Menghadirkan setelan damage "
        "fleksibel yang terkontrol serta kestabilan koneksi yang terjaga selama dua minggu penuh."
    ),
    'buy_lifetimesafe': (
        "Lifetime Safe Permanent", 200000, "Rp 200.000", 75,
        "🎯 <b>Fungsi:</b> Solusi hemat jangka panjang tanpa biaya langganan bulanan. Memberikan "
        "akses selamanya dengan fitur damage fleksibel yang aman dan stabil digunakan sewaktu-waktu."
    ),
    'buy_sultan': (
        "Sultan One Hit 100% (30 Hari)", 150000, "Rp 150.000", 55,
        "🎯 <b>Fungsi:</b> Damage tembus batas, instant kill musuh dalam sekali hit, bypass "
        "anti-cheat paling aman, khusus untuk player serius yang ingin dominasi mutlak di setiap match."
    ),
    'buy_pro': (
        "VIP Pro One Hit 80% (30 Hari)", 100000, "Rp 100.000", 40,
        "🎯 <b>Fungsi:</b> Udah dapet damage sakit, semua skin kebuka, pandangan luas, lengkap "
        "jadi satu! Paling dicari para top global untuk push rank tanpa hambatan."
    ),
    'buy_semiprivate': (
        "Semi-Private 14 Hari", 75000, "Rp 75.000", 25,
        "🎯 <b>Fungsi:</b> Performanya stabil, anti patah-patah dijamin lancar jaya buat bantai "
        "musuh seharian tanpa khawatir lag atau disconnect mendadak."
    ),
    'buy_permanent': (
        "Permanent Legend (Lifetime)", 250000, "Rp 250.000", 90,
        "🎯 <b>Fungsi:</b> Sekali bayar, nikmati update script seumur hidup tanpa perlu perpanjang "
        "langganan tiap bulan. Auto untung buat jangka panjang dan paling worth it!"
    ),
}

# =====================================================================================
#  BAGIAN 2: KEAMANAN, ERROR LOGGING & MULTI-ADMIN
# =====================================================================================

def log_error(context, e):
    try:
        with open(F_ERRORLOG, "a") as f:
            f.write(f"{datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S')} | {context} | {e}\n")
    except Exception:
        pass

def is_banned(chat_id):
    try:
        with open(F_BANNED, "r") as f:
            banned = {line.strip() for line in f if line.strip()}
        return str(chat_id) in banned
    except FileNotFoundError:
        return False

def ban_user(chat_id):
    try:
        if is_banned(chat_id):
            return
        with open(F_BANNED, "a") as f:
            f.write(f"{chat_id}\n")
    except Exception as e:
        log_error("ban_user", e)

def unban_user(chat_id):
    try:
        with open(F_BANNED, "r") as f:
            rows = [line.strip() for line in f if line.strip() and line.strip() != str(chat_id)]
        with open(F_BANNED, "w") as f:
            f.write("\n".join(rows) + ("\n" if rows else ""))
    except FileNotFoundError:
        pass
    except Exception as e:
        log_error("unban_user", e)

def get_admin_role(chat_id):
    if int(chat_id) == int(ADMIN_TELEGRAM_ID):
        return "super"
    try:
        with open(F_ADMINS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == str(chat_id):
                    return parts[1]
    except FileNotFoundError:
        pass
    return None

def is_any_admin(chat_id):
    return get_admin_role(chat_id) is not None

def is_super_admin(chat_id):
    return get_admin_role(chat_id) == "super"

def is_proof_used(proof_unique_id):
    try:
        with open(F_PROOFS, "r") as f:
            used = {line.strip() for line in f if line.strip()}
        return proof_unique_id in used
    except FileNotFoundError:
        return False

def mark_proof_used(proof_unique_id):
    try:
        with open(F_PROOFS, "a") as f:
            f.write(f"{proof_unique_id}\n")
    except Exception as e:
        log_error("mark_proof_used", e)

# =====================================================================================
#  FITUR #3: ANTI-SPAM RATE LIMITER
# =====================================================================================

def is_spam_command(chat_id):
    now = time.time()
    last = last_command_time.get(chat_id, 0)
    if now - last < ANTISPAM_CMD_COOLDOWN:
        return True
    last_command_time[chat_id] = now
    return False

def is_spam_callback(chat_id):
    now = time.time()
    last = last_callback_time.get(chat_id, 0)
    if now - last < ANTISPAM_CALLBACK_COOLDOWN:
        return True
    last_callback_time[chat_id] = now
    return False

def is_spam_photo(chat_id):
    now = time.time()
    last = last_photo_time.get(chat_id, 0)
    if now - last < ANTISPAM_PHOTO_COOLDOWN:
        return True
    last_photo_time[chat_id] = now
    return False

# =====================================================================================
#  FITUR #1: SISTEM STOK FAKE + AUTO RESTOCK
# =====================================================================================

def init_stock_if_empty():
    if os.path.exists(F_STOCKS):
        return
    try:
        with open(F_STOCKS, "w") as f:
            for code in MASTER_PAKET.keys():
                harga = MASTER_PAKET[code][1]
                if harga < 100000:
                    stok_awal = random.randint(150, 250)
                elif harga < 180000:
                    stok_awal = random.randint(80, 150)
                else:
                    stok_awal = random.randint(30, 80)
                f.write(f"{code}|{stok_awal}|{int(time.time())}\n")
    except Exception as e:
        log_error("init_stock_if_empty", e)

def _read_all_stocks():
    stocks = {}
    try:
        with open(F_STOCKS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2:
                    try:
                        stocks[parts[0]] = int(parts[1])
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return stocks

def _write_all_stocks(stocks):
    try:
        with open(F_STOCKS, "w") as f:
            now_ts = int(time.time())
            for code, stok in stocks.items():
                f.write(f"{code}|{stok}|{now_ts}\n")
    except Exception as e:
        log_error("_write_all_stocks", e)

def get_stock(paket_code):
    stocks = _read_all_stocks()
    return stocks.get(paket_code, 100)

def set_stock(paket_code, angka_baru):
    stocks = _read_all_stocks()
    stocks[paket_code] = max(0, int(angka_baru))
    _write_all_stocks(stocks)

def reduce_stock_specific(paket_code, jumlah=1):
    try:
        stocks = _read_all_stocks()
        if paket_code in stocks:
            stocks[paket_code] = max(0, stocks[paket_code] - jumlah)
            _write_all_stocks(stocks)
    except Exception as e:
        log_error("reduce_stock_specific", e)

def reduce_stock_random_all():
    try:
        stocks = _read_all_stocks()
        if not stocks:
            init_stock_if_empty()
            stocks = _read_all_stocks()
        for code in stocks.keys():
            turun = random.randint(STOCK_FAKE_REDUCE_MIN, STOCK_FAKE_REDUCE_MAX)
            stocks[code] = max(0, stocks[code] - turun)
        _write_all_stocks(stocks)
    except Exception as e:
        log_error("reduce_stock_random_all", e)

def auto_restock_if_low():
    try:
        stocks = _read_all_stocks()
        if not stocks:
            init_stock_if_empty()
            stocks = _read_all_stocks()
        changed = False
        for code, stok in stocks.items():
            if stok < STOCK_THRESHOLD_RESTOCK:
                restock_to = random.randint(STOCK_RESTOCK_MIN, STOCK_RESTOCK_MAX)
                stocks[code] = restock_to
                changed = True
        if changed:
            _write_all_stocks(stocks)
    except Exception as e:
        log_error("auto_restock_if_low", e)

def format_stock_label(stok):
    if stok <= 0:
        return "❌ <b>STOK HABIS</b> (Restock Segera)"
    elif stok < 20:
        return f"🔥 <b>SISA {stok} UNIT! GASKEUN!</b>"
    elif stok < 50:
        return f"⚠️ Stok: <b>{stok} unit</b> (Terbatas)"
    else:
        return f"📦 Stok: <b>{stok} unit</b>"

def get_paket_code_by_name(nama_paket):
    for code, data in MASTER_PAKET.items():
        if data[0] == nama_paket:
            return code
    return None

# =====================================================================================
#  FITUR #5: TIER MEMBERSHIP
# =====================================================================================

def get_user_tier(chat_id):
    total = count_user_success_orders(chat_id)
    if total >= TIER_PLATINUM[1]:
        return TIER_PLATINUM[0], TIER_PLATINUM[3], TIER_PLATINUM[4]
    elif total >= TIER_GOLD[1]:
        return TIER_GOLD[0], TIER_GOLD[3], TIER_GOLD[4]
    elif total >= TIER_SILVER[1]:
        return TIER_SILVER[0], TIER_SILVER[3], TIER_SILVER[4]
    else:
        return TIER_BRONZE[0], TIER_BRONZE[3], TIER_BRONZE[4]

def get_tier_progress(chat_id):
    total = count_user_success_orders(chat_id)
    if total < TIER_SILVER[1]:
        sisa = TIER_SILVER[1] - total
        return f"🥉 Bronze → 🥈 Silver ({sisa} transaksi lagi)"
    elif total < TIER_GOLD[1]:
        sisa = TIER_GOLD[1] - total
        return f"🥈 Silver → 🥇 Gold ({sisa} transaksi lagi)"
    elif total < TIER_PLATINUM[1]:
        sisa = TIER_PLATINUM[1] - total
        return f"🥇 Gold → 💎 Platinum ({sisa} transaksi lagi)"
    else:
        return "💎 Platinum (Tier Tertinggi!)"

# =====================================================================================
#  FITUR #4: LUCKY DRAW HARIAN
# =====================================================================================

def get_last_spin_time(chat_id):
    try:
        with open(F_SPINLOG, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[0] == str(chat_id):
                    return int(parts[1])
    except FileNotFoundError:
        pass
    return 0

def can_spin_now(chat_id):
    last = get_last_spin_time(chat_id)
    return (time.time() - last) >= (LUCKY_DRAW_COOLDOWN_JAM * 3600)

def save_spin(chat_id):
    try:
        with open(F_SPINLOG, "a") as f:
            f.write(f"{chat_id}|{int(time.time())}\n")
    except Exception as e:
        log_error("save_spin", e)

def roll_lucky_draw():
    pilihan = random.choices(LUCKY_DRAW_HADIAH, weights=[h[3] for h in LUCKY_DRAW_HADIAH], k=1)[0]
    return pilihan

def get_remaining_spin_time(chat_id):
    last = get_last_spin_time(chat_id)
    sisa_detik = (LUCKY_DRAW_COOLDOWN_JAM * 3600) - (time.time() - last)
    if sisa_detik <= 0:
        return "Siap spin sekarang!"
    jam = int(sisa_detik // 3600)
    menit = int((sisa_detik % 3600) // 60)
    return f"{jam} jam {menit} menit lagi"

# =====================================================================================
#  FITUR #7: KODE VOUCHER MANUAL
# =====================================================================================

def _read_all_vouchers():
    vouchers = {}
    try:
        with open(F_VOUCHERS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 4:
                    kode = parts[0]
                    try:
                        vouchers[kode] = {
                            'diskon': int(parts[1]),
                            'max': int(parts[2]),
                            'terpakai': int(parts[3]),
                            'expired': int(parts[4]) if len(parts) > 4 else 0,
                        }
                    except ValueError:
                        pass
    except FileNotFoundError:
        pass
    return vouchers

def _write_all_vouchers(vouchers):
    try:
        with open(F_VOUCHERS, "w") as f:
            for kode, data in vouchers.items():
                f.write(f"{kode}|{data['diskon']}|{data['max']}|{data['terpakai']}|{data['expired']}\n")
    except Exception as e:
        log_error("_write_all_vouchers", e)

def create_voucher(kode, diskon, max_pakai, durasi_jam=24):
    vouchers = _read_all_vouchers()
    expired_ts = int(time.time()) + (durasi_jam * 3600)
    vouchers[kode.upper()] = {
        'diskon': diskon,
        'max': max_pakai,
        'terpakai': 0,
        'expired': expired_ts,
    }
    _write_all_vouchers(vouchers)

def validate_voucher(kode):
    vouchers = _read_all_vouchers()
    kode_up = kode.upper().strip()
    if kode_up not in vouchers:
        return False, 0, "Kode voucher tidak ditemukan."
    v = vouchers[kode_up]
    if v['terpakai'] >= v['max']:
        return False, 0, "Voucher sudah habis kuota."
    if v['expired'] > 0 and time.time() > v['expired']:
        return False, 0, "Voucher sudah expired."
    return True, v['diskon'], "Voucher valid!"

def use_voucher(kode):
    vouchers = _read_all_vouchers()
    kode_up = kode.upper().strip()
    if kode_up in vouchers:
        vouchers[kode_up]['terpakai'] += 1
        _write_all_vouchers(vouchers)

# =====================================================================================
#  BAGIAN 3: DATABASE & PERSISTENSI DATA
# =====================================================================================

def save_user(chat_id):
    try:
        chat_id_str = str(chat_id).strip()
        if not chat_id_str or chat_id_str.startswith('-'):
            return
        users = []
        try:
            with open(F_USERS, "r") as f:
                users = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            pass
        if chat_id_str not in users:
            with open(F_USERS, "a") as f:
                f.write(chat_id_str + "\n")
    except Exception as e:
        log_error("save_user", e)

def get_user_coupon_status(chat_id):
    try:
        with open(F_COUPONS, "r") as f:
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
            with open(F_COUPONS, "r") as f:
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
        with open(F_COUPONS, "w") as f:
            f.writelines(rows)
    except Exception as e:
        log_error("set_user_coupon_status", e)

def get_user_points(chat_id):
    try:
        with open(F_POINTS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2 and parts[0] == str(chat_id):
                    return int(parts[1])
    except FileNotFoundError:
        pass
    return 0

def _write_point_log(chat_id, delta, alasan):
    try:
        now = datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S')
        with open(F_POINTLOG, "a") as f:
            f.write(f"{chat_id}|{now}|{delta}|{alasan}\n")
    except Exception as e:
        log_error("_write_point_log", e)

def add_user_points(chat_id, amount, alasan="Bonus/Penambahan"):
    try:
        current = get_user_points(chat_id)
        new_total = current + amount
        rows = []
        updated = False
        chat_id_str = str(chat_id)
        try:
            with open(F_POINTS, "r") as f:
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
        with open(F_POINTS, "w") as f:
            f.writelines(rows)
        _write_point_log(chat_id, f"+{amount}", alasan)
    except Exception as e:
        log_error("add_user_points", e)

def reduce_user_points(chat_id, amount, alasan="Penukaran/Pengurangan"):
    current = get_user_points(chat_id)
    new_total = max(0, current - amount)
    rows = []
    chat_id_str = str(chat_id)
    try:
        with open(F_POINTS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 2:
                    c_id, pts = parts
                    if c_id == chat_id_str:
                        pts = str(new_total)
                    rows.append(f"{c_id}|{pts}\n")
    except FileNotFoundError:
        pass
    with open(F_POINTS, "w") as f:
        f.writelines(rows)
    _write_point_log(chat_id, f"-{amount}", alasan)

def save_user_review(chat_id, rating, text_review):
    try:
        now = datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S')
        review_line = f"{chat_id}|{now}|{rating}|{text_review.replace('|', '-')}\n"
        with open(F_REVIEWS, "a") as f:
            f.write(review_line)
    except Exception as e:
        log_error("save_user_review", e)

def save_order(chat_id, paket_nama, harga, resi, payment_method="TRANSFER", point_cost=0, admin_msg_id=0):
    try:
        now = datetime.now(WIB)
        tanggal_str = now.strftime('%d-%m-%Y')
        jam_str = now.strftime('%H:%M:%S WIB')
        timestamp_epoch = int(now.timestamp())
        days_indo = {'Mon': 'Senin', 'Tue': 'Selasa', 'Wed': 'Rabu', 'Thu': 'Kamis',
                     'Fri': 'Jumat', 'Sat': 'Sabtu', 'Sun': 'Minggu'}
        hari_str = days_indo.get(now.strftime('%a'), now.strftime('%a'))
        order_line = (f"{chat_id}|{tanggal_str}|{hari_str}|{jam_str}|{paket_nama}|{harga}|"
                      f"{resi}|PENDING|{timestamp_epoch}|{payment_method}|{point_cost}|{admin_msg_id}\n")
        with open(F_ORDERS, "a") as f:
            f.write(order_line)
    except Exception as e:
        log_error("save_order", e)

def _read_all_orders():
    rows = []
    try:
        with open(F_ORDERS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8:
                    rows.append(parts)
    except FileNotFoundError:
        pass
    return rows

def update_order_status_by_resi(resi_target, status_baru):
    try:
        updated = False
        target_chat_id = None
        target_payment = "TRANSFER"
        target_paket_nama = ""
        current_status_db = ""
        rows = []
        for parts in _read_all_orders():
            chat_id, tanggal, hari, jam, paket, harga, resi = parts[0:7]
            status = parts[7]
            timestamp_epoch = parts[8] if len(parts) > 8 else "0"
            pay_method = parts[9] if len(parts) > 9 else "TRANSFER"
            p_cost = int(parts[10]) if len(parts) > 10 and parts[10].isdigit() else 0
            adm_msg_id = parts[11] if len(parts) > 11 else "0"

            if resi.strip() == resi_target.strip():
                target_chat_id = chat_id
                target_payment = pay_method
                target_paket_nama = paket
                current_status_db = status
                if status != "PENDING":
                    rows.append('|'.join(parts) + "\n")
                    continue
                status = status_baru
                updated = True
            rows.append(f"{chat_id}|{tanggal}|{hari}|{jam}|{paket}|{harga}|{resi}|{status}|"
                        f"{timestamp_epoch}|{pay_method}|{p_cost}|{adm_msg_id}\n")

        if updated:
            with open(F_ORDERS, "w") as f:
                f.writelines(rows)
            if target_chat_id and current_status_db == "PENDING":
                if status_baru == "BERHASIL":
                    set_user_coupon_status(target_chat_id, "USED")
                    if target_payment != "POIN":
                        _, multiplier, _ = get_user_tier(target_chat_id)
                        bonus = int(10 * multiplier)
                        add_user_points(target_chat_id, bonus, f"Bonus pembelian sukses (Tier x{multiplier})")
                    paket_code = get_paket_code_by_name(target_paket_nama)
                    if paket_code:
                        reduce_stock_specific(paket_code, 1)
                    try:
                        _apply_referral_bonus_if_eligible_helper(target_chat_id)
                    except Exception:
                        pass
                elif status_baru in ["DITOLAK", "EXPIRED", "CANCELLED"]:
                    set_user_coupon_status(target_chat_id, "AVAILABLE")
            return True
    except Exception as e:
        log_error("update_order_status_by_resi", e)
    return False

def get_user_orders(chat_id):
    orders = []
    for parts in _read_all_orders():
        if parts[0] == str(chat_id):
            orders.append({
                'tanggal': parts[1], 'hari': parts[2], 'jam': parts[3],
                'paket': parts[4], 'harga': parts[5], 'resi': parts[6],
                'status': parts[7], 'pay_method': parts[9] if len(parts) > 9 else "TRANSFER"
            })
    return orders

def get_orders_by_date_filter(chat_id, tanggal_str):
    return [o for o in get_user_orders(chat_id) if o['tanggal'] == tanggal_str]

def get_latest_user_order_data(chat_id):
    try:
        current_time = int(datetime.now(WIB).timestamp())
        orders = [p for p in _read_all_orders() if p[0] == str(chat_id)]
        if orders:
            last_order = orders[-1]
            resi = last_order[6]
            status = last_order[7]
            timestamp_epoch = int(last_order[8]) if len(last_order) > 8 and last_order[8].isdigit() else current_time
            if status == "PENDING" and (current_time - timestamp_epoch > TRANSAKSI_TIMEOUT_DETIK):
                update_order_status_by_resi(resi, "EXPIRED")
                return resi, "EXPIRED"
            return resi, status
    except Exception as e:
        log_error("get_latest_user_order_data", e)
    return f"PKL-MLBB-{random.randint(10000, 99999)}", "PENDING"

def archive_old_orders():
    try:
        now_epoch = int(datetime.now(WIB).timestamp())
        keep_rows, archive_rows = [], []
        for parts in _read_all_orders():
            epoch = int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else now_epoch
            line = '|'.join(parts) + "\n"
            if now_epoch - epoch > ARCHIVE_UMUR_HARI * 86400:
                archive_rows.append(line)
            else:
                keep_rows.append(line)
        if archive_rows:
            with open(F_ARCHIVE, "a") as f:
                f.writelines(archive_rows)
            with open(F_ORDERS, "w") as f:
                f.writelines(keep_rows)
    except Exception as e:
        log_error("archive_old_orders", e)

def count_user_success_orders(chat_id):
    total = 0
    for parts in _read_all_orders():
        if parts[0] == str(chat_id) and len(parts) > 7 and parts[7].strip() == "BERHASIL":
            total += 1
    return total

# =====================================================================================
#  BAGIAN 4: SISTEM REFERRAL + GACHA
# =====================================================================================

def register_referral(referrer_id, referred_id):
    referrer_id, referred_id = str(referrer_id), str(referred_id)
    if referrer_id == referred_id:
        return False
    try:
        with open(F_REFERRALS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 2 and parts[1] == referred_id:
                    return False
    except FileNotFoundError:
        pass
    try:
        now = int(datetime.now(WIB).timestamp())
        with open(F_REFERRALS, "a") as f:
            f.write(f"{referrer_id}|{referred_id}|{now}|BELUM_BONUS\n")
        return True
    except Exception as e:
        log_error("register_referral", e)
        return False

def roll_gacha_referral_bonus():
    hasil = random.choices(population=[2, 3, 4, 5], weights=[45, 35, 15, 5], k=1)[0]
    return hasil

def _apply_referral_bonus_if_eligible_helper(new_buyer_chat_id):
    try:
        rows = []
        changed = False
        referrer_to_bonus = None
        with open(F_REFERRALS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4:
                    referrer_id, referred_id, ts, status = parts
                    if referred_id == str(new_buyer_chat_id) and status == "BELUM_BONUS":
                        status = "SUDAH_BONUS"
                        referrer_to_bonus = referrer_id
                        changed = True
                    rows.append(f"{referrer_id}|{referred_id}|{ts}|{status}\n")
        if changed:
            with open(F_REFERRALS, "w") as f:
                f.writelines(rows)
        if referrer_to_bonus:
            bonus_poin = roll_gacha_referral_bonus()
            add_user_points(referrer_to_bonus, bonus_poin, f"Bonus referral gacha (+{bonus_poin} poin)")
            try:
                bot.send_message(
                    referrer_to_bonus,
                    f"🎉 <b>BONUS REFERRAL CAIR!</b>\n\n"
                    f"Temanmu berhasil belanja pertama kali.\n"
                    f"🎰 Hasil Gacha Bonus: <b>+{bonus_poin} Poin</b> masuk ke saldo loyalitasmu!",
                    parse_mode="HTML"
                )
            except Exception:
                pass
    except FileNotFoundError:
        pass
    except Exception as e:
        log_error("_apply_referral_bonus_if_eligible_helper", e)

def get_referral_stats(chat_id):
    total, bonus_cair = 0, 0
    try:
        with open(F_REFERRALS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) == 4 and parts[0] == str(chat_id):
                    total += 1
                    if parts[3] == "SUDAH_BONUS":
                        bonus_cair += 1
    except FileNotFoundError:
        pass
    return total, bonus_cair

def get_time_greeting():
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
    hour = datetime.now(WIB).hour
    if 0 <= hour < 7:
        return False, ("⚠️ <b>INFO OPERASIONAL TOKO:</b>\nHalo Kak! Toko sedang istirahat (Offline) "
                       "jam 00:00 - 07:00 WIB. Pesanan tetap bisa dibuat, pengiriman script "
                       "dilanjutkan jam 07:00 WIB! 🙏✨")
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
        "@Sultan_Mlbb***", "@Anjay_Mabar***", "@Gacor_Gaming***", "@TopGlobal_1***",
    ]
    return random.choice(list_nama_tele)

def generate_single_testimonial():
    list_paket = [
        ("Natural Balance (30 Hari)", "Rp 120.000", "45 Poin"),
        ("Light VIP + Drone (30 Hari)", "Rp 95.000", "35 Poin"),
        ("Semi-Safe 14 Hari", "Rp 75.000", "25 Poin"),
        ("Lifetime Safe Permanent", "Rp 200.000", "75 Poin"),
        ("Sultan One Hit 100% (30 Hari)", "Rp 150.000", "55 Poin"),
        ("VIP Pro One Hit 80% (30 Hari)", "Rp 100.000", "40 Poin"),
        ("Semi-Private 14 Hari", "Rp 75.000", "25 Poin"),
        ("Permanent Legend (Lifetime)", "Rp 250.000", "90 Poin")
    ]
    nama = get_random_masked_name()
    paket, harga_rp, harga_poin = random.choice(list_paket)
    menit_lalu = random.randint(2, 45)
    current_hour = datetime.now(WIB).hour
    waktu_ket = "pagi ini" if 4 <= current_hour < 11 else (
        "siang ini" if 11 <= current_hour < 15 else (
            "sore ini" if 15 <= current_hour < 18 else "malam ini"))

    is_poin_pay = random.random() < 0.3
    if is_poin_pay:
        price_text = f"{harga_poin} (Klaim Saldo Poin Loyalitas ✨)"
        pay_method_label = "REDEEMED VIA LOYALTY POINTS"
    else:
        price_text = harga_rp
        pay_method_label = "SUCCESS & SCRIPT DELIVERED"

    reduce_stock_random_all()
    auto_restock_if_low()

    return (
        "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
        f"✅ Buyer ID: {nama}\n"
        f"📦 Item Purchased: {paket}\n"
        f"💵 Price / Method: {price_text}\n"
        f"⏱️ Time: {menit_lalu} menit yang lalu ({waktu_ket})\n"
        f"🔒 Status: {pay_method_label}\n\n"
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
        testi_output += (f"✅ {i}. Buyer ID: {nama}\n   • Dibeli: {paket} ({harga})\n"
                         f"   • Status: LUNAS & SCRIPT TERKIRIM\n\n")
    return testi_output

# =====================================================================================
#  BAGIAN 5: BACKGROUND THREADS
# =====================================================================================

def payment_reminder_loop():
    while True:
        try:
            now_epoch = int(datetime.now(WIB).timestamp())
            for parts in _read_all_orders():
                chat_id = parts[0]
                resi = parts[6]
                status = parts[7]
                epoch = int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else now_epoch
                if status == "PENDING":
                    sisa = TRANSAKSI_TIMEOUT_DETIK - (now_epoch - epoch)
                    if PAYMENT_REMINDER_SEBELUM_DETIK - 30 <= sisa <= PAYMENT_REMINDER_SEBELUM_DETIK:
                        marker_file = f".reminded_{resi}"
                        if not os.path.exists(marker_file):
                            try:
                                bot.send_message(
                                    chat_id,
                                    f"⏰ <b>REMINDER PEMBAYARAN!</b>\n\n"
                                    f"Kak, sisa waktu pembayaranmu tinggal <b>5 menit</b> lagi!\n\n"
                                    f"🔑 Resi: <code>{resi}</code>\n\n"
                                    "Buruan selesaikan pembayaran & kirim bukti transfer ke bot ini "
                                    "sebelum pesanan otomatis expired ya! 🙏",
                                    parse_mode="HTML"
                                )
                                open(marker_file, "w").close()
                            except Exception as e:
                                log_error("payment_reminder_send", e)
        except Exception as e:
            log_error("payment_reminder_loop", e)
        time.sleep(30)

threading.Thread(target=payment_reminder_loop, daemon=True).start()

def timeout_dan_reminder_loop():
    while True:
        try:
            now_epoch = int(datetime.now(WIB).timestamp())
            for parts in _read_all_orders():
                chat_id, resi, status = parts[0], parts[6], parts[7]
                epoch = int(parts[8]) if len(parts) > 8 and parts[8].isdigit() else now_epoch
                if status == "PENDING" and (now_epoch - epoch > TRANSAKSI_TIMEOUT_DETIK):
                    update_order_status_by_resi(resi, "EXPIRED")
                    try:
                        bot.send_message(chat_id,
                                         f"❌ <b>PESANAN EXPIRED</b> (Resi <code>{resi}</code>)\nWaktu 15 menit habis.",
                                         parse_mode="HTML")
                    except Exception:
                        pass
        except Exception as e:
            log_error("timeout_dan_reminder_loop", e)
        time.sleep(30)

threading.Thread(target=timeout_dan_reminder_loop, daemon=True).start()

def archive_loop():
    while True:
        time.sleep(24 * 3600)
        archive_old_orders()

threading.Thread(target=archive_loop, daemon=True).start()

def background_auto_poster():
    time.sleep(60)
    while True:
        try:
            time.sleep(random.choice([1500, 3600, 7200, 10800]))
            bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(),
                             message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        except Exception as e:
            log_error("background_auto_poster", e)
            time.sleep(60)

threading.Thread(target=background_auto_poster, daemon=True).start()

def background_auto_broadcast():
    time.sleep(300)
    broadcast_templates = [
        "📢 <b>INFO PROMO SPESIAL HARI INI!</b> 🔥\n\nBuat Kakak yang mau ngebut <i>push rank</i> tanpa takut kena ban, buruan sikat script VIP kita sekarang!\n🎁 Spesial hari ini, ada potongan harga spesial + bonus <i>Server Lag Panel</i> dan <i>Drone View X10</i> gratis tanpa biaya tambahan.\n\n🛒 Langsung cek katalog lengkapnya di bot: @{bot_username}",
        "🛡️ <b>KENAPA HARUS PAKAI SCRIPT PAKEL MLBBSTORE?</b> ⚡\n\nJangan pertaruhkan akun sultan Kakak pakai script sembarangan yang gampang terdeteksi sistem Moonton!\nDi sini kita pakai enkripsi <i>high-tier anti-detect</i> paling stabil se-Indonesia, aman buat main di mode <i>Ranked</i> Mythic sekalipun.\n\n📦 Pilih paket andalan Kakak sekarang sebelum kehabisan slot: @{bot_username}",
        "⚡ <b>BONUS FREE ALL PACKAGES TANPA SYARAT!</b> 🎁\n\nSetiap pembelian paket apa saja di Official Pakel MlbbStore, Kakak bakal otomatis dapet:\n• Panel Server Lag Musuh (<i>Global Ping Spikes</i>) 🌐\n• Drone View Eksklusif Ultra Wide X1 - X10 🦅\n\n🚀 Yuk dominasi permainan sekarang juga! Order gampang via bot: @{bot_username}",
        "🏆 <b>MAU JADI TOP GLOBAL ATAU NYAMPE MYTHIC GLORY DENGAN CEPAT?</b> 🔥\n\nWaktunya buktikan kemampuan terbaikmu di Land of Dawn! Gunakan <i>Custom Damage</i> dan <i>Light VIP</i> dari Pakel MlbbStore biar gameplay makin gampang dan mulus.\n\n💬 Cek riwayat pesanan, klaim kupon, atau pilih paket langsung di: @{bot_username}",
        "🌟 <b>PEMBERITAHUAN UPDATE STOK & TESTIMONI HARIAN</b> 🚀\n\nRatusan player sudah membuktikan sendiri kestabilan script kita hari ini tanpa kendala. Giliran Kakak buat rasain bedanya pas war!\n💎 Proses cepat, amanah, dan dibimbing sampai beres.\n\n👇 Yuk amankan paket pilihanmu langsung di bot: @{bot_username}",
        "💥 <b>SPECIAL EDITION: SULTAN ONE HIT & INSTANT KILL</b> ⚡\n\nMau ngerasain dominasi mutlak di setiap pertandingan? Paket <i>Sultan One Hit</i> siap bikin musuh kewalahan dan rata dalam sekejap!\n🛡️ Dilengkapi sistem pengaman kelas atas agar akun tetap aman sentosa.\n\n🛒 Sikat promonya sekarang lewat bot: @{bot_username}",
        "🎁 <b>CEK SALDO POIN & KUPON MEMBER KAMU!</b> 💳\n\nTahukah Kakak? Setiap transaksi sukses di Official Pakel MlbbStore, Kakak bakal otomatis dapet tambahan Poin Loyalitas lho!\n🪙 Poinnya bisa ditukar buat bayar paket script gratis tanpa perlu transfer rupiah lagi. Mantap kan?\n\n✨ Yuk cek poinmu sekarang di bot: @{bot_username}",
        "🌐 <b>BASMI LAG & FPS DROP SAAT WAR BERSAMA KITA!</b> 📉➡️📈\n\nKesel banget kan pas lagi momen penting malah patah-patah atau sinyal mendadak merah? Tenang, script kita sudah include fitur *Server Lag Panel* buat stabilin permainan.\n🎯 Main jadi lebih PeDe, mulus, dan bebas hambatan!\n\n📦 Langsung pilih paketnya di sini: @{bot_username}",
        "⏰ <b>WAKTU TERBATAS: GASPOL PUSH RANK AKHIR SEASON!</b> ⏳\n\nJangan biarkan bintangmu turun atau stuck di satu tier terus! Maksimalkan performa permainanmu dengan script premium anti-detect terpercaya se-Indonesia.\n⚡ Dijamin ampuh buat bantu naik tier dengan mulus.\n\n🚀 Amankan paketmu sekarang juga via bot: @{bot_username}",
        "👋 <b>HALO KAKAK-KAKAK PLAYER MLBB INDONESIA!</b> 🎮✨\n\nMau mabar bareng squad tapi minder sama performa hero? Jangan khawatir, Official Pakel MlbbStore selalu siap jadi solusi terbaik buat naikin performa game kamu hari ini.\n💎 Aman, stabil, dan bergaransi.\n\n👇 Yuk langsung mampir ke katalog bot: @{bot_username}"
    ]
    while True:
        try:
            time.sleep(random.randint(14400, 28800))
            try:
                with open(F_USERS, "r") as f:
                    users = [line.strip() for line in f.read().splitlines() if line.strip()]
            except FileNotFoundError:
                continue
            if not users:
                continue
            template_pilihan = random.choice(broadcast_templates)
            pesan_final = template_pilihan.format(bot_username=bot.get_me().username)
            for chat_id in set(users):
                try:
                    bot.send_message(chat_id=chat_id,
                                     text=f"📢 <b>PENGUMUMAN OTOMATIS</b>\n\n{pesan_final}",
                                     parse_mode="HTML", disable_web_page_preview=True)
                    time.sleep(0.05)
                except Exception:
                    pass
        except Exception as e:
            print(f"[AUTO-BROADCAST ERROR]: {e}")
            time.sleep(300)

threading.Thread(target=background_auto_broadcast, daemon=True).start()

def auto_backup_loop():
    while True:
        time.sleep(AUTO_BACKUP_INTERVAL_DETIK)
        for fname in [F_ORDERS, F_USERS, F_POINTS]:
            try:
                if os.path.exists(fname):
                    with open(fname, "rb") as f:
                        bot.send_document(ADMIN_TELEGRAM_ID, f, caption=f"🗄️ Auto-backup: {fname}")
            except Exception as e:
                log_error("auto_backup_loop", e)

threading.Thread(target=auto_backup_loop, daemon=True).start()

init_stock_if_empty()

# =====================================================================================
#  BAGIAN 6: TRANSLATIONS & UI HELPERS
# =====================================================================================

TRANSLATIONS = {
    'id': {
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_testi': "🌟 Testimoni & Real-Time Bukti Order",
        'btn_riwayat': "📦 Cek Riwayat & Status Pesanan Saya",
        'btn_promo': "🎁 Klaim Kupon & Poin Loyalitas",
        'btn_referral': "🎯 Poin & Link Referral Saya",
        'btn_profil': "👤 Profil Akun Saya",
        'btn_lucky': "🎰 Lucky Draw Harian",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Lengkap",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥\n<i>(Kategori: Custom Damage High-Tier & Fair Play Anti-Detect)</i>",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥\n<i>(Kategori: Sultan One Hit Instan & Dominasi Mutlak)</i>",
        'bonus_txt': ("⚡ <b>BONUS SPESIAL FREE ALL PACKAGES (TANPA BIAYA TAMBAHAN):</b>\n"
                      "🎁 Setiap pembelian paket apa saja, otomatis mendapatkan:\n"
                      "  • Panel Server Lag Musuh (Global Ping Spikes)\n"
                      "  • Drone View Eksklusif X1 sampai X10 (Ultra Wide View)\n\n"
                      "📂 <b>SILAKAN PILIH SCRIPT & PELAJARI DETAIL FITUR DI BAWAH INI:</b>"),
        'next_1': "▶️ Lanjut Katalog Bagian 2",
        'prev_2': "◀️ Kembali Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'confirm_instr': ("🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\n"
                          "Setelah sukses membayar, silakan kirim Screenshot Bukti Transfer ke bot ini "
                          "untuk mendapatkan Resi Unik."),
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue & Pricing", 'btn_testi': "🌟 Live Testimonials",
        'btn_riwayat': "📦 My Order History", 'btn_promo': "🎁 Claim Promo & Points",
        'btn_referral': "🎯 My Points & Referral Link",
        'btn_profil': "👤 My Account Profile",
        'btn_lucky': "🎰 Daily Lucky Draw",
        'btn_cara_order': "❓ How to Order", 'btn_bayar': "💳 Payments",
        'btn_faq': "💡 FAQ", 'btn_konfirmasi': "✅ Check Status",
        'btn_admin': "💬 Contact Admin", 'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS:",
        'next_1': "▶️ Next", 'prev_2': "◀️ Back", 'inv_title': "🛒 INVOICE",
        'confirm_instr': "🛡️ Send screenshot.",
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

def build_welcome_text(user, user_points, l='id'):
    greeting = get_time_greeting()
    tier_label, _, _ = get_user_tier(user.id)
    if l == 'id':
        return (
            f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n"
            f"🪙 Saldo Poin Loyalitas Anda: <b>{user_points} Poin</b>\n"
            f"🏅 Tier Anda: <b>{tier_label}</b>\n\n"
            "Pusat layanan script cheat Mobile Legends premium terpercaya, anti-detect kelas atas, "
            "server lag panel, & drone view paling stabil se-Indonesia.\n\n"
            "👇 Silakan pilih menu di bawah ini untuk mulai berbelanja:"
        )
    else:
        return (
            f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n"
            f"🪙 Your Loyalty Points: <b>{user_points} Poin</b>\n"
            f"🏅 Your Tier: <b>{tier_label}</b>\n\n"
            "Trusted premium Mobile Legends script service.\n\n"
            "👇 Please select a menu below to start shopping:"
        )

def build_main_menu_markup(l='id'):
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
        types.InlineKeyboardButton(t['btn_testi'], callback_data='menu_testi'),
        types.InlineKeyboardButton(t['btn_riwayat'], callback_data='menu_riwayat'),
        types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
        types.InlineKeyboardButton(t['btn_referral'], callback_data='menu_referral'),
        types.InlineKeyboardButton(t['btn_profil'], callback_data='menu_profil'),
        types.InlineKeyboardButton(t['btn_lucky'], callback_data='menu_lucky'),
        types.InlineKeyboardButton(t['btn_cara_order'], callback_data='menu_cara_order'),
        types.InlineKeyboardButton(t['btn_bayar'], callback_data='menu_bayar'),
        types.InlineKeyboardButton(t['btn_faq'], callback_data='menu_faq'),
        types.InlineKeyboardButton(t['btn_konfirmasi'], callback_data='menu_konfirmasi'),
    )
    markup.add(types.InlineKeyboardButton(t['btn_admin'], url=ADMIN_LINK))
    return markup

def _kirim_poin_referral(chat_id, message_id, l='id'):
    points = get_user_points(chat_id)
    total_ref, bonus_cair = get_referral_stats(chat_id)
    bot_username = bot.get_me().username
    link = f"https://t.me/{bot_username}?start=ref_{chat_id}"

    share_text = "🔥 Gabung & belanja script VIP MLBB terpercaya di Pakel MlbbStore! Pakai link referral saya ya 👇"
    share_url = f"https://t.me/share/url?url={link}&text={share_text}"

    text = (
        f"🎯 <b>POIN & REFERRAL KAMU</b>\n\n"
        f"🪙 Saldo Poin: <b>{points} Poin</b>\n"
        f"👥 Total teman diundang: <b>{total_ref}</b>\n"
        f"✅ Bonus referral sudah cair: <b>{bonus_cair}</b>\n\n"
        f"🔗 <b>Link Referral Pribadimu:</b>\n<code>{link}</code>\n\n"
        "🎰 <b>Sistem Gacha Bonus Referral:</b>\n"
        "• +2 Poin (45%)\n• +3 Poin (35%)\n• +4 Poin (15%)\n• +5 Poin (5%)\n\n"
        "💡 <i>Ajak teman pakai link ini, makin banyak yang belanja makin besar peluang gacha bonusnya!</i>"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📤 Bagikan ke Teman / Grup", url=share_url),
        types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama')
    )
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                              parse_mode="HTML", reply_markup=markup,
                              disable_web_page_preview=True)
    except Exception:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup,
                         disable_web_page_preview=True)

def _kirim_profil_akun(chat_id, message_id, user, l='id'):
    points = get_user_points(chat_id)
    coupon_status = get_user_coupon_status(chat_id)
    total_sukses = count_user_success_orders(chat_id)
    total_ref, bonus_cair = get_referral_stats(chat_id)
    tier_label, multiplier, diskon = get_user_tier(chat_id)
    tier_progress = get_tier_progress(chat_id)

    if coupon_status == "AVAILABLE":
        status_kupon = "🎁 Tersedia (Belum Dipakai)"
    elif coupon_status == "PENDING":
        status_kupon = "⏳ Pending (Menunggu Verifikasi)"
    else:
        status_kupon = "✅ Sudah Digunakan"

    username_display = f"@{user.username}" if user.username else "-"
    nama_tampil = user.first_name + (f" {user.last_name}" if user.last_name else "")

    text = (
        "👤 <b>PROFIL AKUN SAYA</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"📝 Nama Tampil : <b>{nama_tampil}</b>\n"
        f"🔗 Username     : {username_display}\n"
        f"🆔 ID Telegram  : <code>{chat_id}</code>\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🏅 Tier Membership : <b>{tier_label}</b>\n"
        f"   ├ Poin Bonus: <b>x{multiplier}</b>\n"
        f"   ├ Diskon    : <b>{diskon}%</b>\n"
        f"   └ Progress  : {tier_progress}\n\n"
        f"🪙 Saldo Poin    : <b>{points} Poin</b>\n"
        f"🎫 Status Kupon  : {status_kupon}\n"
        f"📦 Total Transaksi Sukses : <b>{total_sukses}</b>\n"
        f"👥 Total Referral          : <b>{total_ref}</b>\n"
        f"✅ Bonus Referral Cair     : <b>{bonus_cair}</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 <i>Semakin banyak transaksi sukses, tier kamu naik & poin makin gacor!</i>"
    )
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📦 Lihat Riwayat Pesanan", callback_data='menu_riwayat'),
        types.InlineKeyboardButton("🎁 Klaim Poin & Kupon", callback_data='menu_promo'),
        types.InlineKeyboardButton("⬅️ Kembali ke Menu Utama", callback_data='menu_utama')
    )
    try:
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                              parse_mode="HTML", reply_markup=markup,
                              disable_web_page_preview=True)
    except Exception:
        bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup,
                         disable_web_page_preview=True)

def build_katalog_markup(part, l='id'):
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    markup = types.InlineKeyboardMarkup(row_width=2)

    if part == 1:
        paket_urutan = ['buy_natural', 'buy_light', 'buy_semisafe', 'buy_lifetimesafe']
        next_btn_text = t['next_1']
        nav_cb = 'katalog_part2'
    else:
        paket_urutan = ['buy_sultan', 'buy_pro', 'buy_semiprivate', 'buy_permanent']
        next_btn_text = t['prev_2']
        nav_cb = 'katalog_part1'

    for code in paket_urutan:
        nama, harga_angka, harga_str, poin, _ = MASTER_PAKET[code]
        stok = get_stock(code)
        if stok <= 0:
            stok_emoji = "❌"
        elif stok < 20:
            stok_emoji = "🔥"
        elif stok < 50:
            stok_emoji = "⚠️"
        else:
            stok_emoji = "📦"
        btn_label = f"🛒 {nama.split('(')[0].strip()}\n💰 {harga_str} | {stok_emoji} {stok}"
        markup.add(types.InlineKeyboardButton(btn_label, callback_data=code))

    markup.add(types.InlineKeyboardButton(next_btn_text, callback_data=nav_cb))
    markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
    return markup

def build_katalog_text(part, user, l='id', coupon_status="AVAILABLE"):
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    if part == 1:
        paket_urutan = ['buy_natural', 'buy_light', 'buy_semisafe', 'buy_lifetimesafe']
        title = t['cat_title_1'].format(name=user.first_name)
    else:
        paket_urutan = ['buy_sultan', 'buy_pro', 'buy_semiprivate', 'buy_permanent']
        title = t['cat_title_2'].format(name=user.first_name)

    text = f"{title}\n\n{t['bonus_txt']}\n\n"
    text += "━━━━━━━━━━━━━━━━━━━\n\n"

    for code in paket_urutan:
        nama, harga_angka, harga_str, poin, deskripsi = MASTER_PAKET[code]
        stok = get_stock(code)
        stok_label = format_stock_label(stok)
        promo_active = (coupon_status == "AVAILABLE")
        if promo_active:
            harga_promo = harga_angka - 10000
            text += (
                f"👑 <b>{nama}</b>\n"
                f"   💵 Harga: <s>{harga_str}</s> <b>Rp {harga_promo:,}</b> <i>(Hemat Rp 10.000)</i>\n"
                f"   🪙 Atau Tukar: <b>{poin} Poin</b>\n"
                f"   {stok_label}\n"
                f"   {deskripsi}\n\n"
            )
        else:
            text += (
                f"👑 <b>{nama}</b>\n"
                f"   💵 Harga: <b>{harga_str}</b>\n"
                f"   🪙 Atau Tukar: <b>{poin} Poin</b>\n"
                f"   {stok_label}\n"
                f"   {deskripsi}\n\n"
            )

    text += f"🪙 Saldo Poin Anda: <b>{get_user_points(user.id)} Poin</b>"
    if coupon_status == "AVAILABLE":
        text += "\n🎁 <b>INFO PROMO:</b> Anda punya hak potong harga spesial member baru otomatis!"
    return text

# =====================================================================================
#  BAGIAN 7: COMMAND HANDLERS
# =====================================================================================

@bot.message_handler(commands=['resetorders'])
def cmd_reset_orders(message):
    if not is_super_admin(message.chat.id):
        bot.reply_to(message, "⚠️ Perintah khusus admin utama!")
        return
    try:
        open(F_ORDERS, "w").close()
        bot.reply_to(message, "✅ Berhasil dikosongkan.")
    except Exception as e:
        bot.reply_to(message, f"Gagal: {e}")

@bot.message_handler(commands=['laporan', 'report'])
def cmd_laporan(message):
    if not is_any_admin(message.from_user.id):
        return
    try:
        today_str = datetime.now(WIB).strftime('%d-%m-%Y')
        sukses = 0
        ditolak = 0
        expired = 0
        pending = 0
        total_pendapatan = 0
        poin_ditukar = 0
        user_order_hari_ini = set()

        for parts in _read_all_orders():
            if len(parts) < 8:
                continue
            tanggal = parts[1]
            if tanggal != today_str:
                continue
            status = parts[7]
            user_order_hari_ini.add(parts[0])
            if status == "BERHASIL":
                sukses += 1
                pay = parts[9] if len(parts) > 9 else "TRANSFER"
                if pay == "POIN":
                    poin_ditukar += int(parts[10]) if len(parts) > 10 and parts[10].isdigit() else 0
                else:
                    total_pendapatan += int(''.join(ch for ch in parts[5] if ch.isdigit()) or 0)
            elif status == "DITOLAK":
                ditolak += 1
            elif status == "EXPIRED":
                expired += 1
            elif status == "PENDING":
                pending += 1

        text = (
            f"📊 <b>LAPORAN HARIAN</b>\n"
            f"🗓️ Tanggal: <b>{today_str}</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Transaksi Sukses : <b>{sukses}</b>\n"
            f"❌ Ditolak          : <b>{ditolak}</b>\n"
            f"⌛ Expired          : <b>{expired}</b>\n"
            f"⏳ Masih Pending    : <b>{pending}</b>\n"
            "━━━━━━━━━━━━━━━━━━━\n"
            f"💰 <b>Total Pendapatan</b>: Rp {total_pendapatan:,}\n"
            f"🪙 Poin Ditukar     : {poin_ditukar} Poin\n"
            f"👥 User Order Hari Ini: <b>{len(user_order_hari_ini)}</b>\n"
            "━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, text, parse_mode="HTML")
    except Exception as e:
        log_error("cmd_laporan", e)
        bot.reply_to(message, f"Gagal: {e}")

@bot.message_handler(commands=['stok', 'stock'])
def cmd_stok(message):
    if not is_any_admin(message.from_user.id):
        return
    try:
        stocks = _read_all_stocks()
        text = "📦 <b>STOK SEMUA PAKET</b>\n\n"
        for code, data in MASTER_PAKET.items():
            nama = data[0]
            stok = stocks.get(code, 0)
            text += f"• <b>{nama}</b>\n   Stok: <b>{stok}</b> unit\n\n"
        text += "💡 Command:\n/setstok [code] [angka]\n/restock\n/offstok [code]"
        bot.reply_to(message, text, parse_mode="HTML")
    except Exception as e:
        bot.reply_to(message, f"Gagal: {e}")

@bot.message_handler(commands=['setstok'])
def cmd_setstok(message):
    if not is_super_admin(message.chat.id):
        return
    args = message.text.replace('/setstok', '').strip().split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: /setstok buy_sultan 100")
        return
    code = args[0].strip()
    try:
        angka = int(args[1])
    except ValueError:
        bot.reply_to(message, "⚠️ Angka stok harus integer.")
        return
    if code not in MASTER_PAKET:
        bot.reply_to(message, f"⚠️ Kode paket tidak valid. Pakai salah satu: {', '.join(MASTER_PAKET.keys())}")
        return
    set_stock(code, angka)
    bot.reply_to(message, f"✅ Stok {MASTER_PAKET[code][0]} di-set ke {angka}.")

@bot.message_handler(commands=['restock'])
def cmd_restock(message):
    if not is_super_admin(message.chat.id):
        return
    try:
        stocks = _read_all_stocks()
        for code in stocks.keys():
            if code in MASTER_PAKET:
                stocks[code] = random.randint(STOCK_RESTOCK_MIN, STOCK_RESTOCK_MAX)
        _write_all_stocks(stocks)
        bot.reply_to(message, "✅ Semua stok berhasil di-restock ke range 150-250.")
    except Exception as e:
        bot.reply_to(message, f"Gagal: {e}")

@bot.message_handler(commands=['offstok'])
def cmd_offstok(message):
    if not is_super_admin(message.chat.id):
        return
    args = message.text.replace('/offstok', '').strip().split()
    if not args:
        bot.reply_to(message, "⚠️ Format: /offstok buy_sultan")
        return
    code = args[0].strip()
    if code not in MASTER_PAKET:
        bot.reply_to(message, "⚠️ Kode paket tidak valid.")
        return
    set_stock(code, 0)
    bot.reply_to(message, f"✅ Stok {MASTER_PAKET[code][0]} di-set 0 (HABIS).")

@bot.message_handler(commands=['buatvoucher'])
def cmd_buatvoucher(message):
    if not is_super_admin(message.chat.id):
        return
    args = message.text.replace('/buatvoucher', '').strip().split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ Format: /buatvoucher KODE DISKON MAX_PAKAI [DURASI_JAM]\nContoh: /buatvoucher PROMO10 10000 50 24")
        return
    kode = args[0].strip().upper()
    try:
        diskon = int(args[1])
        max_pakai = int(args[2])
        durasi_jam = int(args[3]) if len(args) > 3 else 24
    except ValueError:
        bot.reply_to(message, "⚠️ Diskon, max_pakai, dan durasi harus angka.")
        return
    create_voucher(kode, diskon, max_pakai, durasi_jam)
    bot.reply_to(message,
                 f"✅ Voucher dibuat!\n\n"
                 f"🎫 Kode: <code>{kode}</code>\n"
                 f"💵 Diskon: Rp {diskon:,}\n"
                 f"📊 Max Pakai: {max_pakai} kali\n"
                 f"⏱️ Expired: {durasi_jam} jam",
                 parse_mode="HTML")

@bot.message_handler(commands=['listvoucher'])
def cmd_listvoucher(message):
    if not is_any_admin(message.from_user.id):
        return
    vouchers = _read_all_vouchers()
    if not vouchers:
        bot.reply_to(message, "Belum ada voucher.")
        return
    text = "🎫 <b>DAFTAR VOUCHER</b>\n\n"
    for kode, v in vouchers.items():
        sisa = v['max'] - v['terpakai']
        exp = datetime.fromtimestamp(v['expired'], WIB).strftime('%d-%m-%Y %H:%M') if v['expired'] > 0 else "-"
        text += (f"• <code>{kode}</code>\n"
                 f"  Diskon: Rp {v['diskon']:,}\n"
                 f"  Sisa: {sisa}/{v['max']}\n"
                 f"  Expired: {exp}\n\n")
    bot.reply_to(message, text, parse_mode="HTML")

@bot.message_handler(commands=['grafik'])
def cmd_grafik_bulanan(message):
    if not is_any_admin(message.from_user.id):
        return
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        daily_total = {}
        for o in _read_all_orders():
            if o[7] != "BERHASIL":
                continue
            daily_total[o[1]] = daily_total.get(o[1], 0) + int(''.join(ch for ch in o[5] if ch.isdigit()) or 0)
        if not daily_total:
            bot.reply_to(message, "Belum ada transaksi sukses.")
            return
        plt.figure(figsize=(8, 4))
        plt.plot(sorted(daily_total.keys()),
                 [daily_total[t] for t in sorted(daily_total.keys())], marker='o')
        plt.title("Tren Penjualan")
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        bot.send_photo(message.chat.id, buf, caption="📈 Grafik Penjualan.")
    except Exception as e:
        bot.reply_to(message, f"Gagal: {e}")

@bot.message_handler(commands=['poin'])
def admin_add_points(message):
    if message.chat.id != ADMIN_TELEGRAM_ID:
        bot.reply_to(message, "⚠️ Perintah khusus admin utama!")
        return
    args = message.text.replace('/poin', '').strip().split()
    if len(args) < 2:
        bot.reply_to(message, "⚠️ Format: /poin @user 1000")
        return
    target_username = args[0].strip()
    try:
        jumlah_tambah = int(args[1])
    except ValueError:
        bot.reply_to(message, "⚠️ Jumlah poin harus angka.")
        return
    if not target_username.startswith('@'):
        bot.reply_to(message, "⚠️ Format harus @username")
        return
    target_chat_id = None
    try:
        with open(F_USERS, "r") as f:
            for line in f:
                uid = line.strip()
                if uid and not uid.startswith('-'):
                    try:
                        chat_info = bot.get_chat(int(uid))
                        uname = f"@{chat_info.username}" if chat_info.username else ""
                        if uname.lower() == target_username.lower():
                            target_chat_id = int(uid)
                            break
                    except Exception:
                        pass
    except FileNotFoundError:
        pass
    if not target_chat_id:
        bot.reply_to(message, "User tidak ditemukan.")
        return
    try:
        chat_info = bot.get_chat(target_chat_id)
        add_user_points(target_chat_id, jumlah_tambah, "Penambahan manual admin")
        total_pasti = get_user_points(target_chat_id)
        bot.reply_to(message, f"✅ +{jumlah_tambah} poin ke @{chat_info.username or target_username}. Total: {total_pasti} poin.")
        try:
            bot.send_message(target_chat_id,
                             f"🎁 <b>ADMIN MENAMBAHKAN POIN!</b>\n\n+{jumlah_tambah} Poin\nTotal: <b>{total_pasti} Poin</b>",
                             parse_mode="HTML")
        except Exception:
            pass
    except Exception:
        bot.reply_to(message, "Gagal menambahkan poin.")

@bot.message_handler(commands=['bc', 'broadcast'])
def broadcast_message(message):
    if not is_super_admin(message.chat.id):
        return
    pesan_bc = message.text.replace('/bc', '').replace('/broadcast', '').strip()
    if not pesan_bc:
        bot.reply_to(message, "⚠️ Format: /bc pesan...")
        return
    try:
        with open(F_USERS, "r") as f:
            users = [line.strip() for line in f.read().splitlines() if line.strip()]
    except FileNotFoundError:
        bot.reply_to(message, "Belum ada user.")
        return
    success = 0
    for chat_id in set(users):
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI</b>\n\n{pesan_bc}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ Broadcast selesai. Berhasil: {success}")

@bot.message_handler(commands=['bcs'])
def broadcast_buyers_only(message):
    if not is_super_admin(message.chat.id):
        return
    pesan_bcs = message.text.replace('/bcs', '').strip()
    if not pesan_bcs:
        bot.reply_to(message, "⚠️ Format: /bcs pesan...")
        return
    buyer_ids = set()
    try:
        with open(F_ORDERS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 8 and parts[7].strip() == "BERHASIL":
                    buyer_ids.add(parts[0].strip())
    except FileNotFoundError:
        pass
    success = 0
    for chat_id in buyer_ids:
        try:
            bot.send_message(chat_id, f"💎 <b>INFO KHUSUS VIP</b>\n\n{pesan_bcs}", parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ Broadcast VIP selesai. Berhasil: {success}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if is_spam_command(message.chat.id):
        return
    chat_id = message.chat.id
    if is_banned(chat_id):
        return
    save_user(chat_id)
    user = message.from_user
    l = get_lang(user)

    args = message.text.split()
    if len(args) > 1 and args[1].startswith("ref_"):
        ref_id = args[1].replace("ref_", "").strip()
        if ref_id.isdigit():
            register_referral(ref_id, chat_id)

    user_points = get_user_points(chat_id)
    welcome_text = build_welcome_text(user, user_points, l)
    markup = build_main_menu_markup(l)
    bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['riwayat', 'history'])
def cmd_riwayat(message):
    if is_spam_command(message.chat.id):
        return
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    get_latest_user_order_data(message.chat.id)
    orders = get_user_orders(message.chat.id)
    if not orders:
        text = (f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n"
                "❌ Belum ada riwayat pesanan tercatat.")
    else:
        text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
        for idx, o in enumerate(orders[-5:], 1):
            st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK",
                  "CANCELLED": "❌ DIBATALKAN", "EXPIRED": "⌛ EXPIRED"}.get(o['status'], "⏳ PENDING")
            text += (f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n"
                     f"   • Resi: <code>{o['resi']}</code>\n   • Status: {st}\n\n")
    bot.reply_to(message, text, reply_markup=get_back_markup(l), parse_mode="HTML",
                 disable_web_page_preview=True)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    if is_spam_command(message.chat.id):
        return
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    text = (f"🔍 CEK STATUS RESI (Kak {user.first_name})\n\n"
            "Kirim Nomor Resi atau screenshot bukti transfer.\n\n"
            f"💬 Admin: {ADMIN_USERNAME}") if l == 'id' else "🔍 CHECK RECEIPT"
    bot.reply_to(message, text, disable_web_page_preview=True)

@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    if is_spam_command(message.chat.id):
        return
    try:
        save_user(message.chat.id)
        user = message.from_user
        l = get_lang(user)
        coupon_status = get_user_coupon_status(message.chat.id)
        markup = build_katalog_markup(1, l)
        katalog_text = build_katalog_text(1, user, l, coupon_status)
        bot.send_message(message.chat.id, katalog_text, reply_markup=markup, parse_mode="HTML",
                         disable_web_page_preview=True)
    except Exception as e:
        log_error("cmd_katalog", e)
        bot.reply_to(message, "Terjadi kesalahan saat memuat katalog.")

@bot.message_handler(commands=['sc'])
def cmd_sc_interactive(message):
    if not is_super_admin(message.chat.id):
        return
    save_user(message.chat.id)
    args = message.text.replace('/sc', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format: /sc @UsernamePembeli")
        return
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, data_paket in MASTER_PAKET.items():
        nama, harga_angka, harga_str, poin, _ = data_paket
        markup.add(types.InlineKeyboardButton(f"💎 {nama} — {harga_str}", callback_data=f"sc_{code}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target: <b>{target_buyer}</b>\n👇 Pilih paket:",
                 reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['scp'])
def cmd_scp_interactive(message):
    if message.chat.id != ADMIN_TELEGRAM_ID:
        return
    save_user(message.chat.id)
    args = message.text.replace('/scp', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format: /scp @UsernamePembeli")
        return
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, data_paket in MASTER_PAKET.items():
        nama, harga_angka, harga_str, poin, _ = data_paket
        markup.add(types.InlineKeyboardButton(f"🪙 {nama} — {poin} Poin", callback_data=f"scp_{code}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target: <b>{target_buyer}</b>\n👇 Pilih paket (poin):",
                 reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['testi', 'push'])
def admin_push_testi(message):
    if not is_any_admin(message.from_user.id):
        return
    try:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(),
                         message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        bot.reply_to(message, "✅ Testimoni terkirim ke grup. (Stok otomatis turun!)")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal: {e}")

# =====================================================================================
#  BAGIAN 8: CALLBACK HANDLERS
# =====================================================================================

def mask_username(username):
    if not username:
        return "@Buyer***"
    clean_uname = username.strip()
    if not clean_uname.startswith('@'):
        clean_uname = f"@{clean_uname}"
    name_part = clean_uname[1:]
    if len(name_part) <= 4:
        masked = name_part[:2] + "***"
    else:
        keep_len = max(3, len(name_part) // 2)
        masked = name_part[:keep_len] + "***"
    return f"@{masked}"

def generate_real_testimonial(chat_id, resi_target):
    now = datetime.now(WIB)
    current_hour = now.hour
    if 4 <= current_hour < 11:
        waktu_ket = "pagi ini"
    elif 11 <= current_hour < 15:
        waktu_ket = "siang ini"
    elif 15 <= current_hour < 18:
        waktu_ket = "sore ini"
    else:
        waktu_ket = "malam ini"
    jam_str = now.strftime('%H:%M WIB')
    try:
        chat_info = bot.get_chat(int(chat_id))
        raw_username = f"@{chat_info.username}" if chat_info.username else chat_info.first_name
    except Exception:
        raw_username = "@BuyerMlbb"
    masked_name = mask_username(raw_username)
    detail_paket = "VIP Package"
    detail_harga = "Rp 100.000"
    pay_method_label = "TRANSFER MANUAL"
    try:
        with open(F_ORDERS, "r") as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts) >= 11 and parts[6].strip() == resi_target.strip():
                    detail_paket = parts[4]
                    detail_harga = parts[5]
                    pay_method = parts[9] if len(parts) > 9 else "TRANSFER"
                    pay_method_label = "REDEEMED VIA LOYALTY POINTS 🪙" if pay_method == "POIN" else "SUCCESS & SCRIPT DELIVERED 💳"
                    break
    except Exception as e:
        log_error("generate_real_testimonial", e)
    return (
        "🚨 <b>REAL-TIME TRANSACTION REPORT</b> 🚨\n\n"
        f"✅ Buyer ID: {masked_name}\n"
        f"📦 Item Purchased: {detail_paket}\n"
        f"💵 Price / Method: {detail_harga} ({pay_method_label})\n"
        f"⏱️ Time: {jam_str} ({waktu_ket})\n"
        f"🔒 Status: BERHASIL & TERKIRIM\n\n"
        "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
        f"🤖 Bot Store: @{bot.get_me().username}"
    )

def loading_toast(call_id, text="⏳ Mohon tunggu sebentar, sistem sedang memproses permintaanmu..."):
    try:
        bot.answer_callback_query(call_id, text=text, show_alert=False)
    except Exception:
        pass

@bot.callback_query_handler(func=lambda call: True)
def callback_handler_master(call):
    save_user(call.message.chat.id)
    user = call.from_user
    l = get_lang(user)
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    data = call.data

    if is_banned(chat_id):
        return

    if is_spam_callback(chat_id):
        bot.answer_callback_query(call.id, "⚠️ Santai kak, jangan spam 🙏")
        return

    lock_key = f"{chat_id}_{data}"
    if lock_key in processing_lock:
        bot.answer_callback_query(call.id, "⏳ Diproses...")
        return
    processing_lock.add(lock_key)

    try:
        # --- ADMIN ACTIONS ---
        if data.startswith(('acc_', 'tolak_', 'acc|', 'tolak|', 'apoin|', 'tpoin|')):
            loading_toast(call.id, "⏳ Memverifikasi transaksi...")
            try:
                sep = '|' if '|' in data else '_'
                parts = data.split(sep)
                if len(parts) < 2:
                    bot.answer_callback_query(call.id, text="Format tombol tidak valid.", show_alert=True)
                    return
                action = parts[0].replace('_', '')
                resi_code = parts[1] if action in ['apoin', 'tpoin'] else (parts[2] if len(parts) > 2 else parts[1])
                target_user_id = parts[1] if action not in ['apoin', 'tpoin'] and len(parts) > 2 else None
                current_db_status = ""
                try:
                    with open(F_ORDERS, "r") as f:
                        for line in f:
                            p = line.strip().split('|')
                            if len(p) >= 8 and p[6].strip() == resi_code.strip():
                                target_user_id = p[0]
                                current_db_status = p[7].strip()
                                break
                except Exception:
                    pass
                if not target_user_id:
                    bot.answer_callback_query(call.id, text="Resi tidak ditemukan!", show_alert=True)
                    return
                if current_db_status != "PENDING":
                    bot.answer_callback_query(call.id, text=f"⚠️ Sudah diproses: {current_db_status}!", show_alert=True)
                    return
                original_text = call.message.caption or call.message.text or ""
                if action in ('acc', 'apoin'):
                    p_points_val = 0
                    if action == 'apoin':
                        try:
                            with open(F_ORDERS, "r") as f:
                                for line in f:
                                    p = line.strip().split('|')
                                    if len(p) >= 11 and p[6].strip() == resi_code.strip():
                                        p_points_val = int(p[10]) if p[10].isdigit() else 0
                                        break
                        except Exception:
                            pass
                        current_user_pts = get_user_points(target_user_id)
                        if current_user_pts >= p_points_val:
                            reduce_user_points(target_user_id, p_points_val, "Penukaran poin paket VIP")
                        else:
                            bot.answer_callback_query(call.id, text="Poin pembeli tidak cukup!", show_alert=True)
                            return
                    update_order_status_by_resi(resi_code, "BERHASIL")
                    try:
                        auto_testi_message = generate_real_testimonial(target_user_id, resi_code)
                        bot.send_message(chat_id=GROUP_CHAT_ID, text=auto_testi_message,
                                         message_thread_id=GROUP_TOPIC_ID,
                                         parse_mode="HTML", disable_web_page_preview=True)
                    except Exception as e:
                        log_error("auto_send_testi", e)
                    status_label = (f"✅ DI-ACC ADMIN (Poin Dipotong {p_points_val})"
                                    if action == 'apoin' else
                                    "✅ TELAH DI-ACC ADMIN")
                    new_admin_text = original_text + f"\n\n<b>STATUS: {status_label}</b>"
                    if call.message.content_type == 'photo':
                        bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                                 caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                    else:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text=new_admin_text, parse_mode="HTML", reply_markup=None)
                    detail_paket, detail_harga, waktu_beli = "VIP Package", "Rp 100.000", datetime.now(WIB).strftime('%d-%m-%Y, %H:%M:%S WIB')
                    try:
                        with open(F_ORDERS, "r") as f:
                            for line in f:
                                p = line.strip().split('|')
                                if len(p) >= 8 and p[6].strip() == resi_code.strip():
                                    detail_paket, detail_harga = p[4], p[5]
                                    waktu_beli = f"{p[1]}, {p[3]}"
                                    break
                    except Exception:
                        pass
                    bot.send_message(target_user_id,
                                     "🛒 <b>PakelMlbbStore:</b>\n"
                                     "🎉 <b>PEMBAYARAN ANDA TELAH DI-ACC ADMIN!</b> 🎉\n\n"
                                     f"🔑 No Resi: <code>{resi_code}</code>\n"
                                     "Status: <b>BERHASIL</b>. Selamat menikmati script-nya!\n\n"
                                     "📋 <b>SALIN FORMAT DI BAWAH & KIRIM KE ADMIN:</b>",
                                     parse_mode="HTML")
                    template_chat_admin = (
                        "🔥 KONFIRMASI KLAIM SCRIPT VIP 🔥\n"
                        f"📦 Paket: {detail_paket}\n"
                        f"💵 Harga: {detail_harga}\n"
                        f"🔑 No Resi: {resi_code}\n"
                        f"⏱️ Waktu Order: {waktu_beli}\n"
                        "Status: Lunas & Sudah di-ACC Bot.\n"
                        "Mohon kirimkan link/file script-nya ya Kak. Terima kasih! 🙏"
                    )
                    bot.send_message(target_user_id, f"<code>{template_chat_admin}</code>", parse_mode="HTML")
                    markup_rating = types.InlineKeyboardMarkup(row_width=5)
                    markup_rating.add(
                        types.InlineKeyboardButton("⭐ 1", callback_data=f"rate|1|{resi_code}"),
                        types.InlineKeyboardButton("⭐ 2", callback_data=f"rate|2|{resi_code}"),
                        types.InlineKeyboardButton("⭐ 3", callback_data=f"rate|3|{resi_code}"),
                        types.InlineKeyboardButton("⭐ 4", callback_data=f"rate|4|{resi_code}"),
                        types.InlineKeyboardButton("⭐ 5", callback_data=f"rate|5|{resi_code}")
                    )
                    bot.send_message(target_user_id,
                                     f"⭐ <b>BAGAIMANA PELAYANAN KAMI?</b>\n\nResi: <code>{resi_code}</code>\nBerikan penilaian:",
                                     reply_markup=markup_rating, parse_mode="HTML")
                elif action in ('tolak', 'tpoin'):
                    update_order_status_by_resi(resi_code, "DITOLAK")
                    new_admin_text = original_text + "\n\n<b>STATUS: ❌ DITOLAK</b>"
                    if call.message.content_type == 'photo':
                        bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                                 caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                    else:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text=new_admin_text, parse_mode="HTML", reply_markup=None)
                    bot.send_message(target_user_id,
                                     f"❌ <b>PEMBAYARAN DITOLAK</b>\n\nResi: <code>{resi_code}</code>\nKupon dikembalikan. Hubungi: {ADMIN_USERNAME}",
                                     parse_mode="HTML")
            except Exception as e:
                log_error("callback_admin", e)
                bot.answer_callback_query(call.id, text=f"Error: {e}", show_alert=True)
            return

        # --- MENU UTAMA ---
        if data == 'menu_utama':
            loading_toast(call.id, "⏳ Mengembalikan ke menu...")
            user_points = get_user_points(chat_id)
            markup = build_main_menu_markup(l)
            text = build_welcome_text(user, user_points, l)
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                      reply_markup=markup, parse_mode="HTML",
                                      disable_web_page_preview=True)
            except Exception:
                bot.send_message(chat_id=chat_id, text=text, reply_markup=markup, parse_mode="HTML")
            return

        elif data == 'menu_referral':
            loading_toast(call.id, "⏳ Memuat data referral...")
            _kirim_poin_referral(chat_id, message_id, l)
            return

        elif data == 'menu_profil':
            loading_toast(call.id, "⏳ Memuat profil...")
            _kirim_profil_akun(chat_id, message_id, user, l)
            return

        elif data == 'menu_lucky':
            loading_toast(call.id, "⏳ Memuat Lucky Draw...")
            can_spin = can_spin_now(chat_id)
            if can_spin:
                text = (
                    "🎰 <b>LUCKY DRAW HARIAN</b> 🎰\n\n"
                    "Kamu punya <b>1 kesempatan spin</b> hari ini!\n\n"
                    "🎁 Hadiah yang bisa didapat:\n"
                    "• 🪙 Poin 5 – 50\n"
                    "• 🎁 Diskon 5% – 10%\n"
                    "• 💎 Paket Semi-Safe GRATIS (rare!)\n\n"
                    "Klik tombol di bawah untuk spin!"
                )
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(
                    types.InlineKeyboardButton("🎰 SPIN SEKARANG!", callback_data='spin_now'),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )
            else:
                sisa = get_remaining_spin_time(chat_id)
                text = (
                    "🎰 <b>LUCKY DRAW HARIAN</b> 🎰\n\n"
                    "❌ Kamu sudah spin hari ini.\n\n"
                    f"⏰ Spin berikutnya: <b>{sisa}</b>\n\n"
                    "💡 Balik lagi besok buat spin gratis!"
                )
                markup = types.InlineKeyboardMarkup(row_width=1)
                markup.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text,
                                      parse_mode="HTML", reply_markup=markup)
            except Exception:
                bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)
            return

        elif data == 'spin_now':
            loading_toast(call.id, "🎰 Spin berputar...")
            if not can_spin_now(chat_id):
                bot.answer_callback_query(call.id, text="❌ Kamu sudah spin hari ini!", show_alert=True)
                return
            hadiah = roll_lucky_draw()
            label, tipe, nilai, _ = hadiah
            save_spin(chat_id)
            if tipe == "poin":
                add_user_points(chat_id, nilai, "Hadiah Lucky Draw Harian")
                result_text = (
                    f"🎉 <b>SELAMAT!</b> 🎉\n\n"
                    f"🎰 Hasil Spin: <b>{label}</b>\n\n"
                    f"✅ +{nilai} poin sudah masuk ke saldo kamu!\n"
                    f"🪙 Total Poin Sekarang: <b>{get_user_points(chat_id)} Poin</b>\n\n"
                    "Balik lagi besok buat spin gratis!"
                )
            elif tipe == "diskon":
                try:
                    with open(F_USER_VOUCHER, "a") as f:
                        f.write(f"{chat_id}|DISKON{nilai}|{int(time.time())}\n")
                except Exception:
                    pass
                result_text = (
                    f"🎉 <b>SELAMAT!</b> 🎉\n\n"
                    f"🎰 Hasil Spin: <b>{label}</b>\n\n"
                    f"✅ Voucher diskon {nilai}% aktif otomatis di akun kamu!\n"
                    "Tinggal checkout paket & diskon akan diapply.\n\n"
                    "Balik lagi besok buat spin gratis!"
                )
            else:
                result_text = (
                    f"💎 <b>JACKPOT!!!</b> 💎\n\n"
                    f"🎰 Hasil Spin: <b>{label}</b>\n\n"
                    "🎉 Kamu menang PAKET SEMI-SAFE GRATIS!\n\n"
                    f"📩 Silakan hubungi admin {ADMIN_USERNAME} dengan screenshot pesan ini buat klaim hadiah!"
                )
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=result_text,
                                      parse_mode="HTML",
                                      reply_markup=get_back_markup(l))
            except Exception:
                bot.send_message(chat_id, result_text, parse_mode="HTML",
                                 reply_markup=get_back_markup(l))
            return

        elif data == 'menu_testi':
            loading_toast(call.id, "⏳ Memuat testimoni...")
            fake_data = generate_fake_testimonials_list()
            testi_text = (f"🌟 LIVE TESTIMONI (Kak {user.first_name})\n\n"
                          f"{fake_data}💡 Toko 100% amanah! 🚀")
            markup_testi = types.InlineKeyboardMarkup(row_width=1)
            markup_testi.add(
                types.InlineKeyboardButton("🔄 Refresh", callback_data='menu_testi'),
                types.InlineKeyboardButton("🌟 Testi Lengkap", url=CHANNEL_TESTI_LINK),
                types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text,
                                  reply_markup=markup_testi, disable_web_page_preview=True)
            return

        elif data == 'menu_riwayat':
            loading_toast(call.id, "⏳ Memuat riwayat...")
            get_latest_user_order_data(chat_id)
            orders = get_user_orders(chat_id)
            if not orders:
                riw_text = f"📋 RIWAYAT (Kak {user.first_name})\n\n❌ Belum ada riwayat."
            else:
                riw_text = f"📋 <b>RIWAYAT PESANAN (Kak {user.first_name})</b>\n\n"
                for idx, o in enumerate(orders[-5:], 1):
                    st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK",
                          "CANCELLED": "❌ DIBATALKAN", "EXPIRED": "⌛ EXPIRED"}.get(o['status'], "⏳ PENDING")
                    riw_text += (f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n"
                                 f"   • Resi: <code>{o['resi']}</code>\n   • Status: {st}\n\n")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=riw_text,
                                  reply_markup=get_back_markup(l), parse_mode="HTML",
                                  disable_web_page_preview=True)
            return

        elif data == 'menu_promo':
            loading_toast(call.id, "⏳ Memuat promo...")
            status_c = get_user_coupon_status(chat_id)
            user_pts = get_user_points(chat_id)
            tier_label, multiplier, diskon = get_user_tier(chat_id)
            if status_c == "AVAILABLE":
                kupon_info = "🎁 Kupon Member Baru: <b>TERSEDIA</b>"
            elif status_c == "PENDING":
                kupon_info = "🎁 Kupon Member Baru: <b>PENDING</b>"
            else:
                kupon_info = "🎁 Kupon Member Baru: <b>SUDAH DIGUNAKAN</b>"
            promo_text = (
                f"🎁 <b>PROMO & POIN (Kak {user.first_name})</b>\n\n"
                f"🪙 Saldo Poin: <b>{user_pts} Poin</b>\n"
                f"🏅 Tier: <b>{tier_label}</b>\n"
                f"   ├ Bonus Poin: <b>x{multiplier}</b>\n"
                f"   └ Diskon    : <b>{diskon}%</b>\n\n"
                f"{kupon_info}\n\n"
                "💡 <i>Kumpulkan poin & naikin tier buat dapet bonus lebih gede!</i>"
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text,
                                  reply_markup=get_back_markup(l), parse_mode="HTML")
            return

        elif data == 'menu_faq':
            loading_toast(call.id, "⏳ Memuat FAQ...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="💡 FAQ\n\n❓ Aman dari banned?\n💬 A: Sangat aman.",
                                  reply_markup=get_back_markup(l))
            return

        elif data in ('menu_katalog', 'katalog_part1'):
            loading_toast(call.id, "⏳ Memuat katalog 1...")
            try:
                coupon_status = get_user_coupon_status(chat_id)
                markup = build_katalog_markup(1, l)
                katalog_text = build_katalog_text(1, user, l, coupon_status)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text,
                                      reply_markup=markup, parse_mode="HTML",
                                      disable_web_page_preview=True)
            except Exception as e:
                log_error("katalog_part1", e)
            return

        elif data == 'katalog_part2':
            loading_toast(call.id, "⏳ Memuat katalog 2...")
            try:
                coupon_status = get_user_coupon_status(chat_id)
                markup = build_katalog_markup(2, l)
                katalog_text = build_katalog_text(2, user, l, coupon_status)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text,
                                      reply_markup=markup, parse_mode="HTML",
                                      disable_web_page_preview=True)
            except Exception as e:
                log_error("katalog_part2", e)
            return

        elif data in MASTER_PAKET:
            loading_toast(call.id, "⏳ Menyiapkan opsi...")
            p_name, p_price_angka, p_price_str, p_points, _ = MASTER_PAKET[data]
            stok = get_stock(data)
            if stok <= 0:
                bot.answer_callback_query(call.id, text="❌ Maaf, stok paket ini habis! Tunggu restock ya 🙏", show_alert=True)
                return
            choice_text = (f"🛒 <b>PILIH METODE PEMBAYARAN</b>\n\n"
                           f"📦 Paket: <b>{p_name}</b>\n"
                           f"💵 Harga: <b>{p_price_str}</b>\n"
                           f"🪙 Atau Tukar: <b>{p_points} Poin</b>\n"
                           f"📦 Stok: <b>{stok} unit</b>")
            markup_choice = types.InlineKeyboardMarkup(row_width=1)
            markup_choice.add(
                types.InlineKeyboardButton(f"🪙 Bayar Pakai Saldo Poin ({p_points} Poin)", callback_data=f"paymode_|poin|{data}"),
                types.InlineKeyboardButton(f"💳 Transfer Manual DANA/GoPay ({p_price_str})", callback_data=f"paymode_|transfer|{data}"),
                types.InlineKeyboardButton("📱 QRIS (Otomatis Kirim Foto)", callback_data=f"paymode_|qris|{data}"),
                types.InlineKeyboardButton(t['back'], callback_data='menu_katalog')
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=choice_text,
                                  reply_markup=markup_choice, parse_mode="HTML")
            return

        elif data == 'menu_cara_order':
            loading_toast(call.id, "⏳ Memuat panduan...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="❓ CARA ORDER\n1. Pilih paket.\n2. Pilih metode bayar.\n3. Bayar.\n4. Kirim bukti.\n5. Tunggu ACC.",
                                  reply_markup=get_back_markup(l), disable_web_page_preview=True)
            return

        elif data == 'menu_bayar':
            loading_toast(call.id, "⏳ Memuat metode bayar...")
            markup_bayar = types.InlineKeyboardMarkup(row_width=1)
            markup_bayar.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
            pay_text = (
                "💳 <b>METODE PEMBAYARAN</b>\n\n"
                "1️⃣ <b>QRIS (All E-Wallet):</b>\n   Bot kirim gambar QRIS otomatis saat checkout\n\n"
                f"2️⃣ <b>Transfer Manual:</b>\n   • DANA/GoPay: <code>{INFO_DANA}</code>\n   • A/N: PakelMlbb\n\n"
                f"3️⃣ <b>Saweria:</b>\n   {INFO_SAWERIA}"
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=pay_text,
                                  reply_markup=markup_bayar, parse_mode="HTML",
                                  disable_web_page_preview=True)
            return

        elif data == 'menu_konfirmasi':
            loading_toast(call.id, "⏳ Memuat instruksi...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="✅ Kirim screenshot bukti transfer ke bot ini.",
                                  reply_markup=get_back_markup(l), disable_web_page_preview=True)
            return

        elif data.startswith('cancel_'):
            loading_toast(call.id, "⏳ Membatalkan pesanan...")
            resi_target = data.replace('cancel_', '')
            admin_msg_id = None
            try:
                with open(F_ORDERS, "r") as f:
                    for line in f:
                        p = line.strip().split('|')
                        if len(p) >= 12 and p[6].strip() == resi_target.strip():
                            if p[7].strip() != "PENDING":
                                bot.answer_callback_query(call.id, text="Pesanan sudah diproses sebelumnya.", show_alert=True)
                                return
                            admin_msg_id = int(p[11]) if p[11].isdigit() and int(p[11]) > 0 else None
                            break
            except Exception:
                pass
            success = update_order_status_by_resi(resi_target, "CANCELLED")
            if success:
                if admin_msg_id:
                    try:
                        new_admin_caption = call.message.caption or call.message.text or "KLAIM MASUK"
                        new_admin_caption += "\n\n<b>STATUS: ❌ DIBATALKAN PEMBELI</b>"
                        if call.message.content_type == 'photo':
                            bot.edit_message_caption(chat_id=GROUP_PAY_ID, message_id=admin_msg_id,
                                                     caption=new_admin_caption, parse_mode="HTML", reply_markup=None)
                        else:
                            bot.edit_message_text(chat_id=GROUP_PAY_ID, message_id=admin_msg_id,
                                                  text=new_admin_caption, parse_mode="HTML", reply_markup=None)
                    except Exception as e:
                        log_error("edit_admin_msg_cancel", e)
                cancel_text = (
                    f"❌ <b>PESANAN DIBATALKAN</b>\n\nResi: <code>{resi_target}</code>\nPoin kamu tetap utuh."
                )
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=cancel_text,
                                          parse_mode="HTML", reply_markup=get_back_markup(l))
                except Exception:
                    bot.send_message(chat_id, cancel_text, parse_mode="HTML", reply_markup=get_back_markup(l))
                bot.answer_callback_query(call.id, text="Pesanan dibatalkan!")
            else:
                bot.answer_callback_query(call.id, text="Pesanan sudah diproses.", show_alert=True)
            return

        elif data.startswith('paymode_'):
            parts = data.split('|')
            if len(parts) < 3:
                bot.answer_callback_query(call.id, text="Data tidak valid.", show_alert=True)
                return
            action_type, paket_code = parts[1], parts[2]
            if paket_code not in MASTER_PAKET:
                bot.answer_callback_query(call.id, text="Paket tidak ditemukan.", show_alert=True)
                return
            p_name, p_price_angka, p_price_str, p_points, _ = MASTER_PAKET[paket_code]
            tier_label, multiplier, diskon_tier = get_user_tier(chat_id)
            resi_unik = f"PKL-MLBB-{random.randint(10000, 99999)}"

            # ==== POIN ====
            if action_type == 'poin':
                loading_toast(call.id, "⏳ Cek saldo poin...")
                user_pts = get_user_points(chat_id)
                if user_pts >= p_points:
                    coupon_status = get_user_coupon_status(chat_id)
                    if coupon_status == "AVAILABLE":
                        set_user_coupon_status(chat_id, "PENDING")
                    pending_poin_text = (
                        f"🪙 <b>INVOICE VIA POIN (PENDING)</b>\n\n"
                        f"📦 Paket: {p_name}\n"
                        f"🪙 Poin: <b>{p_points} Poin</b> (Sisa: {user_pts})\n"
                        f"🔑 Resi: <code>{resi_unik}</code>\n\n"
                        "⏳ Menunggu ACC admin."
                    )
                    markup_poin_inv = types.InlineKeyboardMarkup(row_width=1)
                    markup_poin_inv.add(
                        types.InlineKeyboardButton("❌ Batalkan", callback_data=f"cancel_{resi_unik}"),
                        types.InlineKeyboardButton("📦 Riwayat", callback_data='menu_riwayat'),
                        types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                    )
                    try:
                        bot.delete_message(chat_id=chat_id, message_id=message_id)
                    except Exception:
                        pass
                    bot.send_message(chat_id, pending_poin_text, reply_markup=markup_poin_inv, parse_mode="HTML")
                    try:
                        waktu_str = datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S WIB')
                        report_admin_poin = (
                            "🪙 <b>KLAIM POIN MASUK!</b>\n\n"
                            f"👤 @{user.username or user.first_name} (ID: <code>{chat_id}</code>)\n"
                            f"📦 {p_name}\n"
                            f"🪙 {p_points} Poin\n"
                            f"⏱️ {waktu_str}\n"
                            f"🔑 Resi: <code>{resi_unik}</code>"
                        )
                        markup_admin_poin = types.InlineKeyboardMarkup(row_width=2)
                        markup_admin_poin.add(
                            types.InlineKeyboardButton("✅ ACC", callback_data=f"apoin|{resi_unik}"),
                            types.InlineKeyboardButton("❌ TOLAK", callback_data=f"tpoin|{resi_unik}")
                        )
                        admin_sent = bot.send_message(GROUP_PAY_ID, report_admin_poin,
                                                      message_thread_id=GROUP_PAY_TOPIC_ID,
                                                      parse_mode="HTML", reply_markup=markup_admin_poin)
                        save_order(chat_id, p_name, f"{p_points} Poin", resi_unik,
                                   payment_method="POIN", point_cost=p_points,
                                   admin_msg_id=admin_sent.message_id)
                    except Exception as e:
                        log_error("report_admin_poin", e)
                        save_order(chat_id, p_name, f"{p_points} Poin", resi_unik,
                                   payment_method="POIN", point_cost=p_points, admin_msg_id=0)
                    bot.answer_callback_query(call.id, text="Menunggu ACC admin!")
                    return
                else:
                    markup_fallback = types.InlineKeyboardMarkup(row_width=1)
                    markup_fallback.add(
                        types.InlineKeyboardButton(f"💳 Bayar Transfer ({p_price_str})", callback_data=f"paymode_|transfer|{paket_code}"),
                        types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                    )
                    fail_text = f"❌ <b>POIN BELUM CUKUP!</b>\nPoin: {user_pts} | Butuh: {p_points}"
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=fail_text,
                                              parse_mode="HTML", reply_markup=markup_fallback)
                    except Exception:
                        bot.send_message(chat_id, fail_text, parse_mode="HTML", reply_markup=markup_fallback)
                    bot.answer_callback_query(call.id, text="Poin kurang!", show_alert=True)
                    return

            # ==== TRANSFER ====
            elif action_type == 'transfer':
                loading_toast(call.id, "⏳ Menerbitkan invoice...")
                coupon_status = get_user_coupon_status(chat_id)
                is_promo_used = (coupon_status == "AVAILABLE")
                harga_final = p_price_angka
                if diskon_tier > 0:
                    harga_final = int(p_price_angka * (100 - diskon_tier) / 100)
                if is_promo_used:
                    harga_final -= 10000
                harga_final_str = f"Rp {harga_final:,}"
                save_order(chat_id, p_name, harga_final_str, resi_unik, payment_method="TRANSFER",
                           point_cost=0, admin_msg_id=0)
                if is_promo_used:
                    set_user_coupon_status(chat_id, "PENDING")
                invoice_text = (
                    f"{t['inv_title'].format(name=user.first_name)}\n\n"
                    f"📦 <b>Nama Paket</b>       : {p_name}\n"
                    f"💵 <b>Harga Dasar</b>      : {p_price_str}\n"
                )
                if diskon_tier > 0:
                    invoice_text += f"🏅 <b>Diskon Tier ({tier_label})</b>  : -{diskon_tier}%\n"
                if is_promo_used:
                    invoice_text += "🎁 <b>Promo Member Baru</b>  : -Rp 10.000\n"
                invoice_text += (
                    f"💰 <b>Total Bayar Transfer</b> : <b>{harga_final_str}</b>\n"
                    f"🔑 <b>Nomor Resi Unik</b>  : <code>{resi_unik}</code>\n"
                    f"⏱️ <b>Batas Waktu</b>      : 15 Menit\n\n"
                    "💳 <b>PEMBAYARAN VIA TRANSFER MANUAL</b>\n"
                    "Silakan transfer ke salah satu rekening di bawah:\n\n"
                    f"• <b>DANA / GoPay:</b> <code>{INFO_DANA}</code>\n"
                    "• <b>Atas Nama:</b> PakelMlbb\n\n"
                    "⚠️ <b>PENTING — WAJIB DIBACA!</b>\n"
                    f"Masukkan nominal transfer <b>PERSIS</b> sebesar:\n"
                    f"👉 <b>{harga_final_str}</b>\n\n"
                    "Jangan dilebihkan atau dikurangi ya Kak, biar admin gampang verifikasi "
                    "dan pesananmu cepet diproses! 🙏\n\n"
                    "🛡️ <b>INSTRUKSI KONFIRMASI:</b>\n"
                    "Setelah sukses transfer, kirim <b>Screenshot Bukti Transfer</b> ke bot ini untuk "
                    f"mendapatkan script VIP.\n\n👉 Admin: {ADMIN_USERNAME}"
                )
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
                bot.send_message(chat_id, invoice_text, reply_markup=markup_inv,
                                 parse_mode="HTML", disable_web_page_preview=True)
                return

            # ==== QRIS (1 GAMBAR + NOMINAL BULAT) ====
            elif action_type == 'qris':
                loading_toast(call.id, "⏳ Menyiapkan gambar QRIS...")
                coupon_status = get_user_coupon_status(chat_id)
                is_promo_used = (coupon_status == "AVAILABLE")

                harga_final_qris = p_price_angka
                if diskon_tier > 0:
                    harga_final_qris = int(p_price_angka * (100 - diskon_tier) / 100)
                if is_promo_used:
                    harga_final_qris -= 10000

                save_order(chat_id, p_name, f"Rp {harga_final_qris:,}", resi_unik,
                           payment_method="QRIS", point_cost=0, admin_msg_id=0)
                if is_promo_used:
                    set_user_coupon_status(chat_id, "PENDING")

                invoice_caption = (
                    f"{t['inv_title'].format(name=user.first_name)}\n\n"
                    f"📦 <b>Nama Paket</b>       : {p_name}\n"
                    f"💵 <b>Harga Dasar</b>      : {p_price_str}\n"
                )
                if diskon_tier > 0:
                    invoice_caption += f"🏅 <b>Diskon Tier ({tier_label})</b>  : -{diskon_tier}%\n"
                if is_promo_used:
                    invoice_caption += "🎁 <b>Promo Member Baru</b>  : -Rp 10.000\n"
                invoice_caption += (
                    f"💰 <b>Total Bayar QRIS</b> : <b>Rp {harga_final_qris:,}</b>\n"
                    f"🔑 <b>Nomor Resi Unik</b>  : <code>{resi_unik}</code>\n"
                    f"⏱️ <b>Batas Waktu</b>      : 15 Menit\n\n"
                    "📱 <b>PEMBAYARAN VIA QRIS</b>\n"
                    "Silakan scan gambar QRIS di atas menggunakan aplikasi e-wallet / m-banking Anda "
                    "(DANA, OVO, GoPay, ShopeePay, LinkAja, Mobile Banking, dll).\n\n"
                    "⚠️ <b>PENTING — WAJIB DIBACA!</b>\n"
                    f"Masukkan nominal transfer <b>PERSIS</b> sebesar:\n"
                    f"👉 <b>Rp {harga_final_qris:,}</b>\n\n"
                    "Jangan dilebihkan atau dikurangi ya Kak, biar admin gampang verifikasi "
                    "dan pesananmu cepet diproses! 🙏\n\n"
                    "🛡️ <b>INSTRUKSI KONFIRMASI:</b>\n"
                    "Setelah sukses membayar, kirim <b>Screenshot Bukti Transfer</b> ke bot ini untuk "
                    f"mendapatkan script VIP.\n\n👉 Admin: {ADMIN_USERNAME}"
                )

                markup_qris = types.InlineKeyboardMarkup(row_width=1)
                markup_qris.add(
                    types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                    types.InlineKeyboardButton("📦 Cek Riwayat Pesanan Saya", callback_data='menu_riwayat'),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )

                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    pass

                try:
                    bot.send_photo(
                        chat_id=chat_id,
                        photo=QRIS_IMAGE_URL,
                        caption=invoice_caption,
                        parse_mode="HTML",
                        reply_markup=markup_qris
                    )
                except Exception as e:
                    log_error("send_photo_qris", e)
                    bot.send_message(
                        chat_id=chat_id,
                        text=invoice_caption,
                        parse_mode="HTML",
                        reply_markup=markup_qris,
                        disable_web_page_preview=True
                    )
                return

        elif data.startswith('rate|'):
            loading_toast(call.id, "⏳ Memuat ulasan...")
            parts = data.split('|')
            if len(parts) < 3:
                return
            rating_val, resi_code = parts[1], parts[2]
            markup_ulasan = types.InlineKeyboardMarkup(row_width=1)
            if int(rating_val) <= 2:
                markup_ulasan.add(
                    types.InlineKeyboardButton("⚠️ Kurang Memuaskan", callback_data=f"textrev|{resi_code}|{rating_val}|Kurang memuaskan"),
                    types.InlineKeyboardButton("❌ Kecewa", callback_data=f"textrev|{resi_code}|{rating_val}|Sangat buruk")
                )
            elif int(rating_val) == 3:
                markup_ulasan.add(
                    types.InlineKeyboardButton("⭐ Cukup", callback_data=f"textrev|{resi_code}|{rating_val}|Cukup standar"),
                    types.InlineKeyboardButton("👍 Lumayan", callback_data=f"textrev|{resi_code}|{rating_val}|Lumayan bagus")
                )
            else:
                markup_ulasan.add(
                    types.InlineKeyboardButton("🔥 Super Bagus!", callback_data=f"textrev|{resi_code}|{rating_val}|Super bagus"),
                    types.InlineKeyboardButton("🚀 Gercep Banget!", callback_data=f"textrev|{resi_code}|{rating_val}|Sangat puas gercep"),
                    types.InlineKeyboardButton("💯 The Best!", callback_data=f"textrev|{resi_code}|{rating_val}|The best")
                )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text=f"⭐ <b>Terima kasih rating {rating_val} bintang!</b>\nPilih ulasan:",
                                  parse_mode="HTML", reply_markup=markup_ulasan)
            with open(f"pending_review_{chat_id}.txt", "w") as f:
                f.write(f"{resi_code}|{rating_val}")
            return

        elif data.startswith('textrev|'):
            loading_toast(call.id, "⏳ Menyimpan ulasan...")
            parts = data.split('|', 3)
            if len(parts) < 4:
                return
            resi_c, rating_c, quick_text = parts[1], parts[2], parts[3]
            save_user_review(chat_id, rating_c, quick_text)
            try:
                if os.path.exists(f"pending_review_{chat_id}.txt"):
                    os.remove(f"pending_review_{chat_id}.txt")
            except Exception:
                pass
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="🎉 <b>TERIMA KASIH ATAS ULASANNYA!</b>",
                                  parse_mode="HTML")
            return

        elif data.startswith('sc_'):
            loading_toast(call.id, "⏳ Mengirim testi...")
            try:
                data_split = data.split('|')
                if len(data_split) < 2:
                    return
                action, buyer_name = data_split[0], data_split[1]
                paket_code = action.replace('sc_', '')
                if paket_code in MASTER_PAKET:
                    p_nama, _, p_hrg, _, _ = MASTER_PAKET[paket_code]
                else:
                    p_nama, p_hrg = "VIP Package", "Rp 100.000"
                current_hour = datetime.now(WIB).hour
                waktu_ket = "pagi ini" if 4 <= current_hour < 11 else (
                    "siang ini" if 11 <= current_hour < 15 else (
                        "sore ini" if 15 <= current_hour < 18 else "malam ini"))
                post_text = (
                    "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                    f"✅ Buyer ID: {buyer_name}\n"
                    f"📦 Item Purchased: {p_nama}\n"
                    f"💵 Price: {p_hrg}\n"
                    f"⏱️ Time: {random.randint(1, 15)} menit lalu ({waktu_ket})\n"
                    f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
                    "🔥 Terima kasih telah berbelanja! Order juga di bot ya! 👇\n"
                    f"🤖 Bot: @{bot.get_me().username}"
                )
                bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text,
                                 message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
                reduce_stock_random_all()
                auto_restock_if_low()
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=f"✅ <b>TESTI TERKIRIM!</b>\n• {buyer_name}\n• {p_nama}",
                                      parse_mode="HTML")
            except Exception as e:
                bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
            return

        elif data.startswith('scp_'):
            loading_toast(call.id, "⏳ Mengirim testi poin...")
            try:
                data_split = data.split('|')
                if len(data_split) < 2:
                    return
                action, buyer_name = data_split[0], data_split[1]
                paket_code = action.replace('scp_', '')
                if paket_code in MASTER_PAKET:
                    p_nama, _, _, p_poin, _ = MASTER_PAKET[paket_code]
                    p_hrg_poin = f"{p_poin} Poin (Tukar Poin Loyalitas)"
                else:
                    p_nama, p_hrg_poin = "VIP Package", "30 Poin"
                current_hour = datetime.now(WIB).hour
                waktu_ket = "pagi ini" if 4 <= current_hour < 11 else (
                    "siang ini" if 11 <= current_hour < 15 else (
                        "sore ini" if 15 <= current_hour < 18 else "malam ini"))
                post_text = (
                    "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                    f"✅ Buyer ID: {buyer_name}\n"
                    f"📦 Item Purchased: {p_nama}\n"
                    f"💵 Price / Method: {p_hrg_poin}\n"
                    f"⏱️ Time: {random.randint(1, 15)} menit lalu ({waktu_ket})\n"
                    f"🔒 Status: REDEEMED VIA LOYALTY POINTS\n\n"
                    "🔥 Kumpulin poin, sikat script gratisannya! 👇\n"
                    f"🤖 Bot: @{bot.get_me().username}"
                )
                bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text,
                                 message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
                reduce_stock_random_all()
                auto_restock_if_low()
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=f"✅ <b>TESTI POIN TERKIRIM!</b>\n• {buyer_name}\n• {p_nama}",
                                      parse_mode="HTML")
            except Exception as e:
                bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
            return
    except Exception as e:
        log_error("callback_handler_master", e)
    finally:
        threading.Timer(2.0, lambda: processing_lock.discard(lock_key)).start()

def check_bot_status_health():
    try:
        me = bot.get_me()
        print(f"[HEALTH CHECK] Bot @{me.username} (ID: {me.id}) berjalan normal.")
    except Exception as e:
        print(f"[HEALTH CHECK ERROR]: {e}")

threading.Thread(target=check_bot_status_health, daemon=True).start()

@bot.message_handler(func=lambda message: True, content_types=['text'])
def handle_text_and_reviews(message):
    chat_id = message.chat.id
    if message.chat.type != 'private':
        return
    save_user(chat_id)
    user = message.from_user
    l = get_lang(user)
    txt = message.text.strip()

    # Cek voucher manual
    upper_txt = txt.upper().strip()
    if upper_txt.startswith("VOUCHER "):
        kode = upper_txt.replace("VOUCHER ", "").strip()
        valid, diskon, pesan = validate_voucher(kode)
        if valid:
            bot.reply_to(message,
                         f"✅ <b>VOUCHER VALID!</b>\n\n"
                         f"🎫 Kode: <code>{kode}</code>\n"
                         f"💵 Diskon: Rp {diskon:,}\n\n"
                         "Voucher akan otomatis terpakai saat checkout berikutnya.",
                         parse_mode="HTML")
        else:
            bot.reply_to(message, f"❌ Voucher tidak valid: {pesan}")
        return

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
                bot.reply_to(message, "🎉 <b>TERIMA KASIH ATAS ULASANNYA!</b>",
                             reply_markup=get_back_markup(l), parse_mode="HTML")
                return
    except Exception:
        pass

    bot.reply_to(message, f"Halo {user.first_name}! Ketik /start untuk menu utama.",
                 disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if is_banned(message.chat.id):
        return
    if is_spam_photo(message.chat.id):
        bot.reply_to(message, "⚠️ Santai kak, tunggu sebentar ya 🙏")
        return
    save_user(message.chat.id)
    user = message.from_user
    resi_unik, order_status = get_latest_user_order_data(message.chat.id)
    if order_status == "EXPIRED":
        bot.reply_to(message, "❌ <b>WAKTU KONFIRMASI HABIS!</b>", parse_mode="HTML")
        return
    proof_id = message.photo[-1].file_unique_id
    if is_proof_used(proof_id):
        bot.reply_to(message, "⚠️ Bukti transfer ini sudah pernah digunakan!")
        return
    mark_proof_used(proof_id)
    user_caption = message.caption if message.caption else "Tidak ada pesan"
    now = datetime.now(WIB)
    bot.reply_to(message,
                 f"✅ BUKTI DIUNGGAH!\nKak {user.first_name}\n"
                 f"Resi: {resi_unik}\n"
                 f"⏱️ {now.strftime('%d-%m-%Y %H:%M:%S WIB')}\n\n"
                 f"📋 Tunggu verifikasi {ADMIN_USERNAME}",
                 disable_web_page_preview=True)
    try:
        caption_admin = (
            "🚨 <b>BUKTI TRANSFER MASUK!</b>\n\n"
            f"👤 @{user.username or user.first_name} (ID: <code>{user.id}</code>)\n"
            f"✉️ Pesan: \"{user_caption}\"\n"
            f"⏱️ {now.strftime('%d-%m-%Y %H:%M:%S WIB')}\n"
            f"🔑 Resi: {resi_unik}\n\n"
            "👇 Cek mutasi, klik ACC atau TOLAK!"
        )
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("✅ ACC", callback_data=f"acc|{user.id}|{resi_unik}"),
            types.InlineKeyboardButton("❌ TOLAK", callback_data=f"tolak|{user.id}|{resi_unik}")
        )
        bot.send_photo(chat_id=GROUP_PAY_ID, photo=message.photo[-1].file_id,
                       caption=caption_admin, message_thread_id=GROUP_PAY_TOPIC_ID,
                       parse_mode="HTML", reply_markup=markup)
    except Exception as e:
        log_error("handle_photo_forward", e)

print("[INFO] Pakel MlbbStore v7 STABLE Edition Berhasil Dijalankan...")
bot.infinity_polling()