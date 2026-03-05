#!/usr/bin/env python3
"""
Basic test script for the Fridge Manager application.
This script tests the core functionality without complex mocking.
"""

import sys
import os
import json
from datetime import datetime

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from app import app, client
        print("✅ Successfully imported app and client")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("🧪 Testing database connection...")
    try:
        from app import client
        # Test connection
        client.admin.command('ping')
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_flask_app():
    """Test Flask application creation"""
    print("🧪 Testing Flask application...")
    try:
        from app import app
        with app.test_client() as client:
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Flask application working")
                return True
            else:
                print(f"❌ Flask application returned status {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ Flask application test failed: {e}")
        return False

def test_routes():
    """Test basic routes"""
    print("🧪 Testing basic routes...")
    try:
        from app import app
        with app.test_client() as client:
            # Test index route
            response = client.get('/')
            if response.status_code != 200:
                print(f"❌ Index route failed: {response.status_code}")
                return False
            
            # Test search route with empty query
            response = client.post('/search', data={'text': ''})
            if response.status_code != 200:
                print(f"❌ Search route failed: {response.status_code}")
                return False
            
            # Test total route
            response = client.post('/total')
            if response.status_code != 200:
                print(f"❌ Total route failed: {response.status_code}")
                return False
            
            print("✅ All basic routes working")
            return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_database_operations():
    """Test basic database operations"""
    print("🧪 Testing database operations...")
    try:
        from app import client
        
        # Use test database
        test_db = client.test_fridge
        test_collection = test_db.item
        
        # Clear test collection
        test_collection.delete_many({})
        
        # Test insert
        test_item = {
            '_id': 'test_item_123',
            'Name': 'Test Apple',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 5,
            'Type': 'fruit'
        }
        
        result = test_collection.insert_one(test_item)
        if not result.inserted_id:
            print("❌ Insert operation failed")
            return False
        
        # Test find
        found_item = test_collection.find_one({'_id': 'test_item_123'})
        if not found_item:
            print("❌ Find operation failed")
            return False
        
        # Test update
        update_result = test_collection.update_one(
            {'_id': 'test_item_123'},
            {'$set': {'Name': 'Updated Apple'}}
        )
        if update_result.modified_count != 1:
            print("❌ Update operation failed")
            return False
        
        # Test delete
        delete_result = test_collection.delete_one({'_id': 'test_item_123'})
        if delete_result.deleted_count != 1:
            print("❌ Delete operation failed")
            return False
        
        print("✅ All database operations working")
        return True
    except Exception as e:
        print(f"❌ Database operations failed: {e}")
        return False

def test_json_encoding():
    """Test JSON encoding with datetime"""
    print("🧪 Testing JSON encoding...")
    try:
        from app import JSONEncoder
        import json
        
        test_dt = datetime(2024, 12, 31)
        encoder = JSONEncoder()
        encoded = encoder.default(test_dt)
        
        if not isinstance(encoded, str):
            print("❌ JSON encoding failed")
            return False
        
        print("✅ JSON encoding working")
        return True
    except Exception as e:
        print(f"❌ JSON encoding failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🚀 Starting Fridge Manager Basic Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_database_connection,
        test_flask_app,
        test_routes,
        test_database_operations,
        test_json_encoding
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Add spacing between tests
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == '__main__':
    sys.exit(main())
