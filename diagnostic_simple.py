# diagnostic_simple.py
import sys
import os

print(f"Python: {sys.version}")
print(f"Chemin: {sys.executable}")
print(f"Répertoire: {os.getcwd()}")

try:
    import psutil
    print(f"✅ psutil: {psutil.__version__}")
except ImportError as e:
    print(f"❌ psutil: {e}")
    print("👉 Solution: pip install psutil")

print(f"Environnement virtuel: {'venv' in sys.executable}")
