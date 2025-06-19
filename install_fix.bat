@echo off
echo.
echo ================================================================
echo  VibeCoding CLI - Sorun Giderici Kurulum
echo ================================================================
echo.

REM Mevcut kurulumu temizle
echo 🧹 Onceki kurulum kalintilari temizleniyor...
pip uninstall vibe-coding-cli -y >nul 2>&1

REM Python ve pip kontrolu
echo 🔍 Python kontrolu...
python --version
if errorlevel 1 (
    echo ❌ Python bulunamadi!
    pause
    exit /b 1
)

echo 🔍 pip kontrolu...
python -m pip --version
if errorlevel 1 (
    echo ❌ pip bulunamadi!
    pause
    exit /b 1
)

echo.
echo 📋 Kurulum secenekleri:
echo 1. Hizli kurulum (onerilen)
echo 2. Debug kurulum (sorun yasiyorsaniz)
echo 3. Manuel kurulum
echo.

set /p choice="Seciminizi yapin [1]: "
if "%choice%"=="" set choice=1

if "%choice%"=="1" (
    echo.
    echo 🚀 Hizli kurulum basliyor...
    python quick_install.py
) else if "%choice%"=="2" (
    echo.
    echo 🔧 Debug kurulum basliyor...
    python install_vibe_cli_debug.py
) else if "%choice%"=="3" (
    echo.
    echo 📦 Manuel kurulum basliyor...
    echo.
    echo Adim 1: pip guncelleme...
    python -m pip install --upgrade pip
    echo.
    echo Adim 2: Temel paketler...
    python -m pip install rich python-dotenv pydantic httpx
    echo.
    echo Adim 3: AI paketleri...
    python -m pip install pydantic-ai google-generativeai
    echo.
    echo Adim 4: VibeCoding CLI...
    python -m pip install -e .
    echo.
    echo Adim 5: Test...
    vibe --version
) else (
    echo ❌ Gecersiz secim!
    pause
    exit /b 1
)

echo.
if errorlevel 1 (
    echo ❌ Kurulum basarisiz!
    echo.
    echo 🆘 Sorun giderme onerileri:
    echo 1. Antivirus yazilimini gecici kapatin
    echo 2. Yonetici olarak calistirin
    echo 3. Internet baglantinizi kontrol edin
    echo 4. Python 3.8+ yuklu oldugunu dogrulayin
    echo.
) else (
    echo.
    echo 🎉 KURULUM BASARILI!
    echo.
    echo 📋 Sonraki adimlar:
    echo 1. API anahtarinizi alin (DeepSeek veya Gemini)
    echo 2. vibe init my-project komutu ile test edin
    echo.
)

pause 