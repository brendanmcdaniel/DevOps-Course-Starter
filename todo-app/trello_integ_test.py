import os
from unittest.mock import patch, Mock
import pytest
import app
from dotenv import load_dotenv, find_dotenv

@pytest.fixture
def client():
    # file_path = find_dotenv('.env.test')
    # load_dotenv(file_path, override=True)
    test_app = app.create_app()
    with test_app.test_client() as client: 
        yield client

@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_app_board_lists
    response = client.get('/')

def mock_get_app_board_lists(url, params):
    if url == 'https://api.trello.com/1/members/testuser/boards':
        response = Mock()
        response.json.return_value = [{
            "name": "MyNewBoard",
            "desc": "",
            "id": "5f3d53f5b75ee717cef76724",
        },
        {
            "name": "To Do App TEST",
            "desc": "",
            "id": "5f3d53f5b75ee717cef76724"
        }]
        print(response.data.decode('utf-8'))
        return response
    if url == 'https://api.trello.com/1/boards/5f3d53f5b75ee717cef76724/lists':
        response = Mock()
        response.json.return_value = [{
            "id": "5f5ce0a3907ea96d4f9b6a59",
            "name": "To Do",
            "pos": 65535,
            "idBoard": "5f3d53f5b75ee717cef76724"
        },
        {
            "id": "5f5ce0ab9fd8dc3687d59fbe",
            "name": "Doing",
            "pos": 131071,
            "idBoard": "5f3d53f5b75ee717cef76724"
        },
        {
            "id": "5f5ce0ad7801e94e118d795d",
            "name": "Done",
            "pos": 196607,
            "idBoard": "5f3d53f5b75ee717cef76724"
        }]
        return response
    if url.startswith('https://api.trello.com/1/lists/'):
        response = Mock()
        response.json.return_value = [{
        "id": "5f5ce2b7722b80697d711a2f",
        "dateLastActivity": "2021-07-09T14:49:39.102Z",
        "desc": "",
        "idBoard": "5f3d53f5b75ee717cef76724",
        "idList": "5f5ce0a3907ea96d4f9b6a59",
        "idMembersVoted": [],
        "idShort": 17,
        "idLabels": [],
        "name": "A Test Item",
        "pos": 16384,
        "shortLink": "GqHiqqZf"
        }]
        return response
    return None
