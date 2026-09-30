<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<meta name="theme-color" content="#0A0E1A">
<title>Pakel MlbbStore</title>
<style>
/* ============================================================
   RESET & BASE
============================================================ */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    -webkit-tap-highlight-color: transparent;
}
html, body {
    width: 100%;
    min-height: 100vh;
    font-family: 'Segoe UI', 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #0A0E1A;
    color: #F1F5F9;
    overflow-x: hidden;
    -webkit-font-smoothing: antialiased;
    user-select: none;
}
body {
    background: 
        radial-gradient(circle at 20% 0%, rgba(139, 92, 246, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 100%, rgba(6, 182, 212, 0.12) 0%, transparent 50%),
        linear-gradient(180deg, #0A0E1A 0%, #0F1420 100%);
    background-attachment: fixed;
    padding-bottom: 80px;
}
::-webkit-scrollbar { width: 0; height: 0; }

/* ============================================================
   SPLASH SCREEN
============================================================ */
#splash {
    position: fixed;
    inset: 0;
    z-index: 9999;
    background: radial-gradient(circle at center, #1A1F2E 0%, #0A0E1A 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    transition: opacity 0.6s ease, visibility 0.6s ease;
}
#splash.hide {
    opacity: 0;
    visibility: hidden;
}
.splash-logo {
    position: relative;
    width: 130px;
    height: 130px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 28px;
    animation: splashPop 0.8s cubic-bezier(0.68, -0.55, 0.27, 1.55);
}
.splash-logo::before {
    content: '';
    position: absolute;
    inset: -20px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(139, 92, 246, 0.4) 0%, transparent 70%);
    animation: pulseGlow 2s infinite ease-in-out;
}
.splash-logo-icon {
    font-size: 90px;
    z-index: 2;
    filter: drop-shadow(0 0 30px rgba(139, 92, 246, 0.8));
    animation: floatY 3s infinite ease-in-out;
}
.splash-title {
    font-size: 30px;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4, #8B5CF6);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradientMove 3s infinite;
    text-align: center;
    margin-bottom: 10px;
}
.splash-sub {
    font-size: 11px;
    letter-spacing: 5px;
    color: #6B7280;
    margin-bottom: 40px;
    font-weight: 600;
}
.splash-loader {
    width: 50px;
    height: 50px;
    border: 3px solid rgba(139, 92, 246, 0.2);
    border-top-color: #8B5CF6;
    border-right-color: #06B6D4;
    border-radius: 50%;
    animation: spin 0.9s linear infinite;
    margin-bottom: 22px;
}
.splash-status {
    font-family: 'Courier New', monospace;
    font-size: 12px;
    color: #8B5CF6;
    letter-spacing: 1px;
    animation: blink 1.5s infinite;
    text-align: center;
}

/* ============================================================
   OFFLINE OVERLAY
============================================================ */
#offline {
    position: fixed;
    inset: 0;
    z-index: 99999;
    background: linear-gradient(135deg, #0A0E1A 0%, #1A0F1A 100%);
    display: none;
    align-items: center;
    justify-content: center;
    flex-direction: column;
    padding: 30px;
    text-align: center;
}
#offline.show {
    display: flex;
}
.offline-icon {
    width: 110px;
    height: 110px;
    margin-bottom: 26px;
    color: #EF4444;
    animation: pulseWarn 2s infinite;
    filter: drop-shadow(0 0 25px rgba(239, 68, 68, 0.7));
}
.offline-title {
    font-size: 24px;
    font-weight: 800;
    color: #FFF;
    margin-bottom: 14px;
    letter-spacing: 1px;
    text-shadow: 0 0 20px rgba(239, 68, 68, 0.5);
}
.offline-text {
    font-size: 14px;
    color: #9CA3AF;
    line-height: 1.7;
    margin-bottom: 32px;
    max-width: 320px;
}
.offline-text b {
    color: #FBBF24;
    font-weight: 700;
}
.offline-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
    margin-bottom: 30px;
}
.btn-offline {
    padding: 14px 26px;
    border: none;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    letter-spacing: 0.5px;
    transition: all 0.3s ease;
    min-width: 140px;
}
.btn-retry {
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    color: #FFF;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.4);
}
.btn-retry:active { transform: scale(0.96); }
.btn-settings {
    background: rgba(255, 255, 255, 0.08);
    color: #FFF;
    border: 1px solid rgba(255, 255, 255, 0.15);
}
.offline-status {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: #6B7280;
}
.status-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: #EF4444;
    animation: pulseStatus 1.5s infinite;
}

/* ============================================================
   HEADER
============================================================ */
.header {
    position: sticky;
    top: 0;
    z-index: 100;
    background: rgba(10, 14, 26, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    padding: 14px 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.header::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #8B5CF6, #06B6D4, transparent);
    animation: scanLine 3s linear infinite;
}
.header-brand {
    display: flex;
    align-items: center;
    gap: 10px;
}
.header-logo {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.5);
    animation: logoFloat 3s infinite ease-in-out;
}
.header-info h1 {
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 1px;
    background: linear-gradient(135deg, #FFF, #8B5CF6);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.header-info p {
    font-size: 10px;
    color: #10B981;
    font-weight: 600;
    letter-spacing: 0.5px;
    display: flex;
    align-items: center;
    gap: 5px;
    margin-top: 2px;
}
.online-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #10B981;
    animation: pulseStatus 1.5s infinite;
}
.header-menu {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.3);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    cursor: pointer;
    transition: all 0.3s;
}
.header-menu:active {
    background: rgba(139, 92, 246, 0.3);
    transform: scale(0.95);
}

/* ============================================================
   MAIN CONTAINER
============================================================ */
.container {
    padding: 16px;
    max-width: 500px;
    margin: 0 auto;
}

/* ============================================================
   FLASH SALE BANNER
============================================================ */
.flash-banner {
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(251, 191, 36, 0.15));
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 18px;
    padding: 18px;
    margin-bottom: 18px;
    position: relative;
    overflow: hidden;
    animation: borderGlow 2s infinite;
}
.flash-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    right: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(239, 68, 68, 0.1) 0%, transparent 70%);
    animation: rotate 15s linear infinite;
}
.flash-content {
    position: relative;
    z-index: 2;
}
.flash-label {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(135deg, #EF4444, #F59E0B);
    color: #FFF;
    font-size: 11px;
    font-weight: 900;
    padding: 5px 12px;
    border-radius: 999px;
    letter-spacing: 1px;
    margin-bottom: 12px;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.5);
    animation: shake 2s infinite;
}
.flash-title {
    font-size: 18px;
    font-weight: 900;
    color: #FFF;
    margin-bottom: 8px;
    letter-spacing: 0.5px;
}
.flash-timer {
    display: flex;
    gap: 8px;
    margin-bottom: 14px;
}
.timer-box {
    background: rgba(0, 0, 0, 0.5);
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 8px;
    padding: 6px 10px;
    font-family: 'Courier New', monospace;
    font-size: 15px;
    font-weight: 900;
    color: #FBBF24;
    min-width: 38px;
    text-align: center;
    text-shadow: 0 0 10px rgba(251, 191, 36, 0.6);
}
.timer-sep {
    color: #EF4444;
    font-size: 18px;
    font-weight: 900;
    display: flex;
    align-items: center;
}
.flash-btn {
    width: 100%;
    padding: 12px;
    border: none;
    border-radius: 12px;
    background: linear-gradient(135deg, #EF4444, #F59E0B);
    color: #FFF;
    font-size: 13px;
    font-weight: 900;
    letter-spacing: 1px;
    cursor: pointer;
    box-shadow: 0 6px 20px rgba(239, 68, 68, 0.4);
    transition: all 0.3s;
}
.flash-btn:active { transform: scale(0.97); }

/* ============================================================
   SECTION TITLE
============================================================ */
.section-title {
    font-size: 15px;
    font-weight: 800;
    color: #FFF;
    letter-spacing: 1px;
    margin-bottom: 14px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, rgba(139, 92, 246, 0.5), transparent);
}

/* ============================================================
   FILTER CHIPS
============================================================ */
.filters {
    display: flex;
    gap: 8px;
    overflow-x: auto;
    padding-bottom: 10px;
    margin-bottom: 16px;
    scrollbar-width: none;
}
.filters::-webkit-scrollbar { display: none; }
.chip {
    padding: 8px 16px;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(139, 92, 246, 0.2);
    color: #9CA3AF;
    font-size: 12px;
    font-weight: 700;
    white-space: nowrap;
    cursor: pointer;
    transition: all 0.3s;
    flex-shrink: 0;
}
.chip.active {
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    color: #FFF;
    border-color: transparent;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
}
.chip:active { transform: scale(0.95); }

/* ============================================================
   PAKET CARD
============================================================ */
.paket-list {
    display: flex;
    flex-direction: column;
    gap: 14px;
}
.paket-card {
    background: linear-gradient(135deg, rgba(26, 31, 46, 0.9), rgba(15, 20, 32, 0.9));
    border: 1px solid rgba(139, 92, 246, 0.2);
    border-radius: 18px;
    padding: 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.paket-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: linear-gradient(180deg, #8B5CF6, #06B6D4);
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.8);
}
.paket-card.hot {
    border-color: rgba(239, 68, 68, 0.5);
    background: linear-gradient(135deg, rgba(40, 15, 25, 0.95), rgba(15, 20, 32, 0.9));
}
.paket-card.hot::before {
    background: linear-gradient(180deg, #EF4444, #F59E0B);
    box-shadow: 0 0 15px rgba(239, 68, 68, 0.8);
}
.paket-card.out {
    opacity: 0.5;
    filter: grayscale(0.7);
}
.paket-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 10px;
    gap: 10px;
}
.paket-name {
    font-size: 15px;
    font-weight: 900;
    color: #FFF;
    line-height: 1.3;
    flex: 1;
    letter-spacing: 0.3px;
}
.paket-badge {
    font-size: 10px;
    font-weight: 900;
    padding: 4px 10px;
    border-radius: 999px;
    letter-spacing: 0.5px;
    white-space: nowrap;
    flex-shrink: 0;
}
.badge-hot {
    background: linear-gradient(135deg, #EF4444, #F59E0B);
    color: #FFF;
    animation: shake 2s infinite;
}
.badge-ok {
    background: rgba(16, 185, 129, 0.2);
    color: #10B981;
    border: 1px solid rgba(16, 185, 129, 0.4);
}
.badge-out {
    background: rgba(107, 114, 128, 0.3);
    color: #9CA3AF;
}
.paket-price {
    display: flex;
    align-items: baseline;
    gap: 8px;
    margin-bottom: 8px;
    flex-wrap: wrap;
}
.price-main {
    font-size: 20px;
    font-weight: 900;
    background: linear-gradient(135deg, #FBBF24, #F59E0B);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.price-strike {
    font-size: 12px;
    color: #6B7280;
    text-decoration: line-through;
}
.price-poin {
    font-size: 11px;
    color: #06B6D4;
    background: rgba(6, 182, 212, 0.1);
    padding: 3px 8px;
    border-radius: 6px;
    font-weight: 700;
    border: 1px solid rgba(6, 182, 212, 0.3);
}
.paket-desc {
    font-size: 11.5px;
    color: #9CA3AF;
    line-height: 1.55;
    margin-bottom: 14px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.paket-actions {
    display: flex;
    gap: 8px;
}
.btn-order {
    flex: 1;
    padding: 11px;
    border: none;
    border-radius: 11px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    color: #FFF;
    font-size: 12px;
    font-weight: 900;
    letter-spacing: 0.5px;
    cursor: pointer;
    box-shadow: 0 4px 15px rgba(139, 92, 246, 0.4);
    transition: all 0.3s;
}
.btn-order:active { transform: scale(0.96); }
.btn-ask {
    padding: 11px 14px;
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 11px;
    background: rgba(139, 92, 246, 0.1);
    color: #A78BFA;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.3s;
}
.btn-ask:active { transform: scale(0.96); }

/* ============================================================
   QUICK MENU (Home)
============================================================ */
.quick-menu {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-bottom: 20px;
}
.quick-item {
    background: linear-gradient(135deg, rgba(26, 31, 46, 0.9), rgba(15, 20, 32, 0.9));
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: 14px;
    padding: 14px 8px;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 6px;
    cursor: pointer;
    transition: all 0.3s;
}
.quick-item:active {
    transform: scale(0.95);
    border-color: rgba(139, 92, 246, 0.5);
}
.quick-icon {
    font-size: 22px;
    filter: drop-shadow(0 0 8px rgba(139, 92, 246, 0.6));
}
.quick-label {
    font-size: 9.5px;
    color: #9CA3AF;
    font-weight: 700;
    text-align: center;
    letter-spacing: 0.3px;
}

/* ============================================================
   BOTTOM NAV
============================================================ */
.bottom-nav {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    z-index: 200;
    background: rgba(10, 14, 26, 0.98);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1px solid rgba(139, 92, 246, 0.2);
    display: flex;
    padding: 8px 6px 10px;
    box-shadow: 0 -4px 30px rgba(0, 0, 0, 0.5);
}
.nav-item {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    padding: 8px 4px;
    cursor: pointer;
    border-radius: 10px;
    transition: all 0.3s;
}
.nav-item.active {
    background: rgba(139, 92, 246, 0.15);
}
.nav-icon {
    font-size: 19px;
    transition: transform 0.3s;
}
.nav-item.active .nav-icon {
    transform: scale(1.15);
    filter: drop-shadow(0 0 10px rgba(139, 92, 246, 0.8));
}
.nav-label {
    font-size: 9.5px;
    font-weight: 700;
    color: #6B7280;
    letter-spacing: 0.3px;
}
.nav-item.active .nav-label {
    color: #A78BFA;
}

/* ============================================================
   PAGE VIEWS
============================================================ */
.page {
    display: none;
    animation: fadeIn 0.35s ease;
}
.page.active { display: block; }

/* ============================================================
   MODAL DETAIL PAKET
============================================================ */
.modal-overlay {
    position: fixed;
    inset: 0;
    z-index: 300;
    background: rgba(0, 0, 0, 0.8);
    backdrop-filter: blur(8px);
    display: none;
    align-items: flex-end;
    justify-content: center;
    animation: fadeIn 0.3s ease;
}
.modal-overlay.show { display: flex; }
.modal-sheet {
    width: 100%;
    max-width: 500px;
    background: linear-gradient(180deg, #1A1F2E 0%, #0F1420 100%);
    border-radius: 24px 24px 0 0;
    padding: 24px 20px 30px;
    border-top: 2px solid rgba(139, 92, 246, 0.5);
    animation: slideUp 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    max-height: 85vh;
    overflow-y: auto;
    position: relative;
}
.modal-sheet::before {
    content: '';
    position: absolute;
    top: 8px;
    left: 50%;
    transform: translateX(-50%);
    width: 40px;
    height: 4px;
    background: rgba(139, 92, 246, 0.5);
    border-radius: 999px;
}
.modal-close {
    position: absolute;
    top: 16px;
    right: 16px;
    width: 34px;
    height: 34px;
    border-radius: 50%;
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.3);
    color: #EF4444;
    font-size: 18px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    z-index: 5;
}
.modal-title {
    font-size: 20px;
    font-weight: 900;
    color: #FFF;
    margin: 16px 0 14px;
    letter-spacing: 0.3px;
    padding-right: 40px;
}
.modal-info {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 18px;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 14px;
    background: rgba(255, 255, 255, 0.03);
    border-radius: 12px;
    border: 1px solid rgba(139, 92, 246, 0.15);
}
.info-label {
    font-size: 12px;
    color: #9CA3AF;
    font-weight: 600;
}
.info-value {
    font-size: 13px;
    color: #FFF;
    font-weight: 800;
}
.info-value.gold {
    background: linear-gradient(135deg, #FBBF24, #F59E0B);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 16px;
}
.modal-desc {
    font-size: 12.5px;
    color: #B0B7C3;
    line-height: 1.7;
    padding: 14px;
    background: rgba(139, 92, 246, 0.05);
    border-left: 3px solid #8B5CF6;
    border-radius: 10px;
    margin-bottom: 18px;
}
.modal-actions {
    display: flex;
    gap: 10px;
    flex-direction: column;
}
.btn-modal-primary {
    padding: 15px;
    border: none;
    border-radius: 13px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    color: #FFF;
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 0.5px;
    cursor: pointer;
    box-shadow: 0 6px 25px rgba(139, 92, 246, 0.4);
    transition: all 0.3s;
}
.btn-modal-primary:active { transform: scale(0.97); }
.btn-modal-secondary {
    padding: 14px;
    border: 1px solid rgba(139, 92, 246, 0.4);
    border-radius: 13px;
    background: rgba(139, 92, 246, 0.1);
    color: #A78BFA;
    font-size: 13px;
    font-weight: 800;
    cursor: pointer;
    transition: all 0.3s;
}

/* ============================================================
   FORM & INPUT (Voucher, Poin, Riwayat)
============================================================ */
.form-group {
    margin-bottom: 16px;
}
.form-label {
    font-size: 12px;
    font-weight: 800;
    color: #A78BFA;
    letter-spacing: 0.5px;
    margin-bottom: 8px;
    display: block;
}
.form-input {
    width: 100%;
    padding: 14px 16px;
    background: rgba(15, 20, 32, 0.9);
    border: 1px solid rgba(139, 92, 246, 0.3);
    border-radius: 12px;
    color: #FFF;
    font-size: 14px;
    font-family: 'Courier New', monospace;
    letter-spacing: 1px;
    outline: none;
    transition: all 0.3s;
}
.form-input:focus {
    border-color: #8B5CF6;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.3);
}
.form-input::placeholder {
    color: #4B5563;
    letter-spacing: 0;
    font-family: 'Segoe UI', sans-serif;
}
.btn-submit {
    width: 100%;
    padding: 15px;
    border: none;
    border-radius: 13px;
    background: linear-gradient(135deg, #8B5CF6, #06B6D4);
    color: #FFF;
    font-size: 14px;
    font-weight: 900;
    letter-spacing: 1px;
    cursor: pointer;
    box-shadow: 0 6px 25px rgba(139, 92, 246, 0.4);
    transition: all 0.3s;
    margin-top: 4px;
}
.btn-submit:active { transform: scale(0.97); }

/* ============================================================
   TOAST NOTIF
============================================================ */
#toast-container {
    position: fixed;
    top: 80px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 9998;
    display: flex;
    flex-direction: column;
    gap: 10px;
    width: calc(100% - 40px);
    max-width: 420px;
    pointer-events: none;
}
.toast {
    padding: 14px 18px;
    border-radius: 14px;
    background: rgba(26, 31, 46, 0.98);
    border: 1px solid rgba(139, 92, 246, 0.4);
    color: #FFF;
    font-size: 13px;
    font-weight: 700;
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    animation: toastIn 0.4s cubic-bezier(0.68, -0.55, 0.27, 1.55);
    display: flex;
    align-items: center;
    gap: 10px;
    pointer-events: auto;
    letter-spacing: 0.3px;
}
.toast.success {
    border-color: rgba(16, 185, 129, 0.6);
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.15), rgba(26, 31, 46, 0.98));
}
.toast.error {
    border-color: rgba(239, 68, 68, 0.6);
    background: linear-gradient(135deg, rgba(239, 68, 68, 0.15), rgba(26, 31, 46, 0.98));
}
.toast.warning {
    border-color: rgba(251, 191, 36, 0.6);
    background: linear-gradient(135deg, rgba(251, 191, 36, 0.15), rgba(26, 31, 46, 0.98));
}
.toast.hide {
    animation: toastOut 0.3s ease forwards;
}

/* ============================================================
   ANIMASI
============================================================ */
@keyframes spin { to { transform: rotate(360deg); } }
@keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
@keyframes pulseGlow {
    0%, 100% { transform: scale(1); opacity: 0.6; }
    50% { transform: scale(1.15); opacity: 1; }
}
@keyframes pulseWarn {
    0%, 100% { transform: scale(1); opacity: 1; }
    50% { transform: scale(1.1); opacity: 0.85; }
}
@keyframes pulseStatus {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}
@keyframes floatY {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}
@keyframes logoFloat {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-3px); }
}
@keyframes gradientMove {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}
@keyframes scanLine {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
@keyframes rotate { to { transform: rotate(360deg); } }
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    25% { transform: translateX(-2px); }
    75% { transform: translateX(2px); }
}
@keyframes borderGlow {
    0%, 100% { box-shadow: 0 0 20px rgba(239, 68, 68, 0.3); }
    50% { box-shadow: 0 0 35px rgba(239, 68, 68, 0.6); }
}
@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}
@keyframes slideUp {
    from { transform: translateY(100%); }
    to { transform: translateY(0); }
}
@keyframes splashPop {
    0% { transform: scale(0.3); opacity: 0; }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes toastIn {
    from { transform: translateY(-30px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}
@keyframes toastOut {
    to { transform: translateY(-30px); opacity: 0; }
}
</style>
</head>
<body>

<!-- ==================== SPLASH SCREEN ==================== -->
<div id="splash">
    <div class="splash-logo">
        <div class="splash-logo-icon">🎮</div>
    </div>
    <div class="splash-title">PAKEL MLBBSTORE</div>
    <div class="splash-sub">OFFICIAL PREMIUM STORE</div>
    <div class="splash-loader"></div>
    <div class="splash-status" id="splashStatus">🛡️ Establishing secure connection...</div>
</div>

<!-- ==================== OFFLINE OVERLAY ==================== -->
<div id="offline">
    <svg class="offline-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M1 1l22 22M16.72 11.06A10.94 10.94 0 0 1 19 12.55M5 12.55a10.94 10.94 0 0 1 5.17-2.39M10.71 5.05A16 16 0 0 1 22.58 9M1.42 9a15.91 15.91 0 0 1 4.7-2.88M8.53 16.11a6 6 0 0 1 6.95 0M12 20h.01"/>
    </svg>
    <div class="offline-title">⚠️ KONEKSI TERPUTUS</div>
    <div class="offline-text">
        Aktifkan <b>WiFi</b> atau <b>Data Seluler</b><br>
        untuk mengakses <b>Pakel MlbbStore</b>
    </div>
    <div class="offline-buttons">
        <button class="btn-offline btn-retry" onclick="location.reload()">🔄 COBA LAGI</button>
        <button class="btn-offline btn-settings" onclick="openNetworkSettings()">⚙️ SETTINGS</button>
    </div>
    <div class="offline-status">
        <span class="status-dot"></span>
        <span>Menunggu koneksi...</span>
    </div>
</div>

<!-- ==================== HEADER ==================== -->
<div class="header">
    <div class="header-brand">
        <div class="header-logo">🎮</div>
        <div class="header-info">
            <h1>PAKEL MLBBSTORE</h1>
            <p><span class="online-dot"></span> ONLINE • SECURE</p>
        </div>
    </div>
    <div class="header-menu" onclick="scrollTo({top:0, behavior:'smooth'})">☰</div>
</div>

<!-- ==================== MAIN ==================== -->
<div class="container">

    <!-- ========== HOME PAGE ========== -->
    <div id="page-home" class="page active">
        <div class="flash-banner" id="flashBanner">
            <div class="flash-content">
                <div class="flash-label">⚡ FLASH SALE</div>
                <div class="flash-title">Diskon 20% Semua Paket!</div>
                <div class="flash-timer">
                    <div class="timer-box" id="tJam">00</div>
                    <div class="timer-sep">:</div>
                    <div class="timer-box" id="tMenit">00</div>
                    <div class="timer-sep">:</div>
                    <div class="timer-box" id="tDetik">00</div>
                </div>
                <button class="flash-btn" onclick="goPage('katalog')">🛒 ORDER SEKARANG</button>
            </div>
        </div>

        <div class="section-title">⚡ MENU CEPAT</div>
        <div class="quick-menu">
            <div class="quick-item" onclick="goPage('voucher')">
                <div class="quick-icon">🎫</div>
                <div class="quick-label">VOUCHER</div>
            </div>
            <div class="quick-item" onclick="goPage('poin')">
                <div class="quick-icon">🪙</div>
                <div class="quick-label">CEK POIN</div>
            </div>
            <div class="quick-item" onclick="goPage('riwayat')">
                <div class="quick-icon">📦</div>
                <div class="quick-label">RIWAYAT</div>
            </div>
            <div class="quick-item" onclick="openTelegram('Pakel_Mlbb_Store_bot')">
                <div class="quick-icon">💬</div>
                <div class="quick-label">ORDER BOT</div>
            </div>
        </div>

        <div class="section-title">🔥 PAKET TERLARIS</div>
        <div class="paket-list" id="homePaketList"></div>
    </div>

    <!-- ========== KATALOG PAGE ========== -->
    <div id="page-katalog" class="page">
        <div class="section-title">💎 SEMUA PAKET</div>
        <div class="filters" id="filterChips">
            <div class="chip active" data-filter="all">🔥 Semua</div>
            <div class="chip" data-filter="sultan">👑 Sultan</div>
            <div class="chip" data-filter="pro">💎 Pro</div>
            <div class="chip" data-filter="safe">🛡️ Safe</div>
            <div class="chip" data-filter="murah">💰 Murah</div>
        </div>
        <div class="paket-list" id="katalogPaketList"></div>
    </div>

    <!-- ========== PROMO PAGE ========== -->
    <div id="page-promo" class="page">
        <div class="section-title">🎁 PROMO AKTIF</div>
        <div class="flash-banner" id="flashBanner2">
            <div class="flash-content">
                <div class="flash-label">⚡ FLASH SALE AKTIF</div>
                <div class="flash-title">Diskon 20% Semua Paket!</div>
                <div class="flash-timer">
                    <div class="timer-box" id="tJam2">00</div>
                    <div class="timer-sep">:</div>
                    <div class="timer-box" id="tMenit2">00</div>
                    <div class="timer-sep">:</div>
                    <div class="timer-box" id="tDetik2">00</div>
                </div>
            </div>
        </div>

        <div class="section-title" style="margin-top:20px;">🎫 VOUCHER AKTIF</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-head">
                <div class="paket-name">🎫 Kode: <span style="color:#06B6D4;">PROMO10</span></div>
                <div class="paket-badge badge-ok">AKTIF</div>
            </div>
            <div class="paket-desc">Diskon Rp 10.000 untuk semua paket. Kuota terbatas!</div>
            <div class="paket-actions">
                <button class="btn-order" onclick="goPage('voucher')">🎫 REDEEM SEKARANG</button>
            </div>
        </div>

        <div class="section-title" style="margin-top:20px;">🏅 DISKON MEMBER</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-head">
                <div class="paket-name">🥉 Bronze — 0%</div>
            </div>
            <div class="paket-desc">0-4 transaksi sukses</div>
        </div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-head">
                <div class="paket-name">🥈 Silver — 5%</div>
            </div>
            <div class="paket-desc">5-14 transaksi sukses</div>
        </div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-head">
                <div class="paket-name">🥇 Gold — 10%</div>
            </div>
            <div class="paket-desc">15-29 transaksi sukses</div>
        </div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-head">
                <div class="paket-name">💎 Platinum — 15%</div>
            </div>
            <div class="paket-desc">30+ transaksi sukses</div>
        </div>
    </div>

    <!-- ========== VOUCHER PAGE ========== -->
    <div id="page-voucher" class="page">
        <div class="section-title">🎫 REDEEM VOUCHER</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-desc" style="margin-top:0; margin-bottom:16px;">
                Masukkan kode voucher yang kamu punya. Voucher otomatis aktif di akunmu saat checkout!
            </div>
            <div class="form-group">
                <label class="form-label">🎫 KODE VOUCHER</label>
                <input type="text" class="form-input" id="inputVoucher" placeholder="Contoh: PROMO10" maxlength="30">
            </div>
            <button class="btn-submit" onclick="redeemVoucher()">🎫 REDEEM VOUCHER</button>
        </div>

        <div class="section-title" style="margin-top:20px;">📌 CARA PAKAI</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-desc" style="margin-top:0;">
                1. Ketik kode voucher di kolom atas<br>
                2. Klik "REDEEM VOUCHER"<br>
                3. Voucher otomatis aktif di akunmu<br>
                4. Checkout paket → diskon otomatis kepakai
            </div>
        </div>
    </div>

    <!-- ========== POIN PAGE ========== -->
    <div id="page-poin" class="page">
        <div class="section-title">🪙 CEK POIN LOYALITAS</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-desc" style="margin-top:0; margin-bottom:16px;">
                Masukkan <b>Chat ID</b> kamu untuk cek saldo poin & tier.
            </div>
            <div class="form-group">
                <label class="form-label">🆔 CHAT ID TELEGRAM</label>
                <input type="text" class="form-input" id="inputChatId" placeholder="Contoh: 8772023108" maxlength="20">
            </div>
            <button class="btn-submit" onclick="cekPoin()">🪙 CEK POIN SEKARANG</button>
        </div>

        <div id="poinResult" style="display:none; margin-top:20px;">
            <div class="section-title">📊 HASIL</div>
            <div class="paket-card" style="cursor:default;">
                <div class="modal-info">
                    <div class="info-row">
                        <div class="info-label">🪙 Saldo Poin</div>
                        <div class="info-value gold" id="resultPoin">0</div>
                    </div>
                    <div class="info-row">
                        <div class="info-label">🏅 Tier</div>
                        <div class="info-value" id="resultTier">Bronze</div>
                    </div>
                </div>
                <button class="btn-submit" onclick="openTelegram('Pakel_Mlbb_Store_bot')">💬 CEK DI BOT TELEGRAM</button>
            </div>
        </div>
    </div>

    <!-- ========== RIWAYAT PAGE ========== -->
    <div id="page-riwayat" class="page">
        <div class="section-title">📦 CEK RIWAYAT PESANAN</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-desc" style="margin-top:0; margin-bottom:16px;">
                Masukkan nomor resi kamu untuk lihat status pesanan.
            </div>
            <div class="form-group">
                <label class="form-label">🔑 NOMOR RESI</label>
                <input type="text" class="form-input" id="inputResi" placeholder="PKL-MLBB-12345" maxlength="30">
            </div>
            <button class="btn-submit" onclick="cekRiwayat()">📦 CEK STATUS</button>
        </div>

        <div class="section-title" style="margin-top:20px;">💡 TIPS</div>
        <div class="paket-card" style="cursor:default;">
            <div class="paket-desc" style="margin-top:0;">
                Resi bisa dilihat di halaman invoice atau di <b>Riwayat</b> dalam bot Telegram. Chat admin kalau lupa resi!
            </div>
            <div class="paket-actions" style="margin-top:12px;">
                <button class="btn-order" onclick="openTelegram('PakelMlbbOfficial')">💬 CHAT ADMIN</button>
            </div>
        </div>
    </div>

    <!-- ========== PROFIL PAGE ========== -->
    <div id="page-profil" class="page">
        <div class="section-title">👤 PROFIL TOKO</div>
        <div class="paket-card" style="cursor:default; text-align:center;">
            <div class="header-logo" style="margin:0 auto 16px; width:80px; height:80px; font-size:42px;">🎮</div>
            <div class="paket-name" style="text-align:center; font-size:20px; margin-bottom:6px;">Pakel MlbbStore</div>
            <div style="font-size:11px; color:#A78BFA; letter-spacing:2px; font-weight:700; margin-bottom:16px;">
                ⚡ OFFICIAL PREMIUM STORE ⚡
            </div>
            <div class="paket-desc" style="text-align:center;">
                Pusat layanan script Mobile Legends premium terpercaya, anti-detect kelas atas, server lag panel & drone view paling stabil se-Indonesia.
            </div>
        </div>

        <div class="section-title" style="margin-top:20px;">📞 HUBUNGI KAMI</div>
        <div class="paket-list">
            <div class="paket-card" style="cursor:pointer;" onclick="openTelegram('Pakel_Mlbb_Store_bot')">
                <div class="paket-head">
                    <div class="paket-name">🤖 BOT ORDER RESMI</div>
                    <div class="paket-badge badge-hot">ORDER</div>
                </div>
                <div class="paket-desc" style="margin-bottom:0;">@Pakel_Mlbb_Store_bot — Order 24/7 via bot</div>
            </div>
            <div class="paket-card" style="cursor:pointer;" onclick="openTelegram('PakelMlbbOfficial')">
                <div class="paket-head">
                    <div class="paket-name">💬 ADMIN OFFICIAL</div>
                    <div class="paket-badge badge-ok">ADMIN</div>
                </div>
                <div class="paket-desc" style="margin-bottom:0;">@PakelMlbbOfficial — Chat admin langsung</div>
            </div>
            <div class="paket-card" style="cursor:pointer;" onclick="openTelegram('PakelMlbb')">
                <div class="paket-head">
                    <div class="paket-name">👥 GRUP RESMI</div>
                    <div class="paket-badge badge-ok">GRUP</div>
                </div>
                <div class="paket-desc" style="margin-bottom:0;">@PakelMlbb — Grup diskusi & update</div>
            </div>
            <div class="paket-card" style="cursor:pointer;" onclick="window.open('https://t.me/PakelMlbb/368','_blank')">
                <div class="paket-head">
                    <div class="paket-name">🌟 CHANNEL TESTI</div>
                    <div class="paket-badge badge-hot">TESTI</div>
                </div>
                <div class="paket-desc" style="margin-bottom:0;">Lihat bukti order & testimoni real-time</div>
            </div>
        </div>

        <div class="section-title" style="margin-top:20px;">💳 METODE PEMBAYARAN</div>
        <div class="paket-card" style="cursor:default;">
            <div class="modal-info">
                <div class="info-row">
                    <div class="info-label">💳 DANA / GoPay</div>
                    <div class="info-value">085188371150</div>
                </div>
                <div class="info-row">
                    <div class="info-label">📱 QRIS</div>
                    <div class="info-value">Semua E-Wallet</div>
                </div>
                <div class="info-row">
                    <div class="info-label">🪙 Poin Loyalitas</div>
                    <div class="info-value">Tukar Paket</div>
                </div>
            </div>
        </div>
    </div>

</div>

<!-- ==================== MODAL DETAIL PAKET ==================== -->
<div class="modal-overlay" id="modalPaket" onclick="closeModal(event)">
    <div class="modal-sheet" onclick="event.stopPropagation()">
        <div class="modal-close" onclick="closeModal()">✕</div>
        <div class="modal-title" id="modalName">-</div>
        <div class="modal-info">
            <div class="info-row">
                <div class="info-label">💵 Harga</div>
                <div class="info-value gold" id="modalPrice">-</div>
            </div>
            <div class="info-row">
                <div class="info-label">🪙 Atau Tukar Poin</div>
                <div class="info-value" id="modalPoin">-</div>
            </div>
            <div class="info-row">
                <div class="info-label">📦 Stok</div>
                <div class="info-value" id="modalStok">-</div>
            </div>
        </div>
        <div class="modal-desc" id="modalDesc">-</div>
        <div class="modal-actions">
            <button class="btn-modal-primary" id="btnOrderModal">🛒 ORDER VIA TELEGRAM</button>
            <button class="btn-modal-secondary" onclick="openTelegram('PakelMlbbOfficial')">💬 TANYA ADMIN</button>
        </div>
    </div>
</div>

<!-- ==================== TOAST ==================== -->
<div id="toast-container"></div>

<!-- ==================== BOTTOM NAV ==================== -->
<div class="bottom-nav">
    <div class="nav-item active" data-page="home" onclick="goPage('home')">
        <div class="nav-icon">🏠</div>
        <div class="nav-label">HOME</div>
    </div>
    <div class="nav-item" data-page="katalog" onclick="goPage('katalog')">
        <div class="nav-icon">💎</div>
        <div class="nav-label">KATALOG</div>
    </div>
    <div class="nav-item" data-page="promo" onclick="goPage('promo')">
        <div class="nav-icon">🎁</div>
        <div class="nav-label">PROMO</div>
    </div>
    <div class="nav-item" data-page="profil" onclick="goPage('profil')">
        <div class="nav-icon">👤</div>
        <div class="nav-label">PROFIL</div>
    </div>
</div>

<script>
/* ============================================================
   KONFIGURASI TOKO
============================================================ */
const BOT_USERNAME = 'Pakel_Mlbb_Store_bot';
const ADMIN_USERNAME = 'PakelMlbbOfficial';
const FLASH_SALE_DISKON = 20; // dalam persen
const FLASH_SALE_DURASI = 2; // dalam jam

/* ============================================================
   DATA PAKET (DARI FILE pakeltest.py)
============================================================ */
const PAKET_DATA = [
    {
        kode: 'buy_sultan',
        nama: 'Sultan One Hit 100% (30 Hari)',
        harga: 150000,
        harga_str: 'Rp 150.000',
        poin: 55,
        stok: 8,
        kategori: 'sultan',
        desc: '🎯 Damage tembus batas, instant kill musuh dalam sekali hit, bypass anti-cheat paling aman, khusus untuk player serius yang ingin dominasi mutlak di setiap match.'
    },
    {
        kode: 'buy_pro',
        nama: 'VIP Pro One Hit 80% (30 Hari)',
        harga: 100000,
        harga_str: 'Rp 100.000',
        poin: 40,
        stok: 45,
        kategori: 'pro',
        desc: '🎯 Udah dapet damage sakit, semua skin kebuka, pandangan luas, lengkap jadi satu! Paling dicari para top global untuk push rank tanpa hambatan.'
    },
    {
        kode: 'buy_permanent',
        nama: 'Permanent Legend (Lifetime)',
        harga: 250000,
        harga_str: 'Rp 250.000',
        poin: 90,
        stok: 12,
        kategori: 'sultan',
        desc: '🎯 Sekali bayar, nikmati update script seumur hidup tanpa perlu perpanjang langganan tiap bulan. Auto untung buat jangka panjang dan paling worth it!'
    },
    {
        kode: 'buy_natural',
        nama: 'Natural Balance (30 Hari)',
        harga: 120000,
        harga_str: 'Rp 120.000',
        poin: 45,
        stok: 35,
        kategori: 'safe',
        desc: '🎯 Dirancang khusus untuk pemain yang mengutamakan keamanan akun. Pengaturan damage dapat disesuaikan secara mandiri (seperti 2 hit yang tidak mencolok), sehingga performa tetap optimal namun senyap.'
    },
    {
        kode: 'buy_lifetimesafe',
        nama: 'Lifetime Safe Permanent',
        harga: 200000,
        harga_str: 'Rp 200.000',
        poin: 75,
        stok: 20,
        kategori: 'safe',
        desc: '🎯 Solusi hemat jangka panjang tanpa biaya langganan bulanan. Memberikan akses selamanya dengan fitur damage fleksibel yang aman dan stabil digunakan sewaktu-waktu.'
    },
    {
        kode: 'buy_light',
        nama: 'Light VIP + Drone (30 Hari)',
        harga: 95000,
        harga_str: 'Rp 95.000',
        poin: 35,
        stok: 60,
        kategori: 'murah',
        desc: '🎯 Pilihan ekonomis untuk pemakaian bulanan. Kombinasi pas antara damage yang disetel wajar agar tidak terlihat brutal, ditambah pandangan map yang lebih luas untuk membaca pergerakan lawan.'
    },
    {
        kode: 'buy_semisafe',
        nama: 'Semi-Safe 14 Hari',
        harga: 75000,
        harga_str: 'Rp 75.000',
        poin: 25,
        stok: 75,
        kategori: 'murah',
        desc: '🎯 Paket harian yang sangat terjangkau. Menghadirkan setelan damage fleksibel yang terkontrol serta kestabilan koneksi yang terjaga selama dua minggu penuh.'
    },
    {
        kode: 'buy_semiprivate',
        nama: 'Semi-Private 14 Hari',
        harga: 75000,
        harga_str: 'Rp 75.000',
        poin: 25,
        stok: 70,
        kategori: 'murah',
        desc: '🎯 Performanya stabil, anti patah-patah dijamin lancar jaya buat bantai musuh seharian tanpa khawatir lag atau disconnect mendadak.'
    }
];

/* ============================================================
   STATE
============================================================ */
let currentFilter = 'all';
let flashSaleEnd = Date.now() + (FLASH_SALE_DURASI * 3600 * 1000);

/* ============================================================
   SPLASH SCREEN — CEK KONEKSI DULU
============================================================ */
window.addEventListener('load', () => {
    setTimeout(() => {
        checkConnectionOnStart();
    }, 1500);
});

async function checkConnectionOnStart() {
    const statusEl = document.getElementById('splashStatus');
    if (statusEl) statusEl.textContent = '🔍 Checking network...';

    const online = await testConnection();

    if (online) {
        if (statusEl) statusEl.textContent = '✅ Connection secure!';
        setTimeout(() => {
            document.getElementById('splash').classList.add('hide');
            initApp();
        }, 600);
    } else {
        if (statusEl) statusEl.textContent = '❌ No connection!';
        setTimeout(() => {
            document.getElementById('splash').classList.add('hide');
            document.getElementById('offline').classList.add('show');
        }, 800);
    }
}

async function testConnection() {
    if (!navigator.onLine) return false;
    try {
        const controller = new AbortController();
        const timeout = setTimeout(() => controller.abort(), 3000);
        await fetch('https://www.google.com/favicon.ico', {
            method: 'HEAD',
            mode: 'no-cors',
            cache: 'no-cache',
            signal: controller.signal
        });
        clearTimeout(timeout);
        return true;
    } catch (err) {
        return false;
    }
}

/* ============================================================
   INIT APP
============================================================ */
function initApp() {
    renderHomePaket();
    renderKatalogPaket();
    setupFilters();
    startFlashTimer();
    setupConnectionMonitor();
}

/* ============================================================
   RENDER PAKET
============================================================ */
function getStokBadge(stok) {
    if (stok <= 0) return '<div class="paket-badge badge-out">❌ HABIS</div>';
    if (stok < 20) return '<div class="paket-badge badge-hot">🔥 SISA ' + stok + '</div>';
    return '<div class="paket-badge badge-ok">📦 STOK ' + stok + '</div>';
}

function getHargaFinal(harga) {
    return Math.round(harga * (100 - FLASH_SALE_DISKON) / 100);
}

function formatRupiah(n) {
    return 'Rp ' + n.toLocaleString('id-ID');
}

function renderPaketCard(p, isHome = false) {
    const hargaFinal = getHargaFinal(p.harga);
    const isHot = p.stok < 20 && p.stok > 0;
    const isOut = p.stok <= 0;

    return `
        <div class="paket-card ${isHot ? 'hot' : ''} ${isOut ? 'out' : ''}" onclick="openDetail('${p.kode}')">
            <div class="paket-head">
                <div class="paket-name">👑 ${p.nama}</div>
                ${getStokBadge(p.stok)}
            </div>
            <div class="paket-price">
                <div class="price-main">${formatRupiah(hargaFinal)}</div>
                <div class="price-strike">${p.harga_str}</div>
                <div class="price-poin">🪙 ${p.poin} Poin</div>
            </div>
            <div class="paket-desc">${p.desc}</div>
            <div class="paket-actions">
                <button class="btn-order" onclick="event.stopPropagation(); orderPaket('${p.kode}')">
                    🛒 ORDER SEKARANG
                </button>
                <button class="btn-ask" onclick="event.stopPropagation(); openTelegram('${ADMIN_USERNAME}')">
                    💬
                </button>
            </div>
        </div>
    `;
}

function renderHomePaket() {
    const top = PAKET_DATA.slice(0, 4);
    const el = document.getElementById('homePaketList');
    if (el) el.innerHTML = top.map(p => renderPaketCard(p, true)).join('');
}

function renderKatalogPaket() {
    const filtered = currentFilter === 'all' 
        ? PAKET_DATA 
        : PAKET_DATA.filter(p => p.kategori === currentFilter);
    const el = document.getElementById('katalogPaketList');
    if (!el) return;
    if (filtered.length === 0) {
        el.innerHTML = '<div class="paket-card" style="text-align:center; cursor:default;">❌ Paket tidak ditemukan</div>';
        return;
    }
    el.innerHTML = filtered.map(p => renderPaketCard(p)).join('');
}

function setupFilters() {
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('active'));
            chip.classList.add('active');
            currentFilter = chip.dataset.filter;
            renderKatalogPaket();
        });
    });
}

/* ============================================================
   NAVIGASI
============================================================ */
function goPage(page) {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    const target = document.getElementById('page-' + page);
    if (target) target.classList.add('active');

    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));
    const nav = document.querySelector(`.nav-item[data-page="${page}"]`);
    if (nav) nav.classList.add('active');

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

/* ============================================================
   MODAL DETAIL
============================================================ */
function openDetail(kode) {
    const p = PAKET_DATA.find(x => x.kode === kode);
    if (!p) return;

    const hargaFinal = getHargaFinal(p.harga);

    document.getElementById('modalName').textContent = p.nama;
    document.getElementById('modalPrice').textContent = formatRupiah(hargaFinal) + ' (Flash Sale ' + FLASH_SALE_DISKON + '%)';
    document.getElementById('modalPoin').textContent = p.poin + ' Poin';
    document.getElementById('modalStok').textContent = p.stok + ' unit';
    document.getElementById('modalDesc').innerHTML = p.desc;

    const btn = document.getElementById('btnOrderModal');
    if (p.stok <= 0) {
        btn.textContent = '❌ STOK HABIS';
        btn.disabled = true;
        btn.style.opacity = '0.5';
    } else {
        btn.textContent = '🛒 ORDER VIA TELEGRAM';
        btn.disabled = false;
        btn.style.opacity = '1';
        btn.onclick = () => orderPaket(p.kode);
    }

    document.getElementById('modalPaket').classList.add('show');
}

function closeModal(e) {
    if (e && e.target && e.target.id !== 'modalPaket') return;
    document.getElementById('modalPaket').classList.remove('show');
}

/* ============================================================
   ORDER PAKET
============================================================ */
function orderPaket(kode) {
    const p = PAKET_DATA.find(x => x.kode === kode);
    if (!p) return;
    if (p.stok <= 0) {
        showToast('❌ Maaf, stok habis! Tunggu restock ya 🙏', 'error');
        return;
    }
    // Buka bot telegram dengan parameter paket
    const url = `https://t.me/${BOT_USERNAME}?start=order_${kode}`;
    window.open(url, '_blank');
    showToast('✅ Membuka bot Telegram...', 'success');
}

/* ============================================================
   OPEN TELEGRAM
============================================================ */
function openTelegram(username) {
    if (username.startsWith('http')) {
        window.open(username, '_blank');
    } else {
        window.open(`https://t.me/${username.replace('@', '')}`, '_blank');
    }
}

/* ============================================================
   FLASH SALE TIMER
============================================================ */
function startFlashTimer() {
    function update() {
        const sisa = flashSaleEnd - Date.now();
        if (sisa <= 0) {
            ['tJam', 'tMenit', 'tDetik', 'tJam2', 'tMenit2', 'tDetik2'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.textContent = '00';
            });
            const fb = document.getElementById('flashBanner');
            const fb2 = document.getElementById('flashBanner2');
            if (fb) fb.style.display = 'none';
            if (fb2) fb2.style.display = 'none';
            return;
        }
        const jam = Math.floor(sisa / 3600000);
        const menit = Math.floor((sisa % 3600000) / 60000);
        const detik = Math.floor((sisa % 60000) / 1000);

        const j = String(jam).padStart(2, '0');
        const m = String(menit).padStart(2, '0');
        const d = String(detik).padStart(2, '0');

        ['tJam', 'tJam2'].forEach(id => { const el = document.getElementById(id); if (el) el.textContent = j; });
        ['tMenit', 'tMenit2'].forEach(id => { const el = document.getElementById(id); if (el) el.textContent = m; });
        ['tDetik', 'tDetik2'].forEach(id => { const el = document.getElementById(id); if (el) el.textContent = d; });
    }
    update();
    setInterval(update, 1000);
}

/* ============================================================
   REDEEM VOUCHER
============================================================ */
function redeemVoucher() {
    const input = document.getElementById('inputVoucher');
    const kode = (input.value || '').trim().toUpperCase();

    if (!kode || kode.length < 3) {
        showToast('❌ Masukkan kode voucher yang valid!', 'error');
        return;
    }

    // Simulasi validasi voucher
    const voucherValid = ['PROMO10', 'PROMO5', 'WELCOME', 'NEWBIE'];

    if (voucherValid.includes(kode)) {
        showToast('✅ Voucher ' + kode + ' berhasil di-redeem!', 'success');
        input.value = '';
        setTimeout(() => {
            openTelegram(BOT_USERNAME);
        }, 1500);
    } else {
        showToast('❌ Kode voucher tidak ditemukan!', 'error');
    }
}

/* ============================================================
   CEK POIN
============================================================ */
function cekPoin() {
    const input = document.getElementById('inputChatId');
    const chatId = (input.value || '').trim();

    if (!chatId || chatId.length < 5) {
        showToast('❌ Masukkan Chat ID yang valid!', 'error');
        return;
    }

    // Simulasi cek poin
    document.getElementById('resultPoin').textContent = '150';
    document.getElementById('resultTier').textContent = '🥇 Gold';
    document.getElementById('poinResult').style.display = 'block';
    showToast('✅ Data ditemukan!', 'success');

    setTimeout(() => {
        document.getElementById('poinResult').scrollIntoView({ behavior: 'smooth' });
    }, 300);
}

/* ============================================================
   CEK RIWAYAT
============================================================ */
function cekRiwayat() {
    const input = document.getElementById('inputResi');
    const resi = (input.value || '').trim().toUpperCase();

    if (!resi || resi.length < 5) {
        showToast('❌ Masukkan nomor resi yang valid!', 'error');
        return;
    }

    // Redirect ke bot telegram
    const url = `https://t.me/${BOT_USERNAME}?start=cek_${resi}`;
    window.open(url, '_blank');
    showToast('✅ Membuka bot Telegram...', 'success');
}

/* ============================================================
   TOAST NOTIF
============================================================ */
function showToast(msg, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = 'toast ' + type;
    toast.innerHTML = msg;

    container.appendChild(toast);

    setTimeout(() => {
        toast.classList.add('hide');
        setTimeout(() => {
            if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 300);
    }, 3000);
}

/* ============================================================
   CONNECTION MONITOR (Real-time)
============================================================ */
function setupConnectionMonitor() {
    window.addEventListener('online', () => {
        document.getElementById('offline').classList.remove('show');
        showToast('✅ Koneksi kembali! Lanjut belanja 🛒', 'success');
    });

    window.addEventListener('offline', () => {
        document.getElementById('offline').classList.add('show');
    });

    // Periodic check tiap 5 detik
    setInterval(async () => {
        if (!navigator.onLine) {
            document.getElementById('offline').classList.add('show');
            return;
        }
        const online = await testConnection();
        if (!online) {
            document.getElementById('offline').classList.add('show');
        } else {
            document.getElementById('offline').classList.remove('show');
        }
    }, 5000);
}

/* ============================================================
   NETWORK SETTINGS OPENER
============================================================ */
function openNetworkSettings() {
    if (/Android/i.test(navigator.userAgent)) {
        try {
            window.location.href = 'intent://settings/#Intent;scheme=android-app;end';
        } catch (e) {
            showToast('⚠️ Buka Settings HP → WiFi/Data', 'warning');
        }
    } else {
        showToast('⚠️ Buka Settings HP → WiFi/Data', 'warning');
    }
}

/* ============================================================
   PREVENT BACK BUTTON EXIT (Opsional)
============================================================ */
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeModal();
    }
});
</script>
</body>
</html>