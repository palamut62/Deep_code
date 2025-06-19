#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding CLI - Global Kurulum Script'i
Claude Code benzeri terminal aracını global olarak kurar
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
import shutil
import getpass

console = Console()

class VibeCLIInstaller:
    """VibeCoding CLI Kurulum Sınıfı"""
    
    def __init__(self):
        self.console = Console()
        self.system_os = platform.system()
        self.python_version = sys.version_info
        self.project_dir = Path(__file__).parent
        self.global_config_dir = self._get_global_config_dir()
        
    def _get_global_config_dir(self) -> Path:
        """Global konfigürasyon dizinini belirle"""
        if self.system_os == "Windows":
            return Path.home() / "AppData" / "Roaming" / "VibeCoding"
        else:
            return Path.home() / ".config" / "vibecoding"
    
    def display_welcome(self):
        """Kurulum hoş geldin ekranı"""
        welcome_text = """
# 🚀 VibeCoding CLI - Global Kurulum

## Claude Code Benzeri Terminal AI Aracı

Bu kurulum VibeCoding CLI'yi sisteminize global olarak kuracak.
Kurulum sonrası herhangi bir klasörde `vibe` komutu kullanabileceksiniz.

### 🎯 Özellikler:
- **Terminal Tabanlı**: Komut satırından AI ile proje oluşturma
- **Claude Code Benzeri**: Herhangi bir klasörde çalışır
- **6 Uzman AI**: Backend, Frontend, Database, UI/UX, DevOps, Mobile
- **Çoklu API Desteği**: DeepSeek ve Gemini AI
- **Otomatik Proje Oluşturma**: Tam kapsamlı kod dosyaları

### 💻 Kullanım:
```bash
vibe init my-project    # Yeni proje oluştur
vibe --help            # Yardım
vibe --version         # Versiyon
```
        """
        
        panel = Panel(
            welcome_text,
            title="[bold blue]VibeCoding CLI Kurulum[/bold blue]",
            border_style="blue",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def check_requirements(self) -> bool:
        """Sistem gereksinimlerini kontrol et"""
        self.console.print("\n[bold blue]🔍 Sistem Gereksinimleri Kontrol Ediliyor[/bold blue]\n")
        
        # Python versiyonu
        if self.python_version < (3, 8):
            self.console.print(f"[red]❌ Python 3.8+ gerekli. Mevcut: {sys.version}[/red]")
            return False
        else:
            self.console.print(f"[green]✅ Python {sys.version.split()[0]}[/green]")
        
        # pip kontrolü
        try:
            subprocess.run([sys.executable, "-m", "pip", "--version"], 
                         check=True, capture_output=True)
            self.console.print("[green]✅ pip mevcut[/green]")
        except subprocess.CalledProcessError:
            self.console.print("[red]❌ pip bulunamadı![/red]")
            return False
        
        # requirements.txt kontrolü
        req_file = self.project_dir / "requirements.txt"
        if req_file.exists():
            self.console.print("[green]✅ requirements.txt mevcut[/green]")
        else:
            self.console.print("[red]❌ requirements.txt bulunamadı![/red]")
            return False
        
        return True
    
    def install_package(self):
        """Paketi global olarak kur"""
        self.console.print("\n[bold blue]📦 VibeCoding CLI Kuruluyor[/bold blue]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("📦 Paket kuruluyor...", total=None)
            
            try:
                # Pip'i güncelle
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "--upgrade", "pip"
                ], check=True, capture_output=True)
                
                # VibeCoding CLI'yi kur (editable mode)
                subprocess.run([
                    sys.executable, "-m", "pip", "install", "-e", "."
                ], check=True, capture_output=True, cwd=self.project_dir)
                
                progress.update(task, description="✅ Paket başarıyla kuruldu")
                
            except subprocess.CalledProcessError as e:
                progress.update(task, description="❌ Kurulum hatası")
                self.console.print(f"[red]❌ Kurulum hatası: {e}[/red]")
                return False
        
        return True
    
    def setup_global_config(self):
        """Global konfigürasyon ayarla"""
        self.console.print("\n[bold blue]🔧 Global Konfigürasyon[/bold blue]\n")
        
        # Global config dizini oluştur
        self.global_config_dir.mkdir(parents=True, exist_ok=True)
        
        # .env dosyasını global dizine kopyala
        local_env = self.project_dir / ".env"
        global_env = self.global_config_dir / ".env"
        
        if local_env.exists():
            shutil.copy2(local_env, global_env)
            self.console.print(f"[green]✅ Konfigürasyon kopyalandı: {global_env}[/green]")
        else:
            # .env şablonu oluştur
            env_template = """# VibeCoding CLI - Global Konfigürasyon

# DeepSeek API Anahtarı
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Gemini API Anahtarı
GEMINI_API_KEY=your_gemini_api_key_here

# Debug modu
DEBUG=False

# Varsayılan AI sağlayıcısı
DEFAULT_AI_PROVIDER=deepseek
"""
            
            with open(global_env, "w", encoding="utf-8") as f:
                f.write(env_template)
            
            self.console.print(f"[yellow]⚠️ .env şablonu oluşturuldu: {global_env}[/yellow]")
            self.console.print("[yellow]💡 Lütfen API anahtarlarınızı ekleyin![/yellow]")
        
        return True
    
    def setup_api_keys(self):
        """API anahtarlarını ayarla"""
        if not Confirm.ask("\n🔑 API anahtarlarını şimdi ayarlamak ister misiniz?"):
            return True
        
        self.console.print("\n[bold blue]🔑 API Anahtarları Konfigürasyonu[/bold blue]\n")
        
        # API sağlayıcı bilgileri
        providers_info = """
**🤖 Desteklenen AI Sağlayıcıları:**

1. **DeepSeek AI**
   - Website: https://platform.deepseek.com
   - Ücretsiz: 2M token/ay
   - Güçlü kod üretimi

2. **Google Gemini**
   - Website: https://makersuite.google.com
   - Ücretsiz: 60 istek/dakika
   - Çok dilli destek

**Not**: En az bir API anahtarı gereklidir.
        """
        
        self.console.print(Panel(providers_info, title="API Sağlayıcıları", border_style="green"))
        
        # API anahtarlarını al
        deepseek_key = ""
        gemini_key = ""
        
        if Confirm.ask("🔑 DeepSeek API anahtarı eklemek ister misiniz?"):
            deepseek_key = getpass.getpass("DeepSeek API anahtarı: ").strip()
        
        if Confirm.ask("🔑 Gemini API anahtarı eklemek ister misiniz?"):
            gemini_key = getpass.getpass("Gemini API anahtarı: ").strip()
        
        if not deepseek_key and not gemini_key:
            self.console.print("[yellow]⚠️ API anahtarı eklenmedi. Daha sonra manuel olarak ekleyebilirsiniz.[/yellow]")
            return True
        
        # .env dosyasını güncelle
        global_env = self.global_config_dir / ".env"
        env_content = f"""# VibeCoding CLI - Global Konfigürasyon

# DeepSeek API Anahtarı
DEEPSEEK_API_KEY={deepseek_key}

# Gemini API Anahtarı
GEMINI_API_KEY={gemini_key}

# Debug modu
DEBUG=False

# Varsayılan AI sağlayıcısı
DEFAULT_AI_PROVIDER={"deepseek" if deepseek_key else "gemini"}
"""
        
        with open(global_env, "w", encoding="utf-8") as f:
            f.write(env_content)
        
        self.console.print("[green]✅ API anahtarları kaydedildi![/green]")
        return True
    
    def test_installation(self):
        """Kurulumu test et"""
        self.console.print("\n[bold blue]🧪 Kurulum Test Ediliyor[/bold blue]\n")
        
        try:
            # vibe komutunu test et
            result = subprocess.run(
                ["vibe", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=10
            )
            
            if result.returncode == 0:
                self.console.print("[green]✅ vibe komutu çalışıyor![/green]")
                self.console.print(f"[dim]{result.stdout.strip()}[/dim]")
                return True
            else:
                self.console.print("[red]❌ vibe komutu çalışmıyor![/red]")
                return False
                
        except subprocess.TimeoutExpired:
            self.console.print("[red]❌ Komut zaman aşımı![/red]")
            return False
        except FileNotFoundError:
            self.console.print("[red]❌ vibe komutu bulunamadı![/red]")
            return False
    
    def display_completion(self):
        """Kurulum tamamlama mesajı"""
        completion_text = f"""
# 🎉 VibeCoding CLI Başarıyla Kuruldu!

## 🚀 Kullanıma Hazır

Artık herhangi bir klasörde aşağıdaki komutları kullanabilirsiniz:

### 📋 Temel Komutlar:
```bash
vibe init my-project    # Yeni proje oluştur
vibe init              # İnteraktif proje oluşturma
vibe --help           # Yardım menüsü
vibe --version        # Versiyon bilgisi
```

### 🎯 Örnek Kullanım:
```bash
# Web uygulaması oluştur
cd ~/Desktop
vibe init my-web-app

# API projesi oluştur
mkdir ~/projects/my-api
cd ~/projects/my-api
vibe init
```

### 🔧 Konfigürasyon:
- **Global Config**: `{self.global_config_dir}`
- **API Anahtarları**: `{self.global_config_dir}/.env`

### 🆘 Sorun Giderme:
- API anahtarları eksikse: `{self.global_config_dir}/.env` dosyasını düzenleyin
- Komut bulunamazsa: Python PATH'inizi kontrol edin
- Hata raporları: GitHub Issues

## 💡 İpuçları:
- Her proje kendi klasöründe oluşturulur
- AI uzmanları otomatik olarak çalışır
- Tüm dosyalar hazır kod ile oluşturulur
- IDE'nizde açıp hemen geliştirmeye başlayabilirsiniz

**VibeCoding CLI ile AI destekli geliştirme deneyiminiz başlıyor! 🚀**
        """
        
        panel = Panel(
            completion_text,
            title="[bold green]Kurulum Tamamlandı[/bold green]",
            border_style="green",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def run_installation(self):
        """Tam kurulum sürecini çalıştır"""
        self.display_welcome()
        
        # Kurulum adımları
        steps = [
            ("Sistem gereksinimleri", self.check_requirements),
            ("Paket kurulumu", self.install_package),
            ("Global konfigürasyon", self.setup_global_config),
            ("API anahtarları", self.setup_api_keys),
            ("Kurulum testi", self.test_installation)
        ]
        
        for step_name, step_func in steps:
            if not step_func():
                self.console.print(f"\n[red]❌ Kurulum başarısız: {step_name}[/red]")
                self.console.print("Lütfen hataları düzeltin ve tekrar deneyin.")
                sys.exit(1)
        
        self.display_completion()

def main():
    """Ana kurulum fonksiyonu"""
    installer = VibeCLIInstaller()
    installer.run_installation()

if __name__ == "__main__":
    main() 