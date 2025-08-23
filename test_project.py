#!/usr/bin/env python3
"""
Simple project structure and syntax test
Tests that all Python files have valid syntax without importing dependencies
"""

import os
import ast
import sys

def test_python_syntax(file_path):
    """Test if a Python file has valid syntax"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse the file to check syntax
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"

def find_python_files(directory):
    """Find all Python files in a directory"""
    python_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """Main test function"""
    print("🔍 Testing Euramax Project Structure...")
    print("=" * 50)
    
    # Test backend structure
    backend_dir = '/home/runner/work/Euramax/Euramax/backend'
    
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found")
        return False
    
    # Find all Python files
    python_files = find_python_files(backend_dir)
    
    if not python_files:
        print("❌ No Python files found")
        return False
    
    print(f"📁 Found {len(python_files)} Python files")
    print()
    
    # Test each file
    passed = 0
    failed = 0
    
    for file_path in python_files:
        relative_path = os.path.relpath(file_path, backend_dir)
        success, error = test_python_syntax(file_path)
        
        if success:
            print(f"✅ {relative_path}")
            passed += 1
        else:
            print(f"❌ {relative_path}: {error}")
            failed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All Python files have valid syntax!")
        
        # Test project structure
        print("\n🏗️  Testing project structure...")
        
        required_dirs = [
            'app',
            'app/api',
            'app/core', 
            'app/database',
            'app/localization',
            'tests'
        ]
        
        structure_ok = True
        for req_dir in required_dirs:
            full_path = os.path.join(backend_dir, req_dir)
            if os.path.exists(full_path):
                print(f"✅ {req_dir}/")
            else:
                print(f"❌ {req_dir}/ (missing)")
                structure_ok = False
        
        # Test key files
        required_files = [
            'app/main.py',
            'app/core/threat_detector.py',
            'app/core/ai_bot.py',
            'app/core/notification_service.py',
            'app/api/threats.py',
            'app/api/notifications.py',
            'app/api/dashboard.py',
            'app/database/models.py',
            'app/database/database.py'
        ]
        
        for req_file in required_files:
            full_path = os.path.join(backend_dir, req_file)
            if os.path.exists(full_path):
                print(f"✅ {req_file}")
            else:
                print(f"❌ {req_file} (missing)")
                structure_ok = False
        
        if structure_ok:
            print("\n🎉 Project structure is complete!")
            return True
        else:
            print("\n❌ Project structure incomplete")
            return False
    else:
        print("❌ Some files have syntax errors")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)