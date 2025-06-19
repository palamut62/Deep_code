#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding AI System - Kurulum Script'i
Pydantic AI tabanlı yazılım geliştirme ekosistemi kurulumu
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt, Confirm
from rich.markdown import Markdown
import getpass

console = Console()

class VibeCodingAISetup:
    """VibeCoding AI System kurulum sınıfı"""
    
    def __init__(self):
        self.console = Console()
        self.system_os = platform.system()
        self.python_version = sys.version_info
        self.project_dir = Path.cwd()
        
    def display_welcome(self):
        """Kurulum hoş geldin ekranı"""
        welcome_text = """
# 🚀 VibeCoding AI System Kurulumu

## Yazılım Geliştirme Ekosistemi

Bu kurulum, **Pydantic AI** tabanlı VibeCoding AI System'i bilgisayarınıza kuracak.

### 🎯 Sistem Özellikleri:
- **6 Uzman AI Ajanı**: Backend, Frontend, Database, UI/UX, DevOps, Mobile
- **VibeCoding Metodolojisi**: Kaliteli ve sürdürülebilir kod üretimi
- **Tam Kapsamlı Projeler**: Sıfırdan tamamlanmış uygulamalar
- **Çoklu API Desteği**: DeepSeek ve Gemini AI entegrasyonu
- **Otomatik Dosya Oluşturma**: Proje dosyalarını otomatik üretir

### 📋 Kurulum Adımları:
1. Sistem gereksinimleri kontrolü
2. Python paketlerinin yüklenmesi
3. API anahtarlarının konfigürasyonu
4. Test ve doğrulama
        """
        
        panel = Panel(
            Markdown(welcome_text),
            title="[bold blue]VibeCoding AI System - Kurulum[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def check_system_requirements(self):
        """Sistem gereksinimlerini kontrol et"""
        self.console.print("\n[bold blue]🔍 Sistem Gereksinimleri Kontrol Ediliyor[/bold blue]\n")
        
        # Python versiyonu kontrolü
        if self.python_version < (3, 8):
            self.console.print(f"[red]❌ Python 3.8+ gerekli. Mevcut versiyon: {sys.version}[/red]")
            return False
        else:
            self.console.print(f"[green]✅ Python {sys.version.split()[0]} - Uygun[/green]")
        
        # İşletim sistemi
        self.console.print(f"[green]✅ İşletim Sistemi: {self.system_os}[/green]")
        
        # pip kontrolü
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            self.console.print("[green]✅ pip - Mevcut[/green]")
        except subprocess.CalledProcessError:
            self.console.print("[red]❌ pip bulunamadı![/red]")
            return False
        
        return True
    
    def install_packages(self):
        """Gerekli Python paketlerini yükle"""
        self.console.print("\n[bold blue]📦 Python Paketleri Yükleniyor[/bold blue]\n")
        
        requirements_file = self.project_dir / "requirements.txt"
        
        if not requirements_file.exists():
            self.console.print("[red]❌ requirements.txt dosyası bulunamadı![/red]")
            return False
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("📦 Paketler yükleniyor...", total=None)
            
            try:
                # Pip'i güncelle
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade", "pip"
                ], check=True, capture_output=True)
                
                # Requirements'ı yükle
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
                ], check=True, capture_output=True)
                
                progress.update(task, description="✅ Paketler başarıyla yüklendi")
                
            except subprocess.CalledProcessError as e:
                progress.update(task, description="❌ Paket yükleme hatası")
                self.console.print(f"[red]❌ Hata: {e}[/red]")
                return False
        
        self.console.print("[green]✅ Tüm paketler başarıyla yüklendi![/green]")
        return True
    
    def setup_api_keys(self):
        """API anahtarlarını konfigüre et"""
        self.console.print("\n[bold blue]🔑 API Anahtarları Konfigürasyonu[/bold blue]\n")
        
        env_file = self.project_dir / ".env"
        env_example = self.project_dir / ".env.example"
        
        # .env.example'ı kontrol et
        if not env_example.exists():
            # .env.example oluştur
            with open(env_example, "w", encoding="utf-8") as f:
                f.write("""# VibeCoding AI System - API Anahtarları

# DeepSeek API Anahtarı
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Gemini API Anahtarı  
GEMINI_API_KEY=your_gemini_api_key_here

# Debug modu (True/False)
DEBUG=False
""")
            self.console.print("[green]✅ .env.example dosyası oluşturuldu[/green]")
        
        # Mevcut .env dosyasını kontrol et
        if env_file.exists():
            if not Confirm.ask("📄 .env dosyası zaten mevcut. Yeniden yapılandırmak ister misiniz?"):
                self.console.print("[yellow]⚠️ Mevcut konfigürasyon korundu.[/yellow]")
                return True
        
        # API sağlayıcı bilgileri
        providers_info = """
### 🤖 Desteklenen AI Sağlayıcıları:

**1. DeepSeek AI**
- Website: https://platform.deepseek.com
- Ücretsiz tier: 2M token/ay
- Güçlü kod üretimi
- Hızlı yanıt süresi

**2. Google Gemini**
- Website: https://makersuite.google.com
- Ücretsiz tier: 60 istek/dakika
- Çok dilli destek
- Güçlü analiz yetenekleri

**Not**: En az bir API anahtarı gereklidir.
        """
        
        self.console.print(Panel(
            Markdown(providers_info),
            title="[bold green]API Sağlayıcıları[/bold green]",
            border_style="green"
        ))
        
        # API anahtarlarını al
        deepseek_key = ""
        gemini_key = ""
        
        if Confirm.ask("\n🔑 DeepSeek API anahtarı eklemek ister misiniz?"):
            deepseek_key = getpass.getpass("DeepSeek API anahtarı: ").strip()
        
        if Confirm.ask("🔑 Gemini API anahtarı eklemek ister misiniz?"):
            gemini_key = getpass.getpass("Gemini API anahtarı: ").strip()
        
        if not deepseek_key and not gemini_key:
            self.console.print("[red]❌ En az bir API anahtarı gereklidir![/red]")
            return False
        
        # .env dosyasını oluştur
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("# VibeCoding AI System - API Anahtarları\n\n")
            f.write(f"DEEPSEEK_API_KEY={deepseek_key}\n")
            f.write(f"GEMINI_API_KEY={gemini_key}\n")
            f.write("DEBUG=False\n")
        
        self.console.print("[green]✅ API anahtarları başarıyla kaydedildi![/green]")
        return True
    
    def test_installation(self):
        """Kurulumu test et"""
        self.console.print("\n[bold blue]🧪 Kurulum Test Ediliyor[/bold blue]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🧪 Sistem testi yapılıyor...", total=None)
            
            try:
                # Gerekli modülleri import et
                import pydantic_ai
                import rich
                import requests
                import dotenv
                
                progress.update(task, description="✅ Tüm modüller başarıyla yüklendi")
                
            except ImportError as e:
                progress.update(task, description=f"❌ Modül hatası: {e}")
                self.console.print(f"[red]❌ Import hatası: {e}[/red]")
                return False
        
        self.console.print("[green]✅ Kurulum testi başarılı![/green]")
        return True
    
    def create_shortcuts(self):
        """Kısayollar oluştur"""
        self.console.print("\n[bold blue]🔗 Kısayollar Oluşturuluyor[/bold blue]\n")
        
        # Windows için .bat dosyası zaten var
        if self.system_os == "Windows":
            self.console.print("[green]✅ Windows çalıştırma script'i hazır: run_vibe_ai_system.bat[/green]")
        
        # Linux/Mac için shell script oluştur
        elif self.system_os in ["Linux", "Darwin"]:
            script_content = """#!/bin/bash
echo "🚀 VibeCoding AI System Başlatılıyor..."
echo

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 bulunamadı! Lütfen Python3'ü yükleyin."
    exit 1
fi

# Gerekli paketleri yükle
echo "📦 Gerekli paketler yükleniyor..."
pip3 install -r requirements.txt

# VibeCoding AI System'i başlat
echo
echo "🎯 VibeCoding AI System başlatılıyor..."
python3 vibe_coding_ai_system.py
"""
            
            script_file = self.project_dir / "run_vibe_ai_system.sh"
            with open(script_file, "w", encoding="utf-8") as f:
                f.write(script_content)
            
            # Çalıştırma izni ver
            os.chmod(script_file, 0o755)
            self.console.print(f"[green]✅ {self.system_os} çalıştırma script'i oluşturuldu: run_vibe_ai_system.sh[/green]")
    
    def display_completion(self):
        """Kurulum tamamlama ekranı"""
        completion_text = f"""
# 🎉 VibeCoding AI System Başarıyla Kuruldu!

## 🚀 Nasıl Başlatılır:

### Windows:
```
run_vibe_ai_system.bat
```

### Linux/Mac:
```
./run_vibe_ai_system.sh
```

### Manuel:
```
python vibe_coding_ai_system.py
```

## 📋 Kurulum Özeti:
- ✅ Python paketleri yüklendi
- ✅ API anahtarları konfigüre edildi
- ✅ Sistem testi başarılı
- ✅ Çalıştırma script'leri hazır

## 🎯 Sonraki Adımlar:
1. VibeCoding AI System'i başlatın
2. İlk projenizi oluşturun
3. Uzman AI ajanlarıyla çalışın
4. Kaliteli yazılımlar geliştirin!

## 📚 Daha Fazla Bilgi:
- README.md dosyasını okuyun
- KULLANIM_ORNEGI.md'ye göz atın
- Herhangi bir sorun için GitHub Issues kullanın

**Mutlu kodlamalar! 🚀**
        """
        
        panel = Panel(
            Markdown(completion_text),
            title="[bold green]🎉 Kurulum Tamamlandı![/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def run_setup(self):
        """Ana kurulum sürecini çalıştır"""
        try:
            self.display_welcome()
            
            # Sistem gereksinimleri
            if not self.check_system_requirements():
                self.console.print("[red]❌ Sistem gereksinimleri karşılanmıyor![/red]")
                return False
            
            # Paket yükleme
            if not self.install_packages():
                self.console.print("[red]❌ Paket yükleme başarısız![/red]")
                return False
            
            # API konfigürasyonu
            if not self.setup_api_keys():
                self.console.print("[red]❌ API konfigürasyonu başarısız![/red]")
                return False
            
            # Test
            if not self.test_installation():
                self.console.print("[red]❌ Kurulum testi başarısız![/red]")
                return False
            
            # Kısayollar
            self.create_shortcuts()
            
            # Tamamlama
            self.display_completion()
            
            return True
            
        except KeyboardInterrupt:
            self.console.print("\n[yellow]⚠️ Kurulum iptal edildi.[/yellow]")
            return False
        except Exception as e:
            self.console.print(f"\n[red]❌ Kurulum hatası: {str(e)}[/red]")
            return False

def main():
    """Ana fonksiyon"""
    setup = VibeCodingAISetup()
    success = setup.run_setup()
    
    if success:
        console.print("\n[green]🎉 Kurulum başarıyla tamamlandı![/green]")
        if Confirm.ask("\n🚀 VibeCoding AI System'i şimdi başlatmak ister misiniz?"):
            try:
                subprocess.run([sys.executable, "vibe_coding_ai_system.py"])
            except FileNotFoundError:
                console.print("[red]❌ vibe_coding_ai_system.py dosyası bulunamadı![/red]")
    else:
        console.print("\n[red]❌ Kurulum başarısız! Lütfen hataları kontrol edin.[/red]")

if __name__ == "__main__":
    main() 