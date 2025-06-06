#!/usr/bin/env python3
"""
Test minimal pour diagnostiquer les problèmes
"""

def test_basic_imports():
    """Test des imports de base"""
    print("🔍 Test des imports de base...")
    
    try:
        import sys
        import os
        import platform
        print(f"✅ Python {sys.version}")
        print(f"✅ Système: {platform.system()}")
        
        import psutil
        print(f"✅ psutil {psutil.__version__}")
        
        from dataclasses import dataclass, field
        print("✅ dataclasses importé")
        
        return True
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_dataclass():
    """Test simple des dataclasses"""
    print("\n🧪 Test des dataclasses...")
    
    try:
        from dataclasses import dataclass, field
        
        @dataclass
        class TestClass:
            name: str = "test"
            value: int = 42
        
        test_obj = TestClass()
        print(f"✅ Dataclass créée: {test_obj.name}, {test_obj.value}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur dataclass: {e}")
        return False

def test_resource_manager_only():
    """Test du resource manager seul"""
    print("\n🖥️  Test du resource manager...")
    
    try:
        # Import direct
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        from ecoagent.core.resource_manager import ResourceManager
        
        rm = ResourceManager()
        print("✅ Resource Manager créé")
        print(rm.get_system_summary())
        return True
        
    except Exception as e:
        print(f"❌ Erreur resource manager: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🚀 EcoAgent - Test Minimal")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_dataclass,
        test_resource_manager_only
    ]
    
    for test in tests:
        success = test()
        if not success:
            print(f"\n❌ Arrêt à cause de l'échec du test: {test.__name__}")
            break
        print()
    else:
        print("🎉 Tous les tests minimaux passent !")

if __name__ == "__main__":
    main()
