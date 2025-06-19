# 🎯 VibeCoding AI System - Kullanım Örnekleri

Bu dokümanda VibeCoding AI System'in çeşitli senaryolarda nasıl kullanılacağına dair detaylı örnekler bulacaksınız.

## 🚀 Başlangıç

### Sistem Kurulumu ve İlk Çalıştırma

```bash
# 1. Kurulum script'ini çalıştır
python setup_vibe_ai_system.py

# 2. Sistemi başlat
python vibe_coding_ai_system.py
```

## 📋 Örnek Senaryolar

### 1. 🛒 E-Ticaret Web Uygulaması

**Senaryo**: Modern bir e-ticaret sitesi oluşturmak istiyorsunuz.

#### Adım 1: Proje Oluşturma
```
🎯 Seçiminizi yapın: 1

📝 Proje adı: ModernShop
📄 Proje açıklaması: Modern ve kullanıcı dostu e-ticaret platformu

Proje Tipi:
1. web
2. mobile
3. desktop
4. api
5. fullstack

Proje tipi seçin: 5

Önerilen teknolojiler (fullstack):
1. MERN
2. MEAN
3. Django+React
4. Laravel+Vue

Teknoloji yığını: React, FastAPI, PostgreSQL
Ana özellikler: Ürün kataloğu, sepet yönetimi, ödeme sistemi, kullanıcı hesapları
Hedef kitle: Online alışveriş yapan kullanıcılar
Karmaşıklık seviyesi: orta
Veritabanı gerekli mi?: y
Kimlik doğrulama gerekli mi?: y
API gerekli mi?: y
```

#### Adım 2: Otomatik Geliştirme
Sistem otomatik olarak şu uzmanları çalıştıracak:
- **Frontend Uzmanı**: React tabanlı modern arayüz
- **Backend Uzmanı**: FastAPI ile RESTful API
- **Database Uzmanı**: PostgreSQL şema tasarımı
- **UI/UX Uzmanı**: E-ticaret UX pattern'leri
- **DevOps Uzmanı**: Docker ve deployment konfigürasyonu

#### Beklenen Çıktılar
```
generated_projects/ModernShop/
├── project_config.json
├── project_summary.json
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── ProductCard.jsx
│   │   │   ├── ShoppingCart.jsx
│   │   │   └── UserAuth.jsx
│   │   ├── pages/
│   │   │   ├── HomePage.jsx
│   │   │   ├── ProductPage.jsx
│   │   │   └── CheckoutPage.jsx
│   │   └── styles/
│   │       └── tailwind.config.js
│   ├── package.json
│   └── README.md
├── backend/
│   ├── main.py
│   ├── models/
│   │   ├── user.py
│   │   ├── product.py
│   │   └── order.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── products.py
│   │   └── orders.py
│   ├── requirements.txt
│   └── tests/
├── database/
│   ├── schemas/
│   │   └── ecommerce_schema.sql
│   ├── migrations/
│   │   └── 001_initial_tables.sql
│   └── seeds/
│       └── sample_products.sql
├── uiux/
│   ├── design-system/
│   │   └── components.md
│   ├── wireframes/
│   │   └── user-flow.md
│   └── style-guide.md
└── devops/
    ├── docker/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    └── ci-cd/
        └── github-actions.yml
```

### 2. 📱 Sosyal Medya Mobil Uygulaması

**Senaryo**: React Native ile sosyal medya uygulaması geliştirmek istiyorsunuz.

#### Uzman Modu Kullanımı
```
🎯 Seçiminizi yapın: m

👨‍💻 Mobile Uzmanı ile Konsültasyon

Özel istek: Instagram benzeri sosyal medya uygulaması için React Native kodları. 
Fotoğraf paylaşımı, beğeni sistemi, takip sistemi ve mesajlaşma özellikleri olsun.
```

#### Beklenen Uzman Yanıtı
```
🔍 Analiz:
React Native tabanlı sosyal medya uygulaması için modern component yapısı,
state management (Redux Toolkit), navigation (React Navigation) ve 
real-time özellikler (Socket.io) entegrasyonu gerekiyor.

💡 Öneriler:
• Expo CLI kullanarak hızlı geliştirme
• Redux Toolkit ile state management
• React Navigation v6 ile sayfa geçişleri
• Async Storage ile local data
• Firebase ile real-time messaging
• React Native Image Picker ile fotoğraf seçimi

📁 Oluşturulan Dosyalar:
• App.js (Ana uygulama yapısı)
• src/components/PostCard.js (Gönderi kartı)
• src/screens/HomeScreen.js (Ana sayfa)
• src/screens/ProfileScreen.js (Profil sayfası)
• src/navigation/AppNavigator.js (Navigasyon)
• src/store/store.js (Redux store)
• package.json (Bağımlılıklar)
```

### 3. 🔧 RESTful API Projesi

**Senaryo**: Blog sistemi için backend API geliştirmek istiyorsunuz.

#### Backend Uzmanı ile Çalışma
```
🎯 Seçiminizi yapın: b

👨‍💻 Backend Uzmanı ile Konsültasyon

Özel istek: Blog sistemi için FastAPI ile RESTful API. 
JWT authentication, CRUD operasyonları, pagination ve OpenAPI dokümantasyonu.
```

#### Uzman Çıktısı Örneği
```python
# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import models, schemas, database
from typing import List

app = FastAPI(
    title="Blog API",
    description="VibeCoding metodolojisi ile geliştirilmiş blog API'si",
    version="1.0.0"
)

security = HTTPBearer()

# Authentication endpoint
@app.post("/auth/login", response_model=schemas.Token)
async def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
    """Kullanıcı girişi ve JWT token üretimi"""
    # Implementation here
    pass

# Blog posts CRUD
@app.get("/posts", response_model=List[schemas.Post])
async def get_posts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db)):
    """Sayfalama ile blog gönderilerini listele"""
    posts = db.query(models.Post).offset(skip).limit(limit).all()
    return posts

@app.post("/posts", response_model=schemas.Post)
async def create_post(
    post: schemas.PostCreate, 
    db: Session = Depends(database.get_db),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Yeni blog gönderisi oluştur"""
    # JWT validation and post creation
    pass
```

### 4. 🎨 Design System Oluşturma

**Senaryo**: Kurumsal web uygulaması için design system tasarlamak istiyorsunuz.

#### UI/UX Uzmanı ile Çalışma
```
🎯 Seçiminizi yapın: u

👨‍💻 UI/UX Uzmanı ile Konsültasyon

Özel istek: Fintech uygulaması için modern design system. 
Component library, color palette, typography ve accessibility guidelines.
```

#### Beklenen Çıktılar
```markdown
# Design System - FinTech App

## Color Palette

### Primary Colors
- Primary: #2563EB (Blue 600)
- Primary Light: #3B82F6 (Blue 500)
- Primary Dark: #1D4ED8 (Blue 700)

### Secondary Colors
- Success: #10B981 (Emerald 500)
- Warning: #F59E0B (Amber 500)
- Error: #EF4444 (Red 500)
- Info: #06B6D4 (Cyan 500)

### Neutral Colors
- Gray 50: #F9FAFB
- Gray 100: #F3F4F6
- Gray 900: #111827

## Typography

### Font Family
- Primary: Inter, system-ui, sans-serif
- Monospace: 'Fira Code', Consolas, monospace

### Font Sizes
- xs: 12px
- sm: 14px
- base: 16px
- lg: 18px
- xl: 20px
- 2xl: 24px
- 3xl: 30px

## Components

### Button
```css
.btn-primary {
  background-color: var(--color-primary);
  color: white;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  transition: all 0.2s ease;
}

.btn-primary:hover {
  background-color: var(--color-primary-dark);
  transform: translateY(-1px);
}
```

### Card
```css
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  padding: 24px;
  border: 1px solid var(--color-gray-200);
}
```
```

### 5. ⚙️ DevOps Pipeline Kurulumu

**Senaryo**: Mevcut projeniz için CI/CD pipeline kurmak istiyorsunuz.

#### DevOps Uzmanı ile Çalışma
```
🎯 Seçiminizi yapın: o

👨‍💻 DevOps Uzmanı ile Konsültasyon

Özel istek: Node.js uygulaması için GitHub Actions ile CI/CD pipeline. 
Docker containerization, automated testing ve AWS deployment.
```

#### Çıktı Örneği
```yaml
# .github/workflows/ci-cd.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    strategy:
      matrix:
        node-version: [16.x, 18.x]
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Node.js kurulumu ${{ matrix.node-version }}
      uses: actions/setup-node@v3
      with:
        node-version: ${{ matrix.node-version }}
        cache: 'npm'
    
    - name: Bağımlılıkları yükle
      run: npm ci
    
    - name: Testleri çalıştır
      run: npm run test:coverage
    
    - name: Linting kontrolü
      run: npm run lint
    
    - name: Type checking
      run: npm run type-check

  build:
    needs: test
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Docker image build
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest
    
    - name: Docker Hub'a push
      run: |
        echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
        docker push myapp:${{ github.sha }}
        docker push myapp:latest

  deploy:
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - name: AWS'ye deploy
      run: |
        # AWS deployment commands
        echo "Deploying to production..."
```

## 🔄 Workflow Örnekleri

### Tam Proje Geliştirme Süreci

```bash
# 1. Sistem başlat
python vibe_coding_ai_system.py

# 2. Yeni proje oluştur
Komut: 1
Proje: TaskManager
Tip: fullstack
Teknolojiler: Vue.js, Django, PostgreSQL

# 3. Otomatik geliştirme tamamlandıktan sonra özelleştirme
Komut: f  # Frontend uzmanı ile ek özellikler
Komut: b  # Backend uzmanı ile API iyileştirmeleri
Komut: d  # Database uzmanı ile performans optimizasyonu

# 4. Production hazırlığı
Komut: o  # DevOps uzmanı ile deployment
```

### Mevcut Proje Geliştirme

```bash
# 1. Mevcut projeyi yükle
Komut: 2
Proje: TaskManager

# 2. Belirli uzmanlarla çalış
Komut: u  # UI/UX iyileştirmeleri
Komut: m  # Mobile versiyon ekleme
```

## 💡 İpuçları ve Best Practices

### 1. Proje Tanımlama
- **Detaylı açıklama yazın**: Ne kadar detay verirseniz, o kadar iyi sonuç alırsınız
- **Hedef kitle belirtin**: Kullanıcı profilinizi net tanımlayın
- **Özellik listesi yapın**: Ana işlevleri öncelik sırasına göre listeleyin

### 2. Teknoloji Seçimi
- **Projenin ihtiyaçlarını düşünün**: Ölçeklenebilirlik, performans, geliştirme hızı
- **Ekip yetkinliklerini göz önünde bulundurun**: Bilinen teknolojileri tercih edin
- **Güncel teknolojileri seçin**: Long-term support olan çözümleri tercih edin

### 3. Uzman Modları
- **Spesifik istekler yapın**: Genel istekler yerine detaylı talepler
- **Örnek veriler sağlayın**: Sample data ile daha iyi sonuçlar alın
- **İteratif çalışın**: Bir uzmanın çıktısını diğerine input olarak verin

### 4. Kod Kalitesi
- **Test coverage'ı kontrol edin**: Minimum %80 test kapsamı hedefleyin
- **Code review yapın**: Üretilen kodları mutlaka gözden geçirin
- **Documentation okuyun**: Uzmanların oluşturduğu dokümantasyonu inceleyin

## 🔧 Troubleshooting

### Yaygın Sorunlar ve Çözümleri

#### Problem: API Timeout
```bash
# Çözüm: Retry mekanizması devrede, bekleyin
⏰ DeepSeek bağlantı zaman aşımı (1/3)
⏸️ Rate limit, bekleniyor... (2/3)
```

#### Problem: Eksik Dosyalar
```bash
# Çözüm: Uzmanı tekrar çalıştırın
Komut: b  # Backend uzmanını tekrar çalıştır
Özel istek: Eksik migration dosyalarını oluştur
```

#### Problem: Teknoloji Uyumsuzluğu
```bash
# Çözüm: Proje konfigürasyonunu güncelleyin
# project_config.json dosyasını düzenleyin
"tech_stack": ["React", "FastAPI", "PostgreSQL"]
```

## 📚 Daha Fazla Kaynak

- **VibeCoding Metodolojisi**: Clean Code prensipleri
- **Pydantic AI Dokümantasyonu**: Agent framework detayları
- **API Referansları**: DeepSeek ve Gemini API kullanımı
- **Best Practices**: Yazılım geliştirme standartları

---

**VibeCoding AI System ile profesyonel yazılımlar geliştirin! 🚀** 