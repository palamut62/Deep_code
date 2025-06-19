#!/usr/bin/env python3
"""
VibeCoding CLI - Hızlı Test
"""

import sys
from pathlib import Path

print("🧪 VibeCoding CLI - Hızlı Test")
print("=" * 40)

# 1. Dosya varlığı kontrolü
files_to_check = [
    "vibe_cli.py",
    "vibe_coding_ai_system.py", 
    "setup.py",
    "install_vibe_cli.py",
    "requirements.txt"
]

print("\n📁 Dosya Kontrolleri:")
for file in files_to_check:
    if Path(file).exists():
        print(f"✅ {file}")
    else:
        print(f"❌ {file}")

# 2. Import testleri
print("\n📦 Import Testleri:")

try:
    from rich.console import Console
    print("✅ rich")
except ImportError:
    print("❌ rich")

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv")
except ImportError:
    print("❌ python-dotenv")

try:
    import asyncio
    print("✅ asyncio")
except ImportError:
    print("❌ asyncio")

# 3. CLI modül testi
print("\n🔧 CLI Modül Testi:")
try:
    sys.path.append(str(Path.cwd()))
    from vibe_cli import VibeCodingCLI
    cli = VibeCodingCLI()
    print("✅ VibeCodingCLI sınıfı oluşturuldu")
    print(f"📁 Global config: {cli.global_config_dir}")
except Exception as e:
    print(f"❌ CLI modül hatası: {e}")

print("\n�� Test tamamlandı!") 