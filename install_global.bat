@echo off
echo.
echo ================================================================
echo  VibeCoding CLI - Global Kurulum (Windows)
echo ================================================================
echo.
echo Claude Code benzeri terminal AI araci kuruluyor...
echo.

REM Python kontrolu
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python bulunamadi! Lutfen Python 3.8+ yukleyin.
    echo    https://python.org/downloads
    pause
    exit /b 1
)

echo ✅ Python mevcut
echo.

REM Kurulum scriptini calistir
echo 📦 VibeCoding CLI kuruluyor...
python install_vibe_cli.py

if errorlevel 1 (
    echo.
    echo ❌ Kurulum basarisiz!
    pause
    exit /b 1
)

echo.
echo ================================================================
echo  🎉 VibeCoding CLI basariyla kuruldu!
echo ================================================================
echo.
echo Artik herhangi bir klasorde 'vibe' komutunu kullanabilirsiniz:
echo.
echo   vibe init my-project    # Yeni proje olustur
echo   vibe --help            # Yardim
echo.
echo Ornek kullanim:
echo   cd C:\Users\%USERNAME%\Desktop
echo   vibe init my-web-app
echo.
pause 