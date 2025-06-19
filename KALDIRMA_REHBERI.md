# 🗑️ VibeCoding CLI - Kaldırma Rehberi

VibeCoding CLI'yi sisteminizden tamamen kaldırmak için bu rehberi takip edin.

## 🚨 Önemli Uyarı

**VibeCoding CLI global olarak kurulduğu için sadece dosyaları silmek yeterli değildir!**

Aşağıdaki öğelerin temizlenmesi gerekir:
- 📦 Python paketi (pip)
- 💻 Terminal komutu (vibe)
- 📁 Global konfigürasyon dosyaları
- 🔑 API anahtarları
- 🗄️ Cache ve geçici dosyalar

---

## 🛠️ Kaldırma Yöntemleri

### 1️⃣ Otomatik Kaldırma (Önerilen)

#### Windows:
```cmd
# Basit kaldırma
uninstall_global.bat

# Detaylı kaldırma (önerilen)
python uninstall_vibe_cli.py
```

#### Linux/Mac:
```bash
# Basit kaldırma
./uninstall_global.sh

# Detaylı kaldırma (önerilen)
python3 uninstall_vibe_cli.py
```

### 2️⃣ Manuel Kaldırma

Otomatik kaldırma başarısız olursa:

#### 1. pip Paketini Kaldır
```bash
pip uninstall vibe-coding-cli -y
```

#### 2. Global Konfigürasyon Dosyalarını Sil

**Windows:**
```cmd
rmdir /s /q "%APPDATA%\VibeCoding"
```

**Linux/Mac:**
```bash
rm -rf ~/.config/vibecoding
```

#### 3. Cache Dosyalarını Temizle

**Windows:**
```cmd
rmdir /s /q "__pycache__"
rmdir /s /q ".cache"
```

**Linux/Mac:**
```bash
rm -rf ~/.cache/vibe-coding
find . -name "__pycache__" -type d -exec rm -rf {} +
```

#### 4. vibe Komutunu Test Et
```bash
vibe --version
```
Hata verirse başarıyla kaldırılmıştır.

---

## 📁 Proje Dosyaları

### Korunacak Dosyalar
- Mevcut proje klasörü
- `generated_projects/` klasörü (isteğe bağlı)
- Kendi oluşturduğunuz projeler

### Silinecek Dosyalar (İsteğe Bağlı)
```bash
# Proje klasörünü tamamen sil
rm -rf /path/to/Vibe_Coding

# Sadece generated_projects'i sil
rm -rf generated_projects/
```

---

## 🔍 Kaldırma Doğrulaması

Kaldırma işleminden sonra kontrol edin:

### 1. pip Paketi Kontrolü
```bash
pip show vibe-coding-cli
```
**Beklenen:** "Package not found" hatası

### 2. Komut Kontrolü
```bash
vibe --version
```
**Beklenen:** "Command not found" hatası

### 3. Konfigürasyon Kontrolü

**Windows:**
```cmd
dir "%APPDATA%\VibeCoding"
```

**Linux/Mac:**
```bash
ls ~/.config/vibecoding
```
**Beklenen:** Klasör bulunamadı hatası

---

## 🚨 Sorun Giderme

### Kaldırma Başarısız Olursa

1. **Administrator/Root yetkisi ile çalıştırın**
2. **Python ortamını kontrol edin**
3. **Manuel temizlik yapın**

### Hala vibe Komutu Çalışıyorsa

```bash
# Hangi vibe komutunun çalıştığını bulun
which vibe  # Linux/Mac
where vibe  # Windows

# PATH'i kontrol edin
echo $PATH  # Linux/Mac
echo %PATH%  # Windows
```

### pip Paketi Kaldırılamıyorsa

```bash
# Farklı pip komutları deneyin
pip3 uninstall vibe-coding-cli -y
python -m pip uninstall vibe-coding-cli -y
python3 -m pip uninstall vibe-coding-cli -y

# Zorla kaldır
pip uninstall vibe-coding-cli --break-system-packages -y
```

---

## 🔄 Yeniden Kurulum

VibeCoding CLI'yi tekrar kurmak isterseniz:

### Windows:
```cmd
install_global.bat
```

### Linux/Mac:
```bash
./install_global.sh
```

---

## 📞 Destek

Kaldırma sırasında sorun yaşarsanız:

1. **Hata mesajını kaydedin**
2. **Sistem bilgilerini toplayın:**
   - İşletim sistemi
   - Python versiyonu
   - pip versiyonu

3. **Manuel temizlik adımlarını uygulayın**

---

## ✅ Kaldırma Checklist

- [ ] `pip uninstall vibe-coding-cli -y` çalıştırıldı
- [ ] Global konfigürasyon klasörü silindi
- [ ] Cache dosyaları temizlendi
- [ ] `vibe --version` komutu hata veriyor
- [ ] `pip show vibe-coding-cli` paket bulunamadı diyor
- [ ] Proje dosyaları korundu (isteğe bağlı)

**🎉 VibeCoding CLI başarıyla kaldırıldı!**

---

## 👋 Veda Mesajı

VibeCoding CLI'yi kullandığınız için teşekkürler! 

İleride tekrar ihtiyaç duyarsanız, kurulum dosyaları her zaman hazır.

**Happy Coding! 🚀** 