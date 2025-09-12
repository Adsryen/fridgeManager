import unittest
import json
import os
import sys
from unittest.mock import patch, MagicMock
from datetime import datetime

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, client

class TestFridgeManagerApp(unittest.TestCase):
    """Test cases for the Fridge Manager Flask application"""
    
    def setUp(self):
        """Set up test client and test database"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Use a test database
        self.test_db = client.test_fridge
        self.test_collection = self.test_db.item
        
        # Clear test collection before each test
        self.test_collection.delete_many({})
    
    def tearDown(self):
        """Clean up after each test"""
        self.test_collection.delete_many({})
    
    def test_index_route(self):
        """Test the main index route"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn('冰箱管理大師', response.data.decode('utf-8'))
    
    def test_insert_item_success(self):
        """Test successful item insertion"""
        test_data = {
            'itemName': 'Test Apple',
            'itemDate': '2024-12-31',
            'itemPlace': 'cold',
            'itemNum': '5',
            'itemType': 'fruit'
        }
        
        with patch('app.client.fridge.item') as mock_collection:
            mock_collection.insert_one.return_value = MagicMock()
            
            response = self.client.post('/insert', data=test_data)
            self.assertEqual(response.status_code, 302)  # Redirect after insert
    
    def test_insert_item_validation(self):
        """Test item insertion with missing required fields"""
        test_data = {
            'itemName': 'Test Apple',
            # Missing other required fields
        }
        
        response = self.client.post('/insert', data=test_data)
        # Should still redirect but might fail silently
        self.assertEqual(response.status_code, 302)
    
    def test_search_items(self):
        """Test item search functionality"""
        # First insert a test item
        test_item = {
            '_id': 'test_id_123',
            'Name': 'Test Apple',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 5,
            'Type': 'fruit'
        }
        self.test_collection.insert_one(test_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/search', data={'text': 'Apple'})
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            if data:  # If items found
                self.assertEqual(data[0]['Name'], 'Test Apple')
    
    def test_search_empty_query(self):
        """Test search with empty query"""
        response = self.client.post('/search', data={'text': ''})
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
    
    def test_state_ok_route(self):
        """Test getting items that are not expired"""
        # Insert a future item
        future_item = {
            '_id': 'future_item',
            'Name': 'Future Apple',
            'ExpireDate': datetime(2025, 12, 31),
            'Place': 'cold',
            'Num': 3,
            'Type': 'fruit'
        }
        self.test_collection.insert_one(future_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            # Use current timestamp
            current_time = int(datetime.now().timestamp() * 1000)
            response = self.client.post(f'/stateok/{current_time}')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_state_bad_route(self):
        """Test getting expired items"""
        # Insert a past item
        past_item = {
            '_id': 'past_item',
            'Name': 'Expired Apple',
            'ExpireDate': datetime(2020, 1, 1),
            'Place': 'cold',
            'Num': 2,
            'Type': 'fruit'
        }
        self.test_collection.insert_one(past_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            # Use current timestamp
            current_time = int(datetime.now().timestamp() * 1000)
            response = self.client.post(f'/statebad/{current_time}')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_cold_items_route(self):
        """Test getting cold storage items"""
        cold_item = {
            '_id': 'cold_item',
            'Name': 'Cold Milk',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'diary'
        }
        self.test_collection.insert_one(cold_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/cold')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_frozer_items_route(self):
        """Test getting frozen items"""
        frozen_item = {
            '_id': 'frozen_item',
            'Name': 'Frozen Pizza',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'frozer',
            'Num': 2,
            'Type': 'frozen'
        }
        self.test_collection.insert_one(frozen_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/frozer')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_tag_route(self):
        """Test getting items by category"""
        fruit_item = {
            '_id': 'fruit_item',
            'Name': 'Banana',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 6,
            'Type': 'fruit'
        }
        self.test_collection.insert_one(fruit_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/tag/fruit')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_total_items_route(self):
        """Test getting all items"""
        # Insert multiple test items
        items = [
            {
                '_id': 'item1',
                'Name': 'Item 1',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 1,
                'Type': 'fruit'
            },
            {
                '_id': 'item2',
                'Name': 'Item 2',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'frozer',
                'Num': 2,
                'Type': 'meat'
            }
        ]
        for item in items:
            self.test_collection.insert_one(item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/total')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)
    
    def test_delete_item_route(self):
        """Test item deletion"""
        # Insert a test item
        test_item = {
            '_id': 'delete_me',
            'Name': 'Delete This',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        }
        self.test_collection.insert_one(test_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/delete/delete_me')
            self.assertEqual(response.status_code, 200)
    
    def test_get_one_item_route(self):
        """Test getting a single item"""
        test_item = {
            '_id': 'single_item',
            'Name': 'Single Item',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        }
        self.test_collection.insert_one(test_item)
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/getone/single_item')
            self.assertEqual(response.status_code, 200)
            
            data = json.loads(response.data)
            self.assertIsInstance(data, list)
    
    def test_edit_item_route(self):
        """Test item editing"""
        # Insert a test item
        test_item = {
            '_id': 'edit_me',
            'Name': 'Original Name',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        }
        self.test_collection.insert_one(test_item)
        
        edit_data = {
            'itemName': 'Updated Name',
            'itemDate': '2024-12-25',
            'itemPlace': 'frozer',
            'itemNum': '3',
            'itemType': 'meat'
        }
        
        with patch('app.client.fridge.item', self.test_collection):
            response = self.client.post('/edit/edit_me', data=edit_data)
            self.assertEqual(response.status_code, 302)  # Redirect after edit


if __name__ == '__main__':
    unittest.main()
