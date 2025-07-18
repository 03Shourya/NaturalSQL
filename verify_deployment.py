#!/usr/bin/env python3
"""
🚀 NaturalSQL Deployment Verification Script
This script verifies that all components are working correctly before deployment.
"""

import sys
import os
from pathlib import Path

def check_file_exists(filepath, description):
    """Check if a file exists and print status."""
    if os.path.exists(filepath):
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description}: {filepath} - MISSING")
        return False

def check_directory_exists(dirpath, description):
    """Check if a directory exists and print status."""
    if os.path.exists(dirpath) and os.path.isdir(dirpath):
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description}: {dirpath} - MISSING")
        return False

def test_imports():
    """Test that all modules can be imported."""
    print("\n🔧 Testing imports...")
    
    try:
        from pipeline import nl_to_sql
        print("✅ Pipeline imported successfully")
    except ImportError as e:
        print(f"❌ Pipeline import failed: {e}")
        return False
    
    try:
        import gradio as gr
        print(f"✅ Gradio imported successfully (version: {gr.__version__})")
    except ImportError as e:
        print(f"❌ Gradio import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic SQL generation functionality."""
    print("\n🧪 Testing basic functionality...")
    
    try:
        from pipeline import nl_to_sql
        
        # Test a simple query
        test_query = "Show all employees"
        result = nl_to_sql(test_query)
        
        if result and "SELECT" in result:
            print(f"✅ Basic functionality test passed")
            print(f"   Input: '{test_query}'")
            print(f"   Output: '{result}'")
            return True
        else:
            print(f"❌ Basic functionality test failed")
            print(f"   Input: '{test_query}'")
            print(f"   Output: '{result}'")
            return False
            
    except Exception as e:
        print(f"❌ Basic functionality test failed with error: {e}")
        return False

def main():
    """Main verification function."""
    print("🚀 NaturalSQL Deployment Verification")
    print("=" * 50)
    
    # Check core files
    print("\n📋 Checking core files...")
    core_files = [
        ("app.py", "Main Gradio application"),
        ("requirements.txt", "Python dependencies"),
        ("README.md", "Project documentation"),
        (".gitattributes", "Git file handling"),
        ("pipeline.py", "Main pipeline"),
    ]
    
    core_files_ok = True
    for filename, description in core_files:
        if not check_file_exists(filename, description):
            core_files_ok = False
    
    # Check directories
    print("\n📂 Checking directories...")
    directories = [
        ("parser_agent/", "Parser agent components"),
        ("intent_classifier/", "Intent classifier components"),
        ("schema_mapper/", "Schema mapper components"),
        ("query_generator/", "Query generator components"),
        ("agents/", "Agent implementations"),
        ("schema/", "Database schema"),
    ]
    
    directories_ok = True
    for dirname, description in directories:
        if not check_directory_exists(dirname, description):
            directories_ok = False
    
    # Test imports
    imports_ok = test_imports()
    
    # Test functionality
    functionality_ok = test_basic_functionality()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 50)
    
    all_ok = core_files_ok and directories_ok and imports_ok and functionality_ok
    
    if all_ok:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your NaturalSQL app is ready for deployment!")
        print("\n🚀 Next steps:")
        print("1. Create a new Space on Hugging Face")
        print("2. Clone the Space repository")
        print("3. Run: ./deploy.sh <space_directory>")
        print("4. Commit and push to Hugging Face")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("Please fix the issues above before deploying.")
        sys.exit(1)

if __name__ == "__main__":
    main() 