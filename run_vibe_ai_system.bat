@echo off
echo 🚀 VibeCoding AI System Başlatılıyor...
echo.

REM Python'un yüklü olup olmadığını kontrol et
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Lütfen Python'u yükleyin.
    pause
    exit /b 1
)

REM Gerekli paketleri yükle
echo 📦 Gerekli paketler yükleniyor...
pip install -r requirements.txt

REM VibeCoding AI System'i başlat
echo.
echo 🎯 VibeCoding AI System başlatılıyor...
python vibe_coding_ai_system.py

pause 