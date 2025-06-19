#!/bin/bash

echo ""
echo "================================================================"
echo " VibeCoding CLI - Global Kurulum (Unix/Linux/Mac)"
echo "================================================================"
echo ""
echo "Claude Code benzeri terminal AI aracı kuruluyor..."
echo ""

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python 3.8+ yükleyin."
    echo "   https://python.org/downloads"
    exit 1
fi

echo "✅ Python3 mevcut"
echo ""

# Kurulum scriptini çalıştır
echo "📦 VibeCoding CLI kuruluyor..."
python3 install_vibe_cli.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Kurulum başarısız!"
    exit 1
fi

echo ""
echo "================================================================"
echo " 🎉 VibeCoding CLI başarıyla kuruldu!"
echo "================================================================"
echo ""
echo "Artık herhangi bir klasörde 'vibe' komutunu kullanabilirsiniz:"
echo ""
echo "  vibe init my-project    # Yeni proje oluştur"
echo "  vibe --help            # Yardım"
echo ""
echo "Örnek kullanım:"
echo "  cd ~/Desktop"
echo "  vibe init my-web-app"
echo "" 