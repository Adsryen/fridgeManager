import pytest
import json
from datetime import datetime
from unittest.mock import MagicMock

@pytest.mark.unit
def test_index_route(client):
    """Test the main index route using pytest"""
    response = client.get('/')
    assert response.status_code == 200
    assert '冰箱管理大師' in response.data.decode('utf-8')

@pytest.mark.unit
def test_insert_item_success(client, mock_db):
    """Test successful item insertion using pytest"""
    test_data = {
        'itemName': 'Test Apple',
        'itemDate': '2024-12-31',
        'itemPlace': 'cold',
        'itemNum': '5',
        'itemType': 'fruit'
    }
    
    mock_db.insert_one.return_value = MagicMock()
    
    response = client.post('/insert', data=test_data)
    assert response.status_code == 302  # Redirect after insert

@pytest.mark.unit
def test_search_items(client, mock_db, sample_items):
    """Test item search functionality using pytest"""
    mock_db.find.return_value = sample_items
    
    response = client.post('/search', data={'text': 'Apple'})
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.unit
def test_state_ok_route(client, mock_db, sample_items):
    """Test getting items that are not expired using pytest"""
    mock_db.find.return_value = sample_items
    
    current_time = int(datetime.now().timestamp() * 1000)
    response = client.post(f'/stateok/{current_time}')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.unit
def test_cold_items_route(client, mock_db, sample_items):
    """Test getting cold storage items using pytest"""
    cold_items = [item for item in sample_items if item['Place'] == 'cold']
    mock_db.find.return_value = cold_items
    
    response = client.post('/cold')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.unit
def test_tag_route(client, mock_db, sample_items):
    """Test getting items by category using pytest"""
    fruit_items = [item for item in sample_items if item['Type'] == 'fruit']
    mock_db.find.return_value = fruit_items
    
    response = client.post('/tag/fruit')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.unit
def test_total_items_route(client, mock_db, sample_items):
    """Test getting all items using pytest"""
    mock_db.find.return_value = sample_items
    
    response = client.post('/total')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 3

@pytest.mark.unit
def test_delete_item_route(client, mock_db):
    """Test item deletion using pytest"""
    mock_db.delete_one.return_value = MagicMock()
    
    response = client.post('/delete/test_item')
    assert response.status_code == 200

@pytest.mark.unit
def test_get_one_item_route(client, mock_db, sample_item):
    """Test getting a single item using pytest"""
    mock_db.find.return_value = [sample_item]
    
    response = client.post('/getone/test_item_123')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert isinstance(data, list)

@pytest.mark.unit
def test_edit_item_route(client, mock_db):
    """Test item editing using pytest"""
    mock_db.update_one.return_value = MagicMock()
    
    edit_data = {
        'itemName': 'Updated Name',
        'itemDate': '2024-12-25',
        'itemPlace': 'frozer',
        'itemNum': '3',
        'itemType': 'meat'
    }
    
    response = client.post('/edit/test_item', data=edit_data)
    assert response.status_code == 302  # Redirect after edit

@pytest.mark.slow
def test_performance_large_dataset(client, mock_db):
    """Test performance with large dataset"""
    # Create a large dataset
    large_dataset = []
    for i in range(1000):
        large_dataset.append({
            '_id': f'item_{i}',
            'Name': f'Item {i}',
            'ExpireDate': '2024-12-31T00:00:00.000Z',
            'Place': 'cold',
            'Num': 1,
            'Type': 'other'
        })
    
    mock_db.find.return_value = large_dataset
    
    response = client.post('/total')
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert len(data) == 1000
