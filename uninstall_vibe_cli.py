#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding CLI - Kaldırma Script'i
Sistemi tamamen temizler
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Confirm
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

class VibeCLIUninstaller:
    """VibeCoding CLI Kaldırma Sınıfı"""
    
    def __init__(self):
        self.console = Console()
        self.system_os = platform.system()
        self.global_config_dir = self._get_global_config_dir()
        self.items_to_remove = []
        
    def _get_global_config_dir(self) -> Path:
        """Global konfigürasyon dizinini belirle"""
        if self.system_os == "Windows":
            return Path.home() / "AppData" / "Roaming" / "VibeCoding"
        else:
            return Path.home() / ".config" / "vibecoding"
    
    def display_welcome(self):
        """Kaldırma hoş geldin ekranı"""
        welcome_text = """
# 🗑️ VibeCoding CLI - Kaldırma İşlemi

## Nelerin Kaldırılacağı:

### 📦 Python Paketi:
- vibe-coding-cli paketi (pip'den)
- Sistem PATH'inden vibe komutu

### 📁 Konfigürasyon Dosyaları:
- Global ayarlar ve API anahtarları
- Cache ve geçici dosyalar
- Kullanıcı tercihleri

### 🗂️ Oluşturulan Projeler:
- generated_projects/ klasörü (isteğe bağlı)
- Kullanıcı projelerini koruma seçeneği

**⚠️ Bu işlem geri alınamaz!**
        """
        
        panel = Panel(
            welcome_text,
            title="[bold red]VibeCoding CLI Kaldırma[/bold red]",
            border_style="red",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def scan_system(self):
        """Sistemde VibeCoding CLI kalıntılarını tara"""
        self.console.print("\n[bold blue]🔍 Sistem Taraması[/bold blue]\n")
        
        # 1. pip paket kontrolü
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "vibe-coding-cli"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.items_to_remove.append({
                    "type": "pip_package",
                    "name": "vibe-coding-cli",
                    "description": "Python paketi (pip)"
                })
                self.console.print("✅ pip paket bulundu: vibe-coding-cli")
            else:
                self.console.print("ℹ️ pip paket bulunamadı")
        except:
            self.console.print("⚠️ pip paket kontrolü başarısız")
        
        # 2. vibe komutu kontrolü
        try:
            result = subprocess.run(["vibe", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.items_to_remove.append({
                    "type": "command",
                    "name": "vibe",
                    "description": "Terminal komutu"
                })
                self.console.print("✅ vibe komutu bulundu")
            else:
                self.console.print("ℹ️ vibe komutu bulunamadı")
        except:
            self.console.print("ℹ️ vibe komutu bulunamadı")
        
        # 3. Global konfigürasyon kontrolü
        if self.global_config_dir.exists():
            self.items_to_remove.append({
                "type": "config_dir",
                "name": str(self.global_config_dir),
                "description": "Global konfigürasyon klasörü"
            })
            self.console.print(f"✅ Konfigürasyon klasörü bulundu: {self.global_config_dir}")
        else:
            self.console.print("ℹ️ Konfigürasyon klasörü bulunamadı")
        
        # 4. generated_projects kontrolü
        generated_dir = Path.cwd() / "generated_projects"
        if generated_dir.exists():
            self.items_to_remove.append({
                "type": "generated_projects",
                "name": str(generated_dir),
                "description": "Oluşturulan projeler klasörü"
            })
            self.console.print(f"✅ Projeler klasörü bulundu: {generated_dir}")
        else:
            self.console.print("ℹ️ Projeler klasörü bulunamadı")
        
        # 5. Cache dosyaları kontrolü
        cache_locations = [
            Path.home() / ".cache" / "vibe-coding",
            Path.home() / "AppData" / "Local" / "vibe-coding" / "cache",
            Path.cwd() / ".cache",
            Path.cwd() / "__pycache__"
        ]
        
        for cache_dir in cache_locations:
            if cache_dir.exists():
                self.items_to_remove.append({
                    "type": "cache",
                    "name": str(cache_dir),
                    "description": "Cache dosyaları"
                })
                self.console.print(f"✅ Cache bulundu: {cache_dir}")
    
    def display_removal_plan(self):
        """Kaldırma planını göster"""
        if not self.items_to_remove:
            self.console.print("\n[green]✅ VibeCoding CLI bulunamadı - sistem temiz![/green]")
            return False
        
        self.console.print(f"\n[bold yellow]📋 Kaldırılacak Öğeler ({len(self.items_to_remove)} adet):[/bold yellow]\n")
        
        for i, item in enumerate(self.items_to_remove, 1):
            icon = {
                "pip_package": "📦",
                "command": "💻",
                "config_dir": "📁",
                "generated_projects": "🗂️",
                "cache": "🗄️"
            }.get(item["type"], "📄")
            
            self.console.print(f"{icon} {i}. {item['description']}")
            self.console.print(f"   📍 {item['name']}")
        
        return True
    
    def remove_items(self):
        """Öğeleri kaldır"""
        self.console.print("\n[bold red]🗑️ Kaldırma İşlemi Başlıyor[/bold red]\n")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("Kaldırma işlemi...", total=len(self.items_to_remove))
            
            for item in self.items_to_remove:
                progress.update(task, description=f"Kaldırılıyor: {item['description']}")
                
                try:
                    if item["type"] == "pip_package":
                        # pip paketini kaldır
                        subprocess.run([
                            sys.executable, "-m", "pip", "uninstall", 
                            item["name"], "-y"
                        ], capture_output=True)
                        self.console.print(f"✅ {item['description']} kaldırıldı")
                    
                    elif item["type"] in ["config_dir", "generated_projects", "cache"]:
                        # Klasörü sil
                        dir_path = Path(item["name"])
                        if dir_path.exists():
                            shutil.rmtree(dir_path)
                            self.console.print(f"✅ {item['description']} kaldırıldı")
                    
                    elif item["type"] == "command":
                        # Komut pip ile birlikte kaldırılır
                        self.console.print(f"✅ {item['description']} kaldırıldı")
                
                except Exception as e:
                    self.console.print(f"⚠️ {item['description']} kaldırılamadı: {e}")
                
                progress.advance(task)
    
    def verify_removal(self):
        """Kaldırma işlemini doğrula"""
        self.console.print("\n[bold blue]🔍 Kaldırma Doğrulaması[/bold blue]\n")
        
        # vibe komutunu test et
        try:
            result = subprocess.run(["vibe", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                self.console.print("⚠️ vibe komutu hala çalışıyor")
                return False
            else:
                self.console.print("✅ vibe komutu kaldırıldı")
        except:
            self.console.print("✅ vibe komutu kaldırıldı")
        
        # pip paketi test et
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "show", "vibe-coding-cli"],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.console.print("⚠️ pip paketi hala mevcut")
                return False
            else:
                self.console.print("✅ pip paketi kaldırıldı")
        except:
            self.console.print("✅ pip paketi kaldırıldı")
        
        # Konfigürasyon klasörü test et
        if self.global_config_dir.exists():
            self.console.print(f"⚠️ Konfigürasyon klasörü hala mevcut: {self.global_config_dir}")
            return False
        else:
            self.console.print("✅ Konfigürasyon klasörü kaldırıldı")
        
        return True
    
    def display_completion(self, success):
        """Kaldırma tamamlama mesajı"""
        if success:
            completion_text = """
# 🎉 VibeCoding CLI Başarıyla Kaldırıldı!

## ✅ Kaldırılan Öğeler:
- Python paketi (vibe-coding-cli)
- Terminal komutu (vibe)
- Global konfigürasyon dosyaları
- API anahtarları ve ayarlar
- Cache ve geçici dosyalar

## 📁 Proje Dosyaları:
Eğer proje klasörünü de silmek istiyorsanız:
- Manuel olarak proje klasörünü silin
- generated_projects/ klasörünü kontrol edin

## 🔄 Yeniden Kurulum:
İleride tekrar kurmak isterseniz:
- install_global.bat (Windows)
- ./install_global.sh (Linux/Mac)

**VibeCoding CLI sisteminizden tamamen kaldırıldı! 👋**
            """
        else:
            completion_text = """
# ⚠️ Kaldırma İşlemi Tamamlanamadı

## 🔧 Manuel Temizlik:

### 1. pip Paketi:
```bash
pip uninstall vibe-coding-cli -y
```

### 2. Konfigürasyon Klasörü:
- Windows: %APPDATA%\\VibeCoding
- Linux/Mac: ~/.config/vibecoding

### 3. Cache Dosyaları:
- __pycache__ klasörlerini silin
- .cache klasörlerini kontrol edin

### 4. Proje Klasörü:
- Manuel olarak silin

**Bazı dosyalar manuel olarak silinmeli! 🛠️**
            """
        
        panel = Panel(
            completion_text,
            title="[bold green]Kaldırma Tamamlandı[/bold green]" if success else "[bold yellow]Manuel Temizlik Gerekli[/bold yellow]",
            border_style="green" if success else "yellow",
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    def run_uninstall(self):
        """Tam kaldırma sürecini çalıştır"""
        self.display_welcome()
        
        # Kullanıcı onayı
        if not Confirm.ask("\n🗑️ VibeCoding CLI'yi tamamen kaldırmak istiyor musunuz?"):
            self.console.print("[yellow]⏹️ Kaldırma işlemi iptal edildi.[/yellow]")
            return
        
        # Sistem taraması
        self.scan_system()
        
        # Kaldırma planını göster
        if not self.display_removal_plan():
            return
        
        # Son onay
        if not Confirm.ask("\n⚠️ Bu öğeleri kaldırmak istediğinizden emin misiniz?"):
            self.console.print("[yellow]⏹️ Kaldırma işlemi iptal edildi.[/yellow]")
            return
        
        # Projeler için özel soru
        generated_dir = Path.cwd() / "generated_projects"
        if generated_dir.exists():
            keep_projects = Confirm.ask(
                "\n📁 Oluşturulan projeleri korumak istiyor musunuz? (Hayır = silinir)"
            )
            if keep_projects:
                # generated_projects'i kaldırma listesinden çıkar
                self.items_to_remove = [
                    item for item in self.items_to_remove 
                    if item["type"] != "generated_projects"
                ]
                self.console.print("[green]📁 Projeler korunacak[/green]")
        
        # Kaldırma işlemi
        self.remove_items()
        
        # Doğrulama
        success = self.verify_removal()
        
        # Tamamlama
        self.display_completion(success)

def main():
    """Ana kaldırma fonksiyonu"""
    try:
        uninstaller = VibeCLIUninstaller()
        uninstaller.run_uninstall()
    except KeyboardInterrupt:
        console.print("\n\n⏹️ Kaldırma işlemi kullanıcı tarafından durduruldu")
    except Exception as e:
        console.print(f"\n💥 Beklenmeyen hata: {e}")
        console.print("\n🛠️ Manuel kaldırma gerekebilir")

if __name__ == "__main__":
    main() 