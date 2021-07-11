import os
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)
try:
    TRELLO_KEY = os.environ['TRELLO_KEY']
    TRELLO_TOKEN = os.environ['TRELLO_TOKEN']
except KeyError:
    pp.pprint('Trello env vars dont seem to be set')
    TRELLO_KEY = ''
    TRELLO_TOKEN = ''

APP_BOARD_NAME = os.environ['APP_BOARD_NAME']
TRELLO_MEMBER = os.environ['TRELLO_USER']
TRELLO_ENDPOINT = os.environ['TRELLO_ENDPOINT']
PARAMS = {'key': TRELLO_KEY, 'token': TRELLO_TOKEN}

class Item:       
    def __init__(self, id, status, title):
        self.id = id
        self.status = status
        self.title = title
    def __str__(self):
        return "id: %s, status: %s title: %s" % (self.id, self.status.name, self.title)

class Status:
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self):
        return "id: %s, name: %s" % (self.id, self.name)

def get_item(id):
    temp_item = requests.get(TRELLO_ENDPOINT+'cards/'+id, params=PARAMS).json()
    temp_item_list_name = requests.get(TRELLO_ENDPOINT+'cards/'+id+'/list', params=PARAMS).json()
    item_list = Status(temp_item['idList'], temp_item_list_name['name'])
    returned_item = Item(temp_item['id'],item_list, temp_item['name'])
    return returned_item

def add_item(listId, title):
    requests.post(TRELLO_ENDPOINT+'cards?name='+title+'&idList='+listId, params=PARAMS).json()

def delete_item(id):
    requests.delete(TRELLO_ENDPOINT+'cards/'+id, params=PARAMS).json()

def save_item(id, idList, title):
    requests.put(TRELLO_ENDPOINT+'cards/'+id+'?name='+title+'&idList='+idList, params=PARAMS).json()

def get_app_board(APP_BOARD_NAME):
    boards = requests.get(TRELLO_ENDPOINT+'members/'+TRELLO_MEMBER+'/boards', params=PARAMS).json()
    for x in range(len(boards)):
        if boards[x]['name'] == APP_BOARD_NAME:
            board = (boards[x]['name'], boards[x]['id'])
    return board

def get_app_board_lists():
    app_board_id=get_app_board(APP_BOARD_NAME)[1]
    app_board_lists = requests.get(
        TRELLO_ENDPOINT
        +'boards/'
        +app_board_id
        +'/lists',
        params=PARAMS).json()
    board_lists=[]
    for x in range(len(app_board_lists)):  
        board_lists = board_lists + [Status(app_board_lists[x]['id'], app_board_lists[x]['name'])]
    return board_lists

def get_board_list_cards(app_board_lists):
    cards=[]
    for status in app_board_lists:
        list_cards = requests.get(TRELLO_ENDPOINT+'lists/'+status.id+'/cards', params=PARAMS).json()      
        for x in range(len(list_cards)):
            cards = cards + [Item(list_cards[x]['id'],status,list_cards[x]['name'])]
    return cards

def get_items():
    return get_board_list_cards(get_app_board_lists())
