#!/usr/bin/env python3
"""
VibeCoding CLI - Hızlı Kurulum
Basit ve hızlı kurulum için
"""

import subprocess
import sys
from pathlib import Path

def install_package(package):
    """Tek paketi kur"""
    try:
        print(f"📦 {package} kuruluyor...")
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", package, "--quiet"
        ])
        print(f"✅ {package} kuruldu")
        return True
    except:
        print(f"❌ {package} kurulamadı")
        return False

def main():
    print("🚀 VibeCoding CLI - Hızlı Kurulum")
    print("=" * 40)
    
    # Temel paketleri kur
    packages = [
        "rich>=13.0.0",
        "python-dotenv>=1.0.0", 
        "pydantic>=2.0.0",
        "pydantic-ai>=0.0.13",
        "httpx>=0.25.0",
        "google-generativeai>=0.3.0"
    ]
    
    print(f"📦 {len(packages)} paket kurulacak...")
    
    failed = []
    for pkg in packages:
        if not install_package(pkg):
            failed.append(pkg)
    
    if failed:
        print(f"\n⚠️ Kurulamayan: {', '.join(failed)}")
    
    # VibeCoding CLI'yi kur
    print("\n🔧 VibeCoding CLI kuruluyor...")
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-e", ".", "--quiet"
        ])
        print("✅ VibeCoding CLI kuruldu")
    except:
        print("❌ VibeCoding CLI kurulamadı")
        return False
    
    # Test
    print("\n🧪 Test ediliyor...")
    try:
        result = subprocess.run(["vibe", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("🎉 KURULUM BAŞARILI!")
            print("✅ vibe komutu çalışıyor")
            print("\n📋 Kullanım:")
            print("vibe init my-project")
            return True
        else:
            print("❌ vibe komutu çalışmıyor")
            return False
    except:
        print("❌ Test başarısız")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n🆘 Sorun yaşıyorsanız:")
        print("python install_vibe_cli_debug.py")
        print("komutunu deneyin")
        sys.exit(1) 