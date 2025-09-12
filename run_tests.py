#!/usr/bin/env python3
"""
Test runner script for the Fridge Manager application.
This script provides an easy way to run different types of tests.
"""

import os
import sys
import subprocess
import argparse

def run_unittest_tests():
    """Run unittest-based tests"""
    print("🧪 Running unittest-based tests...")
    print("=" * 50)
    
    # Run test_app.py
    result1 = subprocess.run([sys.executable, '-m', 'unittest', 'tests.test_app'], 
                           capture_output=True, text=True)
    
    # Run test_database.py
    result2 = subprocess.run([sys.executable, '-m', 'unittest', 'tests.test_database'], 
                           capture_output=True, text=True)
    
    print("Unit Tests (test_app.py):")
    print(result1.stdout)
    if result1.stderr:
        print("Errors:", result1.stderr)
    
    print("\nIntegration Tests (test_database.py):")
    print(result2.stdout)
    if result2.stderr:
        print("Errors:", result2.stderr)
    
    return result1.returncode == 0 and result2.returncode == 0

def run_pytest_tests():
    """Run pytest-based tests"""
    print("🧪 Running pytest-based tests...")
    print("=" * 50)
    
    result = subprocess.run([sys.executable, '-m', 'pytest', 'tests/test_pytest.py', '-v'], 
                          capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def run_all_tests():
    """Run all tests"""
    print("🧪 Running all tests...")
    print("=" * 50)
    
    # Run unittest tests
    unittest_success = run_unittest_tests()
    
    print("\n" + "=" * 50)
    
    # Run pytest tests
    pytest_success = run_pytest_tests()
    
    return unittest_success and pytest_success

def run_coverage_tests():
    """Run tests with coverage report"""
    print("🧪 Running tests with coverage...")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, '-m', 'pytest', 
        'tests/', 
        '--cov=app', 
        '--cov-report=term-missing',
        '--cov-report=html:htmlcov'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def install_dependencies():
    """Install test dependencies"""
    print("📦 Installing test dependencies...")
    print("=" * 50)
    
    result = subprocess.run([
        sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("Errors:", result.stderr)
    
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Fridge Manager Test Runner')
    parser.add_argument('--type', choices=['unittest', 'pytest', 'all', 'coverage'], 
                       default='all', help='Type of tests to run')
    parser.add_argument('--install', action='store_true', 
                       help='Install dependencies before running tests')
    
    args = parser.parse_args()
    
    if args.install:
        if not install_dependencies():
            print("❌ Failed to install dependencies")
            return 1
    
    success = False
    
    if args.type == 'unittest':
        success = run_unittest_tests()
    elif args.type == 'pytest':
        success = run_pytest_tests()
    elif args.type == 'coverage':
        success = run_coverage_tests()
    else:  # all
        success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
