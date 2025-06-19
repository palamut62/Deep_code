#!/bin/bash
# VibeCoding CLI - Kaldırma Script'i (Linux/Mac)

set -e  # Hata durumunda çık

# Renkler
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${PURPLE}"
echo "████████████████████████████████████████████████████████████████"
echo "█                                                              █"
echo "█            🗑️ VibeCoding CLI - Kaldırma İşlemi               █"
echo "█                                                              █"
echo "████████████████████████████████████████████████████████████████"
echo -e "${NC}"

echo -e "${BLUE}📋 Bu script aşağıdaki işlemleri gerçekleştirecek:${NC}"
echo
echo -e "    📦 pip paketini kaldırma (vibe-coding-cli)"
echo -e "    💻 vibe komutunu sistem PATH'inden çıkarma"
echo -e "    📁 Global konfigürasyon dosyalarını silme"
echo -e "    🗄️ Cache ve geçici dosyaları temizleme"
echo

# Kullanıcı onayı
read -p $'⚠️ VibeCoding CLI\'yi tamamen kaldırmak istiyor musunuz? (e/H): ' confirm
if [[ ! $confirm =~ ^[Ee]$ ]]; then
    echo -e "${YELLOW}⏹️ Kaldırma işlemi iptal edildi.${NC}"
    exit 0
fi

echo
echo -e "${BLUE}🔍 Python kurulumu kontrol ediliyor...${NC}"

# Python kontrolü
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python bulunamadı! Python 3 kurulu olmalı.${NC}"
    exit 1
fi

# Python komutunu belirle
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo -e "${GREEN}✅ Python bulundu: $($PYTHON_CMD --version)${NC}"

echo
echo -e "${BLUE}🗑️ VibeCoding CLI kaldırılıyor...${NC}"
echo

# pip paketi kaldır
echo -e "${CYAN}📦 pip paketini kaldırıyor...${NC}"
if $PYTHON_CMD -m pip uninstall vibe-coding-cli -y 2>/dev/null; then
    echo -e "${GREEN}✅ pip paketi kaldırıldı${NC}"
else
    echo -e "${YELLOW}⚠️ pip paketi kaldırılamadı veya zaten kaldırılmış${NC}"
fi

echo
echo -e "${CYAN}📁 Konfigürasyon dosyaları kaldırılıyor...${NC}"

# Konfigürasyon klasörü
CONFIG_DIR="$HOME/.config/vibecoding"
if [ -d "$CONFIG_DIR" ]; then
    rm -rf "$CONFIG_DIR"
    echo -e "${GREEN}✅ Konfigürasyon klasörü kaldırıldı: $CONFIG_DIR${NC}"
else
    echo -e "${YELLOW}ℹ️ Konfigürasyon klasörü bulunamadı${NC}"
fi

echo
echo -e "${CYAN}🗄️ Cache dosyaları temizleniyor...${NC}"

# Cache dosyaları
CACHE_LOCATIONS=(
    "$HOME/.cache/vibe-coding"
    "$(pwd)/__pycache__"
    "$(pwd)/.cache"
)

for cache_dir in "${CACHE_LOCATIONS[@]}"; do
    if [ -d "$cache_dir" ]; then
        rm -rf "$cache_dir"
        echo -e "${GREEN}✅ Cache kaldırıldı: $cache_dir${NC}"
    fi
done

echo
echo -e "${CYAN}🔍 Kaldırma işlemi doğrulanıyor...${NC}"

# vibe komutunu test et
if command -v vibe &> /dev/null; then
    echo -e "${YELLOW}⚠️ vibe komutu hala çalışıyor - manuel temizlik gerekebilir${NC}"
else
    echo -e "${GREEN}✅ vibe komutu kaldırıldı${NC}"
fi

# pip paketi test et
if $PYTHON_CMD -m pip show vibe-coding-cli &> /dev/null; then
    echo -e "${YELLOW}⚠️ pip paketi hala mevcut - manuel temizlik gerekebilir${NC}"
else
    echo -e "${GREEN}✅ pip paketi kaldırıldı${NC}"
fi

echo
echo -e "${GREEN}"
echo "████████████████████████████████████████████████████████████████"
echo "█                                                              █"
echo "█               🎉 Kaldırma İşlemi Tamamlandı!                 █"
echo "█                                                              █"
echo "████████████████████████████████████████████████████████████████"
echo -e "${NC}"

echo -e "${GREEN}✅ VibeCoding CLI sisteminizden kaldırıldı${NC}"
echo
echo -e "${BLUE}📁 Proje Dosyaları:${NC}"
echo -e "   - Bu klasördeki dosyalar korundu"
echo -e "   - generated_projects/ klasörünü manuel silebilirsiniz"
echo
echo -e "${BLUE}🔄 Yeniden Kurulum:${NC}"
echo -e "   - ./install_global.sh dosyasını çalıştırın"
echo

# generated_projects klasörü için soru
if [ -d "generated_projects" ]; then
    read -p $'📁 generated_projects klasörünü silmek istiyor musunuz? (e/H): ' keep_projects
    if [[ $keep_projects =~ ^[Ee]$ ]]; then
        rm -rf "generated_projects"
        echo -e "${GREEN}✅ generated_projects klasörü silindi${NC}"
    else
        echo -e "${BLUE}📁 generated_projects klasörü korundu${NC}"
    fi
fi

echo
echo -e "${PURPLE}👋 VibeCoding CLI kullandığınız için teşekkürler!${NC}"
echo

# Manuel temizlik talimatları
echo -e "${YELLOW}🛠️ Manuel Temizlik (gerekirse):${NC}"
echo
echo -e "${CYAN}1. pip Paketi:${NC}"
echo -e "   $PYTHON_CMD -m pip uninstall vibe-coding-cli -y"
echo
echo -e "${CYAN}2. Konfigürasyon:${NC}"
echo -e "   rm -rf ~/.config/vibecoding"
echo
echo -e "${CYAN}3. Cache:${NC}"
echo -e "   rm -rf ~/.cache/vibe-coding"
echo -e "   find . -name '__pycache__' -type d -exec rm -rf {} +"
echo 