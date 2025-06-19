#!/usr/bin/env python3
"""
PromptCraft AI - VibeCoding Terminal Uygulaması
Doğal dildeki metinleri yapay zeka için etkili promptlara dönüştürür.
"""

import os
import sys
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.live import Live
import requests
import google.generativeai as genai
import getpass
import time
import threading

# Environment variables yükle
load_dotenv()

class PromptCraftApp:
    """PromptCraft AI - VibeCoding mantığı ile çalışan ana uygulama sınıfı"""
    
    def __init__(self):
        """Uygulamayı başlat ve konfigürasyonu yükle"""
        self.console = Console()
        self.debug_mode = os.getenv('DEBUG', 'false').lower() == 'true'
        self.default_provider = os.getenv('DEFAULT_AI_PROVIDER', 'deepseek')
        
        # API anahtarlarını kontrol et
        self.deepseek_api_key = os.getenv('DEEPSEEK_API_KEY')
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # İlk kurulum kontrolü
        if not self.deepseek_api_key and not self.gemini_api_key:
            self.first_time_setup()
        
        # Gemini API'yi yapılandır
        if self.gemini_api_key:
            genai.configure(api_key=self.gemini_api_key)
        
        self.vibe_coding_prompts = {
            "analiz": """Sen bir VibeCoding uzmanısın. Aşağıdaki doğal dil metnini analiz et ve yapay zeka için optimize edilmiş bir prompt haline getir.

VibeCoding Kuralları:
1. Net ve spesifik talimatlar ver
2. Bağlamı açıkça belirt
3. Beklenen çıktı formatını tanımla
4. Örnekler kullan
5. Adım adım yaklaşım benimse

Analiz edilecek metin: {user_input}

Lütfen bu metni etkili bir AI promptuna dönüştür ve neden bu şekilde yapılandırdığını açıkla.""",
            
            "optimizasyon": """Aşağıdaki promptu VibeCoding prensipleri doğrultusunda optimize et:

Mevcut Prompt: {user_input}

Optimizasyon kriterleri:
- Belirsizlikleri gider
- Spesifik talimatlar ekle
- Çıktı formatını netleştir
- Bağlam bilgisi güçlendir
- Performans odaklı yapı kur

Optimize edilmiş versiyonu ve değişikliklerin açıklamasını ver.""",
            
            "template": """Şu konu için VibeCoding standardında bir prompt şablonu oluştur: {user_input}

Şablon şunları içermeli:
- Rol tanımı
- Görev açıklaması
- Bağlam bilgisi
- Çıktı formatı
- Kalite kriterleri
- Örnek kullanım

Kullanılabilir ve yeniden düzenlenebilir bir şablon hazırla."""
        }
    
    def debug_log(self, message: str, context: str = "MAIN") -> None:
        """Debug mesajlarını kontrollü şekilde yazdır"""
        if self.debug_mode:
            self.console.print(f"[DEBUG][{context}] {message}", style="dim yellow")
    
    def first_time_setup(self) -> None:
        """İlk kurulum - API anahtarlarını al ve test et"""
        self.console.clear()
        
        # Hoş geldin mesajı
        welcome_text = Text()
        welcome_text.append("🎉 PromptCraft AI'ye Hoş Geldiniz!\n", style="bold blue")
        welcome_text.append("İlk kullanım için API anahtarlarınızı ayarlayalım.\n", style="cyan")
        welcome_text.append("En az bir AI sağlayıcısı gereklidir.", style="yellow")
        
        panel = Panel(welcome_text, title="🚀 İlk Kurulum", border_style="blue", padding=(1, 2))
        self.console.print(panel)
        
        # API sağlayıcı bilgileri
        info_table = Table(title="🤖 Desteklenen AI Sağlayıcıları", border_style="green")
        info_table.add_column("Sağlayıcı", style="bold cyan")
        info_table.add_column("Website", style="blue")
        info_table.add_column("Ücretsiz", style="green")
        
        info_table.add_row("DeepSeek", "https://platform.deepseek.com", "✅ Evet")
        info_table.add_row("Gemini", "https://makersuite.google.com/app/apikey", "✅ Evet")
        
        self.console.print(info_table)
        self.console.print()
        
        # API anahtarlarını al
        api_keys_entered = False
        
        while not api_keys_entered:
            self.console.print("📝 API anahtarlarınızı girin (Enter ile geç):\n", style="bold")
            
            # DeepSeek API
            deepseek_key = getpass.getpass("🔑 DeepSeek API Key: ").strip()
            if deepseek_key:
                self.console.print("✅ DeepSeek API anahtarı alındı", style="green")
            
            # Gemini API  
            gemini_key = getpass.getpass("🔑 Gemini API Key: ").strip()
            if gemini_key:
                self.console.print("✅ Gemini API anahtarı alındı", style="green")
            
            # En az bir anahtar kontrolü
            if not deepseek_key and not gemini_key:
                self.console.print("❌ En az bir API anahtarı girmelisiniz!", style="red")
                if not Confirm.ask("Tekrar denemek ister misiniz?"):
                    self.console.print("👋 PromptCraft AI kapatılıyor...", style="yellow")
                    sys.exit(0)
                continue
            
            # API anahtarlarını test et
            self.console.print("\n🧪 API anahtarları test ediliyor...\n", style="yellow")
            
            valid_keys = {}
            test_prompt = "Merhaba, bu bir test mesajıdır. Sadece 'Test başarılı!' yanıtı ver."
            
            # Progress bar oluştur
            progress = Progress(
                SpinnerColumn("dots12", style="cyan"),
                TextColumn("[bold blue]{task.description}"),
                TimeElapsedColumn(),
                console=self.console,
                transient=True
            )
            
            with progress:
                # DeepSeek test
                if deepseek_key:
                    temp_deepseek_key = self.deepseek_api_key
                    self.deepseek_api_key = deepseek_key
                    
                    task = progress.add_task("🔍 DeepSeek API test ediliyor...", total=None)
                    result = self.call_deepseek_api_animated(test_prompt, progress, task)
                    if result:
                        self.console.print("✅ DeepSeek API çalışıyor!", style="green")
                        valid_keys['DEEPSEEK_API_KEY'] = deepseek_key
                    else:
                        self.console.print("❌ DeepSeek API geçersiz!", style="red")
                    
                    self.deepseek_api_key = temp_deepseek_key
                
                # Gemini test
                if gemini_key:
                    temp_gemini_key = self.gemini_api_key
                    self.gemini_api_key = gemini_key
                    
                    try:
                        genai.configure(api_key=gemini_key)
                        task = progress.add_task("🔍 Gemini API test ediliyor...", total=None)
                        result = self.call_gemini_api_animated(test_prompt, progress, task)
                        if result:
                            self.console.print("✅ Gemini API çalışıyor!", style="green")
                            valid_keys['GEMINI_API_KEY'] = gemini_key
                        else:
                            self.console.print("❌ Gemini API geçersiz!", style="red")
                    except:
                        self.console.print("❌ Gemini API geçersiz!", style="red")
                    
                    self.gemini_api_key = temp_gemini_key
            
            # Geçerli anahtar kontrolü
            if not valid_keys:
                self.console.print("\n❌ Hiçbir API anahtarı çalışmıyor!", style="red")
                self.console.print("💡 API anahtarlarınızı kontrol edin ve tekrar deneyin.", style="yellow")
                if not Confirm.ask("Tekrar denemek ister misiniz?"):
                    self.console.print("👋 PromptCraft AI kapatılıyor...", style="yellow")
                    sys.exit(0)
                continue
            
            # .env dosyasını güncelle
            self.save_api_keys(valid_keys)
            
            # Başarı mesajı
            self.console.print(f"\n🎉 Kurulum tamamlandı!", style="bold green")
            self.console.print(f"✅ {len(valid_keys)} API anahtarı kaydedildi", style="green")
            
            # Varsayılan sağlayıcıyı belirle
            if 'DEEPSEEK_API_KEY' in valid_keys:
                self.default_provider = 'deepseek'
                self.deepseek_api_key = valid_keys['DEEPSEEK_API_KEY']
            elif 'GEMINI_API_KEY' in valid_keys:
                self.default_provider = 'gemini'
                self.gemini_api_key = valid_keys['GEMINI_API_KEY']
                genai.configure(api_key=self.gemini_api_key)
            
            self.console.print(f"🤖 Varsayılan AI: {self.default_provider.upper()}", style="cyan")
            
            input("\nEnter tuşuna basarak devam edin...")
            api_keys_entered = True
    
    def save_api_keys(self, api_keys: dict) -> None:
        """API anahtarlarını .env dosyasına kaydet"""
        try:
            # Mevcut .env dosyasını oku
            env_content = {}
            if os.path.exists('.env'):
                with open('.env', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            env_content[key.strip()] = value.strip()
            
            # Yeni API anahtarlarını ekle
            for key, value in api_keys.items():
                env_content[key] = value
            
            # Varsayılan sağlayıcıyı ayarla
            if 'DEEPSEEK_API_KEY' in api_keys:
                env_content['DEFAULT_AI_PROVIDER'] = 'deepseek'
            elif 'GEMINI_API_KEY' in api_keys:
                env_content['DEFAULT_AI_PROVIDER'] = 'gemini'
            
            # Debug modunu ayarla (eğer yoksa)
            if 'DEBUG' not in env_content:
                env_content['DEBUG'] = 'false'
            
            # .env dosyasını yaz
            with open('.env', 'w', encoding='utf-8') as f:
                f.write("# PromptCraft AI - API Anahtarları\n")
                f.write("# Bu dosya otomatik oluşturulmuştur\n\n")
                
                f.write("# API Anahtarları\n")
                if 'DEEPSEEK_API_KEY' in env_content:
                    f.write(f"DEEPSEEK_API_KEY={env_content['DEEPSEEK_API_KEY']}\n")
                else:
                    f.write("DEEPSEEK_API_KEY=\n")
                
                if 'GEMINI_API_KEY' in env_content:
                    f.write(f"GEMINI_API_KEY={env_content['GEMINI_API_KEY']}\n")
                else:
                    f.write("GEMINI_API_KEY=\n")
                
                f.write(f"\n# Varsayılan AI Sağlayıcısı\n")
                f.write(f"DEFAULT_AI_PROVIDER={env_content.get('DEFAULT_AI_PROVIDER', 'deepseek')}\n")
                
                f.write(f"\n# Debug Modu\n")
                f.write(f"DEBUG={env_content.get('DEBUG', 'false')}\n")
            
            self.console.print("💾 API anahtarları kaydedildi!", style="green")
            
        except Exception as e:
            self.console.print(f"❌ API anahtarları kaydedilemedi: {str(e)}", style="red")
            self.debug_log(f"API kaydetme hatası: {str(e)}", "ERROR")
    
    def display_welcome(self) -> None:
        """Karşılama mesajını ve ana menüyü göster"""
        # Ana başlık
        title_text = Text()
        title_text.append("⚡ ", style="bold yellow")
        title_text.append("PromptCraft", style="bold blue")
        title_text.append(" AI", style="bold cyan")
        
        subtitle_text = Text()
        subtitle_text.append("Doğal dildeki fikirlerinizi güçlü AI promptlarına dönüştürün", style="dim cyan")
        
        # Sistem bilgileri
        info_text = Text()
        info_text.append(f"🤖 AI Sağlayıcısı: ", style="white")
        info_text.append(f"{self.default_provider.upper()}", style="bold green")
        info_text.append(f" | 🔧 VibeCoding v1.0", style="dim white")
        
        welcome_content = Text()
        welcome_content.append(title_text)
        welcome_content.append("\n")
        welcome_content.append(subtitle_text)
        welcome_content.append("\n\n")
        welcome_content.append(info_text)
        
        panel = Panel(welcome_content, title="🎯 PromptCraft AI Studio", border_style="blue", padding=(1, 2))
        self.console.print(panel)
        
        # Ana menü seçeneklerini göster
        self.display_main_menu()
    
    def display_main_menu(self) -> None:
        """Ana menü seçeneklerini göster"""
        self.console.print("\n")
        
        # Ana özellikler
        features_table = Table(title="🎯 Ana Özellikler", border_style="green", show_header=True, header_style="bold green")
        features_table.add_column("Seçenek", style="bold cyan", width=12)
        features_table.add_column("Açıklama", style="white")
        features_table.add_column("Örnek", style="dim yellow")
        
        features_table.add_row(
            "1", 
            "🔍 Doğal Dil Analizi", 
            "Metninizi AI promptuna dönüştür"
        )
        features_table.add_row(
            "2", 
            "⚡ Prompt Optimizasyonu", 
            "Mevcut promptunuzu güçlendirin"
        )
        features_table.add_row(
            "3", 
            "📋 Şablon Oluşturma", 
            "Yeniden kullanılabilir şablonlar"
        )
        
        self.console.print(features_table)
        
        # Ayarlar ve yardım
        settings_table = Table(title="⚙️ Ayarlar & Yardım", border_style="yellow", show_header=True, header_style="bold yellow")
        settings_table.add_column("Seçenek", style="bold cyan", width=12)
        settings_table.add_column("Açıklama", style="white")
        
        settings_table.add_row("s", "🔄 AI Sağlayıcısı Değiştir")
        settings_table.add_row("t", "🧪 API Bağlantılarını Test Et")
        settings_table.add_row("r", "🔄 API Anahtarlarını Sıfırla")
        settings_table.add_row("h", "❓ Yardım & Komutlar")
        settings_table.add_row("q", "👋 Çıkış")
        
        self.console.print(settings_table)
    
    def display_menu(self) -> None:
        """Eski menü formatını göster (help komutu için)"""
        table = Table(title="📋 Tüm Komutlar", border_style="cyan")
        table.add_column("Komut", style="bold green")
        table.add_column("Kısayol", style="bold cyan")
        table.add_column("Açıklama", style="white")
        
        table.add_row("analiz", "1", "Doğal dil metnini AI promptuna dönüştür")
        table.add_row("optimizasyon", "2", "Mevcut promptu optimize et")
        table.add_row("template", "3", "Belirli bir konu için prompt şablonu oluştur")
        table.add_row("provider", "s", "AI sağlayıcısını değiştir (deepseek/gemini)")
        table.add_row("test", "t", "API bağlantılarını test et")
        table.add_row("reset", "r", "API anahtarlarını sıfırla")
        table.add_row("help", "h", "Yardım menüsünü göster")
        table.add_row("exit", "q", "Uygulamadan çık")
        
        self.console.print(table)
    
    def call_deepseek_api(self, prompt: str) -> Optional[str]:
        """DeepSeek API'sini çağır"""
        if not self.deepseek_api_key:
            self.console.print("❌ DeepSeek API anahtarı bulunamadı!", style="red")
            self.console.print("💡 .env dosyasında DEEPSEEK_API_KEY değişkenini ayarlayın", style="yellow")
            return None
        
        self.debug_log("DeepSeek API çağrısı yapılıyor", "API")
        
        try:
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "PromptCraft-AI/1.0"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Sen yardımcı bir AI asistanısın. Türkçe yanıt ver."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }
            
            self.debug_log(f"API çağrısı yapılıyor: {len(prompt)} karakter", "API")
            
            # Yeniden deneme mekanizması
            for attempt in range(3):
                try:
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=60,  # Timeout artırıldı
                        verify=True
                    )
                    
                    self.debug_log(f"API yanıtı alındı: {response.status_code}", "API")
                    
                    if response.status_code == 200:
                        result = response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            self.debug_log(f"Başarılı yanıt: {len(content)} karakter", "API")
                            return content
                        else:
                            self.console.print("❌ DeepSeek API yanıtı beklenmeyen formatta!", style="red")
                            return None
                    
                    elif response.status_code == 401:
                        self.console.print("❌ DeepSeek API anahtarı geçersiz!", style="red")
                        self.console.print("💡 API anahtarınızı kontrol edin: https://platform.deepseek.com", style="yellow")
                        return None
                    
                    elif response.status_code == 429:
                        self.console.print(f"⚠️ DeepSeek API rate limit (deneme {attempt + 1}/3)", style="yellow")
                        if attempt < 2:
                            import time
                            time.sleep(2 ** attempt)  # Exponential backoff
                            continue
                        else:
                            self.console.print("❌ DeepSeek API rate limit aşıldı!", style="red")
                            return None
                    
                    elif response.status_code == 500:
                        self.console.print(f"⚠️ DeepSeek sunucu hatası (deneme {attempt + 1}/3)", style="yellow")
                        if attempt < 2:
                            import time
                            time.sleep(1)
                            continue
                        else:
                            self.console.print("❌ DeepSeek sunucu hatası devam ediyor!", style="red")
                            return None
                    
                    else:
                        error_msg = f"DeepSeek API Hatası: {response.status_code}"
                        try:
                            error_detail = response.json()
                            if "error" in error_detail:
                                error_msg += f" - {error_detail['error'].get('message', 'Bilinmeyen hata')}"
                        except:
                            pass
                        
                        self.console.print(f"❌ {error_msg}", style="red")
                        return None
                        
                except requests.exceptions.Timeout:
                    self.console.print(f"⚠️ DeepSeek API timeout (deneme {attempt + 1}/3)", style="yellow")
                    if attempt < 2:
                        continue
                    else:
                        self.console.print("❌ DeepSeek API bağlantı zaman aşımı!", style="red")
                        return None
                        
                except requests.exceptions.ConnectionError:
                    self.console.print(f"⚠️ DeepSeek API bağlantı hatası (deneme {attempt + 1}/3)", style="yellow")
                    if attempt < 2:
                        import time
                        time.sleep(1)
                        continue
                    else:
                        self.console.print("❌ DeepSeek API'ye bağlanılamıyor!", style="red")
                        self.console.print("💡 İnternet bağlantınızı kontrol edin", style="yellow")
                        return None
                        
        except Exception as e:
            self.console.print(f"❌ DeepSeek API Beklenmeyen Hata: {str(e)}", style="red")
            self.debug_log(f"DeepSeek API hata detayı: {str(e)}", "ERROR")
            return None
    
    def call_deepseek_api_animated(self, prompt: str, progress, task_id) -> Optional[str]:
        """Animasyonlu DeepSeek API çağrısı"""
        if not self.deepseek_api_key:
            progress.update(task_id, description="❌ DeepSeek API anahtarı bulunamadı!")
            time.sleep(1)
            return None
        
        try:
            progress.update(task_id, description="🔗 DeepSeek'e bağlanıyor...")
            time.sleep(0.3)
            
            headers = {
                "Authorization": f"Bearer {self.deepseek_api_key}",
                "Content-Type": "application/json",
                "User-Agent": "PromptCraft-AI/1.0"
            }
            
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "system", 
                        "content": "Sen yardımcı bir AI asistanısın. Türkçe yanıt ver."
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "temperature": 0.7,
                "max_tokens": 2000,
                "stream": False
            }
            
            progress.update(task_id, description="📤 İstek gönderiliyor...")
            time.sleep(0.2)
            
            # Yeniden deneme mekanizması
            for attempt in range(3):
                try:
                    if attempt > 0:
                        progress.update(task_id, description=f"🔄 Yeniden deneniyor... ({attempt + 1}/3)")
                        time.sleep(0.5)
                    
                    progress.update(task_id, description="⏳ DeepSeek yanıtı bekleniyor...")
                    
                    response = requests.post(
                        "https://api.deepseek.com/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=60,
                        verify=True
                    )
                    
                    if response.status_code == 200:
                        progress.update(task_id, description="✅ Yanıt alındı, işleniyor...")
                        time.sleep(0.2)
                        
                        result = response.json()
                        if "choices" in result and len(result["choices"]) > 0:
                            content = result["choices"][0]["message"]["content"]
                            progress.update(task_id, description="🎉 DeepSeek yanıtı hazır!")
                            time.sleep(0.3)
                            return content
                        else:
                            progress.update(task_id, description="❌ Yanıt formatı hatalı!")
                            time.sleep(1)
                            return None
                    
                    elif response.status_code == 401:
                        progress.update(task_id, description="❌ API anahtarı geçersiz!")
                        time.sleep(1)
                        return None
                    
                    elif response.status_code == 429:
                        progress.update(task_id, description=f"⏸️ Rate limit, bekleniyor... ({attempt + 1}/3)")
                        if attempt < 2:
                            time.sleep(2 ** attempt)
                            continue
                        else:
                            progress.update(task_id, description="❌ Rate limit aşıldı!")
                            time.sleep(1)
                            return None
                    
                    elif response.status_code == 500:
                        progress.update(task_id, description=f"🔧 Sunucu hatası, yeniden deneniyor... ({attempt + 1}/3)")
                        if attempt < 2:
                            time.sleep(1)
                            continue
                        else:
                            progress.update(task_id, description="❌ Sunucu hatası devam ediyor!")
                            time.sleep(1)
                            return None
                    
                    else:
                        progress.update(task_id, description=f"❌ API Hatası: {response.status_code}")
                        time.sleep(1)
                        return None
                        
                except requests.exceptions.Timeout:
                    progress.update(task_id, description=f"⏰ Bağlantı zaman aşımı ({attempt + 1}/3)")
                    if attempt < 2:
                        time.sleep(1)
                        continue
                    else:
                        progress.update(task_id, description="❌ Bağlantı zaman aşımı!")
                        time.sleep(1)
                        return None
                        
                except requests.exceptions.ConnectionError:
                    progress.update(task_id, description=f"🌐 Bağlantı hatası ({attempt + 1}/3)")
                    if attempt < 2:
                        time.sleep(1)
                        continue
                    else:
                        progress.update(task_id, description="❌ İnternet bağlantısı hatası!")
                        time.sleep(1)
                        return None
                        
        except Exception as e:
            progress.update(task_id, description=f"❌ Beklenmeyen hata!")
            time.sleep(1)
            return None
    
    def call_gemini_api(self, prompt: str) -> Optional[str]:
        """Gemini API'sini çağır"""
        if not self.gemini_api_key:
            self.console.print("❌ Gemini API anahtarı bulunamadı!", style="red")
            return None
        
        self.debug_log("Gemini API çağrısı yapılıyor", "API")
        
        try:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            self.console.print(f"❌ Gemini API Hatası: {str(e)}", style="red")
            return None
    
    def call_gemini_api_animated(self, prompt: str, progress, task_id) -> Optional[str]:
        """Animasyonlu Gemini API çağrısı"""
        if not self.gemini_api_key:
            progress.update(task_id, description="❌ Gemini API anahtarı bulunamadı!")
            time.sleep(1)
            return None
        
        try:
            progress.update(task_id, description="🔗 Gemini'ye bağlanıyor...")
            time.sleep(0.3)
            
            progress.update(task_id, description="⚙️ Gemini modeli hazırlanıyor...")
            time.sleep(0.2)
            
            model = genai.GenerativeModel('gemini-pro')
            
            progress.update(task_id, description="📤 İstek gönderiliyor...")
            time.sleep(0.2)
            
            progress.update(task_id, description="⏳ Gemini yanıtı bekleniyor...")
            
            response = model.generate_content(prompt)
            
            progress.update(task_id, description="✅ Yanıt alındı, işleniyor...")
            time.sleep(0.2)
            
            if response.text:
                progress.update(task_id, description="🎉 Gemini yanıtı hazır!")
                time.sleep(0.3)
                return response.text
            else:
                progress.update(task_id, description="❌ Boş yanıt alındı!")
                time.sleep(1)
                return None
            
        except Exception as e:
            progress.update(task_id, description=f"❌ Gemini API hatası!")
            time.sleep(1)
            return None
    
    def get_ai_response_with_animation(self, prompt: str, provider: Optional[str] = None) -> Optional[str]:
        """Animasyonlu AI yanıtı alma"""
        active_provider = provider or self.default_provider
        
        # Progress bar ve spinner oluştur
        progress = Progress(
            SpinnerColumn("dots12", style="cyan"),
            TextColumn("[bold blue]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        )
        
        result = None
        
        with progress:
            # İlk sağlayıcıyı dene
            if active_provider == "deepseek":
                task = progress.add_task(f"🤖 DeepSeek AI ile işleniyor...", total=None)
                result = self.call_deepseek_api_animated(prompt, progress, task)
                
                if result is None and self.gemini_api_key:
                    progress.update(task, description="🔄 Gemini'ye geçiliyor...")
                    time.sleep(0.5)
                    progress.update(task, description="🤖 Gemini AI ile işleniyor...")
                    result = self.call_gemini_api_animated(prompt, progress, task)
                    
            elif active_provider == "gemini":
                task = progress.add_task(f"🤖 Gemini AI ile işleniyor...", total=None)
                result = self.call_gemini_api_animated(prompt, progress, task)
                
                if result is None and self.deepseek_api_key:
                    progress.update(task, description="🔄 DeepSeek'e geçiliyor...")
                    time.sleep(0.5)
                    progress.update(task, description="🤖 DeepSeek AI ile işleniyor...")
                    result = self.call_deepseek_api_animated(prompt, progress, task)
            else:
                self.console.print("❌ Geçersiz AI sağlayıcısı!", style="red")
                return None
        
        return result
    
    def get_ai_response(self, prompt: str, provider: Optional[str] = None) -> Optional[str]:
        """Seçilen AI sağlayıcısından yanıt al (eski versiyon - test için)"""
        return self.get_ai_response_with_animation(prompt, provider)
    
    def process_command(self, command: str) -> bool:
        """Kullanıcı komutunu işle"""
        command = command.strip().lower()
        
        # Çıkış komutları
        if command in ["exit", "quit", "q"]:
            self.console.print("👋 PromptCraft AI'dan ayrılıyorsunuz. İyi günler!", style="green")
            return False
        
        # Yardım komutları
        elif command in ["help", "h"]:
            self.display_menu()
            return True
        
        # Sağlayıcı değiştirme
        elif command in ["provider", "s"]:
            self.change_provider()
            return True
        
        # Ana özellikler - tam isim
        elif command in ["analiz", "optimizasyon", "template"]:
            self.handle_vibe_coding_task(command)
            return True
        
        # Ana özellikler - kısayol
        elif command == "1":
            self.handle_vibe_coding_task("analiz")
            return True
        elif command == "2":
            self.handle_vibe_coding_task("optimizasyon")
            return True
        elif command == "3":
            self.handle_vibe_coding_task("template")
            return True
        
        # Ana menüyü tekrar göster
        elif command in ["menu", "m"]:
            self.display_main_menu()
            return True
        
        # API test özelliği
        elif command in ["test", "t"]:
            self.test_api_connections()
            return True
        
        # API anahtarlarını sıfırla
        elif command in ["reset", "r"]:
            self.reset_api_keys()
            return True
        
        else:
            self.console.print("❌ Geçersiz seçenek!", style="red")
            self.console.print("💡 Kullanılabilir seçenekler: 1, 2, 3, s, t, r, h, q", style="yellow")
            self.console.print("   Veya 'h' yazarak tüm komutları görebilirsiniz.", style="dim")
            return True
    
    def test_api_connections(self) -> None:
        """API bağlantılarını test et"""
        self.console.print("\n🔍 API Bağlantıları Test Ediliyor...\n", style="bold cyan")
        
        test_prompt = "Merhaba, bu bir test mesajıdır. Kısaca 'Test başarılı!' yanıtı ver."
        
        # Progress bar oluştur
        progress = Progress(
            SpinnerColumn("dots12", style="cyan"),
            TextColumn("[bold blue]{task.description}"),
            TimeElapsedColumn(),
            console=self.console,
            transient=True
        )
        
        with progress:
            # DeepSeek testi
            if self.deepseek_api_key:
                task = progress.add_task("🧪 DeepSeek API test ediliyor...", total=None)
                result = self.call_deepseek_api_animated(test_prompt, progress, task)
                if result:
                    self.console.print("✅ DeepSeek API çalışıyor!", style="green")
                else:
                    self.console.print("❌ DeepSeek API çalışmıyor!", style="red")
            else:
                self.console.print("⚠️ DeepSeek API anahtarı bulunamadı", style="dim")
            
            # Gemini testi
            if self.gemini_api_key:
                task = progress.add_task("🧪 Gemini API test ediliyor...", total=None)
                result = self.call_gemini_api_animated(test_prompt, progress, task)
                if result:
                    self.console.print("✅ Gemini API çalışıyor!", style="green")
                else:
                    self.console.print("❌ Gemini API çalışmıyor!", style="red")
            else:
                self.console.print("⚠️ Gemini API anahtarı bulunamadı", style="dim")
        
        # Genel durum
        working_apis = []
        if self.deepseek_api_key:
            working_apis.append("DeepSeek")
        if self.gemini_api_key:
            working_apis.append("Gemini")
        
        if working_apis:
            self.console.print(f"\n📊 Kullanılabilir API'ler: {', '.join(working_apis)}", style="green")
        else:
            self.console.print("\n❌ Hiçbir API anahtarı bulunamadı!", style="red")
            self.console.print("💡 .env dosyasını düzenleyerek API anahtarlarınızı ekleyin", style="yellow")
    
    def reset_api_keys(self) -> None:
        """API anahtarlarını sıfırla ve yeniden ayarla"""
        self.console.print("\n🔄 API Anahtarlarını Sıfırlama\n", style="bold yellow")
        
        if not Confirm.ask("API anahtarlarınızı sıfırlamak ve yeniden ayarlamak istiyor musunuz?"):
            self.console.print("❌ İşlem iptal edildi.", style="yellow")
            return
        
        # .env dosyasını temizle
        try:
            if os.path.exists('.env'):
                os.remove('.env')
            self.console.print("🗑️ Mevcut API anahtarları silindi", style="yellow")
        except Exception as e:
            self.console.print(f"❌ .env dosyası silinemedi: {str(e)}", style="red")
        
        # Yeniden kurulum başlat
        self.deepseek_api_key = None
        self.gemini_api_key = None
        self.first_time_setup()
    
    def change_provider(self) -> None:
        """AI sağlayıcısını değiştir"""
        current_provider = self.default_provider
        available_providers = []
        
        if self.deepseek_api_key:
            available_providers.append("deepseek")
        if self.gemini_api_key:
            available_providers.append("gemini")
        
        if not available_providers:
            self.console.print("❌ Hiçbir AI sağlayıcısı yapılandırılmamış!", style="red")
            return
        
        if len(available_providers) == 1:
            self.console.print(f"ℹ️ Yalnızca {available_providers[0]} kullanılabilir.", style="yellow")
            return
        
        self.console.print(f"Mevcut sağlayıcı: {current_provider}")
        
        table = Table(title="Kullanılabilir AI Sağlayıcıları")
        table.add_column("Sağlayıcı", style="green")
        table.add_column("Durum", style="white")
        
        for provider in available_providers:
            status = "✅ Aktif" if provider == current_provider else "⚪ Kullanılabilir"
            table.add_row(provider, status)
        
        self.console.print(table)
        
        new_provider = Prompt.ask(
            "Yeni sağlayıcı seçin",
            choices=available_providers,
            default=current_provider
        )
        
        if new_provider != current_provider:
            self.default_provider = new_provider
            self.console.print(f"✅ AI sağlayıcısı {new_provider} olarak değiştirildi!", style="green")
    
    def handle_vibe_coding_task(self, task_type: str) -> None:
        """VibeCoding görevini işle"""
        task_descriptions = {
            "analiz": "Doğal dil metnini AI promptuna dönüştürme",
            "optimizasyon": "Mevcut promptu optimize etme", 
            "template": "Prompt şablonu oluşturma"
        }
        
        self.console.print(f"\n📝 {task_descriptions[task_type]} görevi başlatılıyor...", style="cyan")
        
        # Kullanıcıdan giriş al
        if task_type == "template":
            user_input = Prompt.ask("Hangi konu için şablon oluşturmak istiyorsunuz?")
        elif task_type == "optimizasyon":
            user_input = Prompt.ask("Optimize edilecek promptu girin")
        else:
            user_input = Prompt.ask("Analiz edilecek metni girin")
        
        if not user_input.strip():
            self.console.print("❌ Boş giriş! Lütfen geçerli bir metin girin.", style="red")
            return
        
        # Prompt hazırla ve AI'dan yanıt al
        vibe_prompt = self.vibe_coding_prompts[task_type].format(user_input=user_input)
        
        response = self.get_ai_response(vibe_prompt)
        
        if response:
            self.display_result(response, task_type)
            
            # Sonucu dosyaya kaydetme seçeneği
            if Confirm.ask("Bu sonucu dosyaya kaydetmek ister misiniz?"):
                self.save_result(response, task_type, user_input)
        else:
            self.console.print("❌ AI yanıtı alınamadı. Lütfen tekrar deneyin.", style="red")
    
    def display_result(self, result: str, task_type: str) -> None:
        """AI yanıtını güzel bir şekilde göster"""
        task_titles = {
            "analiz": "🔍 Analiz Sonucu",
            "optimizasyon": "⚡ Optimizasyon Sonucu",
            "template": "📋 Şablon Sonucu"
        }
        
        panel = Panel(
            result,
            title=task_titles[task_type],
            border_style="green",
            expand=False
        )
        
        self.console.print("\n")
        self.console.print(panel)
    
    def save_result(self, result: str, task_type: str, original_input: str) -> None:
        """Sonucu dosyaya kaydet"""
        import datetime
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"vibe_coding_{task_type}_{timestamp}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"VibeCoding {task_type.title()} Sonucu\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"Tarih: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Görev Türü: {task_type}\n")
                f.write(f"AI Sağlayıcısı: {self.default_provider}\n\n")
                f.write("Orijinal Giriş:\n")
                f.write("-" * 20 + "\n")
                f.write(original_input + "\n\n")
                f.write("AI Yanıtı:\n")
                f.write("-" * 20 + "\n")
                f.write(result)
            
            self.console.print(f"✅ Sonuç '{filename}' dosyasına kaydedildi!", style="green")
            
        except Exception as e:
            self.console.print(f"❌ Dosya kaydetme hatası: {str(e)}", style="red")
    
    def run(self) -> None:
        """Ana uygulama döngüsü"""
        self.display_welcome()
        self.console.print("\n")
        
        try:
            while True:
                command = Prompt.ask("PromptCraft", default="")
                
                if not self.process_command(command):
                    break
                    
                self.console.print()  # Boş satır ekle
                
        except KeyboardInterrupt:
            self.console.print("\n\n👋 PromptCraft AI kapatılıyor...", style="yellow")
        except Exception as e:
            self.console.print(f"\n❌ Beklenmeyen hata: {str(e)}", style="red")
            self.debug_log(f"Hata detayları: {str(e)}", "ERROR")

def main():
    """Ana fonksiyon"""
    app = PromptCraftApp()
    app.run()

if __name__ == "__main__":
    main() 