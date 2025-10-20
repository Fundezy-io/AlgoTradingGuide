#!/usr/bin/env python3
"""
Setup Verification Script for Fundezy AlgoTradingGuide
=====================================================

This script verifies that your development environment is properly set up
for working with the Fundezy trading platform.

Run this script to check:
- Python dependencies
- Environment configuration
- File structure
- Basic imports

Usage: python verify_setup.py
"""

import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.7+")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    required_packages = {
        'requests': 'HTTP requests library',
        'pandas': 'Data manipulation library', 
        'numpy': 'Numerical computing library',
        'dotenv': 'Environment variable loader'
    }
    
    missing_packages = []
    
    for package, description in required_packages.items():
        try:
            if package == 'dotenv':
                import dotenv
                module_name = 'python-dotenv'
            else:
                __import__(package)
                module_name = package
            print(f"✅ {module_name} - {description}")
        except ImportError:
            print(f"❌ {package} - {description} (MISSING)")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("   Run: pip3 install -r requirements.txt")
        return False
    
    return True

def check_file_structure():
    """Check if all required files are present"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        'fundezy_trading_client.py',
        'config.py', 
        'algorithm_template.py',
        'test_connection.py',
        'quick_test_bot.py',
        'requirements.txt',
        '.env.example',
        '.env'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} (MISSING)")
            missing_files.append(file)
    
    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    
    return True

def check_environment_config():
    """Check environment configuration"""
    print("\n⚙️  Checking environment configuration...")
    
    try:
        import config
        
        # Check if environment variables are loaded
        if hasattr(config, 'FTP_EMAIL') and hasattr(config, 'FTP_PASSWORD'):
            print("✅ Configuration module loaded successfully")
            
            # Check if credentials are set (not default values)
            if config.FTP_EMAIL == "your-email@example.com":
                print("⚠️  Email not configured (still using default)")
                print("   Edit .env file and set FTP_EMAIL=your-actual-email@example.com")
            else:
                print(f"✅ Email configured: {config.FTP_EMAIL}")
            
            if config.FTP_PASSWORD == "your-password":
                print("⚠️  Password not configured (still using default)")
                print("   Edit .env file and set FTP_PASSWORD=your-actual-password")
            else:
                print("✅ Password configured (hidden)")
            
            print(f"✅ API Base URL: {config.FTP_API_BASE_URL}")
            print(f"✅ Broker ID: {config.FTP_BROKER_ID}")
            
            return True
            
        else:
            print("❌ Configuration module missing required attributes")
            return False
            
    except ImportError as e:
        print(f"❌ Cannot import config module: {e}")
        return False

def check_trading_client():
    """Check if trading client can be imported"""
    print("\n🔌 Checking trading client...")
    
    try:
        from fundezy_trading_client import FundezyTradingClient
        print("✅ FundezyTradingClient imported successfully")
        
        # Try to create client instance
        client = FundezyTradingClient()
        print("✅ Trading client instance created")
        
        return True
        
    except ImportError as e:
        print(f"❌ Cannot import FundezyTradingClient: {e}")
        return False
    except Exception as e:
        print(f"❌ Error creating trading client: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🚀 Fundezy AlgoTradingGuide Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python_version,
        check_dependencies,
        check_file_structure,
        check_environment_config,
        check_trading_client
    ]
    
    passed = 0
    total = len(checks)
    
    for check in checks:
        if check():
            passed += 1
        print()  # Add spacing between checks
    
    print("=" * 50)
    print(f"📊 Verification Results: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Setup verification completed successfully!")
        print("\n🚀 Next steps:")
        print("   1. Edit .env file with your Fundezy credentials")
        print("   2. Run: python test_connection.py")
        print("   3. Run: python quick_test_bot.py")
        print("   4. Start building your algorithm!")
    else:
        print("⚠️  Some issues found. Please fix them before proceeding.")
        print("   Check the error messages above for guidance.")

if __name__ == "__main__":
    main()