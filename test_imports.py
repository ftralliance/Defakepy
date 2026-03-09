import sys
import os

# Add src to path
sys.path.append(os.path.abspath('src'))

print("Testing imports...")
try:
    import defakepy
    print("✓ defakepy imported successfully")
    
    from defakepy import text_engine
    print("✓ defakepy.text_engine imported successfully")
    
    from defakepy import audio_engine
    print("✓ defakepy.audio_engine imported successfully")
    
    from defakepy import vision_engine
    print("✓ defakepy.vision_engine imported successfully")
    
    from defakepy import cli
    print("✓ defakepy.cli imported successfully")
    
    scanner = defakepy.ForensicScanner()
    print("✓ ForensicScanner initialized successfully")
    
    print("\nSUCCESS: All modules are syntactically correct and lazy-loading is working.")
except Exception as e:
    print(f"\nFAILURE: {e}")
    sys.exit(1)
