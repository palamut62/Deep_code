# 🚀 VibeCoding CLI - Terminal Tabanlı AI Geliştirme Aracı

Claude Code benzeri terminal uygulaması. DeepSeek ve Gemini AI kullanarak herhangi bir klasörde tam kapsamlı yazılım projeleri oluşturur.

## ✨ Özellikler

- **Claude Code Benzeri**: Herhangi bir klasörde `vibe init` komutu ile proje oluşturma
- **6 Uzman AI Ajanı**: Backend, Frontend, Database, UI/UX, DevOps, Mobile
- **Çoklu AI Desteği**: DeepSeek ve Gemini API entegrasyonu
- **Otomatik Kod Üretimi**: Tam kapsamlı proje dosyaları oluşturma
- **VibeCoding Metodolojisi**: Kaliteli ve sürdürülebilir kod üretimi
- **Global Kurulum**: Sistem genelinde kullanılabilir terminal aracı

## 🛠️ Kurulum

### Otomatik Kurulum (Önerilen)

#### Windows:
```batch
# install_global.bat dosyasını çift tıklayın
# veya PowerShell'de:
.\install_global.bat
```

#### Linux/Mac:
```bash
# Terminal'de:
./install_global.sh
```

### Manuel Kurulum

```bash
# 1. Bağımlılıkları yükle
pip install -r requirements.txt

# 2. Global kurulum
python install_vibe_cli.py

# 3. Test et
vibe --version
```

## 🎯 Kullanım

### Temel Komutlar

```bash
vibe init [proje-adı]    # Yeni proje oluştur
vibe --help             # Yardım menüsü
vibe --version          # Versiyon bilgisi
```

### Örnek Kullanımlar

#### 1. Web Uygulaması Oluşturma
```bash
cd ~/Desktop
vibe init my-web-app
# İnteraktif proje oluşturma süreci başlar
```

#### 2. API Projesi Oluşturma
```bash
mkdir ~/projects/my-api
cd ~/projects/my-api
vibe init
# Proje tipini "api" olarak seçin
```

#### 3. Mobil Uygulama Projesi
```bash
vibe init social-app
# Proje tipini "mobile" olarak seçin
```

## 🎯 Desteklenen Proje Tipleri

| Tip | Açıklama | Teknolojiler |
|-----|----------|-------------|
| **web** | Web uygulaması | React, Vue.js, Angular |
| **api** | RESTful API | FastAPI, Express.js, Django |
| **mobile** | Mobil uygulama | React Native, Flutter |
| **desktop** | Masaüstü uygulaması | Electron, Tauri |
| **fullstack** | Tam yığın uygulama | React + FastAPI |

## 🤖 AI Uzmanları

### 👨‍💻 Backend Uzmanı
- RESTful API tasarımı
- Veritabanı entegrasyonu
- Authentication sistemi
- Mikroservis mimarisi

### 🎨 Frontend Uzmanı
- Modern UI/UX tasarımı
- Responsive web tasarımı
- State management
- Component mimarisi

### 🗄️ Database Uzmanı
- Veri modelleme
- Migration scriptleri
- Performance optimizasyonu
- Backup stratejileri

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
- Cross-platform development
- Native performans
- Push notification
- App store optimization

## 🔧 API Konfigürasyonu

### DeepSeek API
- **Website**: https://platform.deepseek.com
- **Ücretsiz Tier**: 2M token/ay
- **Güçlü Yanları**: Kod üretimi, hızlı yanıt

### Gemini API
- **Website**: https://makersuite.google.com
- **Ücretsiz Tier**: 60 istek/dakika
- **Güçlü Yanları**: Çok dilli destek, analiz

## 📁 Proje Yapısı

Oluşturulan projeler şu yapıya sahiptir:

```
my-project/
├── vibe-project.json       # Proje konfigürasyonu
├── README.md              # Proje dokümantasyonu
├── backend/               # Backend dosyaları
│   ├── main.py
│   ├── models/
│   └── requirements.txt
├── frontend/              # Frontend dosyaları
│   ├── src/
│   ├── components/
│   └── package.json
├── database/              # Database dosyaları
│   ├── schemas/
│   └── migrations/
└── devops/               # DevOps dosyaları
    ├── Dockerfile
    └── docker-compose.yml
```

## 🚀 Avantajlar

- **Claude Code Benzeri**: Herhangi bir klasörde çalışır
- **Hızlı Kurulum**: Tek komutla global kurulum
- **Tam Kapsamlı**: 6 uzman AI ile eksiksiz projeler
- **Çoklu Platform**: Windows, Linux, Mac desteği
- **Sürdürülebilir**: VibeCoding metodolojisi ile kaliteli kod

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
```

### İzin Hatası (Linux/Mac)
```bash
# Script'i executable yap
chmod +x install_global.sh
```

## 🤝 Katkıda Bulunma

1. Repository'yi fork edin
2. Feature branch oluşturun (`git checkout -b feature/yeni-ozellik`)
3. Değişiklikleri commit edin (`git commit -m 'feat: yeni özellik eklendi'`)
4. Branch'i push edin (`git push origin feature/yeni-ozellik`)
5. Pull Request oluşturun

## 📝 Lisans

Bu proje MIT lisansı altında lisanslanmıştır.

## 🆘 Destek

- **GitHub Issues**: Hata raporları ve özellik istekleri
- **Dokümantasyon**: README_VIBE_AI_SYSTEM.md
- **Örnekler**: KULLANIM_ORNEGI_AI_SYSTEM.md

---

**VibeCoding CLI ile AI destekli geliştirme deneyiminizi yaşayın! 🚀** # Deep_code
