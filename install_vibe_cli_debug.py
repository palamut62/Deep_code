#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VibeCoding CLI - Debug Kurulum Script'i
Her adımı gösterir ve hataları yakalar
"""

import os
import sys
import subprocess
import platform
from pathlib import Path
import time

def print_step(step_name, step_num, total_steps):
    """Adım bilgisini yazdır"""
    print(f"\n{'='*60}")
    print(f"📋 ADIM {step_num}/{total_steps}: {step_name}")
    print(f"{'='*60}")

def run_command_with_output(command, description):
    """Komutu çalıştır ve çıktıyı göster"""
    print(f"\n🔧 {description}")
    print(f"💻 Komut: {' '.join(command)}")
    
    try:
        # Komutu çalıştır ve çıktıyı gerçek zamanlı göster
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Çıktıyı satır satır göster
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(f"  📤 {output.strip()}")
        
        return_code = process.poll()
        
        if return_code == 0:
            print(f"✅ {description} - BAŞARILI")
            return True
        else:
            print(f"❌ {description} - BAŞARISIZ (kod: {return_code})")
            return False
            
    except Exception as e:
        print(f"❌ Hata: {e}")
        return False

def main():
    """Ana kurulum fonksiyonu"""
    print("🚀 VibeCoding CLI - Debug Kurulum")
    print("Her adım detaylı olarak gösterilecek...")
    
    total_steps = 5
    
    # ADIM 1: Python ve pip kontrolü
    print_step("Sistem Kontrolleri", 1, total_steps)
    
    print("🔍 Python versiyonu:")
    print(f"  📍 Python: {sys.version}")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ gerekli!")
        return False
    else:
        print("✅ Python versiyonu uygun")
    
    # pip kontrolü
    pip_success = run_command_with_output(
        [sys.executable, "-m", "pip", "--version"],
        "pip versiyonu kontrol ediliyor"
    )
    
    if not pip_success:
        print("❌ pip bulunamadı!")
        return False
    
    # ADIM 2: pip güncelleme
    print_step("pip Güncelleme", 2, total_steps)
    
    pip_upgrade_success = run_command_with_output(
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
        "pip güncelleniyor"
    )
    
    if not pip_upgrade_success:
        print("⚠️ pip güncellenemedi, devam ediliyor...")
    
    # ADIM 3: Requirements kurulumu
    print_step("Bağımlılık Kurulumu", 3, total_steps)
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ requirements.txt bulunamadı!")
        return False
    
    print("📦 requirements.txt içeriği:")
    with open(req_file, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            print(f"  {line_num:2d}: {line.strip()}")
    
    # Her paketi tek tek kur
    with open(req_file, "r", encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
    
    print(f"\n📦 {len(requirements)} paket kurulacak:")
    
    failed_packages = []
    for i, package in enumerate(requirements, 1):
        print(f"\n📦 Paket {i}/{len(requirements)}: {package}")
        
        success = run_command_with_output(
            [sys.executable, "-m", "pip", "install", package],
            f"{package} kuruluyor"
        )
        
        if not success:
            failed_packages.append(package)
            print(f"⚠️ {package} kurulamadı, devam ediliyor...")
        
        time.sleep(0.5)  # Kısa bekleme
    
    if failed_packages:
        print(f"\n⚠️ Kurulamayan paketler: {', '.join(failed_packages)}")
        print("Devam ediliyor...")
    
    # ADIM 4: VibeCoding CLI kurulumu
    print_step("VibeCoding CLI Kurulumu", 4, total_steps)
    
    vibe_install_success = run_command_with_output(
        [sys.executable, "-m", "pip", "install", "-e", "."],
        "VibeCoding CLI kuruluyor (editable mode)"
    )
    
    if not vibe_install_success:
        print("❌ VibeCoding CLI kurulamadı!")
        return False
    
    # ADIM 5: Test
    print_step("Kurulum Testi", 5, total_steps)
    
    test_success = run_command_with_output(
        ["vibe", "--version"],
        "vibe komutu test ediliyor"
    )
    
    if test_success:
        print("\n🎉 KURULUM BAŞARILI!")
        print("✅ VibeCoding CLI kullanıma hazır")
        print("\n📋 Sonraki adımlar:")
        print("1. API anahtarlarınızı ayarlayın")
        print("2. vibe init my-project komutu ile test edin")
        return True
    else:
        print("\n❌ KURULUM BAŞARISIZ!")
        print("vibe komutu çalışmıyor")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            print("\n🆘 Sorun giderme:")
            print("1. Python 3.8+ yüklü olduğundan emin olun")
            print("2. İnternet bağlantınızı kontrol edin")
            print("3. Antivirus yazılımınızı geçici olarak kapatın")
            print("4. Yönetici olarak çalıştırmayı deneyin")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Kurulum kullanıcı tarafından durduruldu")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Beklenmeyen hata: {e}")
        sys.exit(1) 