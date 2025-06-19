@echo off
chcp 65001 > nul
title VibeCoding CLI - Kaldırma

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █            🗑️ VibeCoding CLI - Kaldırma İşlemi               █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 📋 Bu script aşağıdaki işlemleri gerçekleştirecek:
echo.
echo    📦 pip paketini kaldırma (vibe-coding-cli)
echo    💻 vibe komutunu sistem PATH'inden çıkarma
echo    📁 Global konfigürasyon dosyalarını silme
echo    🗄️ Cache ve geçici dosyaları temizleme
echo.

set /p confirm="⚠️ VibeCoding CLI'yi tamamen kaldırmak istiyor musunuz? (E/H): "
if /i not "%confirm%"=="E" (
    echo.
    echo ⏹️ Kaldırma işlemi iptal edildi.
    pause
    exit /b 0
)

echo.
echo 🔍 Python kurulumu kontrol ediliyor...

python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Python kurulu olmalı.
    pause
    exit /b 1
)

echo ✅ Python bulundu

echo.
echo 🗑️ VibeCoding CLI kaldırılıyor...
echo.

echo 📦 pip paketini kaldırıyor...
python -m pip uninstall vibe-coding-cli -y
if errorlevel 1 (
    echo ⚠️ pip paketi kaldırılamadı veya zaten kaldırılmış
) else (
    echo ✅ pip paketi kaldırıldı
)

echo.
echo 📁 Konfigürasyon dosyaları kaldırılıyor...

set "config_dir=%APPDATA%\VibeCoding"
if exist "%config_dir%" (
    rmdir /s /q "%config_dir%"
    echo ✅ Konfigürasyon klasörü kaldırıldı: %config_dir%
) else (
    echo ℹ️ Konfigürasyon klasörü bulunamadı
)

echo.
echo 🗄️ Cache dosyaları temizleniyor...

if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ __pycache__ klasörü kaldırıldı
)

if exist ".cache" (
    rmdir /s /q ".cache"
    echo ✅ .cache klasörü kaldırıldı
)

echo.
echo 🔍 Kaldırma işlemi doğrulanıyor...

vibe --version >nul 2>&1
if errorlevel 1 (
    echo ✅ vibe komutu kaldırıldı
) else (
    echo ⚠️ vibe komutu hala çalışıyor - manuel temizlik gerekebilir
)

python -m pip show vibe-coding-cli >nul 2>&1
if errorlevel 1 (
    echo ✅ pip paketi kaldırıldı
) else (
    echo ⚠️ pip paketi hala mevcut - manuel temizlik gerekebilir
)

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █               🎉 Kaldırma İşlemi Tamamlandı!                 █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo ✅ VibeCoding CLI sisteminizden kaldırıldı
echo.
echo 📁 Proje Dosyaları:
echo    - Bu klasördeki dosyalar korundu
echo    - generated_projects/ klasörünü manuel silebilirsiniz
echo.
echo 🔄 Yeniden Kurulum:
echo    - install_global.bat dosyasını çalıştırın
echo.

set /p keep_projects="📁 generated_projects klasörünü silmek istiyor musunuz? (E/H): "
if /i "%keep_projects%"=="E" (
    if exist "generated_projects" (
        rmdir /s /q "generated_projects"
        echo ✅ generated_projects klasörü silindi
    ) else (
        echo ℹ️ generated_projects klasörü bulunamadı
    )
) else (
    echo 📁 generated_projects klasörü korundu
)

echo.
echo 👋 VibeCoding CLI kullandığınız için teşekkürler!
echo.
pause 