import pytest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the parent directory to the path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture
def app():
    """Create application for testing"""
    from app import app
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

@pytest.fixture
def mock_db():
    """Mock database for testing"""
    with patch('app.client.fridge.item') as mock_collection:
        yield mock_collection

@pytest.fixture
def sample_item():
    """Sample item data for testing"""
    return {
        '_id': 'test_item_123',
        'Name': 'Test Apple',
        'ExpireDate': '2024-12-31T00:00:00.000Z',
        'Place': 'cold',
        'Num': 5,
        'Type': 'fruit'
    }

@pytest.fixture
def sample_items():
    """Sample items data for testing"""
    return [
        {
            '_id': 'item1',
            'Name': 'Apple',
            'ExpireDate': '2024-12-31T00:00:00.000Z',
            'Place': 'cold',
            'Num': 3,
            'Type': 'fruit'
        },
        {
            '_id': 'item2',
            'Name': 'Milk',
            'ExpireDate': '2024-12-25T00:00:00.000Z',
            'Place': 'cold',
            'Num': 1,
            'Type': 'diary'
        },
        {
            '_id': 'item3',
            'Name': 'Pizza',
            'ExpireDate': '2024-12-20T00:00:00.000Z',
            'Place': 'frozer',
            'Num': 2,
            'Type': 'frozen'
        }
    ]
