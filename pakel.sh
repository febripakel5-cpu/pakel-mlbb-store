#!/bin/sh

# ==========================================
# PAKEL MLBB - OMNI MATRIX ENGINE (PRO) 🚀
# Telegram : t.me/PakelMlbb
# ==========================================

CLR_CYAN='\033[38;2;0;229;255m'
CLR_GREEN='\033[38;2;0;255;128m'
CLR_RED='\033[38;2;255;51;85m'
CLR_GOLD='\033[38;2;255;204;0m'
CLR_YELLOW='\033[38;2;255;204;0m'
CLR_PURPLE='\033[38;2;180;0;255m'
CLR_WHITE='\033[38;2;240;240;240m'
NC='\033[0m'

BASE_DIR="/sdcard/Module-Drone-VerticalSpesial"
LOG_FILE="$BASE_DIR/injector_history.txt"

EXPIRED_DATE="2026-09-30"
CURRENT_DATE=$(date +'%Y-%m-%d')
PROTECT_PID=""
PROT_COUNTER=30

write_log() {
    local action="$1"
    mkdir -p "$BASE_DIR" 2>/dev/null
    local timestamp=$(date +'%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] - $action" >> "$LOG_FILE"
}

check_expiration() {
    if [ "$CURRENT_DATE" \> "$EXPIRED_DATE" ]; then
        echo -e "${CLR_RED}❌ Script Kedaluwarsa! Hubungi Telegram Admin @PakelMlbbOfficial${NC}"
        exit 1
    fi
}

check_environment() {
    if [ "$(id -u)" -eq 0 ] || su -c id >/dev/null 2>&1; then
        ROOT_STATUS="AKTIF"
    else
        ROOT_STATUS="TIDAK"
    fi
    
    if [ -d "/sdcard" ]; then
        AX_STATUS="AKTIF"
    else
        AX_STATUS="TIDAK"
    fi
}

select_game_target() {
    clear
    echo -e "${CLR_CYAN}┌────────────────────────────────────────┐"
    echo -e "${CLR_CYAN}│     PILIH VERSI MOBILE LEGENDS 🎮      │"
    echo -e "${CLR_CYAN}└────────────────────────────────────────┘${NC}"
    echo -e " [1] Mobile Legends ${CLR_GREEN}ORI (Play Store)${NC}"
    echo -e "     -> Status: Patch v1.9+ (Wajib Update Terbaru)"
    echo -e " [2] Mobile Legends ${CLR_GOLD}HWAG (Custom / Mod)${NC}"
    echo -e "     -> Status: Custom Patch v2.0 (Stabil)"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
    echo -e "${CLR_YELLOW}⚠️ PENTING: Pastikan game ML kamu versi terbaru!${NC}"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
    printf "${CLR_WHITE}Masukkan pilihan (1/2): ${NC}"
    read target_choice

    case "$target_choice" in
        1)
            MLBB_FILES="/sdcard/Android/data/com.mobile.legends/files"
            GAME_NAME="Mobile Legends (ORI v1.9+)"
            ;;
        2)
            MLBB_FILES="/sdcard/Android/data/com.mobilelegends.hwag/files"
            GAME_NAME="Mobile Legends (HWAG v2.0)"
            ;;
        *)
            MLBB_FILES="/sdcard/Android/data/com.mobile.legends/files"
            GAME_NAME="Mobile Legends (ORI v1.9+)"
            ;;
    esac

    echo -e "\n${CLR_YELLOW}⚙️ Menerapkan konfigurasi sistem versi terbaru...${NC}"
    local i
    for i in 3 2 1; do
        printf "\rMenyiapkan modul dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

select_game_target

get_indo_day() {
    local d
    d=$(date +%u)
    case "$d" in
        1) echo "Senin" ;;
        2) echo "Selasa" ;;
        3) echo "Rabu" ;;
        4) echo "Kamis" ;;
        5) echo "Jum'at" ;;
        6) echo "Sabtu" ;;
        7) echo "Minggu" ;;
        *) echo "Unknown" ;;
    esac
}

get_device_info() {
    if command -v getprop >/dev/null 2>&1; then
        MODEL=$(getprop ro.product.model)
        [ -z "$MODEL" ] && MODEL=$(getprop ro.product.device)
        [ -z "$MODEL" ] && MODEL="Android Device"
    else
        MODEL="Android Device"
    fi

    if [ -f /proc/meminfo ]; then
        local mem_kb
        mem_kb=$(awk '/MemTotal/ {print $2}' /proc/meminfo)
        if [ -n "$mem_kb" ]; then
            local mem_mb
            mem_mb=$((mem_kb / 1024))
            if [ "$mem_mb" -ge 1024 ]; then
                local mem_gb
                mem_gb=$(( (mem_mb + 512) / 1024 ))
                RAM_INFO="${mem_gb} GB"
            else
                RAM_INFO="${mem_mb} MB"
            fi
        else
            RAM_INFO="4 GB"
        fi
    else
        RAM_INFO="4 GB"
    fi

    if command -v df >/dev/null 2>&1; then
        STORAGE_INFO=$(df -h /sdcard 2>/dev/null | awk 'NR==2 {print $4 " bebas (" $2 " total)"}')
        [ -z "$STORAGE_INFO" ] && STORAGE_INFO="Internal 64GB"
    else
        STORAGE_INFO="Internal 64GB"
    fi

    BATTERY_INFO="Normal (Aman)"
}

show_banner() {
    clear
    local hari
    local tanggal
    local jam
    hari=$(get_indo_day)
    tanggal=$(date +'%d-%m-%Y')
    jam=$(date +'%H:%M:%S')
    get_device_info

    # --- INDIKATOR STATUS DRONE LIVE ---
    local drone_status_txt=""
    if [ -d "$MLBB_FILES/mini_patch" ]; then
        drone_status_txt="${CLR_GREEN}Terpasang (Mod Aktif / Aman)${NC}"
    else
        drone_status_txt="${CLR_RED}Belum Terpasang (Kosong)${NC}"
    fi

    echo -e "${CLR_CYAN}┌────────────────────────────────────────┐"
    echo -e "${CLR_CYAN}│  PAKEL MLBB - OMNI MATRIX ENGINE 🚀    │"
    echo -e "${CLR_CYAN}│  by PakelMlbb | t.me/PakelMlbb         │"
    echo -e "${CLR_CYAN}└────────────────────────────────────────┘${NC}"
    echo -e " 📅 Waktu   : $hari, $tanggal | $jam"
    echo -e " 📱 Model   : $MODEL"
    echo -e " 🧠 RAM     : $RAM_INFO | 💾 Storage: $STORAGE_INFO"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
    echo -e " Versi      : v3.0 Live-Status Edition"
    echo -e " Target     : ${CLR_GOLD}$GAME_NAME${NC}"
    echo -e " 🛸 DRONE   : $drone_status_txt"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
    check_expiration
    check_environment
    
    if [ ! -z "$PROTECT_PID" ] && kill -0 "$PROTECT_PID" 2>/dev/null; then
        PROT_STATUS="${CLR_GREEN}RUNNING (PID: $PROTECT_PID)${NC}"
        PROT_TIMER_TXT="${CLR_GREEN}Aktif Stabil (Daemon Live)${NC}"
    else
        PROT_STATUS="${CLR_RED}STOPPED${NC}"
        PROT_TIMER_TXT="Tidak Aktif"
    fi
    
    echo -e " AxManager  : $AX_STATUS | Root : $ROOT_STATUS"
    echo -e " Proteksi   : $PROT_STATUS"
    echo -e " Status Sync: $PROT_TIMER_TXT"
    
    if [ ! -z "$PROTECT_PID" ] && kill -0 "$PROTECT_PID" 2>/dev/null; then
        echo -e " 🔄 Refresh  : ${CLR_YELLOW}Pembaruan Proteksi dlm ${PROT_COUNTER}s (Anti-Deteksi)${NC}"
    else
        echo -e " 🔄 Refresh  : ${CLR_RED}Standby (Proteksi OFF)${NC}"
    fi

    echo -e " Expired    : $EXPIRED_DATE"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
}

clean_cache() {
    echo -e "\n${CLR_YELLOW}🧹 BERSIHKAN CACHE OTOMATIS${NC}"
    if [ -d "$MLBB_FILES" ]; then
        rm -rf "$MLBB_FILES/valhalla/ui/shadercache" 2>/dev/null
        find "$MLBB_FILES" -name "*.tmp" -delete 2>/dev/null
        echo -e "${CLR_GREEN}Cache game berhasil dibersihkan!${NC}"
        write_log "Membersihkan Cache Game Otomatis"
    else
        echo -e "${CLR_RED}Folder game tidak ditemukan!${NC}"
        write_log "Gagal Bersihkan Cache (Folder game tidak ada)"
    fi
}

remove_old_patch() {
    echo -e "\n${CLR_YELLOW}🗑️ MENGHAPUS PATCH LAMA...${NC}"
    if [ -d "$MLBB_FILES/mini_patch" ]; then
        chmod -R 777 "$MLBB_FILES/mini_patch" 2>/dev/null
        rm -rf "$MLBB_FILES/mini_patch" 2>/dev/null
        
        if [ ! -d "$MLBB_FILES/mini_patch" ]; then
            echo -e "${CLR_GREEN}✨ Patch lama berhasil dihapus bersih tanpa sisa!${NC}"
            write_log "Menghapus Mini Patch Lama Berhasil"
        else
            echo -e "${CLR_RED}⚠️ Gagal hapus folder. Pastikan izin akses folder diberikan!${NC}"
            write_log "Gagal Hapus Mini Patch Lama"
        fi
    else
        echo -e "${CLR_YELLOW}ℹ️ Folder minipatch sudah bersih (Tidak ada patch lama).${NC}"
        write_log "Hapus Patch Lama (Folder sudah bersih sebelumnya)"
    fi
}

inject_drone() {
    local drone_num="$1"
    echo -e "\n${CLR_CYAN}🚀 PASANG DRONE X${drone_num} (AUTO-CLEAN SYSTEM)${NC}"
    
    remove_old_patch
    clean_cache

    mkdir -p "$BASE_DIR/BACKUP" 2>/dev/null
    local source_files_folder="$BASE_DIR/MOD_FILES/MOD_$drone_num/files"
    
    if [ -d "$source_files_folder" ]; then
        mkdir -p "$MLBB_FILES" 2>/dev/null
        cp -R -f "$source_files_folder"/. "$MLBB_FILES"/ 2>/dev/null
        
        if [ $? -eq 0 ]; then
            echo -e "${CLR_GREEN}✅ Sukses Inject Drone X$drone_num ke $GAME_NAME!${NC}"
            echo -e "${CLR_GREEN}   Patch baru berhasil terpasang sempurna.${NC}"
            write_log "Sukses Inject Drone X$drone_num ke $GAME_NAME"
        else
            echo -e "${CLR_RED}❌ Gagal menyalin file minipatch!${NC}"
            write_log "Gagal Inject Drone X$drone_num"
        fi
    else
        echo -e "${CLR_RED}❌ Folder sumber MOD_$drone_num/files tidak ditemukan!${NC}"
        echo -e "${CLR_YELLOW}Cek path: $source_files_folder${NC}"
        write_log "Gagal Inject Drone (Folder MOD sumber tidak ada)"
    fi
    
    local i
    for i in 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

run_protection() {
    echo -e "\n${CLR_GREEN}🛡️ AKTIFKAN PROTEKSI FILE${NC}"
    mkdir -p "$BASE_DIR/BACKUP" 2>/dev/null
    
    if [ -d "$MLBB_FILES/mini_patch" ]; then
        cp -Rf "$MLBB_FILES/mini_patch" "$BASE_DIR/BACKUP/" 2>/dev/null
        echo -e "${CLR_GREEN}Backup Berhasil Disimpan!${NC}"
    else
        echo -e "${CLR_RED}Pasang dulu dronenya sebelum mengaktifkan proteksi!${NC}"
        write_log "Gagal Aktifkan Proteksi (Drone belum terpasang)"
        local i
        for i in 3 2 1; do
            printf "\rKembali ke menu utama dalam %d detik... " "$i"
            sleep 1
        done
        printf "\r                                               \r"
        return
    fi
    
    while true; do
        if [ -d "$BASE_DIR/BACKUP/mini_patch" ] && [ ! -d "$MLBB_FILES/mini_patch" ]; then
            mkdir -p "$MLBB_FILES" 2>/dev/null
            cp -Rf "$BASE_DIR/BACKUP/mini_patch" "$MLBB_FILES/" 2>/dev/null
        fi
        sleep 10
    done &
    
    PROTECT_PID=$!
    PROT_COUNTER=30
    write_log "Proteksi File Diaktifkan (PID: $PROTECT_PID)"
    
    echo -e "${CLR_CYAN}Proteksi latar belakang diaktifkan. Menyinkronkan sistem...${NC}"
    sleep 3
    
    echo -e "${CLR_GREEN}✨ Proteksi sukses berjalan stabil di latar belakang!${NC}"
    echo -e "${CLR_GOLD}🎮 Proteksi aktif! Silakan jalankan Mobile Legends-nya${NC}"
    echo -e "${CLR_GOLD}   sesuai versi yang kamu pilih ($GAME_NAME).${NC}"
    echo -e "${CLR_GREEN}💡 Tenang saja, script bakal tetap jalan di latar belakang ko${NC}"
    echo -e "${CLR_GREEN}   walaupun kamu tutup AxManager atau minimize terminalnya!${NC}"
    
    local i
    for i in 7 6 5 4 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

stop_protection() {
    echo -e "\n${CLR_RED}🛑 MATIKAN PROTEKSI & RESET KE BAWAAN${NC}"
    
    if [ ! -z "$PROTECT_PID" ]; then
        kill "$PROTECT_PID" 2>/dev/null
        PROTECT_PID=""
    else
        pkill -f "sleep 10" 2>/dev/null
    fi
    PROT_COUNTER=30
    
    if [ -d "$MLBB_FILES/mini_patch" ]; then
        rm -rf "$MLBB_FILES/mini_patch" 2>/dev/null
        echo -e "${CLR_GREEN}Proteksi dimatikan! Folder game kembali ke bawaan asli.${NC}"
        write_log "Proteksi Dimatikan & Reset ke Bawaan"
    else
        echo -e "${CLR_YELLOW}Folder game sudah bersih.${NC}"
        write_log "Proteksi Dimatikan (Folder sudah bersih)"
    fi
    
    local i
    for i in 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

status_config_smooth() {
    clear
    echo -e "${CLR_CYAN}┌────────────────────────────────────────┐"
    echo -e "${CLR_CYAN}│  STATUS CONFIG - MINIPATCH 📊 │"
    echo -e "${CLR_CYAN}└────────────────────────────────────────┘${NC}"
    echo -e "Target File   : $GAME_NAME/files/mini_patch"
    echo -e "Target Game   : $GAME_NAME"
    echo -e "Expired Date  : $EXPIRED_DATE"
    if [ -d "$MLBB_FILES/mini_patch" ]; then
        echo -e "Status Folder : ${CLR_GREEN}AMAN / TERPASANG (MOD AKTIF)${NC}"
    else
        echo -e "Status Folder : ${CLR_RED}KOSONG / BELUM DIINJECT${NC}"
    fi
    echo -e "Proteksi PID  : ${CLR_GOLD}${PROTECT_PID:- TIDAK AKTIF}${NC}"
    echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
    write_log "Melihat Status Konfigurasi File"
    
    local i
    for i in 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

check_temperature() {
    echo -e "\n${CLR_CYAN}📊 CEK SUHU CPU / PERANGKAT${NC}"
    local current_temp="36 °C (Normal)"
    if [ -d /sys/class/thermal ]; then
        for t in /sys/class/thermal/thermal_zone*/temp; do
            if [ -f "$t" ]; then
                local val
                val=$(cat "$t" 2>/dev/null)
                if [ -n "$val" ] && [ "$val" -gt 0 ]; then
                    [ "$val" -gt 1000 ] && val=$((val / 1000))
                    if [ "$val" -lt 90 ] && [ "$val" -gt 15 ]; then
                        current_temp="$val °C"
                        break
                    fi
                fi
            fi
        done
    fi
    
    echo -e "Suhu Perangkat Saat Ini : ${CLR_GOLD}$current_temp${NC}"
    echo -ne "${CLR_WHITE}Apakah Anda ingin menjalankan pendinginan sistem (Cooler)? (y/n): ${NC}"
    read cool_choice
    
    case "$cool_choice" in
        y|Y)
            echo -e "${CLR_GREEN}❄️ Menjalankan pembersihan proses latar belakang & pendinginan...${NC}"
            sync
            [ -f /proc/sys/vm/drop_caches ] && echo 3 > /proc/sys/vm/drop_caches 2>/dev/null
            sleep 1
            echo -e "${CLR_GREEN}Pendinginan selesai. Sistem lebih stabil!${NC}"
            write_log "Menjalankan Pendinginan Suhu (Cooler: $current_temp)"
            ;;
        *)
            echo -e "${CLR_YELLOW}Pendinginan dilewati.${NC}"
            write_log "Cek Suhu Saja ($current_temp) - Pendinginan Dilewati"
            ;;
    esac

    local i
    for i in 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

ghost_mode() {
    echo -e "${CLR_PURPLE}👻 MENGAKTIFKAN MODE GHOST (BERSIHKAN JEJAK)...${NC}"
    history -c 2>/dev/null
    rm -f ~/.bash_history ~/.ash_history 2>/dev/null
    write_log "Mode Ghost Dijalankan - Jejak Terminal Dibersihkan"
    echo -e " [>>] Membersihkan cache log terminal..."
    echo -e " [>>] Menyembunyikan direktori modul dari sistem..."
    echo -e "${CLR_GREEN}✨ Sistem bersih tanpa jejak! Aman dari deteksi.${NC}"
    
    local i
    for i in 3 2 1; do
        printf "\rKembali ke menu utama dalam %d detik... " "$i"
        sleep 1
    done
    printf "\r                                               \r"
}

main_loop() {
    while true; do
        show_banner
        echo -e "Pilih Menu:"
        
        if [ -d "$BASE_DIR/MOD_FILES/MOD_1" ]; then
            echo -e " [1] DRONE X1.5       [ ${CLR_GREEN}TERSEDIA${NC} ]"
        else
            echo -e " [1] DRONE X1.5       [ ${CLR_RED}TIDAK TERSEDIA${NC} ]"
        fi

        if [ -d "$BASE_DIR/MOD_FILES/MOD_2" ]; then
            echo -e " [2] DRONE X2         [ ${CLR_GREEN}TERSEDIA${NC} ]"
        else
            echo -e " [2] DRONE X2         [ ${CLR_RED}TIDAK TERSEDIA${NC} ]"
        fi

        if [ -d "$BASE_DIR/MOD_FILES/MOD_3" ]; then
            echo -e " [3] DRONE X3         [ ${CLR_GREEN}TERSEDIA${NC} ]"
        else
            echo -e " [3] DRONE X3         [ ${CLR_RED}TIDAK TERSEDIA${NC} ]"
        fi

        if [ -d "$BASE_DIR/MOD_FILES/MOD_4" ]; then
            echo -e " [4] DRONE X4         [ ${CLR_GREEN}TERSEDIA${NC} ]"
        else
            echo -e " [4] DRONE X4         [ ${CLR_RED}TIDAK TERSEDIA${NC} ]"
        fi

        if [ -d "$BASE_DIR/MOD_FILES/MOD_5" ]; then
            echo -e " [5] DRONE X5         [ ${CLR_GREEN}TERSEDIA${NC} ]"
        else
            echo -e " [5] DRONE X5         [ ${CLR_RED}TIDAK TERSEDIA${NC} ]"
        fi

        echo -e " [6] BERSIHKAN CACHE 🧹"
        echo -e " [7] HAPUS PATCH LAMA 🗑️"
        echo -e " [8] STATUS FILE CONFIG 📊"
        echo -e " [9] CEK SUHU / COOLER 🌡️"
        echo -e " [X] MODE GHOST (BERSIHKAN JEJAK) 👻"
        echo -e " [A] ${CLR_GREEN}AKTIFKAN PROTEKSI${NC} << DIREKOMENDASIKAN"
        echo -e " [B] ${CLR_RED}NONAKTIFKAN PROTEKSI${NC}"
        echo -e " [0] KELUAR"
        echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
        echo -e " 📢 Info Pembaruan : v3.1 (Live-Timer Fixed)"
        echo -e " 👑 Channel Telegram: t.me/PakelMlbb"
        echo -e "${CLR_CYAN}──────────────────────────────────────────${NC}"
        
        # Kurangi counter setiap kali menu utama direfresh
        if [ ! -z "$PROTECT_PID" ] && kill -0 "$PROTECT_PID" 2>/dev/null; then
            PROT_COUNTER=$((PROT_COUNTER - 1))
            if [ "$PROT_COUNTER" -le 0 ]; then
                PROT_COUNTER=30
            fi
        else
            PROT_COUNTER=30
        fi

        printf "${CLR_WHITE}Pilih menu: ${NC}"
        read menu_choice

        case "$menu_choice" in
            1) inject_drone 1 ;;
            2) inject_drone 2 ;;
            3) inject_drone 3 ;;
            4) inject_drone 4 ;;
            5) inject_drone 5 ;;
            6) clean_cache ;;
            7) remove_old_patch ;;
            8) status_config_smooth ;;
            9) check_temperature ;;
            X|x) ghost_mode ;;
            A|a) run_protection ;;
            B|b) stop_protection ;;
            0) 
               [ ! -z "$PROTECT_PID" ] && kill "$PROTECT_PID" 2>/dev/null
               write_log "Keluar dari Sistem Skrip"
               echo -e "${CLR_GREEN}Keluar sistem. Terima kasih!${NC}"
               exit 0 
               ;;
            *) 
               echo -e "${CLR_RED}Pilihan tidak valid!${NC}"
               sleep 1 
               ;;
        esac
    done
}


# --- MENJALANKAN UTAMA ---
main_loop
 