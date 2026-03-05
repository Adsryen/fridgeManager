import unittest
import os
import sys
from datetime import datetime
import tempfile

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ['SQLITE_DB_DIR'] = tempfile.mkdtemp(prefix='fridge_manager_tests_')

from app import client

class TestDatabaseOperations(unittest.TestCase):
    """Integration tests for database operations"""
    
    def setUp(self):
        """Set up test database connection"""
        self.client = client
        self.test_db = self.client.test_fridge
        self.test_collection = self.test_db.item
        
        # Clear test collection before each test
        self.test_collection.delete_many({})
    
    def tearDown(self):
        """Clean up after each test"""
        self.test_collection.delete_many({})
        self.client.close()
    
    def test_database_connection(self):
        """Test database connection"""
        # Test if we can connect to SQLite
        self.assertIsNotNone(self.client)
        
        # Test if we can access the test database
        self.assertIsNotNone(self.test_db)
        
        # Test if we can access the collection
        self.assertIsNotNone(self.test_collection)
    
    def test_insert_item(self):
        """Test inserting an item into the database"""
        test_item = {
            '_id': 'test_insert_123',
            'Name': 'Test Apple',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 5,
            'Type': 'fruit'
        }
        
        # Insert the item
        result = self.test_collection.insert_one(test_item)
        self.assertIsNotNone(result.inserted_id)
        
        # Verify the item was inserted
        inserted_item = self.test_collection.find_one({'_id': 'test_insert_123'})
        self.assertIsNotNone(inserted_item)
        self.assertEqual(inserted_item['Name'], 'Test Apple')
        self.assertEqual(inserted_item['Num'], 5)
        self.assertEqual(inserted_item['Type'], 'fruit')
    
    def test_find_items_by_name(self):
        """Test finding items by name using regex"""
        # Insert test items
        items = [
            {
                '_id': 'apple1',
                'Name': 'Red Apple',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 3,
                'Type': 'fruit'
            },
            {
                '_id': 'apple2',
                'Name': 'Green Apple',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 2,
                'Type': 'fruit'
            },
            {
                '_id': 'banana1',
                'Name': 'Banana',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 6,
                'Type': 'fruit'
            }
        ]
        
        for item in items:
            self.test_collection.insert_one(item)
        
        # Search for items containing "Apple"
        apple_items = list(self.test_collection.find({'Name': {'$regex': 'Apple'}}))
        self.assertEqual(len(apple_items), 2)
        
        # Search for items containing "Banana"
        banana_items = list(self.test_collection.find({'Name': {'$regex': 'Banana'}}))
        self.assertEqual(len(banana_items), 1)
        self.assertEqual(banana_items[0]['Name'], 'Banana')
    
    def test_find_items_by_expiry_date(self):
        """Test finding items by expiry date"""
        current_date = datetime(2024, 6, 15)
        
        # Insert test items with different expiry dates
        items = [
            {
                '_id': 'expired1',
                'Name': 'Expired Milk',
                'ExpireDate': datetime(2024, 6, 1),  # Past date
                'Place': 'cold',
                'Num': 1,
                'Type': 'diary'
            },
            {
                '_id': 'current1',
                'Name': 'Current Bread',
                'ExpireDate': datetime(2024, 6, 20),  # Future date
                'Place': 'cold',
                'Num': 2,
                'Type': 'bread'
            },
            {
                '_id': 'future1',
                'Name': 'Future Cheese',
                'ExpireDate': datetime(2024, 12, 31),  # Far future
                'Place': 'cold',
                'Num': 1,
                'Type': 'diary'
            }
        ]
        
        for item in items:
            self.test_collection.insert_one(item)
        
        # Find items that are not expired (>= current date)
        not_expired = list(self.test_collection.find({'ExpireDate': {"$gte": current_date}}))
        self.assertEqual(len(not_expired), 2)
        
        # Find items that are expired (< current date)
        expired = list(self.test_collection.find({'ExpireDate': {"$lt": current_date}}))
        self.assertEqual(len(expired), 1)
        self.assertEqual(expired[0]['Name'], 'Expired Milk')
    
    def test_find_items_by_place(self):
        """Test finding items by storage place"""
        # Insert test items in different places
        items = [
            {
                '_id': 'cold1',
                'Name': 'Cold Milk',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 1,
                'Type': 'diary'
            },
            {
                '_id': 'frozen1',
                'Name': 'Frozen Pizza',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'frozer',
                'Num': 2,
                'Type': 'frozen'
            },
            {
                '_id': 'room1',
                'Name': 'Room Temperature Bread',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'room',
                'Num': 1,
                'Type': 'bread'
            }
        ]
        
        for item in items:
            self.test_collection.insert_one(item)
        
        # Find cold items
        cold_items = list(self.test_collection.find({'Place': 'cold'}))
        self.assertEqual(len(cold_items), 1)
        self.assertEqual(cold_items[0]['Name'], 'Cold Milk')
        
        # Find frozen items
        frozen_items = list(self.test_collection.find({'Place': 'frozer'}))
        self.assertEqual(len(frozen_items), 1)
        self.assertEqual(frozen_items[0]['Name'], 'Frozen Pizza')
        
        # Find room temperature items
        room_items = list(self.test_collection.find({'Place': 'room'}))
        self.assertEqual(len(room_items), 1)
        self.assertEqual(room_items[0]['Name'], 'Room Temperature Bread')
    
    def test_find_items_by_type(self):
        """Test finding items by food type"""
        # Insert test items of different types
        items = [
            {
                '_id': 'fruit1',
                'Name': 'Apple',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 5,
                'Type': 'fruit'
            },
            {
                '_id': 'vegetable1',
                'Name': 'Carrot',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 3,
                'Type': 'vegetable'
            },
            {
                '_id': 'meat1',
                'Name': 'Chicken',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'frozer',
                'Num': 2,
                'Type': 'meat'
            }
        ]
        
        for item in items:
            self.test_collection.insert_one(item)
        
        # Find fruit items
        fruit_items = list(self.test_collection.find({'Type': 'fruit'}))
        self.assertEqual(len(fruit_items), 1)
        self.assertEqual(fruit_items[0]['Name'], 'Apple')
        
        # Find vegetable items
        vegetable_items = list(self.test_collection.find({'Type': 'vegetable'}))
        self.assertEqual(len(vegetable_items), 1)
        self.assertEqual(vegetable_items[0]['Name'], 'Carrot')
        
        # Find meat items
        meat_items = list(self.test_collection.find({'Type': 'meat'}))
        self.assertEqual(len(meat_items), 1)
        self.assertEqual(meat_items[0]['Name'], 'Chicken')
    
    def test_update_item(self):
        """Test updating an item in the database"""
        # Insert a test item
        original_item = {
            '_id': 'update_test',
            'Name': 'Original Name',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        }
        self.test_collection.insert_one(original_item)
        
        # Update the item
        update_data = {
            'Name': 'Updated Name',
            'ExpireDate': datetime(2024, 12, 25),
            'Place': 'frozer',
            'Num': 3,
            'Type': 'meat'
        }
        
        result = self.test_collection.update_one(
            {'_id': 'update_test'}, 
            {'$set': update_data}
        )
        
        self.assertEqual(result.modified_count, 1)
        
        # Verify the update
        updated_item = self.test_collection.find_one({'_id': 'update_test'})
        self.assertIsNotNone(updated_item)
        self.assertEqual(updated_item['Name'], 'Updated Name')
        self.assertEqual(updated_item['Place'], 'frozer')
        self.assertEqual(updated_item['Num'], 3)
        self.assertEqual(updated_item['Type'], 'meat')
    
    def test_delete_item(self):
        """Test deleting an item from the database"""
        # Insert a test item
        test_item = {
            '_id': 'delete_test',
            'Name': 'Delete This',
            'ExpireDate': datetime(2024, 12, 31),
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        }
        self.test_collection.insert_one(test_item)
        
        # Verify the item exists
        item = self.test_collection.find_one({'_id': 'delete_test'})
        self.assertIsNotNone(item)
        
        # Delete the item
        result = self.test_collection.delete_one({'_id': 'delete_test'})
        self.assertEqual(result.deleted_count, 1)
        
        # Verify the item is deleted
        deleted_item = self.test_collection.find_one({'_id': 'delete_test'})
        self.assertIsNone(deleted_item)
    
    def test_find_all_items(self):
        """Test finding all items in the collection"""
        # Insert multiple test items
        items = [
            {
                '_id': 'all1',
                'Name': 'Item 1',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'cold',
                'Num': 1,
                'Type': 'fruit'
            },
            {
                '_id': 'all2',
                'Name': 'Item 2',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'frozer',
                'Num': 2,
                'Type': 'meat'
            },
            {
                '_id': 'all3',
                'Name': 'Item 3',
                'ExpireDate': datetime(2024, 12, 31),
                'Place': 'room',
                'Num': 3,
                'Type': 'vegetable'
            }
        ]
        
        for item in items:
            self.test_collection.insert_one(item)
        
        # Find all items
        all_items = list(self.test_collection.find())
        self.assertEqual(len(all_items), 3)
        
        # Verify all items are present
        item_names = [item['Name'] for item in all_items]
        self.assertIn('Item 1', item_names)
        self.assertIn('Item 2', item_names)
        self.assertIn('Item 3', item_names)


if __name__ == '__main__':
    unittest.main()
