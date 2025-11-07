#!/usr/bin/env python3
"""
Setup Validation Script for LiteLLM Gateway
Verifies that the installation matches the official documentation at:
https://docs.litellm.ai/docs/
"""

import os
import sys
from pathlib import Path
import yaml

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"  ✅ {description}: {filepath}")
        return True
    else:
        print(f"  ❌ {description} NOT FOUND: {filepath}")
        return False

def check_dependencies():
    """Check if required Python packages are installed"""
    print("\n📦 Checking Python Dependencies...")
    
    required_packages = {
        'litellm': 'LiteLLM core package',
        'dotenv': 'Environment variable loader (python-dotenv)',
        'yaml': 'YAML configuration parser (pyyaml)',
        'openai': 'OpenAI SDK (for testing)',
    }
    
    all_installed = True
    for package, description in required_packages.items():
        try:
            __import__(package)
            print(f"  ✅ {description} ({package})")
        except ImportError:
            print(f"  ❌ {description} ({package}) NOT INSTALLED")
            all_installed = False
    
    return all_installed

def check_config_file():
    """Validate config.yaml structure"""
    print("\n📄 Validating config.yaml...")
    
    config_path = Path('config.yaml')
    if not config_path.exists():
        print("  ❌ config.yaml not found!")
        return False
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Check for required sections
        required_sections = ['model_list', 'litellm_settings', 'general_settings']
        all_valid = True
        
        for section in required_sections:
            if section in config:
                print(f"  ✅ Section '{section}' present")
            else:
                print(f"  ❌ Section '{section}' missing")
                all_valid = False
        
        # Check model_list
        if 'model_list' in config and isinstance(config['model_list'], list):
            print(f"  ✅ Found {len(config['model_list'])} model(s) configured")
            for model in config['model_list']:
                if 'model_name' in model and 'litellm_params' in model:
                    model_name = model['model_name']
                    provider = model['litellm_params'].get('model', 'unknown')
                    print(f"     • {model_name} → {provider}")
        
        # Check master_key
        if config.get('general_settings', {}).get('master_key'):
            print("  ✅ Master key configured (os.environ/LITELLM_MASTER_KEY)")
        else:
            print("  ⚠️  Master key not configured (authentication disabled)")
        
        return all_valid
        
    except yaml.YAMLError as e:
        print(f"  ❌ YAML parsing error: {e}")
        return False
    except Exception as e:
        print(f"  ❌ Error reading config: {e}")
        return False

def check_env_file():
    """Check environment variables"""
    print("\n🔐 Checking Environment Configuration...")
    
    env_file = Path('.env')
    template_file = Path('env.template')
    
    if not env_file.exists():
        print(f"  ⚠️  .env file not found (using env.template as reference)")
        if template_file.exists():
            print(f"  💡 To create: cp env.template .env")
        return False
    else:
        print(f"  ✅ .env file exists")
    
    # Load .env to check variables
    from dotenv import load_dotenv
    load_dotenv()
    
    important_vars = {
        'LITELLM_MASTER_KEY': 'Gateway authentication key',
        'OPENAI_API_KEY': 'OpenAI API access (optional)',
        'ANTHROPIC_API_KEY': 'Anthropic API access (optional)',
    }
    
    has_master_key = False
    has_provider_key = False
    
    for var, description in important_vars.items():
        value = os.getenv(var)
        if value and value != f"your-{var.lower().replace('_', '-')}-here":
            if var == 'LITELLM_MASTER_KEY':
                has_master_key = True
            else:
                has_provider_key = True
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ⚠️  {var}: Not set ({description})")
    
    if not has_master_key:
        print(f"\n  💡 Set LITELLM_MASTER_KEY for authentication")
    
    if not has_provider_key:
        print(f"  💡 Set at least one provider API key (OPENAI_API_KEY or ANTHROPIC_API_KEY)")
    
    return has_master_key and has_provider_key

def check_litellm_version():
    """Check LiteLLM version"""
    print("\n🔍 Checking LiteLLM Version...")
    
    try:
        import subprocess
        result = subprocess.run(['litellm', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            # Parse version from output like "LiteLLM: Current Version = 1.79.1"
            version_line = result.stdout.strip()
            if 'Version' in version_line:
                version = version_line.split('=')[-1].strip()
                print(f"  ✅ LiteLLM version: {version}")
                
                # Check if it's recent enough (>= 1.44.0 recommended)
                try:
                    parts = version.split('.')
                    major, minor = int(parts[0]), int(parts[1])
                    if major > 1 or (major == 1 and minor >= 44):
                        print(f"  ✅ Version is up to date (>= 1.44.0)")
                    else:
                        print(f"  ⚠️  Version might be outdated (recommend >= 1.44.0)")
                except:
                    pass
                
                return True
        
        print(f"  ⚠️  Could not determine version (but LiteLLM is installed)")
        return True
    except Exception as e:
        print(f"  ❌ Could not check version: {e}")
        return False

def main():
    """Main validation function"""
    print("=" * 70)
    print("🚀 LiteLLM Gateway - Setup Validation")
    print("=" * 70)
    print("\nBased on: https://docs.litellm.ai/docs/")
    print()
    
    results = []
    
    # Check files
    print("📁 Checking Required Files...")
    results.append(check_file_exists('config.yaml', 'Configuration file'))
    results.append(check_file_exists('env.template', 'Environment template'))
    results.append(check_file_exists('start_gateway.py', 'Gateway starter script'))
    results.append(check_file_exists('test_gateway.py', 'Gateway test script'))
    results.append(check_file_exists('requirements.txt', 'Requirements file'))
    
    # Check dependencies
    results.append(check_dependencies())
    
    # Check LiteLLM version
    results.append(check_litellm_version())
    
    # Validate config
    results.append(check_config_file())
    
    # Check environment
    env_ok = check_env_file()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 Validation Summary")
    print("=" * 70)
    
    if all(results):
        print("✅ All critical checks passed!")
        if env_ok:
            print("✅ Environment configured correctly!")
            print("\n🎯 Next steps:")
            print("   1. Run: python start_gateway.py")
            print("   2. Test: python test_gateway.py")
        else:
            print("⚠️  Environment needs configuration")
            print("\n🎯 Next steps:")
            print("   1. Copy: cp env.template .env")
            print("   2. Edit .env and add your API keys")
            print("   3. Run: python start_gateway.py")
    else:
        print("❌ Some checks failed. Please review the errors above.")
        print("\n💡 Common fixes:")
        print("   • Install dependencies: pip install -r requirements.txt")
        print("   • Check config.yaml syntax")
        print("   • Ensure all required files exist")
        return 1
    
    print("\n📚 Resources:")
    print("   • Documentation: https://docs.litellm.ai/docs/")
    print("   • Quick Start: https://docs.litellm.ai/docs/proxy/quick_start")
    print("   • GitHub: https://github.com/BerriAI/litellm")
    print()
    
    return 0

if __name__ == '__main__':
    sys.exit(main())

