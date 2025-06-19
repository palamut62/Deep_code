#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding AI System - Yazılım Geliştirme Ekosistemi
Pydantic AI ile güçlendirilmiş uzman AI ajanları kullanarak
tam kapsamlı yazılım projeleri oluşturur.
"""

import asyncio
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import json
import shutil

from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
from rich.syntax import Syntax
from dotenv import load_dotenv
import httpx

# Environment variables yükle
load_dotenv()

console = Console()

class ProjectConfig(BaseModel):
    """Proje konfigürasyon modeli"""
    name: str = Field(description="Proje adı")
    description: str = Field(description="Proje açıklaması")
    type: str = Field(description="Proje tipi (web, mobile, desktop, api)")
    tech_stack: List[str] = Field(description="Teknoloji yığını")
    features: List[str] = Field(description="Özellikler listesi")
    target_audience: str = Field(description="Hedef kitle")
    complexity: str = Field(description="Karmaşıklık seviyesi (basit, orta, karmaşık)")
    database_needed: bool = Field(description="Veritabanı gereksinimi")
    auth_needed: bool = Field(description="Kimlik doğrulama gereksinimi")
    api_needed: bool = Field(description="API gereksinimi")

class FileStructure(BaseModel):
    """Dosya yapısı modeli"""
    path: str = Field(description="Dosya yolu")
    content: str = Field(description="Dosya içeriği")
    file_type: str = Field(description="Dosya tipi")
    description: str = Field(description="Dosya açıklaması")

class ExpertResponse(BaseModel):
    """Uzman yanıt modeli"""
    expert_type: str = Field(description="Uzman tipi")
    analysis: str = Field(description="Analiz")
    recommendations: List[str] = Field(description="Öneriler")
    code_files: List[FileStructure] = Field(description="Kod dosyaları")
    dependencies: List[str] = Field(description="Bağımlılıklar")
    next_steps: List[str] = Field(description="Sonraki adımlar")

class VibeCodingAISystem:
    """VibeCoding AI Sistemi Ana Sınıfı"""
    
    def __init__(self):
        self.console = Console()
        self.api_key = None
        self.model = None
        self.experts = {}
        self.current_project = None
        self.output_dir = Path("generated_projects")
        self.output_dir.mkdir(exist_ok=True)
        
        # API anahtarını yükle
        self._load_api_key()
        self._initialize_experts()
    
    def _load_api_key(self):
        """API anahtarını yükle"""
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if deepseek_key:
            self.api_key = deepseek_key
            self.model_type = "deepseek"
        elif gemini_key:
            self.api_key = gemini_key
            self.model_type = "gemini"
        else:
            self.console.print("[red]❌ API anahtarı bulunamadı! Lütfen .env dosyasını kontrol edin.[/red]")
            sys.exit(1)
    
    def _initialize_experts(self):
        """Uzman AI ajanlarını başlat"""
        
        # Backend Uzmanı
        self.experts['backend'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir Backend Geliştirme Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Güçlü ve ölçeklenebilir backend mimarileri tasarla
            - RESTful API'ler ve GraphQL endpoint'leri oluştur
            - Veritabanı şemaları ve ORM modelleri tasarla
            - Güvenlik, performans ve best practice'leri uygula
            - Mikroservis mimarileri öner
            
            💡 VibeCoding Yaklaşımı:
            - Kod kalitesi ve sürdürülebilirlik odaklı
            - Test-driven development (TDD)
            - Clean Architecture prensiplerine uygun
            - SOLID prensiplerine bağlı
            - Async/await pattern'leri kullan
            
            🛠️ Teknolojiler:
            Python (FastAPI, Django, Flask), Node.js (Express, NestJS), 
            Java (Spring Boot), C# (.NET Core), Go, Rust
            
            📋 Çıktın:
            - Detaylı kod dosyaları
            - API dokümantasyonu
            - Veritabanı migration'ları
            - Docker konfigürasyonları
            - Test dosyaları
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # Frontend Uzmanı
        self.experts['frontend'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir Frontend Geliştirme Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Modern, responsive ve kullanıcı dostu arayüzler tasarla
            - Component-based mimarileri uygula
            - State management çözümleri öner
            - Performance optimizasyonu yap
            - Accessibility (a11y) standartlarını uygula
            
            💡 VibeCoding Yaklaşımı:
            - Mobile-first design
            - Progressive Web App (PWA) özellikleri
            - Modern CSS (Grid, Flexbox, CSS Variables)
            - TypeScript kullanımı
            - Component testing
            
            🛠️ Teknolojiler:
            React, Vue.js, Angular, Svelte, Next.js, Nuxt.js,
            Tailwind CSS, Styled Components, SASS/SCSS
            
            📋 Çıktın:
            - Component dosyaları
            - Styling dosyaları
            - Routing konfigürasyonları
            - State management setup
            - Test dosyaları
            - Build konfigürasyonları
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # Database Uzmanı
        self.experts['database'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir Veritabanı Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Optimal veritabanı şemaları tasarla
            - İndexleme stratejileri öner
            - Migration dosyaları oluştur
            - Query optimizasyonu yap
            - Backup ve recovery planları hazırla
            
            💡 VibeCoding Yaklaşımı:
            - Normalizasyon vs denormalizasyon dengesini kur
            - ACID özelliklerini koru
            - Scalability için sharding stratejileri
            - Data integrity constraints
            - Performance monitoring
            
            🛠️ Teknolojiler:
            PostgreSQL, MySQL, MongoDB, Redis, SQLite,
            SQLAlchemy, Prisma, TypeORM, Mongoose
            
            📋 Çıktın:
            - Schema dosyaları
            - Migration scripts
            - Seed data
            - İndex tanımları
            - Stored procedures
            - Database konfigürasyonları
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # UI/UX Uzmanı
        self.experts['uiux'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir UI/UX Tasarım Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Kullanıcı deneyimi odaklı tasarımlar oluştur
            - Design system ve component library tasarla
            - Wireframe ve prototype'lar hazırla
            - Usability testing önerileri sun
            - Accessibility guidelines uygula
            
            💡 VibeCoding Yaklaşımı:
            - User-centered design
            - Design thinking metodolojisi
            - Atomic design principles
            - Responsive design patterns
            - Microinteractions
            
            🛠️ Teknolojiler:
            Figma, Sketch, Adobe XD, InVision,
            Storybook, Chromatic, Design Tokens
            
            📋 Çıktın:
            - Design system dosyaları
            - Component specifications
            - Style guide
            - Interaction patterns
            - Accessibility checklist
            - Usability test scenarios
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # DevOps Uzmanı
        self.experts['devops'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir DevOps Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - CI/CD pipeline'ları tasarla
            - Konteynerizasyon stratejileri oluştur
            - Infrastructure as Code (IaC) uygula
            - Monitoring ve logging sistemleri kur
            - Security best practices uygula
            
            💡 VibeCoding Yaklaşımı:
            - GitOps workflow
            - Blue-green deployment
            - Automated testing integration
            - Infrastructure monitoring
            - Security scanning
            
            🛠️ Teknolojiler:
            Docker, Kubernetes, Jenkins, GitHub Actions,
            Terraform, Ansible, Prometheus, Grafana
            
            📋 Çıktın:
            - Dockerfile'lar
            - Kubernetes manifests
            - CI/CD konfigürasyonları
            - Infrastructure scripts
            - Monitoring konfigürasyonları
            - Security policies
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # Mobile Uzmanı
        self.experts['mobile'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir Mobile Geliştirme Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Cross-platform mobile uygulamaları tasarla
            - Native performance optimizasyonu yap
            - Mobile-specific UX patterns uygula
            - Offline-first yaklaşımlar öner
            - App store optimizasyonu yap
            
            💡 VibeCoding Yaklaşımı:
            - Progressive Web Apps (PWA)
            - Responsive design principles
            - Touch-first interactions
            - Battery optimization
            - Network efficiency
            
            🛠️ Teknolojiler:
            React Native, Flutter, Ionic, Xamarin,
            Swift (iOS), Kotlin (Android), Capacitor
            
            📋 Çıktın:
            - Mobile app components
            - Navigation setup
            - State management
            - Native module integrations
            - Build configurations
            - App store assets
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            """
        )
        
        # Test Uzmanı
        self.experts['test'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen bir Test Uzmanısın ve Kalite Güvence (QA) Uzmanısın. VibeCoding metodolojisini kullanarak:
            
            🎯 GÖREVIN:
            - Kapsamlı test stratejileri oluştur
            - Unit, Integration ve E2E testleri tasarla
            - Code coverage analizi yap
            - Performance ve load testleri planla
            - Bug tracking ve quality assurance süreçleri kur
            - Test automation framework'leri öner
            
            💡 VibeCoding Yaklaşımı:
            - Test-Driven Development (TDD)
            - Behavior-Driven Development (BDD)
            - Continuous Testing (CT)
            - Risk-based testing
            - Shift-left testing strategy
            - Quality gates implementation
            
            🛠️ Test Teknolojileri:
            
            **Backend Testing:**
            - Python: pytest, unittest, coverage.py
            - Node.js: Jest, Mocha, Chai, Supertest
            - Java: JUnit, TestNG, Mockito
            - C#: NUnit, xUnit, MSTest
            
            **Frontend Testing:**
            - Jest, React Testing Library, Enzyme
            - Cypress, Playwright, Selenium
            - Storybook, Chromatic
            - Lighthouse, WebPageTest
            
            **API Testing:**
            - Postman, Newman
            - RestAssured, Karate
            - Insomnia, Thunder Client
            
            **Performance Testing:**
            - JMeter, K6, Artillery
            - LoadRunner, Gatling
            
            **Security Testing:**
            - OWASP ZAP, Burp Suite
            - SonarQube, CodeQL
            
            📋 Çıktın:
            - Test plan dosyaları
            - Unit test dosyaları
            - Integration test suites
            - E2E test scenarios
            - Performance test scripts
            - Security test cases
            - CI/CD test pipeline konfigürasyonları
            - Test coverage raporları
            - Quality metrics dashboard
            - Bug report templates
            - Test automation scripts
            
            🔍 Analiz Yeteneklerin:
            - Mevcut kodları analiz et
            - Test coverage eksikliklerini tespit et
            - Code quality metrics hesapla
            - Potential bug'ları öngör
            - Performance bottleneck'leri belirle
            - Security vulnerability'leri tespit et
            - Best practice violations'ları bul
            - Refactoring önerileri sun
            
            📊 Raporlama:
            - Detaylı test raporu oluştur
            - Code quality scorecard hazırla
            - Risk assessment matrix
            - Test execution summary
            - Defect density analysis
            - Performance benchmark results
            
            Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
            Tüm kodları titizlikle analiz et ve eksiklikleri detaylandır.
            """
        )
        
        # Akıllı Proje Analizci
        self.experts['smart_analyzer'] = Agent(
            model=self._get_model(),
            result_type=ExpertResponse,
            system_prompt="""
            Sen VibeCoding Akıllı Proje Analizci'sin. Tek bir kullanıcı isteğini alıp, minimum sorularla netleştirerek otomatik teknoloji seçimi yapan ve hazır çözüm üreten bir uzmansın.
            
            🎯 GÖREVIN:
            
            1. 🔍 İSTEK ANALİZİ:
               - Kullanıcının doğal dil isteğini detaylı analiz et
               - Proje türünü, kapsamını ve hedefleri belirle
               - Teknik gereksinimleri çıkar
               - Kullanıcı kitlesini ve kullanım senaryolarını tahmin et
               
            2. 🤔 MİNİMUM SORU STRATEJİSİ:
               - Sadece kritik belirsizlikleri netleştir
               - En fazla 2-3 temel soru sor
               - Gereksiz detay sorularından kaçın
               - Hızlı netleştirme odaklı yaklaşım
               
            3. 🛠️ OTOMATİK TEKNOLOJİ SEÇİMİ:
               - En uygun programlama dilini seç
               - Optimal veritabanını belirle
               - Framework ve kütüphaneleri seç
               - AI/LLM modelini öner (OpenAI, Gemini, Claude)
               - Cloud platformunu belirle
               - Development tools'ları seç
               
            4. 📋 ÇÖZÜM TASLAĞI:
               - Detaylı proje planı hazırla
               - Dosya yapısını oluştur
               - Teknoloji yığını açıkla
               - Implementation roadmap'i çiz
               - Zaman tahmini yap
               
            💡 TEKNOLOJİ SEÇİM KRİTERLERİN:
            
            **Programlama Dilleri:**
            - Python: AI/ML, Data Science, Backend API
            - JavaScript/TypeScript: Web Frontend, Full-stack
            - Java: Enterprise, Android, Büyük ölçekli sistemler
            - C#: Windows, Enterprise, Game Development
            - Go: Mikroservisler, Cloud-native, Performance
            - Rust: System programming, WebAssembly
            - Swift: iOS, macOS uygulamaları
            - Kotlin: Android, Cross-platform
            
            **Frontend Frameworks:**
            - React: Popüler, büyük ekosistem
            - Vue.js: Öğrenmesi kolay, performanslı
            - Angular: Enterprise, büyük projeler
            - Svelte: Performans odaklı, modern
            - Next.js: React-based, SSR/SSG
            
            **Backend Frameworks:**
            - FastAPI: Python, modern, hızlı
            - Django: Python, full-featured
            - Express.js: Node.js, minimal
            - NestJS: Node.js, enterprise
            - Spring Boot: Java, enterprise
            - ASP.NET Core: C#, cross-platform
            
            **Veritabanları:**
            - PostgreSQL: Güçlü, ölçeklenebilir
            - MySQL: Popüler, kolay
            - MongoDB: NoSQL, esnek
            - Redis: Cache, session store
            - SQLite: Küçük projeler
            
            **AI/LLM Modelleri:**
            - OpenAI GPT-4: Genel amaçlı, güçlü
            - Google Gemini: Multimodal, hızlı
            - Claude: Uzun context, analitik
            - Local models: Gizlilik, maliyet
            
                         🎯 ÇIKTI FORMATI:
             
             Şu yapıda yanıt ver:
             
             **analysis**: İsteğin detaylı analizi ve proje gereksinimlerinin özeti
             **recommendations**: 2-3 kritik netleştirme sorusu (soru formatında)
             **dependencies**: Seçilen teknolojiler listesi
             **code_files**: Temel kod dosyaları (varsa)
             **next_steps**: Uygulanabilir adım adım plan
             
             ÖNEMLİ KURALLAR:
             - analysis bölümünde projeyi detaylı analiz et
             - recommendations'da sadece kritik belirsizlikleri soru olarak sor
             - dependencies'de seçilen teknolojileri listele
             - code_files'da temel dosya yapısını oluştur (isteğe bağlı)
             - next_steps'de implementasyon adımlarını ver
             
             Her zaman Türkçe yanıt ver ve VibeCoding prensiplerini uygula.
             Hızlı, etkili ve uygulanabilir çözümler sun.
            """
        )
    
    def _get_model(self):
        """Model string'ini döndür"""
        if self.model_type == "deepseek":
            # DeepSeek için OpenAI compatible API kullan
            os.environ["OPENAI_API_KEY"] = self.api_key
            os.environ["OPENAI_BASE_URL"] = "https://api.deepseek.com"
            return "openai:deepseek-chat"
        else:
            # Gemini için API key'i environment'a set et
            os.environ["GEMINI_API_KEY"] = self.api_key
            return "gemini-1.5-flash"
    
    def display_welcome(self):
        """Hoş geldin ekranını göster"""
        # Terminal temizle
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Basit ve temiz hoş geldin mesajı
        self.console.print("\n")
        self.console.print("="*80, style="blue")
        self.console.print("🚀 VibeCoding AI System - Yazılım Geliştirme Ekosistemi", style="bold blue", justify="center")
        self.console.print("="*80, style="blue")
        self.console.print("\n")
        
        self.console.print("👨‍💻 [bold]Uzman Ekibiniz:[/bold]")
        self.console.print("   • Backend Uzmanı: API, veritabanı ve sunucu mimarisi")
        self.console.print("   • Frontend Uzmanı: Modern kullanıcı arayüzleri")
        self.console.print("   • Database Uzmanı: Veri modelleme ve optimizasyon")
        self.console.print("   • UI/UX Uzmanı: Kullanıcı deneyimi tasarımı")
        self.console.print("   • DevOps Uzmanı: Deployment ve altyapı")
        self.console.print("   • Mobile Uzmanı: Mobil uygulama geliştirme")
        self.console.print("   • Test Uzmanı: Kod analizi, test stratejileri ve kalite güvence")
        
        self.console.print("\n🎯 [bold]VibeCoding Metodolojisi:[/bold]")
        self.console.print("   • Kaliteli kod üretir")
        self.console.print("   • Best practices uygular")
        self.console.print("   • Sürdürülebilir çözümler sunar")
        self.console.print("   • Test-driven yaklaşım benimser")
        
        self.console.print("\n🧠 [bold]Akıllı Proje Analizi:[/bold]")
        self.console.print("   • Tek girdi ile otomatik çözüm üretimi")
        self.console.print("   • Minimum soru ile hızlı netleştirme")
        self.console.print("   • Otomatik teknoloji seçimi")
        self.console.print("   • Doğrudan uygulanabilir kod taslakları")
        self.console.print("\n")
    
    def display_main_menu(self):
        """Ana menüyü göster"""
        self.console.print("-"*80, style="cyan")
        self.console.print("🎯 ANA MENÜ", style="bold cyan", justify="center")
        self.console.print("-"*80, style="cyan")
        
        # Ana Özellikler
        self.console.print("\n[bold yellow]📋 PROJE YÖNETİMİ:[/bold yellow]")
        self.console.print("  [cyan]1[/cyan] - 🚀 Yeni Proje Oluştur")
        self.console.print("  [cyan]2[/cyan] - 📂 Mevcut Proje Yükle")
        self.console.print("  [cyan]3[/cyan] - 🔧 Proje Geliştir")
        self.console.print("  [cyan]4[/cyan] - 📋 Proje Listesi")
        self.console.print("  [cyan]5[/cyan] - 🧠 Akıllı Proje Analizi")
        
        # Uzman Modları
        self.console.print("\n[bold yellow]👨‍💻 UZMAN MODLARI:[/bold yellow]")
        self.console.print("  [cyan]b[/cyan] - 🔧 Backend Uzmanı")
        self.console.print("  [cyan]f[/cyan] - 🎨 Frontend Uzmanı")
        self.console.print("  [cyan]d[/cyan] - 🗄️ Database Uzmanı")
        self.console.print("  [cyan]u[/cyan] - ✨ UI/UX Uzmanı")
        self.console.print("  [cyan]o[/cyan] - ⚙️ DevOps Uzmanı")
        self.console.print("  [cyan]m[/cyan] - 📱 Mobile Uzmanı")
        self.console.print("  [cyan]t[/cyan] - 🧪 Test Uzmanı")
        
        # Sistem
        self.console.print("\n[bold yellow]⚙️ SİSTEM:[/bold yellow]")
        self.console.print("  [cyan]h[/cyan] - ❓ Yardım")
        self.console.print("  [cyan]q[/cyan] - 🚪 Çıkış")
        
        self.console.print("\n" + "-"*80, style="cyan")
    
    async def create_new_project(self):
        """Yeni proje oluştur"""
        self.console.print("\n[bold blue]🚀 Yeni Proje Oluşturma[/bold blue]\n")
        
        # Proje bilgilerini al
        project_name = Prompt.ask("📝 Proje adı")
        project_description = Prompt.ask("📄 Proje açıklaması")
        
        # Proje tipi seçimi
        project_types = {
            "1": "web",
            "2": "mobile", 
            "3": "desktop",
            "4": "api",
            "5": "fullstack"
        }
        
        self.console.print("\n[bold]Proje Tipi:[/bold]")
        for key, value in project_types.items():
            self.console.print(f"{key}. {value.title()}")
        
        project_type_choice = Prompt.ask("Proje tipi seçin", choices=list(project_types.keys()))
        project_type = project_types[project_type_choice]
        
        # Teknoloji yığını
        tech_suggestions = {
            "web": ["React", "Vue.js", "Angular", "Next.js", "Nuxt.js"],
            "mobile": ["React Native", "Flutter", "Ionic", "Xamarin"],
            "desktop": ["Electron", "Tauri", "PyQt", "Tkinter"],
            "api": ["FastAPI", "Django REST", "Express.js", "Spring Boot"],
            "fullstack": ["MERN", "MEAN", "Django+React", "Laravel+Vue"]
        }
        
        suggested_techs = tech_suggestions.get(project_type, [])
        self.console.print(f"\n[bold]Önerilen teknolojiler ({project_type}):[/bold]")
        for i, tech in enumerate(suggested_techs, 1):
            self.console.print(f"{i}. {tech}")
        
        tech_stack = Prompt.ask("Teknoloji yığını (virgülle ayırın)").split(",")
        tech_stack = [tech.strip() for tech in tech_stack]
        
        # Özellikler
        features = Prompt.ask("Ana özellikler (virgülle ayırın)").split(",")
        features = [feature.strip() for feature in features]
        
        # Diğer bilgiler
        target_audience = Prompt.ask("Hedef kitle")
        complexity = Prompt.ask("Karmaşıklık seviyesi", choices=["basit", "orta", "karmaşık"])
        database_needed = Confirm.ask("Veritabanı gerekli mi?")
        auth_needed = Confirm.ask("Kimlik doğrulama gerekli mi?")
        api_needed = Confirm.ask("API gerekli mi?")
        
        # Proje konfigürasyonu oluştur
        project_config = ProjectConfig(
            name=project_name,
            description=project_description,
            type=project_type,
            tech_stack=tech_stack,
            features=features,
            target_audience=target_audience,
            complexity=complexity,
            database_needed=database_needed,
            auth_needed=auth_needed,
            api_needed=api_needed
        )
        
        self.current_project = project_config
        
        # Proje dizini oluştur
        project_dir = self.output_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Konfigürasyonu kaydet
        config_file = project_dir / "project_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(project_config.model_dump(), f, ensure_ascii=False, indent=2)
        
        self.console.print(f"\n[green]✅ Proje '{project_name}' oluşturuldu![/green]")
        self.console.print(f"📁 Proje dizini: {project_dir}")
        
        # Otomatik geliştirme başlat
        if Confirm.ask("\n🚀 Hemen geliştirmeye başlamak ister misiniz?"):
            await self.develop_project()
    
    async def develop_project(self):
        """Projeyi geliştir"""
        if not self.current_project:
            self.console.print("[red]❌ Aktif proje bulunamadı! Önce bir proje oluşturun veya yükleyin.[/red]")
            return
        
        self.console.print(f"\n[bold blue]🔧 '{self.current_project.name}' Projesi Geliştiriliyor[/bold blue]\n")
        
        # Gerekli uzmanları belirle
        required_experts = self._determine_required_experts(self.current_project)
        
        self.console.print("[bold]Çalışacak uzmanlar:[/bold]")
        for expert in required_experts:
            self.console.print(f"👨‍💻 {expert.title()} Uzmanı")
        
        # Her uzmanla çalış
        project_dir = self.output_dir / self.current_project.name
        all_responses = {}
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            for expert_type in required_experts:
                task = progress.add_task(f"🤖 {expert_type.title()} uzmanıyla çalışılıyor...", total=None)
                
                try:
                    expert_response = await self._consult_expert(expert_type, self.current_project)
                    all_responses[expert_type] = expert_response
                    
                    # Dosyaları oluştur
                    expert_dir = project_dir / expert_type
                    expert_dir.mkdir(exist_ok=True)
                    
                    for file_struct in expert_response.code_files:
                        file_path = expert_dir / file_struct.path
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(file_struct.content)
                    
                    progress.update(task, description=f"✅ {expert_type.title()} uzmanı tamamlandı")
                    
                except Exception as e:
                    progress.update(task, description=f"❌ {expert_type.title()} uzmanında hata: {str(e)}")
                    self.console.print(f"[red]Hata ({expert_type}): {str(e)}[/red]")
        
        # Sonuçları göster
        await self._display_project_results(all_responses)
        
        # Proje özetini kaydet
        summary_file = project_dir / "project_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump({
                "project": self.current_project.model_dump(),
                "experts": {k: v.model_dump() for k, v in all_responses.items()},
                "generated_at": datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
        
        self.console.print(f"\n[green]🎉 Proje başarıyla oluşturuldu![/green]")
        self.console.print(f"📁 Proje dizini: {project_dir}")
    
    async def smart_project_analysis(self):
        """Akıllı proje analizi - tek girdi ile otomatik çözüm"""
        self.console.print("\n[bold blue]🧠 Akıllı Proje Analizi[/bold blue]")
        self.console.print("[dim]Tek bir istekle otomatik teknoloji seçimi ve çözüm üretimi[/dim]\n")
        
        # Kullanıcının doğal dil isteğini al
        user_request = Prompt.ask("💭 Projenizi doğal dilde anlatın (ne yapmak istiyorsunuz?)")
        
        if not user_request.strip():
            self.console.print("[red]❌ Lütfen bir proje isteği girin.[/red]")
            return
        
        response = None
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🧠 Akıllı analiz yapılıyor...", total=None)
            
            try:
                # Akıllı analizci ile konsültasyon
                smart_prompt = f"""
                Kullanıcı İsteği: "{user_request}"
                
                Bu isteği VibeCoding Akıllı Proje Analizci olarak analiz et:
                
                1. İsteği detaylı analiz et ve proje gereksinimlerini çıkar
                2. Sadece kritik belirsizlikleri netleştirmek için minimum soru sor
                3. En uygun teknoloji yığınını otomatik seç
                4. Uygulanabilir çözüm taslağı hazırla
                5. Temel kod dosyalarını oluştur
                
                Hızlı, etkili ve doğrudan uygulanabilir bir çözüm sun.
                """
                
                smart_expert = self.experts['smart_analyzer']
                result = await smart_expert.run(smart_prompt)
                response = result.data
                
                progress.update(task, description="✅ Analiz tamamlandı")
                
            except Exception as e:
                progress.update(task, description=f"❌ Hata oluştu: {str(e)}")
                self.console.print(f"[red]❌ Hata: {str(e)}[/red]")
                return
        
        # Progress bar bittikten sonra devam et
        if response:
            # Sonuçları göster
            await self._display_smart_analysis_results(response, user_request)
            
            # Netleştirme sorularını sor
            await self._ask_clarification_questions(response, user_request)
            
            # Proje oluşturma seçeneği sun
            if Confirm.ask("\n🚀 Bu analiz sonucuna göre proje oluşturmak ister misiniz?"):
                await self._create_project_from_analysis(response, user_request)
    
    async def _display_smart_analysis_results(self, response: ExpertResponse, user_request: str):
        """Akıllı analiz sonuçlarını göster"""
        self.console.print("\n" + "="*80, style="green")
        self.console.print("🧠 Akıllı Proje Analizi Sonuçları", style="bold green", justify="center")
        self.console.print("="*80, style="green")
        
        # Kullanıcı isteği
        self.console.print(f"\n[bold yellow]💭 İSTEĞİNİZ:[/bold yellow]")
        self.console.print(f'"{user_request}"')
        
        # Analiz sonuçları
        self.console.print(f"\n[bold yellow]🔍 PROJE ANALİZİ:[/bold yellow]")
        self.console.print(response.analysis)
        
        # Öneriler (netleştirme soruları olarak)
        if response.recommendations:
            self.console.print(f"\n[bold yellow]🤔 NETLEŞTİRME SORULARI:[/bold yellow]")
            for i, rec in enumerate(response.recommendations, 1):
                self.console.print(f"  {i}. {rec}")
        
        # Bağımlılıklar (teknoloji seçimi olarak)
        if response.dependencies:
            self.console.print(f"\n[bold yellow]🛠️ SEÇİLEN TEKNOLOJİLER:[/bold yellow]")
            for dep in response.dependencies:
                self.console.print(f"  • {dep}")
        
        # Kod dosyaları
        if response.code_files:
            self.console.print(f"\n[bold yellow]📁 OLUŞTURULACAK DOSYALAR:[/bold yellow]")
            for file_struct in response.code_files:
                self.console.print(f"  📄 {file_struct.path} ({file_struct.file_type})")
                self.console.print(f"      {file_struct.description}")
        
        # Sonraki adımlar
        if response.next_steps:
            self.console.print(f"\n[bold yellow]➡️ UYGULAMA PLANI:[/bold yellow]")
            for i, step in enumerate(response.next_steps, 1):
                self.console.print(f"  {i}. {step}")
        
        self.console.print("\n" + "="*80, style="green")
    
    async def _ask_clarification_questions(self, response: ExpertResponse, user_request: str):
        """Netleştirme sorularını sor ve kullanıcı yanıtlarını al"""
        if not response.recommendations:
            return
        
        self.console.print("\n[bold blue]🤔 Netleştirme Soruları[/bold blue]")
        self.console.print("[dim]Projenizi daha iyi anlayabilmek için birkaç soru soracağım:[/dim]\n")
        
        clarifications = {}
        
        for i, question in enumerate(response.recommendations, 1):
            # Her soruyu temizle ve kullanıcı dostu hale getir
            clean_question = question.replace("**", "").replace("*", "").strip()
            if not clean_question.endswith("?"):
                clean_question += "?"
            
            self.console.print(f"[yellow]{i}. {clean_question}[/yellow]")
            answer = Prompt.ask("   Yanıtınız", default="Varsayılan")
            
            # Kullanıcının yanıtını göster
            self.console.print(f"   [green]→ {answer}[/green]")
            
            clarifications[f"soru_{i}"] = {
                "question": clean_question,
                "answer": answer
            }
            self.console.print()
        
        # Yanıtları response'a ekle (ek bilgi olarak)
        if hasattr(response, 'clarifications'):
            response.clarifications = clarifications
        else:
            # Eğer model bu alanı desteklemiyorsa, next_steps'e ekle
            clarification_summary = "\n\nKullanıcı Yanıtları:\n"
            for key, value in clarifications.items():
                clarification_summary += f"- {value['question']} → {value['answer']}\n"
            
            if response.next_steps:
                response.next_steps.append(f"Kullanıcı yanıtları dikkate alınarak geliştirme yapılacak: {clarification_summary}")
            else:
                response.next_steps = [f"Kullanıcı yanıtları dikkate alınarak geliştirme yapılacak: {clarification_summary}"]
        
        self.console.print("[green]✅ Teşekkürler! Yanıtlarınız kaydedildi.[/green]")
        
        # Kaydedilen yanıtları özetle
        self._display_saved_answers(clarifications)
    
    def _display_saved_answers(self, clarifications: dict):
        """Kaydedilen yanıtları göster"""
        self.console.print("\n[bold blue]💾 Kaydedilen Yanıtlarınız:[/bold blue]")
        for key, value in clarifications.items():
            self.console.print(f"[cyan]❓ {value['question']}[/cyan]")
            self.console.print(f"[green]✓ {value['answer']}[/green]")
            self.console.print()
    
    async def _create_project_from_analysis(self, response: ExpertResponse, user_request: str):
        """Analiz sonucundan proje oluştur"""
        # Proje adı öner
        suggested_name = user_request.split()[0:3]  # İlk 3 kelime
        suggested_name = "_".join([word.lower().replace(",", "").replace(".", "") for word in suggested_name])
        
        project_name = Prompt.ask("📝 Proje adı", default=suggested_name)
        
        # Teknoloji yığınını çıkar
        tech_stack = []
        for dep in response.dependencies:
            # Bağımlılıklardan teknolojileri çıkar
            if any(tech in dep.lower() for tech in ['react', 'vue', 'angular', 'next']):
                tech_stack.append('Frontend Framework')
            elif any(tech in dep.lower() for tech in ['python', 'node', 'java', 'c#']):
                tech_stack.append('Backend')
            elif any(tech in dep.lower() for tech in ['postgresql', 'mysql', 'mongodb']):
                tech_stack.append('Database')
        
        if not tech_stack:
            tech_stack = ['Web Application']
        
        # Proje konfigürasyonu oluştur
        project_config = ProjectConfig(
            name=project_name,
            description=user_request,
            type="web",  # Default olarak web
            tech_stack=response.dependencies if response.dependencies else tech_stack,
            features=response.recommendations if response.recommendations else ["Temel Özellikler"],
            target_audience="Genel Kullanıcılar",
            complexity="orta",
            database_needed=any("database" in dep.lower() or "sql" in dep.lower() for dep in response.dependencies),
            auth_needed=any("auth" in rec.lower() or "login" in rec.lower() for rec in response.recommendations),
            api_needed=any("api" in dep.lower() for dep in response.dependencies)
        )
        
        self.current_project = project_config
        
        # Proje dizini oluştur
        project_dir = self.output_dir / project_name
        project_dir.mkdir(exist_ok=True)
        
        # Akıllı analiz dosyalarını kaydet
        smart_dir = project_dir / "smart_analysis"
        smart_dir.mkdir(exist_ok=True)
        
        # Analiz dosyalarını kaydet (varsa)
        if response.code_files:
            for file_struct in response.code_files:
                file_path = smart_dir / file_struct.path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_struct.content)
        else:
            # Kod dosyası yoksa temel bir README oluştur
            readme_file = smart_dir / "README.md"
            with open(readme_file, "w", encoding="utf-8") as f:
                f.write(f"# {project_name}\n\n")
                f.write(f"## Proje Açıklaması\n{user_request}\n\n")
                f.write("## Analiz Sonuçları\n")
                f.write(f"{response.analysis}\n\n")
                f.write("## Teknolojiler\n")
                for dep in response.dependencies:
                    f.write(f"- {dep}\n")
                f.write("\n## Sonraki Adımlar\n")
                for step in response.next_steps:
                    f.write(f"- {step}\n")
        
        # Analiz raporunu kaydet
        analysis_report = smart_dir / "analysis_report.md"
        with open(analysis_report, "w", encoding="utf-8") as f:
            f.write(f"# Akıllı Proje Analizi - {project_name}\n\n")
            f.write(f"## Kullanıcı İsteği\n{user_request}\n\n")
            f.write(f"## Analiz\n{response.analysis}\n\n")
            f.write(f"## Seçilen Teknolojiler\n")
            for dep in response.dependencies:
                f.write(f"- {dep}\n")
            f.write(f"\n## Uygulama Planı\n")
            for step in response.next_steps:
                f.write(f"- {step}\n")
        
        # Konfigürasyonu kaydet
        config_file = project_dir / "project_config.json"
        with open(config_file, "w", encoding="utf-8") as f:
            json.dump(project_config.model_dump(), f, ensure_ascii=False, indent=2)
        
        self.console.print(f"\n[green]✅ Proje '{project_name}' akıllı analiz ile oluşturuldu![/green]")
        self.console.print(f"📁 Proje dizini: {project_dir}")
        self.console.print(f"🧠 Analiz dosyaları: {smart_dir}")
        
        # Otomatik geliştirme seçeneği
        if Confirm.ask("\n🚀 Hemen diğer uzmanlarla geliştirmeye başlamak ister misiniz?"):
            await self.develop_project()
    
    def _determine_required_experts(self, project: ProjectConfig) -> List[str]:
        """Proje için gerekli uzmanları belirle"""
        experts = []
        
        # Proje tipine göre uzmanları belirle
        if project.type in ["web", "fullstack"]:
            experts.extend(["frontend", "backend"])
        elif project.type == "mobile":
            experts.append("mobile")
        elif project.type == "api":
            experts.append("backend")
        elif project.type == "desktop":
            experts.append("frontend")
        
        # Veritabanı gerekirse database uzmanı ekle
        if project.database_needed:
            experts.append("database")
        
        # Her projede UI/UX, DevOps ve Test uzmanları çalışsın
        experts.extend(["uiux", "devops", "test"])
        
        return list(set(experts))  # Tekrarları kaldır
    
    async def _consult_expert(self, expert_type: str, project: ProjectConfig) -> ExpertResponse:
        """Uzmanla konsültasyon yap"""
        expert = self.experts[expert_type]
        
        # Uzman için özel prompt oluştur
        expert_prompt = self._create_expert_prompt(expert_type, project)
        
        # Uzmanla konuş
        result = await expert.run(expert_prompt)
        return result.data
    
    def _create_expert_prompt(self, expert_type: str, project: ProjectConfig) -> str:
        """Uzman için özel prompt oluştur"""
        base_prompt = f"""
        VibeCoding metodolojisini kullanarak '{project.name}' projesi için {expert_type} geliştirmesi yap.
        
        PROJE BİLGİLERİ:
        - İsim: {project.name}
        - Açıklama: {project.description}
        - Tip: {project.type}
        - Teknoloji Yığını: {', '.join(project.tech_stack)}
        - Özellikler: {', '.join(project.features)}
        - Hedef Kitle: {project.target_audience}
        - Karmaşıklık: {project.complexity}
        - Veritabanı: {'Evet' if project.database_needed else 'Hayır'}
        - Kimlik Doğrulama: {'Evet' if project.auth_needed else 'Hayır'}
        - API: {'Evet' if project.api_needed else 'Hayır'}
        
        GÖREVLER:
        1. Proje analizi yap
        2. {expert_type.title()} önerileri sun
        3. Gerekli kod dosyalarını oluştur
        4. Bağımlılıkları listele
        5. Sonraki adımları belirle
        
        VibeCoding prensiplerini uygula:
        - Temiz ve sürdürülebilir kod
        - Best practices
        - Test edilebilir yapı
        - Dokümantasyon
        - Performance odaklı
        
        Detaylı ve uygulanabilir çözümler sun.
        """
        
        return base_prompt
    
    async def _display_project_results(self, responses: Dict[str, ExpertResponse]):
        """Proje sonuçlarını göster"""
        self.console.print("\n[bold blue]📋 Proje Geliştirme Sonuçları[/bold blue]\n")
        
        for expert_type, response in responses.items():
            # Uzman paneli
            panel_content = f"""
**🔍 Analiz:**
{response.analysis}

**💡 Öneriler:**
{chr(10).join(f'• {rec}' for rec in response.recommendations)}

**📁 Oluşturulan Dosyalar:**
{chr(10).join(f'• {file.path} ({file.file_type})' for file in response.code_files)}

**📦 Bağımlılıklar:**
{chr(10).join(f'• {dep}' for dep in response.dependencies)}

**➡️ Sonraki Adımlar:**
{chr(10).join(f'• {step}' for step in response.next_steps)}
            """
            
            panel = Panel(
                Markdown(panel_content),
                title=f"[bold green]👨‍💻 {expert_type.title()} Uzmanı[/bold green]",
                border_style="green",
                padding=(1, 2)
            )
            
            self.console.print(panel)
    
    def list_projects(self):
        """Projeleri listele"""
        self.console.print("\n" + "="*80, style="cyan")
        self.console.print("📂 Mevcut Projeler", style="bold cyan", justify="center")
        self.console.print("="*80, style="cyan")
        
        projects = []
        for project_dir in self.output_dir.iterdir():
            if project_dir.is_dir():
                config_file = project_dir / "project_config.json"
                if config_file.exists():
                    try:
                        with open(config_file, "r", encoding="utf-8") as f:
                            config = json.load(f)
                        projects.append((project_dir.name, config))
                    except:
                        continue
        
        if not projects:
            self.console.print("\n[yellow]📭 Henüz proje oluşturulmamış.[/yellow]")
            self.console.print("-"*80, style="cyan")
            return
        
        self.console.print()
        for i, (project_name, config) in enumerate(projects, 1):
            self.console.print(f"[bold cyan]{i}. {project_name}[/bold cyan]")
            self.console.print(f"   📁 Tip: [green]{config.get('type', 'N/A')}[/green]")
            
            description = config.get('description', 'N/A')
            if len(description) > 60:
                description = description[:60] + "..."
            self.console.print(f"   📝 Açıklama: {description}")
            
            tech_stack = config.get('tech_stack', [])
            if tech_stack:
                tech_display = ", ".join(tech_stack[:4])
                if len(tech_stack) > 4:
                    tech_display += f" (+{len(tech_stack)-4} daha)"
                self.console.print(f"   🛠️ Teknolojiler: [yellow]{tech_display}[/yellow]")
            
            self.console.print()
        
        self.console.print("-"*80, style="cyan")
    
    def load_project(self):
        """Mevcut projeyi yükle"""
        self.list_projects()
        
        project_name = Prompt.ask("\n📂 Yüklenecek proje adı")
        project_dir = self.output_dir / project_name
        config_file = project_dir / "project_config.json"
        
        if not config_file.exists():
            self.console.print(f"[red]❌ '{project_name}' projesi bulunamadı![/red]")
            return
        
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = json.load(f)
            
            self.current_project = ProjectConfig(**config_data)
            self.console.print(f"[green]✅ '{project_name}' projesi yüklendi![/green]")
            
        except Exception as e:
            self.console.print(f"[red]❌ Proje yüklenirken hata: {str(e)}[/red]")
    
    async def consult_single_expert(self, expert_type: str):
        """Tek uzmanla konsültasyon"""
        if not self.current_project:
            self.console.print("[red]❌ Aktif proje bulunamadı! Önce bir proje oluşturun veya yükleyin.[/red]")
            return
        
        self.console.print(f"\n[bold blue]👨‍💻 {expert_type.title()} Uzmanı ile Konsültasyon[/bold blue]\n")
        
        # Test uzmanı için özel işlem
        if expert_type == "test":
            await self._consult_test_expert()
            return
        
        additional_request = Prompt.ask("Özel istek (boş bırakabilirsiniz)", default="")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task(f"🤖 {expert_type.title()} uzmanıyla konuşuluyor...", total=None)
            
            try:
                # Prompt'u özelleştir
                expert_prompt = self._create_expert_prompt(expert_type, self.current_project)
                if additional_request:
                    expert_prompt += f"\n\nÖZEL İSTEK: {additional_request}"
                
                response = await self._consult_expert(expert_type, self.current_project)
                
                progress.update(task, description=f"✅ {expert_type.title()} uzmanı yanıtladı")
                
                # Sonucu göster
                await self._display_project_results({expert_type: response})
                
                # Dosyaları kaydet
                if Confirm.ask("\n💾 Oluşturulan dosyaları kaydetmek ister misiniz?"):
                    project_dir = self.output_dir / self.current_project.name
                    expert_dir = project_dir / expert_type
                    expert_dir.mkdir(parents=True, exist_ok=True)
                    
                    for file_struct in response.code_files:
                        file_path = expert_dir / file_struct.path
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(file_struct.content)
                    
                    self.console.print(f"[green]✅ Dosyalar {expert_dir} dizinine kaydedildi![/green]")
                
            except Exception as e:
                progress.update(task, description=f"❌ Hata oluştu: {str(e)}")
                self.console.print(f"[red]❌ Hata: {str(e)}[/red]")
    
    async def _consult_test_expert(self):
        """Test uzmanı ile özel konsültasyon"""
        self.console.print("[bold yellow]🧪 Test Uzmanı - Kod Analizi ve Test Stratejisi[/bold yellow]\n")
        
        # Proje dizinini kontrol et
        project_dir = self.output_dir / self.current_project.name
        if not project_dir.exists():
            self.console.print("[red]❌ Proje dizini bulunamadı! Önce projeyi geliştirin.[/red]")
            return
        
        # Mevcut kodları topla
        existing_code = self._collect_existing_code(project_dir)
        
        # Test uzmanına özel prompt oluştur
        test_prompt = f"""
        VibeCoding Test Uzmanı olarak '{self.current_project.name}' projesinin kapsamlı analizini yap.
        
        PROJE BİLGİLERİ:
        - İsim: {self.current_project.name}
        - Açıklama: {self.current_project.description}
        - Tip: {self.current_project.type}
        - Teknoloji Yığını: {', '.join(self.current_project.tech_stack)}
        - Karmaşıklık: {self.current_project.complexity}
        
        MEVCUT KOD YAPISI:
        {existing_code}
        
        GÖREVLERİN:
        
        1. 🔍 KOD ANALİZİ:
           - Mevcut kodları detaylı analiz et
           - Code quality metrics hesapla
           - Best practice violations tespit et
           - Security vulnerability'leri bul
           - Performance bottleneck'leri belirle
           - Refactoring gereken alanları listele
        
        2. 🧪 TEST STRATEJİSİ:
           - Unit test stratejisi oluştur
           - Integration test planı hazırla
           - E2E test scenarios tasarla
           - Performance test önerileri sun
           - Security test cases oluştur
        
        3. 📊 KALİTE GÜVENCE:
           - Test coverage hedefleri belirle
           - Quality gates tanımla
           - CI/CD test pipeline öner
           - Code review checklist hazırla
        
        4. 📋 TEST DOSYALARI:
           - Kapsamlı test dosyaları oluştur
           - Mock data ve fixtures hazırla
           - Test automation scripts yaz
           - Performance test scripts oluştur
        
        5. 📈 RAPORLAMA:
           - Detaylı analiz raporu hazırla
           - Risk assessment matrix oluştur
           - Quality scorecard hazırla
           - İyileştirme önerileri sun
        
        VibeCoding prensiplerini uygula ve tüm eksiklikleri detaylandır.
        Test-driven development yaklaşımını benimse.
        """
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            TimeElapsedColumn(),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🧪 Test uzmanı kod analizi yapıyor...", total=None)
            
            try:
                response = await self._consult_expert("test", self.current_project)
                
                # Test uzmanına özel prompt ekle
                test_expert = self.experts["test"]
                result = await test_expert.run(test_prompt)
                response = result.data
                
                progress.update(task, description="✅ Test analizi tamamlandı")
                
                # Sonucu göster
                await self._display_test_results(response)
                
                # Dosyaları kaydet
                if Confirm.ask("\n💾 Test dosyalarını ve analiz raporunu kaydetmek ister misiniz?"):
                    project_dir = self.output_dir / self.current_project.name
                    test_dir = project_dir / "test"
                    test_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Test dosyalarını kaydet
                    for file_struct in response.code_files:
                        file_path = test_dir / file_struct.path
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(file_struct.content)
                    
                    # Analiz raporunu kaydet
                    report_file = test_dir / "test_analysis_report.md"
                    with open(report_file, "w", encoding="utf-8") as f:
                        f.write(f"# Test Analizi Raporu - {self.current_project.name}\n\n")
                        f.write(f"## Analiz\n{response.analysis}\n\n")
                        f.write(f"## Öneriler\n")
                        for rec in response.recommendations:
                            f.write(f"- {rec}\n")
                        f.write(f"\n## Sonraki Adımlar\n")
                        for step in response.next_steps:
                            f.write(f"- {step}\n")
                    
                    self.console.print(f"[green]✅ Test dosyaları ve analiz raporu {test_dir} dizinine kaydedildi![/green]")
                
            except Exception as e:
                progress.update(task, description=f"❌ Hata oluştu: {str(e)}")
                self.console.print(f"[red]❌ Hata: {str(e)}[/red]")
    
    def _collect_existing_code(self, project_dir: Path) -> str:
        """Mevcut kodları topla"""
        code_summary = "MEVCUT PROJE DOSYALARI:\n\n"
        
        for expert_dir in project_dir.iterdir():
            if expert_dir.is_dir() and expert_dir.name != "test":
                code_summary += f"📁 {expert_dir.name.upper()} KLASÖRÜ:\n"
                
                for file_path in expert_dir.rglob("*"):
                    if file_path.is_file() and file_path.suffix in ['.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.sql', '.json', '.yml', '.yaml', '.md']:
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                if len(content) > 1000:  # Uzun dosyaları kısalt
                                    content = content[:1000] + "\n... (dosya kesildi)"
                                code_summary += f"\n📄 {file_path.name}:\n```\n{content}\n```\n"
                        except:
                            code_summary += f"\n📄 {file_path.name}: (okunamadı)\n"
                
                code_summary += "\n"
        
        return code_summary
    
    async def _display_test_results(self, response: ExpertResponse):
        """Test sonuçlarını özel formatta göster"""
        self.console.print("\n[bold blue]🧪 Test Uzmanı Analiz Sonuçları[/bold blue]\n")
        
        # Analiz sonuçları
        self.console.print("[bold yellow]🔍 KOD ANALİZİ:[/bold yellow]")
        self.console.print(response.analysis)
        
        # Öneriler
        self.console.print("\n[bold yellow]💡 ÖNERİLER:[/bold yellow]")
        for i, rec in enumerate(response.recommendations, 1):
            self.console.print(f"  {i}. {rec}")
        
        # Test dosyaları
        self.console.print("\n[bold yellow]📁 OLUŞTURULAN TEST DOSYALARI:[/bold yellow]")
        for file_struct in response.code_files:
            self.console.print(f"  📄 {file_struct.path} ({file_struct.file_type})")
            self.console.print(f"      {file_struct.description}")
        
        # Bağımlılıklar
        if response.dependencies:
            self.console.print("\n[bold yellow]📦 TEST BAĞIMLILIKLARI:[/bold yellow]")
            for dep in response.dependencies:
                self.console.print(f"  • {dep}")
        
        # Sonraki adımlar
        self.console.print("\n[bold yellow]➡️ SONRAKİ ADIMLAR:[/bold yellow]")
        for i, step in enumerate(response.next_steps, 1):
            self.console.print(f"  {i}. {step}")
    
    def display_help(self):
        """Yardım menüsünü göster"""
        # Terminal temizle
        os.system('cls' if os.name == 'nt' else 'clear')
        
        self.console.print("="*80, style="blue")
        self.console.print("📚 VibeCoding AI System - Yardım Kılavuzu", style="bold blue", justify="center")
        self.console.print("="*80, style="blue")
        
        self.console.print("\n[bold yellow]📋 ANA KOMUTLAR:[/bold yellow]")
        self.console.print("  [cyan]1[/cyan] - Yeni Proje Oluştur")
        self.console.print("      • Sıfırdan yeni bir proje başlatır")
        self.console.print("      • Proje tipini, teknolojileri ve özellikleri belirler")
        self.console.print("      • Tüm uzman ekibi ile otomatik geliştirme başlatır")
        
        self.console.print("  [cyan]2[/cyan] - Mevcut Proje Yükle")
        self.console.print("      • Daha önce oluşturulan projeleri yükler")
        self.console.print("      • Proje üzerinde çalışmaya devam eder")
        
        self.console.print("  [cyan]3[/cyan] - Proje Geliştir")
        self.console.print("      • Aktif proje için tüm uzmanları çalıştırır")
        self.console.print("      • Kapsamlı geliştirme süreci başlatır")
        
        self.console.print("  [cyan]4[/cyan] - Proje Listesi")
        self.console.print("      • Oluşturulan tüm projeleri listeler")
        
        self.console.print("  [cyan]5[/cyan] - Akıllı Proje Analizi")
        self.console.print("      • Tek girdi ile otomatik teknoloji seçimi")
        self.console.print("      • Minimum soru ile hızlı çözüm üretimi")
        self.console.print("      • Doğrudan uygulanabilir kod taslakları")
        
        self.console.print("\n[bold yellow]👨‍💻 UZMAN MODLARI:[/bold yellow]")
        self.console.print("  [cyan]b[/cyan] - Backend Uzmanı: API, veritabanı, sunucu mimarisi")
        self.console.print("  [cyan]f[/cyan] - Frontend Uzmanı: Kullanıcı arayüzü, responsive tasarım")
        self.console.print("  [cyan]d[/cyan] - Database Uzmanı: Veri modelleme, optimizasyon")
        self.console.print("  [cyan]u[/cyan] - UI/UX Uzmanı: Kullanıcı deneyimi, tasarım sistemi")
        self.console.print("  [cyan]o[/cyan] - DevOps Uzmanı: Deployment, CI/CD, altyapı")
        self.console.print("  [cyan]m[/cyan] - Mobile Uzmanı: Mobil uygulama geliştirme")
        self.console.print("  [cyan]t[/cyan] - Test Uzmanı: Kod analizi, test stratejileri, kalite güvence")
        
        self.console.print("\n[bold yellow]🎯 VibeCoding Metodolojisi:[/bold yellow]")
        self.console.print("  • [green]Temiz Kod[/green]: Okunabilir ve sürdürülebilir")
        self.console.print("  • [green]Best Practices[/green]: Endüstri standartları")
        self.console.print("  • [green]Test-Driven[/green]: Test edilebilir yapı")
        self.console.print("  • [green]Performance[/green]: Optimizasyon odaklı")
        self.console.print("  • [green]Documentation[/green]: Kapsamlı dokümantasyon")
        
        self.console.print("\n[bold yellow]📁 Dosya Yapısı:[/bold yellow]")
        self.console.print("  generated_projects/")
        self.console.print("  ├── proje_adi/")
        self.console.print("  │   ├── project_config.json")
        self.console.print("  │   ├── project_summary.json")
        self.console.print("  │   ├── smart_analysis/")
        self.console.print("  │   ├── backend/")
        self.console.print("  │   ├── frontend/")
        self.console.print("  │   ├── database/")
        self.console.print("  │   ├── uiux/")
        self.console.print("  │   ├── devops/")
        self.console.print("  │   ├── mobile/")
        self.console.print("  │   └── test/")
        
        self.console.print("\n[bold yellow]💡 İpuçları:[/bold yellow]")
        self.console.print("  • Proje oluştururken detaylı açıklamalar yazın")
        self.console.print("  • Teknoloji seçimlerinde projenin ihtiyaçlarını düşünün")
        self.console.print("  • Uzman modlarını özel geliştirmeler için kullanın")
        self.console.print("  • Oluşturulan dosyaları inceleyip özelleştirin")
        
        self.console.print("\n" + "="*80, style="blue")
        input("\nDevam etmek için Enter'a basın...")
    
    async def run(self):
        """Ana çalışma döngüsü"""
        self.display_welcome()
        
        while True:
            self.display_main_menu()
            
            choice = Prompt.ask("\n🎯 Seçiminizi yapın").lower().strip()
            
            try:
                if choice == "1":
                    await self.create_new_project()
                elif choice == "2":
                    self.load_project()
                elif choice == "3":
                    await self.develop_project()
                elif choice == "4":
                    self.list_projects()
                elif choice == "5":
                    await self.smart_project_analysis()
                elif choice == "b":
                    await self.consult_single_expert("backend")
                elif choice == "f":
                    await self.consult_single_expert("frontend")
                elif choice == "d":
                    await self.consult_single_expert("database")
                elif choice == "u":
                    await self.consult_single_expert("uiux")
                elif choice == "o":
                    await self.consult_single_expert("devops")
                elif choice == "m":
                    await self.consult_single_expert("mobile")
                elif choice == "t":
                    await self.consult_single_expert("test")
                elif choice == "h":
                    self.display_help()
                elif choice == "q":
                    self.console.print("\n[green]👋 VibeCoding AI System'den çıkılıyor...[/green]")
                    break
                else:
                    self.console.print("[red]❌ Geçersiz seçim! Lütfen tekrar deneyin.[/red]")
                    
            except KeyboardInterrupt:
                self.console.print("\n[yellow]⚠️ İşlem iptal edildi.[/yellow]")
            except Exception as e:
                self.console.print(f"[red]❌ Beklenmeyen hata: {str(e)}[/red]")

async def main():
    """Ana fonksiyon"""
    try:
        system = VibeCodingAISystem()
        await system.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]👋 Program sonlandırıldı.[/yellow]")
    except Exception as e:
        console.print(f"[red]❌ Kritik hata: {str(e)}[/red]")

if __name__ == "__main__":
    asyncio.run(main()) 