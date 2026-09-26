import telebot
from telebot import types
import random
import time
import threading
import io
import os
from datetime import datetime, timezone, timedelta

# =====================================================================================
#  OFFICIAL PAKEL MLBBSTORE - MASTER ULTIMATE SECURITY & REFERRAL EDITION (UPGRADED)
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
QRIS_WEB_LINK = "https://ibb.co.com/cX2J28kj"

WIB = timezone(timedelta(hours=7))

TRANSAKSI_TIMEOUT_DETIK = 900
PAYMENT_REMINDER_SEBELUM_DETIK = 300
ARCHIVE_UMUR_HARI = 30
AUTO_BACKUP_INTERVAL_DETIK = 6 * 3600

# --- QRIS Custom Links (per nominal harga) ---
QRIS_CUSTOM_LINKS = {
    65000: QRIS_WEB_LINK,
    75000: QRIS_WEB_LINK,
    85000: QRIS_WEB_LINK,
    90000: QRIS_WEB_LINK,
    95000: QRIS_WEB_LINK,
    100000: QRIS_WEB_LINK,
    110000: QRIS_WEB_LINK,
    120000: QRIS_WEB_LINK,
    140000: QRIS_WEB_LINK,
    150000: QRIS_WEB_LINK,
    190000: QRIS_WEB_LINK,
    200000: QRIS_WEB_LINK,
    240000: QRIS_WEB_LINK,
    250000: QRIS_WEB_LINK,
}
QRIS_DEFAULT_LINK = QRIS_WEB_LINK

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

processing_lock = set()
pending_flow = {}

# =====================================================================================
#  MASTER KATALOG PAKET (SINGLE SOURCE OF TRUTH)
# =====================================================================================
# Struktur: code -> (nama_paket, harga_angka, harga_str, poin_tukar)
MASTER_PAKET = {
    'buy_natural':      ("Natural Balance (30 Hari)",        120000, "Rp 120.000", 45),
    'buy_light':        ("Light VIP + Drone (30 Hari)",       95000, "Rp 95.000",  35),
    'buy_semisafe':     ("Semi-Safe 14 Hari",                 75000, "Rp 75.000",  25),
    'buy_lifetimesafe': ("Lifetime Safe Permanent",          200000, "Rp 200.000", 75),
    'buy_sultan':       ("Sultan One Hit 100% (30 Hari)",    150000, "Rp 150.000", 55),
    'buy_pro':          ("VIP Pro One Hit 80% (30 Hari)",    100000, "Rp 100.000", 40),
    'buy_semiprivate':  ("Semi-Private 14 Hari",              75000, "Rp 75.000",  25),
    'buy_permanent':    ("Permanent Legend (Lifetime)",      250000, "Rp 250.000", 90),
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
                        add_user_points(target_chat_id, 10, "Bonus pembelian sukses")
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
    """Hitung total transaksi BERHASIL milik user."""
    total = 0
    for parts in _read_all_orders():
        if parts[0] == str(chat_id) and len(parts) > 7 and parts[7].strip() == "BERHASIL":
            total += 1
    return total

# =====================================================================================
#  BAGIAN 4: SISTEM REFERRAL + GACHA & GENERATOR KODE UNIK
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
    """Gacha acak bonus poin referral: 2/3/4/5 poin dengan bobot 45/35/15/5."""
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

def generate_unique_price(harga_dasar):
    kode_unik = random.randint(111, 399)
    return harga_dasar + kode_unik, kode_unik

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
        "@Zul_Ganz***", "@Rizky_Store***", "@Ibnu_Hkm***", "@Pandu_ID***",
        "@Fikri_Xp***", "@Aditya_Prat***", "@Eko_Cyber***", "@Bayu_Sena***",
        "@angga_99***", "@febri_nj***", "@putra_ml***", "@rendi_sultan***",
        "@agung_Gz***", "@bagus_ID***", "@deni_Xyz***", "@eko_prast***",
        "@gilang_store***", "@heru_mlbb***", "@ilham_ganz***", "@jeri_xpl***",
        "@kiki_pro***", "@lutfi_ID***", "@miko_sultan***", "@opan_gamer***",
        "@rama_cell***", "@rendra_ID***", "@septian_mz***", "@tegar_store***",
        "@rizal_mlbb***", "@yoga_sultan***", "@zidan_ID***", "@dika_store***",
        "@Aldo_Galaksi***", "@Bima_Sakti***", "@Cakra_Kusuma***", "@Dandi_Pamungkas***",
        "@Fandi_Achmad***", "@Genta_Buana***", "@Hafid_Alfarizi***", "@Jefri_Nichol***",
        "@Krisna_Mukti***", "@Lana_Del_Ray***", "@Mahendra_Putra***", "@Niko_Al_Hakim***",
        "@Oki_Setiawan***", "@Prabu_Siliwangi***", "@Qois_Maulana***", "@Rangga_Dwi***",
        "@Satrio_Piningit***", "@Taufik_Hidayat***", "@Ucok_Baba***", "@Vicky_Nitinegoro***",
        "@Wahyu_Hidayat***", "@Xaverius_Edbert***", "@Yusuf_Mansur***", "@Zulfikar_Moch***",
        "@Abdi_Negara***", "@Bintang_Lima***", "@Candra_Kirana***", "@Dewa_Kipas***",
        "@Erlangga_Dewa***", "@Fahri_Hamzah***", "@Gatot_Kaca***", "@Haris_Takir***",
        "@Irfan_Bachdim***", "@Joko_Widodo***", "@Kusuma_Wardhana***", "@Lintang_Malam***",
        "@Mahmud_Assegaf***", "@Nabil_Bafadal***", "@Omar_Daniel***", "@Pandu_Kesuma***",
        "@Raden_Mas***", "@Sultan_Hasan***", "@Trisno_Buntal***", "@Umar_Bin_Khattab***",
        "@Vega_Pancaroba***", "@Wisnu_Wardhana***", "@Yudi_Tamvan***", "@Zainal_Abidin***"
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
#  BAGIAN 5: BACKGROUND THREADS OTOMATIS
# =====================================================================================

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

# =====================================================================================
#  BAGIAN 6: TRANSLATIONS & REFERRAL UI
# =====================================================================================

TRANSLATIONS = {
    'id': {
        'btn_katalog': "💎 Katalog VIP & Harga Paket",
        'btn_testi': "🌟 Testimoni & Real-Time Bukti Order",
        'btn_riwayat': "📦 Cek Riwayat & Status Pesanan Saya",
        'btn_promo': "🎁 Klaim Kupon & Poin Loyalitas",
        'btn_referral': "🎯 Poin & Link Referral Saya",
        'btn_profil': "👤 Profil Akun Saya",
        'btn_cara_order': "❓ Panduan Cara Order",
        'btn_bayar': "💳 Metode Pembayaran Lengkap",
        'btn_faq': "💡 FAQ / Pertanyaan Umum",
        'btn_konfirmasi': "✅ Cek Status & Konfirmasi Resi",
        'btn_admin': "💬 Hubungi Admin Resmi",
        'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 1 (Kak {name}) 🔥\n*(Kategori: Custom Damage High-Tier & Fair Play Anti-Detect)*",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - BAGIAN 2 (Kak {name}) 🔥\n*(Kategori: Sultan One Hit Instan & Dominasi Mutlak)*",
        'bonus_txt': "⚡ BONUS SPESIAL FREE ALL PACKAGES (TANPA BIAYA TAMBAHAN): \n🎁 Setiap pembelian paket apa saja, otomatis mendapatkan:\n  • Panel Server Lag Musuh (Global Ping Spikes)\n  • Drone View Eksklusif X1 sampai X10 (Ultra Wide View)\n\n📂 SILAKAN PILIH SCRIPT & PELAJARI DETAIL FITUR DI BAWAH INI:",
        'next_1': "▶️ Lanjut Katalog Bagian 2",
        'prev_2': "◀️ Kembali Katalog Bagian 1",
        'inv_title': "🛒 INVOICE PEMESANAN RESMI VIP (Kak {name}) 🧾",
        'pay_info': (
            "💳 SILAKAN PILIH METODE PEMBAYARAN DI BAWAH INI:\n\n"
            "1️⃣ QRIS (CROSS-BORDER / ALL E-WALLET):\n"
            f"   • Link QRIS: {QRIS_WEB_LINK}\n\n"
            "2️⃣ TRANSFER MANUAL DANA / GOPAY (RECOMMENDED):\n"
            f"   • Nomor: <code>{INFO_DANA}</code>\n"
            "   • Atas Nama: PakelMlbb\n\n"
            "3️⃣ SAWERIA (Support Kartu & E-Wallet):\n"
            f"   • Link: {INFO_SAWERIA}\n"
        ),
        'confirm_instr': "🛡️ INSTRUKSI KONFIRMASI PEMBAYARAN:\nSetelah sukses membayar via transfer manual / QRIS, silakan kirim Screenshot Bukti Transfer ke bot ini untuk mendapatkan Resi Unik.",
    },
    'en': {
        'btn_katalog': "💎 VIP Catalogue & Pricing", 'btn_testi': "🌟 Live Testimonials",
        'btn_riwayat': "📦 My Order History", 'btn_promo': "🎁 Claim Promo & Points",
        'btn_referral': "🎯 My Points & Referral Link",
        'btn_profil': "👤 My Account Profile",
        'btn_cara_order': "❓ How to Order", 'btn_bayar': "💳 Payments",
        'btn_faq': "💡 FAQ", 'btn_konfirmasi': "✅ Check Status",
        'btn_admin': "💬 Contact Admin", 'back': "⬅️ Kembali ke Menu Utama",
        'cat_title_1': "🔥 VIP EXCLUSIVE CATALOGUE - PART 1 ({name}) 🔥",
        'cat_title_2': "🔥 VIP EXCLUSIVE CATALOGUE - PART 2 ({name}) 🔥",
        'bonus_txt': "⚡ SPECIAL BONUS:",
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

def build_welcome_text(user, user_points, l='id'):
    """Teks welcome yang konsisten & lengkap di /start dan menu utama."""
    greeting = get_time_greeting()
    if l == 'id':
        return (
            f"🔥 {greeting}, Kak {user.first_name}! Selamat datang di Official Pakel MlbbStore 🙏✨\n\n"
            f"🪙 Saldo Poin Loyalitas Anda: <b>{user_points} Poin</b>\n\n"
            "Pusat layanan script cheat Mobile Legends premium terpercaya, anti-detect kelas atas, server lag panel, & drone view paling stabil se-Indonesia.\n\n"
            "👇 Silakan pilih menu di bawah ini untuk mulai berbelanja:"
        )
    else:
        return (
            f"🔥 {greeting}, {user.first_name}! Welcome to Official Pakel MlbbStore 🙏✨\n\n"
            f"🪙 Your Loyalty Points: <b>{user_points} Poin</b>\n\n"
            "Trusted premium Mobile Legends script service, high-tier anti-detect, server lag panel, & most stable drone view in Indonesia.\n\n"
            "👇 Please select a menu below to start shopping:"
        )

def build_main_menu_markup(l='id', include_store_msg=None):
    """Menu utama grid 2 kolom."""
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(t['btn_katalog'], callback_data='menu_katalog'),
        types.InlineKeyboardButton(t['btn_testi'], callback_data='menu_testi'),
        types.InlineKeyboardButton(t['btn_riwayat'], callback_data='menu_riwayat'),
        types.InlineKeyboardButton(t['btn_promo'], callback_data='menu_promo'),
        types.InlineKeyboardButton(t['btn_referral'], callback_data='menu_referral'),
        types.InlineKeyboardButton(t['btn_profil'], callback_data='menu_profil'),
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

    share_text = f"🔥 Gabung & belanja script VIP MLBB terpercaya di Pakel MlbbStore! Pakai link referral saya ya 👇"
    share_url = f"https://t.me/share/url?url={link}&text={share_text}"

    text = (
        f"🎯 <b>POIN & REFERRAL KAMU</b>\n\n"
        f"🪙 Saldo Poin: <b>{points} Poin</b>\n"
        f"👥 Total teman diundang: <b>{total_ref}</b>\n"
        f"✅ Bonus referral sudah cair: <b>{bonus_cair}</b>\n\n"
        f"🔗 <b>Link Referral Pribadimu:</b>\n<code>{link}</code>\n\n"
        "🎰 <b>Sistem Gacha Bonus Referral:</b>\n"
        "Setiap teman yang sukses belanja pertama kali akan memberimu bonus poin acak:\n"
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
        f"🌐 Bahasa       : {l.upper()}\n"
        "━━━━━━━━━━━━━━━━━━━\n"
        f"🪙 Saldo Poin    : <b>{points} Poin</b>\n"
        f"🎫 Status Kupon  : {status_kupon}\n"
        f"📦 Total Transaksi Sukses : <b>{total_sukses}</b>\n"
        f"👥 Total Referral          : <b>{total_ref}</b>\n"
        f"✅ Bonus Referral Cair     : <b>{bonus_cair}</b>\n"
        "━━━━━━━━━━━━━━━━━━━\n\n"
        "💡 <i>Semakin banyak transaksi sukses, semakin banyak poin loyalitasmu untuk klaim script VIP gratis!</i>"
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

def build_katalog_markup(part, l='id', coupon_status="AVAILABLE"):
    """Grid 2 kolom untuk katalog paket."""
    t = TRANSLATIONS.get(l, TRANSLATIONS['id'])
    markup = types.InlineKeyboardMarkup(row_width=2)

    if part == 1:
        paket_urutan = ['buy_natural', 'buy_light', 'buy_semisafe', 'buy_lifetimesafe']
        next_btn_text = t['next_1']
        nav_cb = 'katalog_part2'
        alt_btn = None
    else:
        paket_urutan = ['buy_sultan', 'buy_pro', 'buy_semiprivate', 'buy_permanent']
        next_btn_text = t['prev_2']
        nav_cb = 'katalog_part1'
        alt_btn = None

    for code in paket_urutan:
        nama, harga_angka, harga_str, poin = MASTER_PAKET[code]
        btn_label = f"🛒 {nama.split('(')[0].strip()}\n💰 {harga_str} | 🪙 {poin} Poin"
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
    for code in paket_urutan:
        nama, harga_angka, harga_str, poin = MASTER_PAKET[code]
        promo_active = (coupon_status == "AVAILABLE")
        if promo_active:
            harga_promo = harga_angka - 10000
            text += f"• 👑 <b>{nama}</b>\n   💵 Harga: <s>{harga_str}</s> <b>Rp {harga_promo:,}</b> (Hemat Rp 10.000)\n   🪙 Atau Tukar: <b>{poin} Poin</b>\n\n"
        else:
            text += f"• 👑 <b>{nama}</b>\n   💵 Harga: <b>{harga_str}</b>\n   🪙 Atau Tukar: <b>{poin} Poin</b>\n\n"

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
        bot.reply_to(message, "⚠️ Format salah! Contoh: /poin @PakelMlbbOfficial 1000")
        return

    target_username = args[0].strip()
    try:
        jumlah_tambah = int(args[1])
    except ValueError:
        bot.reply_to(message, "⚠️ Jumlah poin harus berupa angka! Contoh: /poin @username 500")
        return

    if not target_username.startswith('@'):
        bot.reply_to(message, "⚠️ Format username harus diawali dengan tanda '@' (Contoh: @UsernameAsli)")
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
        bot.reply_to(message, "Member atau pengguna tidak ditemukan.")
        return

    try:
        chat_info = bot.get_chat(target_chat_id)
        add_user_points(target_chat_id, jumlah_tambah, "Penambahan manual oleh admin")
        total_pasti = get_user_points(target_chat_id)
        bot.reply_to(message, f"Berhasil ditambahkan {jumlah_tambah} poin ke pengguna @{chat_info.username or target_username} (ID: {target_chat_id}). Poin kamu saat ini ada {total_pasti}.")
        try:
            bot.send_message(
                target_chat_id,
                f"🎁 <b>SELAMAT! ADMIN MENAMBAHKAN POIN UNTUKMU</b> 🎁\n\n"
                f"➕ Jumlah Ditambahkan: <b>+{jumlah_tambah} Poin</b>\n"
                f"🪙 Saldo Poin Kamu Saat Ini: <b>{total_pasti} Poin</b>\n\n"
                "Silakan gunakan poinmu untuk klaim script VIP gratis di katalog bot! ✨",
                parse_mode="HTML"
            )
        except Exception:
            pass
    except Exception:
        bot_name = bot.get_me().first_name
        bot.reply_to(message, f"Pengguna belum pernah mencoba bot {bot_name}.")

@bot.message_handler(commands=['bc', 'broadcast'])
def broadcast_message(message):
    save_user(message.chat.id)
    pesan_bc = message.text.replace('/bc', '').replace('/broadcast', '').strip()
    if not pesan_bc:
        bot.reply_to(message, "⚠️ Format salah! Contoh: /bc Halo semua, ada promo script VIP baru nih!")
        return
    try:
        with open(F_USERS, "r") as f:
            users = [line.strip() for line in f.read().splitlines() if line.strip()]
    except FileNotFoundError:
        bot.reply_to(message, "⚠️ Belum ada user tercatat.")
        return
    success = 0
    for chat_id in set(users):
        try:
            bot.send_message(chat_id, f"📢 <b>PENGUMUMAN RESMI PAKEL MLBBSTORE</b>\n\n{pesan_bc}",
                             parse_mode="HTML")
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
        with open(F_ORDERS, "r") as f:
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
            bot.send_message(chat_id, f"💎 <b>INFO KHUSUS PELANGGAN SETIA PAKEL MLBBSTORE</b>\n\n{pesan_bcs}",
                             parse_mode="HTML")
            success += 1
            time.sleep(0.05)
        except Exception:
            pass
    bot.send_message(message.chat.id, f"✅ Broadcast Khusus VIP Selesai! Berhasil: {success}")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
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
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    get_latest_user_order_data(message.chat.id)
    orders = get_user_orders(message.chat.id)
    if not orders:
        text = (f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n"
                "❌ Belum ada riwayat pesanan tercatat.\n"
                "💡 Silakan pilih paket di /katalog untuk melakukan pemesanan baru!")
    else:
        text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
        for idx, o in enumerate(orders[-5:], 1):
            st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK",
                  "CANCELLED": "❌ DIBATALKAN OLEH PEMBELI",
                  "EXPIRED": "⌛ EXPIRED (Waktu 15 Menit Habis)"}.get(o['status'], "⏳ PENDING")
            text += (f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n"
                     f"   • No Resi: <code>{o['resi']}</code>\n"
                     f"   • Waktu: {o['hari']}, {o['tanggal']} ({o['jam']})\n"
                     f"   • Status: {st}\n\n")
        text += "💡 <i>Kirim bukti transfer jika belum dikonfirmasi admin!</i>"
    bot.reply_to(message, text, reply_markup=get_back_markup(l), parse_mode="HTML",
                 disable_web_page_preview=True)

@bot.message_handler(commands=['cekresi', 'resi'])
def cmd_cekresi(message):
    save_user(message.chat.id)
    user = message.from_user
    l = get_lang(user)
    text = (f"🔍 CEK STATUS RESI PEMBELIAN VIP (Kak {user.first_name})\n\n"
            "Kirimkan Nomor Resi Unik atau screenshot bukti transfer ke sini.\n\n"
            f"💬 Admin: {ADMIN_USERNAME}") if l == 'id' else f"🔍 CHECK RECEIPT STATUS ({user.first_name})"
    bot.reply_to(message, text, disable_web_page_preview=True)

@bot.message_handler(commands=['katalog'])
def cmd_katalog(message):
    try:
        save_user(message.chat.id)
        user = message.from_user
        l = get_lang(user)
        coupon_status = get_user_coupon_status(message.chat.id)
        markup = build_katalog_markup(1, l, coupon_status)
        katalog_text = build_katalog_text(1, user, l, coupon_status)
        bot.send_message(message.chat.id, katalog_text, reply_markup=markup, parse_mode="HTML")
    except Exception as e:
        log_error("cmd_katalog", e)
        bot.reply_to(message, "Terjadi kesalahan saat memuat katalog.")

@bot.message_handler(commands=['sc'])
def cmd_sc_interactive(message):
    save_user(message.chat.id)
    args = message.text.replace('/sc', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format salah! Gunakan format:\nContoh: /sc @UsernamePembeli")
        return
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, (nama, harga_angka, harga_str, poin) in MASTER_PAKET.items():
        markup.add(types.InlineKeyboardButton(f"💎 {nama} — {harga_str}", callback_data=f"sc_{code}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target Pembeli: <b>{target_buyer}</b>\n👇 Silakan pilih paket script yang dibeli:",
                 reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['scp'])
def cmd_scp_interactive(message):
    if message.chat.id != ADMIN_TELEGRAM_ID:
        bot.reply_to(message, "⚠️ Perintah khusus admin utama!")
        return
    save_user(message.chat.id)
    args = message.text.replace('/scp', '').strip()
    if not args:
        bot.reply_to(message, "⚠️ Format salah! Gunakan format:\nContoh: /scp @UsernamePembeli")
        return
    target_buyer = args if args.startswith('@') else f"@{args}"
    markup = types.InlineKeyboardMarkup(row_width=1)
    for code, (nama, harga_angka, harga_str, poin) in MASTER_PAKET.items():
        markup.add(types.InlineKeyboardButton(f"🪙 {nama} — {poin} Poin", callback_data=f"scp_{code}|{target_buyer}"))
    bot.reply_to(message, f"🎯 Target Pembeli via Poin: <b>{target_buyer}</b>\n👇 Silakan pilih paket script yang ditukar dengan poin:",
                 reply_markup=markup, parse_mode="HTML")

@bot.message_handler(commands=['testi', 'push'])
def admin_push_testi(message):
    try:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=generate_single_testimonial(),
                         message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
        bot.reply_to(message, "✅ Berhasil! Testimoni real-time baru saja dikirim ke grup komunitas utama.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Gagal mengirim testimoni: {e}")

# =====================================================================================
#  BAGIAN 8: CALLBACK HANDLERS, FOTO, & POLLING MASTER
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
                    if pay_method == "POIN":
                        pay_method_label = "REDEEMED VIA LOYALTY POINTS 🪙"
                    else:
                        pay_method_label = "SUCCESS & SCRIPT DELIVERED 💳"
                    break
    except Exception as e:
        log_error("generate_real_testimonial", e)

    testi_text = (
        "🚨 <b>REAL-TIME TRANSACTION REPORT</b> 🚨\n\n"
        f"✅ Buyer ID: {masked_name}\n"
        f"📦 Item Purchased: {detail_paket}\n"
        f"💵 Price / Method: {detail_harga} ({pay_method_label})\n"
        f"⏱️ Time: {jam_str} ({waktu_ket})\n"
        f"🔒 Status: BERHASIL & TERKIRIM\n\n"
        "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
        f"🤖 Bot Store: @{bot.get_me().username}"
    )
    return testi_text

def loading_toast(call_id, text="⏳ Mohon tunggu sebentar, sistem sedang memproses permintaanmu..."):
    """Kirim efek loading interaktif pada tombol."""
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
                    bot.answer_callback_query(call.id, text="Gagal: Data resi tidak ditemukan di database!", show_alert=True)
                    return

                if current_db_status != "PENDING":
                    bot.answer_callback_query(call.id, text=f"⚠️ PERINGATAN: Pesanan ini sudah diproses sebelumnya dengan status {current_db_status}!", show_alert=True)
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
                            bot.answer_callback_query(call.id, text="Gagal ACC: Saldo poin pembeli tidak mencukupi!", show_alert=True)
                            return

                    update_order_status_by_resi(resi_code, "BERHASIL")

                    try:
                        auto_testi_message = generate_real_testimonial(target_user_id, resi_code)
                        bot.send_message(chat_id=GROUP_CHAT_ID, text=auto_testi_message,
                                         message_thread_id=GROUP_TOPIC_ID,
                                         parse_mode="HTML", disable_web_page_preview=True)
                    except Exception as e:
                        log_error("auto_send_testi", e)

                    status_label = (f"✅ DI-ACC ADMIN (Poin Dipotong {p_points_val} & Kupon Hangus)"
                                    if action == 'apoin' else
                                    "✅ TELAH DI-ACC OLEH ADMIN (Kupon Hangus & Poin Ditambahkan)")
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

                    buyer_msg = (
                        "🛒 <b>PakelMlbbStore:</b>\n"
                        "🎉 <b>PEMBAYARAN ANDA TELAH DI-ACC ADMIN!</b> 🎉\n\n"
                        f"🔑 No Resi: <code>{resi_code}</code>\n"
                        "Status transaksi Anda sudah <b>BERHASIL</b> di sistem. Selamat menikmati script-nya!\n\n"
                        "📋 <b>SILAKAN SALIN FORMAT PESAN DI BAWAH INI DAN KIRIM KE ADMIN:</b>\n"
                        "👇 (Cukup ketuk/klik teks di bawah untuk menyalin otomatis)"
                    )
                    bot.send_message(target_user_id, buyer_msg, parse_mode="HTML")

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
                    review_prompt_text = (
                        "⭐ <b>BAGAIMANA PELAYANAN KAMI, KAK?</b> ⭐\n\n"
                        f"Terima kasih telah berbelanja di Official Pakel MlbbStore (Resi: <code>{resi_code}</code>)!\n"
                        "Silakan berikan penilaian bintang di bawah ini:"
                    )
                    bot.send_message(target_user_id, review_prompt_text, reply_markup=markup_rating, parse_mode="HTML")

                elif action in ('tolak', 'tpoin'):
                    update_order_status_by_resi(resi_code, "DITOLAK")
                    new_admin_text = original_text + "\n\n<b>STATUS: ❌ DITOLAK OLEH ADMIN (Kupon Dikembalikan)</b>"
                    if call.message.content_type == 'photo':
                        bot.edit_message_caption(chat_id=chat_id, message_id=message_id,
                                                 caption=new_admin_text, parse_mode="HTML", reply_markup=None)
                    else:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                              text=new_admin_text, parse_mode="HTML", reply_markup=None)

                    buyer_msg = (
                        "❌ <b>MOHON MAAF, PEMBAYARAN DITOLAK</b> ❌\n\n"
                        f"🔑 No Resi: <code>{resi_code}</code>\n"
                        "Bukti pembayaran Anda tidak valid atau mutasi tidak ditemukan.\n"
                        "💡 <i>Tenang Kak, kupon Anda telah dikembalikan secara utuh!</i>\n\n"
                        f"💬 Silakan hubungi Admin resmi untuk konfirmasi lebih lanjut: {ADMIN_USERNAME}"
                    )
                    bot.send_message(target_user_id, buyer_msg, parse_mode="HTML",
                                     disable_web_page_preview=True)
            except Exception as e:
                log_error("callback_admin", e)
                bot.answer_callback_query(call.id, text=f"Error: {e}", show_alert=True)
            return

        # --- MENU UTAMA ---
        if data == 'menu_utama':
            loading_toast(call.id, "⏳ Mengembalikan ke menu utama...")
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

        # --- REFERRAL ---
        elif data == 'menu_referral':
            loading_toast(call.id, "⏳ Memuat data referral...")
            _kirim_poin_referral(chat_id, message_id, l)
            return

        # --- PROFIL AKUN ---
        elif data == 'menu_profil':
            loading_toast(call.id, "⏳ Memuat profil akun kamu...")
            _kirim_profil_akun(chat_id, message_id, user, l)
            return

        # --- TESTI ---
        elif data == 'menu_testi':
            loading_toast(call.id, "⏳ Memuat testimoni terbaru...")
            fake_data = generate_fake_testimonials_list()
            testi_text = (f"🌟 LIVE TESTIMONI & TRANSAKSI SUKSES (Kak {user.first_name})\n\n"
                          f"{fake_data}💡 Toko 100% amanah & terpercaya! 🚀")
            markup_testi = types.InlineKeyboardMarkup(row_width=1)
            markup_testi.add(
                types.InlineKeyboardButton("🔄 Refresh Testimoni Terbaru", callback_data='menu_testi'),
                types.InlineKeyboardButton("🌟 Lihat Ratusan Testi di Channel", url=CHANNEL_TESTI_LINK),
                types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=testi_text,
                                  reply_markup=markup_testi, disable_web_page_preview=True)
            return

        # --- RIWAYAT ---
        elif data == 'menu_riwayat':
            loading_toast(call.id, "⏳ Memuat riwayat pesanan...")
            get_latest_user_order_data(chat_id)
            orders = get_user_orders(chat_id)
            if not orders:
                riw_text = (f"📋 RIWAYAT PESANAN SAYA (Kak {user.first_name})\n\n"
                            "❌ Belum ada riwayat pesanan tercatat.")
            else:
                riw_text = f"📋 <b>RIWAYAT PESANAN SAYA (Kak {user.first_name})</b>\n\n"
                for idx, o in enumerate(orders[-5:], 1):
                    st = {"BERHASIL": "✅ BERHASIL", "DITOLAK": "❌ DITOLAK",
                          "CANCELLED": "❌ DIBATALKAN", "EXPIRED": "⌛ EXPIRED"}.get(o['status'], "⏳ PENDING")
                    riw_text += (f"<b>{idx}. {o['paket']}</b>\n   • Harga: {o['harga']}\n"
                                 f"   • Resi: <code>{o['resi']}</code>\n   • Status: {st}\n\n")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=riw_text,
                                  reply_markup=get_back_markup(l), parse_mode="HTML",
                                  disable_web_page_preview=True)
            return

        # --- PROMO ---
        elif data == 'menu_promo':
            loading_toast(call.id, "⏳ Memuat promo & poin...")
            status_c = get_user_coupon_status(chat_id)
            user_pts = get_user_points(chat_id)

            if status_c == "AVAILABLE":
                kupon_info = "🎁 Status Kupon Member Baru: <b>TERSEDIA (Belum Digunakan)</b>\n💡 Otomatis terpotong saat kamu checkout pesanan pertama!"
            elif status_c == "PENDING":
                kupon_info = "🎁 Status Kupon Member Baru: <b>PENDING (Sedang Menunggu Verifikasi)</b>"
            else:
                kupon_info = "🎁 Status Kupon Member Baru: <b>SUDAH DIGUNAKAN</b>"

            promo_text = (
                f"🎁 <b>PROMO & POIN LOYALITAS (Kak {user.first_name})</b> 🎁\n\n"
                f"🪙 Saldo Poin Anda: <b>{user_pts} Poin</b>\n\n"
                f"{kupon_info}\n\n"
                "💡 <i>Kumpulkan terus poin transaksi suksesmu dan tukarkan dengan paket script VIP gratis tanpa bayar!</i>"
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=promo_text,
                                  reply_markup=get_back_markup(l), parse_mode="HTML")
            return

        # --- FAQ ---
        elif data == 'menu_faq':
            loading_toast(call.id, "⏳ Memuat FAQ...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="💡 FAQ PAKEL MLBBSTORE\n\n❓ Aman dari banned? \n💬 A: Sangat aman, enkripsi anti-detect tinggi.",
                                  reply_markup=get_back_markup(l))
            return

        # --- KATALOG ---
        elif data in ('menu_katalog', 'katalog_part1'):
            loading_toast(call.id, "⏳ Memuat katalog bagian 1...")
            try:
                coupon_status = get_user_coupon_status(chat_id)
                markup = build_katalog_markup(1, l, coupon_status)
                katalog_text = build_katalog_text(1, user, l, coupon_status)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text,
                                      reply_markup=markup, parse_mode="HTML",
                                      disable_web_page_preview=True)
            except Exception as e:
                log_error("katalog_part1", e)
            return

        elif data == 'katalog_part2':
            loading_toast(call.id, "⏳ Memuat katalog bagian 2...")
            try:
                coupon_status = get_user_coupon_status(chat_id)
                markup = build_katalog_markup(2, l, coupon_status)
                katalog_text = build_katalog_text(2, user, l, coupon_status)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=katalog_text,
                                      reply_markup=markup, parse_mode="HTML",
                                      disable_web_page_preview=True)
            except Exception as e:
                log_error("katalog_part2", e)
            return

        # --- PILIH PAKET ---
        elif data in MASTER_PAKET:
            loading_toast(call.id, "⏳ Menyiapkan opsi pembayaran...")
            p_name, p_price_angka, p_price_str, p_points = MASTER_PAKET[data]
            choice_text = (f"🛒 <b>PILIH METODE PEMBAYARAN</b>\n\n"
                           f"📦 Paket: <b>{p_name}</b>\n"
                           f"💵 Harga: <b>{p_price_str}</b>\n"
                           f"🪙 Atau Tukar: <b>{p_points} Poin</b>")
            markup_choice = types.InlineKeyboardMarkup(row_width=1)
            markup_choice.add(
                types.InlineKeyboardButton(f"🪙 Bayar Pakai Saldo Poin ({p_points} Poin)", callback_data=f"paymode_|poin|{data}"),
                types.InlineKeyboardButton(f"💳 Transfer Manual DANA/GoPay ({p_price_str})", callback_data=f"paymode_|transfer|{data}"),
                types.InlineKeyboardButton("📱 QRIS (Scan / Link)", callback_data=f"paymode_|qris|{data}"),
                types.InlineKeyboardButton(t['back'], callback_data='menu_katalog')
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=choice_text,
                                  reply_markup=markup_choice, parse_mode="HTML")
            return

        # --- CARA ORDER ---
        elif data == 'menu_cara_order':
            loading_toast(call.id, "⏳ Memuat panduan...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="❓ PANDUAN CARA ORDER\n1. Pilih paket di katalog.\n2. Pilih metode pembayaran (Transfer/QRIS/Poin).\n3. Selesaikan pembayaran.\n4. Kirim bukti transfer ke bot.\n5. Tunggu ACC admin & script dikirim.",
                                  reply_markup=get_back_markup(l), disable_web_page_preview=True)
            return

        # --- BAYAR ---
        elif data == 'menu_bayar':
            loading_toast(call.id, "⏳ Memuat metode pembayaran...")
            markup_bayar = types.InlineKeyboardMarkup(row_width=1)
            markup_bayar.add(types.InlineKeyboardButton(t['back'], callback_data='menu_utama'))
            pay_text = (
                "💳 <b>METODE PEMBAYARAN LENGKAP</b>\n\n"
                f"1️⃣ <b>QRIS (All E-Wallet):</b>\n   • Link QRIS: {QRIS_WEB_LINK}\n\n"
                f"2️⃣ <b>Transfer Manual DANA/GoPay:</b>\n   • Nomor: <code>{INFO_DANA}</code>\n   • A/N: PakelMlbb\n\n"
                f"3️⃣ <b>Saweria (Kartu/E-Wallet):</b>\n   • Link: {INFO_SAWERIA}"
            )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=pay_text,
                                  reply_markup=markup_bayar, parse_mode="HTML",
                                  disable_web_page_preview=True)
            return

        # --- KONFIRMASI ---
        elif data == 'menu_konfirmasi':
            loading_toast(call.id, "⏳ Memuat instruksi...")
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text="✅ Kirim screenshot bukti transfer ke bot ini untuk konfirmasi.",
                                  reply_markup=get_back_markup(l), disable_web_page_preview=True)
            return

        # --- CANCEL ---
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
                                bot.answer_callback_query(call.id, text="Pesanan sudah dibatalkan atau diproses sebelumnya.", show_alert=True)
                                return
                            admin_msg_id = int(p[11]) if p[11].isdigit() and int(p[11]) > 0 else None
                            break
            except Exception:
                pass

            success = update_order_status_by_resi(resi_target, "CANCELLED")
            if success:
                if admin_msg_id:
                    try:
                        new_admin_caption = call.message.caption or call.message.text or "ADA KLAIM PEMBAYARAN MASUK!"
                        new_admin_caption += "\n\n<b>STATUS: ❌ DIBATALKAN OLEH PEMBELI (Poin Tetap Utuh)</b>"
                        if call.message.content_type == 'photo':
                            bot.edit_message_caption(chat_id=GROUP_PAY_ID, message_id=admin_msg_id,
                                                     caption=new_admin_caption, parse_mode="HTML", reply_markup=None)
                        else:
                            bot.edit_message_text(chat_id=GROUP_PAY_ID, message_id=admin_msg_id,
                                                  text=new_admin_caption, parse_mode="HTML", reply_markup=None)
                    except Exception as e:
                        log_error("edit_admin_msg_cancel", e)

                cancel_text = (
                    f"❌ <b>PESANAN BERHASIL DIBATALKAN</b> ❌\n\n"
                    f"🔑 No Resi: <code>{resi_target}</code>\n"
                    "Pesanan ini telah dibatalkan atas permintaan Anda.\n"
                    "💡 Saldo poin Anda tetap utuh seperti semula karena belum pernah dipotong."
                )
                try:
                    bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=cancel_text,
                                          parse_mode="HTML", reply_markup=get_back_markup(l))
                except Exception:
                    bot.send_message(chat_id, cancel_text, parse_mode="HTML",
                                     reply_markup=get_back_markup(l))
                bot.answer_callback_query(call.id, text="Pesanan dibatalkan, poin tetap utuh!")
            else:
                bot.answer_callback_query(call.id, text="Pesanan sudah diproses atau dibatalkan sebelumnya.", show_alert=True)
            return

        # --- PAYMODE ---
        elif data.startswith('paymode_'):
            parts = data.split('|')
            if len(parts) < 3:
                bot.answer_callback_query(call.id, text="Data pembayaran tidak valid.", show_alert=True)
                return

            action_type, paket_code = parts[1], parts[2]
            if paket_code not in MASTER_PAKET:
                bot.answer_callback_query(call.id, text="Paket tidak ditemukan.", show_alert=True)
                return

            p_name, p_price_angka, p_price_str, p_points = MASTER_PAKET[paket_code]
            resi_unik = f"PKL-MLBB-{random.randint(10000, 99999)}"

            # ==== POIN ====
            if action_type == 'poin':
                loading_toast(call.id, "⏳ Memeriksa saldo poin...")
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
                        waktu_str = datetime.now(WIB).strftime('%d-%m-%Y %H:%M:%S WIB')
                        report_admin_poin = (
                            "🪙 <b>ADA KLAIM PEMBAYARAN VIA POIN MASUK!</b> 🪙\n\n"
                            f"👤 Dari User: @{user.username if user.username else user.first_name} (ID: <code>{chat_id}</code>)\n"
                            f"📦 Paket: {p_name}\n"
                            f"🪙 Nominal Poin: <b>{p_points} Poin</b> (Saldo User: {user_pts} Poin)\n"
                            f"⏱️ Waktu: {waktu_str}\n"
                            f"🔑 No Resi Unik: <code>{resi_unik}</code>\n\n"
                            "👇 <i>Silakan klik ACC untuk memotong poin & menyetujui, atau TOLAK jika ingin membatalkan!</i>"
                        )
                        markup_admin_poin = types.InlineKeyboardMarkup(row_width=2)
                        markup_admin_poin.add(
                            types.InlineKeyboardButton("✅ ACC POIN", callback_data=f"apoin|{resi_unik}"),
                            types.InlineKeyboardButton("❌ TOLAK POIN", callback_data=f"tpoin|{resi_unik}")
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

                    bot.answer_callback_query(call.id, text="Invoice poin diterbitkan, menunggu ACC admin!")
                    return
                else:
                    markup_fallback = types.InlineKeyboardMarkup(row_width=1)
                    markup_fallback.add(
                        types.InlineKeyboardButton(f"💳 Lanjut Bayar Via Transfer Saja ({p_price_str})", callback_data=f"paymode_|transfer|{paket_code}"),
                        types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                    )
                    fail_text = f"❌ <b>MAAF, POIN ANDA BELUM CUKUP!</b>\nPoin Anda: {user_pts} | Butuh: {p_points} Poin"
                    try:
                        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=fail_text,
                                              parse_mode="HTML", reply_markup=markup_fallback)
                    except Exception:
                        bot.send_message(chat_id, fail_text, parse_mode="HTML", reply_markup=markup_fallback)
                    bot.answer_callback_query(call.id, text="Poin tidak mencukupi!", show_alert=True)
                    return

            # ==== TRANSFER ====
            elif action_type == 'transfer':
                loading_toast(call.id, "⏳ Menerbitkan invoice transfer...")
                coupon_status = get_user_coupon_status(chat_id)
                is_promo_used = (coupon_status == "AVAILABLE")

                save_order(chat_id, p_name, p_price_str, resi_unik, payment_method="TRANSFER",
                           point_cost=0, admin_msg_id=0)
                if is_promo_used:
                    set_user_coupon_status(chat_id, "PENDING")

                invoice_text = (
                    f"{t['inv_title'].format(name=user.first_name)}\n\n"
                    f"📦 Paket Dipilih: <b>{p_name}</b>\n💵 Harga: <b>{p_price_str}</b>"
                )
                if is_promo_used:
                    invoice_text += " <i>(Sudah termasuk Potongan Promo Member Baru ✨)</i>"
                invoice_text += (f"\n🔢 Nomor Resi Unik: <code>{resi_unik}</code>\n⏱️ Batas Waktu: 15 Menit\n\n"
                                 f"{t['pay_info']}\n\n{t['confirm_instr']}\n👉 Admin: {ADMIN_USERNAME}")

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

            # ==== QRIS ====
            elif action_type == 'qris':
                loading_toast(call.id, "⏳ Menyiapkan QRIS...")
                coupon_status = get_user_coupon_status(chat_id)
                is_promo_used = (coupon_status == "AVAILABLE")

                # Hitung harga QRIS (pakai kode unik agar unik per transaksi)
                harga_qris, kode_unik_qris = generate_unique_price(p_price_angka)
                # Ambil link QRIS sesuai nominal (kalau tidak ada, pakai default)
                qris_link = QRIS_CUSTOM_LINKS.get(p_price_angka, QRIS_DEFAULT_LINK)

                save_order(chat_id, p_name, f"Rp {harga_qris:,}", resi_unik,
                           payment_method="QRIS", point_cost=0, admin_msg_id=0)
                if is_promo_used:
                    set_user_coupon_status(chat_id, "PENDING")

                invoice_text = (
                    f"{t['inv_title'].format(name=user.first_name)}\n\n"
                    f"📦 Paket Dipilih: <b>{p_name}</b>\n"
                    f"💵 Harga Dasar: <b>{p_price_str}</b>"
                )
                if is_promo_used:
                    invoice_text += " <i>(Sudah termasuk Potongan Promo Member Baru ✨)</i>"
                invoice_text += (
                    f"\n🔢 Kode Unik: <b>{kode_unik_qris}</b>\n"
                    f"💰 Total Bayar via QRIS: <b>Rp {harga_qris:,}</b>\n"
                    f"🔑 Nomor Resi Unik: <code>{resi_unik}</code>\n"
                    f"⏱️ Batas Waktu: 15 Menit\n\n"
                    "📱 <b>PEMBAYARAN VIA QRIS</b>\n"
                    f"🔗 Link QRIS: {qris_link}\n\n"
                    "💡 <i>Scan QR / buka link di atas, bayar sesuai Total Bayar (termasuk kode unik), "
                    "lalu kirim screenshot bukti transfer ke bot ini.</i>\n\n"
                    f"👉 Admin: {ADMIN_USERNAME}"
                )

                markup_qris = types.InlineKeyboardMarkup(row_width=1)
                markup_qris.add(
                    types.InlineKeyboardButton("🔗 Buka Link QRIS", url=qris_link),
                    types.InlineKeyboardButton("❌ Batalkan Pesanan Ini", callback_data=f"cancel_{resi_unik}"),
                    types.InlineKeyboardButton("📦 Cek Riwayat Pesanan Saya", callback_data='menu_riwayat'),
                    types.InlineKeyboardButton(t['back'], callback_data='menu_utama')
                )
                try:
                    bot.delete_message(chat_id=chat_id, message_id=message_id)
                except Exception:
                    pass
                bot.send_message(chat_id, invoice_text, reply_markup=markup_qris,
                                 parse_mode="HTML", disable_web_page_preview=True)
                return

        # --- RATING ---
        elif data.startswith('rate|'):
            loading_toast(call.id, "⏳ Memuat opsi ulasan...")
            parts = data.split('|')
            if len(parts) < 3:
                return
            rating_val, resi_code = parts[1], parts[2]
            markup_ulasan = types.InlineKeyboardMarkup(row_width=1)
            if int(rating_val) <= 2:
                markup_ulasan.add(
                    types.InlineKeyboardButton("⚠️ Kurang Memuaskan / Masih Ada Kendala", callback_data=f"textrev|{resi_code}|{rating_val}|Pelayanan kurang memuaskan"),
                    types.InlineKeyboardButton("❌ Kecewa / Buruk", callback_data=f"textrev|{resi_code}|{rating_val}|Sangat buruk")
                )
            elif int(rating_val) == 3:
                markup_ulasan.add(
                    types.InlineKeyboardButton("⭐ Cukup / Standar Saja", callback_data=f"textrev|{resi_code}|{rating_val}|Cukup standar"),
                    types.InlineKeyboardButton("👍 Lumayan Bagus", callback_data=f"textrev|{resi_code}|{rating_val}|Lumayan bagus")
                )
            else:
                markup_ulasan.add(
                    types.InlineKeyboardButton("🔥 Super Bagus & Mantap Banget!", callback_data=f"textrev|{resi_code}|{rating_val}|Super bagus dan mantap"),
                    types.InlineKeyboardButton("🚀 Sangat Puas, Pelayanan Gercep!", callback_data=f"textrev|{resi_code}|{rating_val}|Sangat puas, gercep"),
                    types.InlineKeyboardButton("💯 Top Global / The Best Lah Pokoknya!", callback_data=f"textrev|{resi_code}|{rating_val}|The best pokoknya")
                )
            bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                  text=f"⭐ <b>Terima kasih rating {rating_val} bintangnya!</b>\nPilih ulasan cepat atau ketik manual:",
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
                                  text="🎉 <b>TERIMA KASIH ATAS ULASANNYA, KAK!</b>\nPenilaian Anda berhasil disimpan.",
                                  parse_mode="HTML")
            return

        # --- ADMIN TESTI MANUAL: SC ---
        elif data.startswith('sc_'):
            loading_toast(call.id, "⏳ Mengirim testimoni ke grup...")
            try:
                data_split = data.split('|')
                if len(data_split) < 2:
                    return
                action, buyer_name = data_split[0], data_split[1]
                paket_code = action.replace('sc_', '')
                if paket_code in MASTER_PAKET:
                    p_nama, _, p_hrg, _ = MASTER_PAKET[paket_code]
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
                    f"⏱️ Time: {random.randint(1, 15)} menit yang lalu ({waktu_ket})\n"
                    f"🔒 Status: SUCCESS & SCRIPT DELIVERED\n\n"
                    "🔥 Terima kasih telah berbelanja di Official Pakel MlbbStore! Aman, lancar, & anti-detect. Mau order juga? Langsung sikat ke bot ya! 👇\n"
                    f"🤖 Bot Store: @{bot.get_me().username}"
                )
                bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text,
                                 message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=f"✅ <b>BERHASIL DIKIRIM KE GRUP UTAMA!</b>\n• Pembeli: {buyer_name}\n• Paket: {p_nama} ({p_hrg})",
                                      parse_mode="HTML")
            except Exception as e:
                bot.answer_callback_query(call.id, text=f"Gagal: {e}", show_alert=True)
            return

        # --- ADMIN TESTI MANUAL: SCP (POIN) ---
        elif data.startswith('scp_'):
            loading_toast(call.id, "⏳ Mengirim testimoni poin ke grup...")
            try:
                data_split = data.split('|')
                if len(data_split) < 2:
                    return
                action, buyer_name = data_split[0], data_split[1]
                paket_code = action.replace('scp_', '')
                if paket_code in MASTER_PAKET:
                    p_nama, _, _, p_poin = MASTER_PAKET[paket_code]
                    p_hrg_poin = f"{p_poin} Poin (Tukar Poin Loyalitas)"
                else:
                    p_nama, p_hrg_poin = "VIP Package", "30 Poin (Tukar Poin Loyalitas)"

                current_hour = datetime.now(WIB).hour
                waktu_ket = "pagi ini" if 4 <= current_hour < 11 else (
                    "siang ini" if 11 <= current_hour < 15 else (
                        "sore ini" if 15 <= current_hour < 18 else "malam ini"))

                post_text = (
                    "🚨 REAL-TIME TRANSACTION REPORT 🚨\n\n"
                    f"✅ Buyer ID: {buyer_name}\n"
                    f"📦 Item Purchased: {p_nama}\n"
                    f"💵 Price / Method: {p_hrg_poin}\n"
                    f"⏱️ Time: {random.randint(1, 15)} menit yang lalu ({waktu_ket})\n"
                    f"🔒 Status: REDEEMED VIA LOYALTY POINTS & DELIVERED\n\n"
                    "🔥 Terima kasih telah menukarkan poinmu di Official Pakel MlbbStore! Main aman, kumpulin poinnya, sikat script gratisannya! 👇\n"
                    f"🤖 Bot Store: @{bot.get_me().username}"
                )
                bot.send_message(chat_id=GROUP_CHAT_ID, text=post_text,
                                 message_thread_id=GROUP_TOPIC_ID, disable_web_page_preview=True)
                bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                      text=f"✅ <b>BERHASIL KIRIM TESTI TUKAR POIN KE GRUP!</b>\n• Pembeli: {buyer_name}\n• Paket: {p_nama} ({p_hrg_poin})",
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
                bot.reply_to(message, "🎉 <b>TERIMA KASIH ATAS ULASAN TERBAIKMU!</b>\nUlasan Anda berhasil disimpan.",
                             reply_markup=get_back_markup(l), parse_mode="HTML")
                return
    except Exception:
        pass

    bot.reply_to(message, f"Halo {user.first_name}! Ketik /start untuk membuka menu utama.",
                 disable_web_page_preview=True)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    if is_banned(message.chat.id):
        return
    save_user(message.chat.id)
    user = message.from_user
    resi_unik, order_status = get_latest_user_order_data(message.chat.id)

    if order_status == "EXPIRED":
        bot.reply_to(message, "❌ <b>WAKTU KONFIRMASI HABIS (TIMEOUT 15 MENIT)!</b>", parse_mode="HTML")
        return

    # Anti penggunaan bukti transfer berulang
    proof_id = message.photo[-1].file_unique_id
    if is_proof_used(proof_id):
        bot.reply_to(message, "⚠️ Bukti transfer ini sudah pernah digunakan sebelumnya!")
        return
    mark_proof_used(proof_id)

    user_caption = message.caption if message.caption else "Tidak ada pesan"
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
            "👇 <i>Silakan cek mutasi e-wallet, lalu klik tombol di bawah untuk ACC atau TOLAK!</i>"
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

print("[INFO] Pakel MlbbStore Master Ultimate UPGRADED Edition Berhasil Dijalankan...")
bot.infinity_polling()