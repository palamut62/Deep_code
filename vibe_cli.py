#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding CLI - Terminal Tabanlı AI Geliştirme Aracı
Claude Code benzeri terminal uygulaması
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path
from typing import Optional, List
import json
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from dotenv import load_dotenv

# Mevcut VibeCoding modüllerini import et
from vibe_coding_ai_system import VibeCodingAISystem

console = Console()

class VibeCodingCLI:
    """VibeCoding CLI Ana Sınıfı"""
    
    def __init__(self):
        self.console = Console()
        self.current_dir = Path.cwd()
        self.ai_system = None
        self.global_config_dir = self._get_global_config_dir()
        self._load_global_config()
        
    def _get_global_config_dir(self) -> Path:
        """Global konfigürasyon dizinini belirle"""
        import platform
        system_os = platform.system()
        if system_os == "Windows":
            return Path.home() / "AppData" / "Roaming" / "VibeCoding"
        else:
            return Path.home() / ".config" / "vibecoding"
    
    def _load_global_config(self):
        """Global konfigürasyonu yükle"""
        # Önce local .env'i dene
        load_dotenv()
        
        # Sonra global .env'i dene
        global_env = self.global_config_dir / ".env"
        if global_env.exists():
            load_dotenv(global_env)
        
    def display_banner(self):
        """CLI banner göster"""
        banner = """
╭─────────────────────────────────────────────────────────────╮
│                                                             │
│  ██╗   ██╗██╗██████╗ ███████╗     ██████╗██╗     ██╗       │
│  ██║   ██║██║██╔══██╗██╔════╝    ██╔════╝██║     ██║       │
│  ██║   ██║██║██████╔╝█████╗      ██║     ██║     ██║       │
│  ╚██╗ ██╔╝██║██╔══██╗██╔══╝      ██║     ██║     ██║       │
│   ╚████╔╝ ██║██████╔╝███████╗    ╚██████╗███████╗██║       │
│    ╚═══╝  ╚═╝╚═════╝ ╚══════╝     ╚═════╝╚══════╝╚═╝       │
│                                                             │
│           Terminal Tabanlı AI Geliştirme Aracı             │
│                                                             │
╰─────────────────────────────────────────────────────────────╯
        """
        self.console.print(banner, style="bold cyan")
        self.console.print("🚀 VibeCoding CLI - Claude Code benzeri AI geliştirme aracı", style="bold blue")
        self.console.print("💡 Herhangi bir klasörde 'vibe' komutu ile projenizi oluşturun\n", style="yellow")
    
    def check_api_keys(self) -> bool:
        """API anahtarlarını kontrol et"""
        deepseek_key = os.getenv("DEEPSEEK_API_KEY")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if not deepseek_key and not gemini_key:
            self.console.print("[red]❌ API anahtarı bulunamadı![/red]")
            self.console.print("[yellow]💡 Lütfen .env dosyasını oluşturun ve API anahtarlarınızı ekleyin:[/yellow]")
            self.console.print("   DEEPSEEK_API_KEY=your_key_here")
            self.console.print("   GEMINI_API_KEY=your_key_here")
            return False
        
        return True
    
    async def init_project(self, project_name: Optional[str] = None):
        """Yeni proje başlat"""
        if not self.check_api_keys():
            return
            
        # Proje adını al
        if not project_name:
            project_name = Prompt.ask("📝 Proje adı", default="my-project")
        
        project_path = self.current_dir / project_name
        
        # Klasör kontrolü
        if project_path.exists():
            if not Confirm.ask(f"📁 '{project_name}' klasörü zaten mevcut. Devam edilsin mi?"):
                return
        else:
            project_path.mkdir(exist_ok=True)
        
        # Proje dizinine geç
        os.chdir(project_path)
        self.current_dir = project_path
        
        self.console.print(f"[green]✅ Proje klasörü: {project_path}[/green]")
        
        # AI sistemini başlat
        self.ai_system = VibeCodingAISystem()
        
        # Proje oluşturma süreci
        await self.create_project_interactive()
    
    async def create_project_interactive(self):
        """İnteraktif proje oluşturma"""
        self.console.print("\n[bold blue]🎯 Proje Oluşturma Süreci[/bold blue]\n")
        
        # Proje tipi seçimi
        project_types = [
            "web - Web uygulaması",
            "api - RESTful API",
            "mobile - Mobil uygulama", 
            "desktop - Masaüstü uygulaması",
            "fullstack - Tam yığın uygulama"
        ]
        
        self.console.print("📋 Proje Tipleri:")
        for i, ptype in enumerate(project_types, 1):
            self.console.print(f"  {i}. {ptype}")
        
        choice = Prompt.ask("Proje tipi seçin", choices=["1", "2", "3", "4", "5"], default="1")
        project_type = project_types[int(choice)-1].split(" - ")[0]
        
        # Proje açıklaması
        description = Prompt.ask("📄 Proje açıklaması", default="Yeni proje")
        
        # Teknoloji yığını
        tech_suggestions = {
            "web": "React, TypeScript, Tailwind CSS",
            "api": "FastAPI, PostgreSQL, Redis",
            "mobile": "React Native, TypeScript",
            "desktop": "Electron, React, TypeScript",
            "fullstack": "React, FastAPI, PostgreSQL"
        }
        
        tech_stack = Prompt.ask("🛠️ Teknoloji yığını", 
                               default=tech_suggestions.get(project_type, ""))
        
        # Özellikler
        features = Prompt.ask("✨ Ana özellikler (virgülle ayırın)", 
                            default="Kullanıcı yönetimi, Dashboard")
        
        # AI sistemi ile proje oluştur
        await self.generate_project_with_ai(
            project_type=project_type,
            description=description,
            tech_stack=tech_stack.split(","),
            features=features.split(",")
        )
    
    async def generate_project_with_ai(self, project_type: str, description: str, 
                                     tech_stack: List[str], features: List[str]):
        """AI ile proje oluştur"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            task = progress.add_task("🤖 AI ile proje oluşturuluyor...", total=None)
            
            # Proje konfigürasyonu oluştur
            from vibe_coding_ai_system import ProjectConfig
            
            project_config = ProjectConfig(
                name=self.current_dir.name,
                description=description,
                type=project_type,
                tech_stack=[tech.strip() for tech in tech_stack],
                features=[feature.strip() for feature in features],
                target_audience="Genel kullanıcılar",
                complexity="orta",
                database_needed=True,
                auth_needed=True,
                api_needed=True
            )
            
            # AI sistemini çalıştır
            progress.update(task, description="🔧 Uzman AI ajanları çalışıyor...")
            
            try:
                # Proje geliştirme
                required_experts = self.ai_system._determine_required_experts(project_config)
                responses = {}
                
                for expert_type in required_experts:
                    progress.update(task, description=f"👨‍💻 {expert_type.title()} uzmanı çalışıyor...")
                    response = await self.ai_system._consult_expert(expert_type, project_config)
                    responses[expert_type] = response
                
                # Dosyaları oluştur
                progress.update(task, description="📁 Proje dosyaları oluşturuluyor...")
                await self.create_project_files(project_config, responses)
                
                progress.update(task, description="✅ Proje başarıyla oluşturuldu!")
                
            except Exception as e:
                progress.update(task, description=f"❌ Hata: {str(e)}")
                self.console.print(f"[red]❌ Proje oluşturma hatası: {e}[/red]")
                return
        
        # Sonuçları göster
        self.display_project_summary(project_config, responses)
    
    async def create_project_files(self, project_config, responses):
        """Proje dosyalarını oluştur"""
        
        # Proje konfigürasyonunu kaydet
        config_data = {
            "name": project_config.name,
            "description": project_config.description,
            "type": project_config.type,
            "tech_stack": project_config.tech_stack,
            "features": project_config.features,
            "created_at": str(Path.cwd()),
            "vibe_cli_version": "1.0.0"
        }
        
        with open("vibe-project.json", "w", encoding="utf-8") as f:
            json.dump(config_data, f, indent=2, ensure_ascii=False)
        
        # Her uzman için dosyaları oluştur
        for expert_type, response in responses.items():
            expert_dir = Path(expert_type)
            expert_dir.mkdir(exist_ok=True)
            
            # Kod dosyalarını oluştur
            for file_struct in response.code_files:
                file_path = expert_dir / file_struct.path
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(file_struct.content)
            
            # Bağımlılıkları kaydet
            if response.dependencies:
                deps_file = expert_dir / "requirements.txt"
                with open(deps_file, "w", encoding="utf-8") as f:
                    for dep in response.dependencies:
                        f.write(f"{dep}\n")
        
        # Ana README oluştur
        readme_content = f"""# {project_config.name}

{project_config.description}

## 🚀 VibeCoding CLI ile Oluşturuldu

Bu proje VibeCoding CLI aracı ile otomatik olarak oluşturulmuştur.

## 📋 Proje Bilgileri

- **Tip**: {project_config.type}
- **Teknolojiler**: {', '.join(project_config.tech_stack)}
- **Özellikler**: {', '.join(project_config.features)}

## 🛠️ Geliştirme

Her klasör kendi README dosyasını içerir:

"""
        
        for expert_type in responses.keys():
            readme_content += f"- `{expert_type}/` - {expert_type.title()} dosyaları\n"
        
        readme_content += """
## 🔧 Kurulum

1. Gerekli bağımlılıkları yükleyin
2. Konfigürasyon dosyalarını düzenleyin  
3. Uygulamayı çalıştırın

## 📞 Destek

VibeCoding CLI ile oluşturulan projeler için destek: https://github.com/your-repo
"""
        
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
    
    def display_project_summary(self, project_config, responses):
        """Proje özetini göster"""
        self.console.print("\n[bold green]🎉 Proje Başarıyla Oluşturuldu![/bold green]\n")
        
        # Proje tablosu
        table = Table(title="📊 Proje Özeti", border_style="green")
        table.add_column("Özellik", style="cyan")
        table.add_column("Değer", style="white")
        
        table.add_row("Proje Adı", project_config.name)
        table.add_row("Tip", project_config.type)
        table.add_row("Teknolojiler", ", ".join(project_config.tech_stack))
        table.add_row("Özellikler", ", ".join(project_config.features))
        table.add_row("Konum", str(self.current_dir))
        
        self.console.print(table)
        
        # Oluşturulan dosyalar
        self.console.print("\n[bold blue]📁 Oluşturulan Dosyalar:[/bold blue]")
        for expert_type, response in responses.items():
            self.console.print(f"\n[cyan]{expert_type.title()} Uzmanı:[/cyan]")
            for file_struct in response.code_files:
                self.console.print(f"  📄 {expert_type}/{file_struct.path}")
        
        # Sonraki adımlar
        self.console.print("\n[bold yellow]🚀 Sonraki Adımlar:[/bold yellow]")
        self.console.print("1. Proje klasörünü IDE'nizde açın")
        self.console.print("2. Bağımlılıkları yükleyin")
        self.console.print("3. Konfigürasyon dosyalarını düzenleyin")
        self.console.print("4. Uygulamayı çalıştırın")
        self.console.print(f"\n[green]💡 Proje konumu: {self.current_dir}[/green]")
    
    def display_help(self):
        """Yardım menüsü"""
        help_text = """
[bold blue]VibeCoding CLI - Kullanım Kılavuzu[/bold blue]

[bold]Komutlar:[/bold]
  vibe init [proje-adı]     Yeni proje oluştur
  vibe --help              Bu yardım menüsünü göster
  vibe --version           Versiyon bilgisi

[bold]Örnekler:[/bold]
  vibe init my-web-app     'my-web-app' adında yeni proje
  vibe init                İnteraktif proje oluşturma

[bold]Gereksinimler:[/bold]
  - Python 3.8+
  - DeepSeek veya Gemini API anahtarı
  - .env dosyasında API anahtarları

[bold]API Anahtarları:[/bold]
  DEEPSEEK_API_KEY=your_key
  GEMINI_API_KEY=your_key

[bold]Desteklenen Proje Tipleri:[/bold]
  - web        Web uygulaması
  - api        RESTful API
  - mobile     Mobil uygulama
  - desktop    Masaüstü uygulaması
  - fullstack  Tam yığın uygulama
        """
        
        panel = Panel(help_text, border_style="blue", padding=(1, 2))
        self.console.print(panel)
    
    async def run_full_system(self):
        """Tam VibeCoding AI sistemini başlat"""
        # VibeCoding AI System'i import et ve başlat
        from vibe_coding_ai_system import VibeCodingAISystem
        
        ai_system = VibeCodingAISystem()
        await ai_system.run()

def main():
    """Ana CLI fonksiyonu"""
    parser = argparse.ArgumentParser(
        description="VibeCoding CLI - Terminal Tabanlı AI Geliştirme Aracı",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command", 
        nargs="?", 
        choices=["init"],
        help="Komut (init: yeni proje oluştur)"
    )
    
    parser.add_argument(
        "project_name",
        nargs="?",
        help="Proje adı (isteğe bağlı)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="VibeCoding CLI 1.0.0"
    )
    
    args = parser.parse_args()
    
    cli = VibeCodingCLI()
    
    # Komut yok ise tam AI sistemini başlat
    if not args.command:
        asyncio.run(cli.run_full_system())
        return
    
    # Init komutu
    if args.command == "init":
        cli.display_banner()
        asyncio.run(cli.init_project(args.project_name))

if __name__ == "__main__":
    main() 