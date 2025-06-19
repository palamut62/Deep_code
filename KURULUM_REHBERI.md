# 🚀 VibeCoding CLI - Kurulum Rehberi

## Claude Code Benzeri Terminal AI Aracı

VibeCoding CLI, herhangi bir klasörde `vibe init` komutu ile tam kapsamlı yazılım projeleri oluşturan terminal tabanlı AI aracıdır.

## 📋 Sistem Gereksinimleri

- **Python 3.8+**
- **pip (Python paket yöneticisi)**
- **İnternet bağlantısı**
- **DeepSeek veya Gemini API anahtarı**

## 🛠️ Kurulum Adımları

### 1. Otomatik Kurulum (Önerilen)

#### Windows:
```batch
# Proje klasöründe:
SUPER_INSTALL.bat
```

Bu sistem otomatik olarak:
- ✅ Önceki kurulum kalıntılarını temizler
- ✅ pip dependency hatalarını çözer
- ✅ Bozuk paketleri (~andas) düzeltir
- ✅ Bağımlılıkları güvenli şekilde kurar
- ✅ VibeCoding CLI'yi başarıyla kurar
- ✅ Kurulumu test eder ve doğrular

#### Linux/Mac:
```bash
# Terminal'de:
./install_global.sh
```

### 2. Manuel Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Global kurulum scripti çalıştır
python install_vibe_cli.py

# 3. Kurulumu test et
vibe --version
```

## 🔑 API Anahtarı Konfigürasyonu

### DeepSeek API
1. https://platform.deepseek.com adresine git
2. Hesap oluştur
3. API anahtarını al
4. Ücretsiz: 2M token/ay

### Gemini API
1. https://makersuite.google.com adresine git
2. API anahtarı oluştur
3. Ücretsiz: 60 istek/dakika

### Konfigürasyon Dosyası

Kurulum sırasında API anahtarları otomatik olarak yapılandırılır:

**Windows**: `%APPDATA%\VibeCoding\.env`
**Linux/Mac**: `~/.config/vibecoding/.env`

```env
# VibeCoding CLI - Global Konfigürasyon
DEEPSEEK_API_KEY=your_deepseek_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
DEBUG=False
DEFAULT_AI_PROVIDER=deepseek
```

## 🎯 Kullanım

### Temel Komutlar

```bash
vibe init [proje-adı]    # Yeni proje oluştur
vibe --help             # Yardım menüsü
vibe --version          # Versiyon bilgisi
```

### Örnek Kullanım

```bash
# 1. İstediğiniz klasöre gidin
cd ~/Desktop

# 2. Yeni proje oluşturun
vibe init my-web-app

# 3. İnteraktif süreç başlar
# - Proje tipi seçin (web, api, mobile, desktop, fullstack)
# - Teknoloji yığını belirtin
# - Özellikler listeleyin
# - AI uzmanları otomatik çalışır

# 4. Proje hazır!
cd my-web-app
# IDE'nizde açın ve geliştirmeye başlayın
```

## 🤖 AI Uzmanları

### 👨‍💻 Backend Uzmanı
- FastAPI, Django, Express.js
- RESTful API tasarımı
- Veritabanı entegrasyonu
- Authentication sistemi

### 🎨 Frontend Uzmanı
- React, Vue.js, Angular
- Modern UI/UX tasarımı
- Responsive web tasarımı
- State management

### 🗄️ Database Uzmanı
- PostgreSQL, MySQL, MongoDB
- Veri modelleme
- Migration scriptleri
- Performance optimizasyonu

### ✨ UI/UX Uzmanı
- Kullanıcı deneyimi tasarımı
- Design system oluşturma
- Wireframe ve prototipleme
- Accessibility standartları

### ⚙️ DevOps Uzmanı
- Docker containerization
- CI/CD pipeline'ları
- Kubernetes deployment
- Monitoring ve logging

### 📱 Mobile Uzmanı
- React Native, Flutter
- Cross-platform development
- Native performans
- Push notification

## 📁 Proje Yapısı

Oluşturulan her proje şu yapıya sahiptir:

```
my-project/
├── vibe-project.json       # Proje konfigürasyonu
├── README.md              # Proje dokümantasyonu
├── backend/               # Backend dosyaları
│   ├── main.py
│   ├── models/
│   ├── routes/
│   └── requirements.txt
├── frontend/              # Frontend dosyaları
│   ├── src/
│   │   ├── components/
│   │   └── pages/
│   ├── package.json
│   └── tailwind.config.js
├── database/              # Database dosyaları
│   ├── schemas/
│   ├── migrations/
│   └── seeds/
├── uiux/                  # UI/UX dosyaları
│   ├── design-system/
│   └── wireframes/
├── devops/               # DevOps dosyaları
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── kubernetes/
└── mobile/               # Mobile dosyaları (varsa)
    ├── src/
    └── components/
```

## 🔧 Sorun Giderme

### Komut Bulunamıyor
```bash
# Python PATH kontrol et
python -m pip show vibe-coding-cli

# Yeniden kur
python install_vibe_cli.py
```

### API Hatası
```bash
# Global config dosyasını düzenle
# Windows: %APPDATA%\VibeCoding\.env
# Linux/Mac: ~/.config/vibecoding/.env

# API anahtarlarını kontrol et
```

### İzin Hatası (Linux/Mac)
```bash
# Script'i executable yap
chmod +x install_global.sh
```

### Import Hatası
```bash
# Eksik paketleri yükle
pip install -r requirements.txt

# Python versiyonu kontrol et
python --version  # 3.8+ olmalı
```

## 🎉 Kurulum Sonrası

Kurulum başarılı olduktan sonra:

1. **Test Edin**: `vibe --version`
2. **İlk Proje**: `vibe init test-project`
3. **IDE'de Açın**: Oluşturulan projeyi IDE'nizde açın
4. **Geliştirin**: Hazır kod dosyaları ile geliştirmeye başlayın

## 💡 İpuçları

- **Proje Adları**: Kebab-case kullanın (my-web-app)
- **Klasör Seçimi**: Boş bir klasörde çalıştırın
- **API Sınırları**: Ücretsiz tier'ların limitlerini takip edin
- **Yedekleme**: Önemli projelerinizi yedekleyin

## 📞 Destek

- **Dokümantasyon**: README_VIBE_AI_SYSTEM.md
- **Kullanım Örnekleri**: KULLANIM_ORNEGI_AI_SYSTEM.md
- **GitHub Issues**: Hata raporları ve özellik istekleri
- **Test Script**: `python quick_test.py`

---

**VibeCoding CLI ile AI destekli geliştirme deneyiminizi yaşayın! 🚀** 