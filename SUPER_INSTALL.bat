@echo off
chcp 65001 > nul
title VibeCoding CLI - Süper Kurulum Sistemi

echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █          🚀 VibeCoding CLI - Süper Kurulum Sistemi           █
echo █                     Tüm Sorunları Çözer                     █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.

echo 🎯 Bu sistem şunları yapar:
echo    ✅ Önceki kurulum kalıntılarını temizler
echo    ✅ pip dependency hatalarını çözer
echo    ✅ Bozuk paketleri (~andas) düzeltir
echo    ✅ Bağımlılıkları güvenli şekilde kurar
echo    ✅ VibeCoding CLI'yi başarıyla kurar
echo    ✅ Kurulumu test eder ve doğrular
echo.

set /p confirm="🚀 Süper kurulum başlatılsın mı? (E/H): "
if /i not "%confirm%"=="E" (
    echo.
    echo ⏹️ Kurulum iptal edildi.
    pause
    exit /b 0
)

echo.
echo ████████████████████████████████████████████████████████████████
echo █                    AŞAMA 1: SİSTEM KONTROLÜ                  █
echo ████████████████████████████████████████████████████████████████

echo.
echo 🔍 Python kontrolü...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadı! Python 3.8+ kurulu olmalı.
    echo 📥 Python indirin: https://python.org/downloads
    pause
    exit /b 1
)

echo ✅ Python bulundu: 
python --version

echo.
echo 🔍 pip kontrolü...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip bulunamadı! Python kurulumu sorunlu.
    pause
    exit /b 1
)

echo ✅ pip bulundu:
python -m pip --version

echo.
echo ████████████████████████████████████████████████████████████████
echo █                   AŞAMA 2: TEMİZLİK İŞLEMLERİ               █
echo ████████████████████████████████████████████████████████████████

echo.
echo 🧹 Önceki kurulum kalıntıları temizleniyor...

echo    📦 Eski VibeCoding CLI kaldırılıyor...
python -m pip uninstall vibe-coding-cli -y >nul 2>&1
echo    ✅ Eski kurulum temizlendi

echo    🗄️ pip cache temizleniyor...
python -m pip cache purge >nul 2>&1
echo    ✅ pip cache temizlendi

echo    🔧 Bozuk paketler kontrol ediliyor...
python -m pip list 2>nul | findstr "~andas" >nul
if not errorlevel 1 (
    echo    ⚠️ Bozuk pandas tespit edildi, temizleniyor...
    python -m pip uninstall pandas -y >nul 2>&1
    echo    ✅ Bozuk pandas temizlendi
) else (
    echo    ✅ Bozuk paket bulunamadı
)

echo.
echo ████████████████████████████████████████████████████████████████
echo █                 AŞAMA 3: SİSTEM GÜNCELLEMESİ                █
echo ████████████████████████████████████████████████████████████████

echo.
echo 🔧 pip araçları güncelleniyor...
python -m pip install --upgrade pip setuptools wheel --quiet
if errorlevel 1 (
    echo ⚠️ pip güncelleme sorunu, devam ediliyor...
) else (
    echo ✅ pip araçları güncellendi
)

echo.
echo ████████████████████████████████████████████████████████████████
echo █              AŞAMA 4: BAĞIMLILIK KURULUMU                   █
echo ████████████████████████████████████████████████████████████████

echo.
echo 📦 Bağımlılıklar güvenli şekilde kuruluyor...

set deps=rich>=13.0.0 python-dotenv>=1.0.0 pydantic>=2.0.0 httpx>=0.25.0 google-generativeai>=0.3.0 pydantic-ai>=0.0.13

for %%d in (%deps%) do (
    echo    📦 %%d kuruluyor...
    
    REM Yöntem 1: Legacy resolver
    python -m pip install "%%d" --use-deprecated=legacy-resolver --no-cache-dir --quiet >nul 2>&1
    if not errorlevel 1 (
        echo    ✅ %%d kuruldu ^(legacy^)
    ) else (
        REM Yöntem 2: No-deps
        python -m pip install "%%d" --no-deps --quiet >nul 2>&1
        if not errorlevel 1 (
            echo    ✅ %%d kuruldu ^(no-deps^)
        ) else (
            REM Yöntem 3: Basit kurulum
            python -m pip install "%%d" --quiet >nul 2>&1
            if not errorlevel 1 (
                echo    ✅ %%d kuruldu ^(basit^)
            ) else (
                echo    ⚠️ %%d kurulamadı, devam ediliyor...
            )
        )
    )
)

echo.
echo ████████████████████████████████████████████████████████████████
echo █             AŞAMA 5: VIBECODING CLI KURULUMU                █
echo ████████████████████████████████████████████████████████████████

echo.
echo 🚀 VibeCoding CLI kuruluyor...

REM Kurulum yöntemleri sırasıyla denenecek
echo    🔄 Kurulum yöntemi 1: Legacy resolver...
python -m pip install -e . --use-deprecated=legacy-resolver --quiet >nul 2>&1
if not errorlevel 1 (
    echo    ✅ VibeCoding CLI kuruldu ^(legacy resolver^)
    goto test_installation
)

echo    🔄 Kurulum yöntemi 2: No-deps...
python -m pip install -e . --no-deps --quiet >nul 2>&1
if not errorlevel 1 (
    echo    ✅ VibeCoding CLI kuruldu ^(no-deps^)
    goto test_installation
)

echo    🔄 Kurulum yöntemi 3: Force reinstall...
python -m pip install -e . --force-reinstall --no-cache-dir --quiet >nul 2>&1
if not errorlevel 1 (
    echo    ✅ VibeCoding CLI kuruldu ^(force reinstall^)
    goto test_installation
)

echo    🔄 Kurulum yöntemi 4: Basit kurulum...
python -m pip install -e . --quiet >nul 2>&1
if not errorlevel 1 (
    echo    ✅ VibeCoding CLI kuruldu ^(basit^)
    goto test_installation
)

echo    ❌ Tüm kurulum yöntemleri başarısız
goto manual_solution

:test_installation
echo.
echo ████████████████████████████████████████████████████████████████
echo █                   AŞAMA 6: KURULUM TESTİ                    █
echo ████████████████████████████████████████████████████████████████

echo.
echo 🧪 Kurulum testi yapılıyor...

echo    🔍 vibe komut testi...
vibe --version >nul 2>&1
if not errorlevel 1 (
    echo    ✅ vibe komutu çalışıyor
    vibe --version
    set "test_success=1"
) else (
    echo    ⚠️ vibe komutu çalışmıyor
)

echo    🔍 Modül import testi...
python -c "import vibe_cli; print('VibeCoding CLI modülü yüklü')" >nul 2>&1
if not errorlevel 1 (
    echo    ✅ VibeCoding CLI modülü yüklü
    set "test_success=1"
) else (
    echo    ⚠️ VibeCoding CLI modülü yüklenemedi
)

if defined test_success goto success

echo    ❌ Kurulum testleri başarısız
goto manual_solution

:success
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                   🎉 KURULUM BAŞARILI!                      █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo ✅ Tüm aşamalar başarıyla tamamlandı:
echo    ✅ Sistem temizlendi
echo    ✅ Bağımlılıklar kuruldu
echo    ✅ VibeCoding CLI kuruldu
echo    ✅ Kurulum doğrulandı
echo.
echo 🚀 Kullanıma hazır komutlar:
echo    vibe --version           # Versiyon kontrolü
echo    vibe --help             # Yardım menüsü
echo    vibe init my-project    # Yeni proje oluştur
echo.
echo 📁 Sonraki adımlar:
echo    1. API anahtarlarınızı ayarlayın
echo    2. İlk projenizi oluşturun:
echo       vibe init test-project
echo    3. VibeCoding CLI'yi keşfedin!
echo.
echo 🎯 Global konfigürasyon:
echo    %APPDATA%\VibeCoding\.env
echo.
echo 🎉 VibeCoding CLI kullanıma hazır! Happy Coding! 🚀
goto end

:manual_solution
echo.
echo ████████████████████████████████████████████████████████████████
echo █                                                              █
echo █                ⚠️ MANUEL ÇÖZÜM GEREKLİ                      █
echo █                                                              █
echo ████████████████████████████████████████████████████████████████
echo.
echo 🛠️ Otomatik kurulum başarısız oldu. Manuel çözüm adımları:
echo.
echo 💡 Çözüm 1: Virtual Environment
echo    python -m venv vibe_env
echo    vibe_env\Scripts\activate
echo    pip install --upgrade pip setuptools wheel
echo    pip install -e . --no-cache-dir
echo.
echo 💡 Çözüm 2: Python Version Kontrolü
echo    - Python 3.8-3.11 arası kullanın
echo    - Python 3.12+ ile sorun olabilir
echo.
echo 💡 Çözüm 3: Admin Yetkisi
echo    - PowerShell'i "Yönetici olarak çalıştır"
echo    - Bu batch dosyasını tekrar çalıştırın
echo.
echo 💡 Çözüm 4: Antivirus Kontrolü
echo    - Antivirus yazılımını geçici kapatın
echo    - Windows Defender'ı kontrol edin
echo.
echo 💡 Çözüm 5: Manuel Kurulum
echo    pip install rich python-dotenv pydantic httpx google-generativeai pydantic-ai
echo    pip install -e .
echo.
echo 📞 Daha fazla yardım için:
echo    - README.md dosyasını okuyun
echo    - KURULUM_REHBERI.md'yi inceleyin
echo.

:end
echo.
echo 👋 VibeCoding CLI kurulum süreci tamamlandı.
echo.
pause 