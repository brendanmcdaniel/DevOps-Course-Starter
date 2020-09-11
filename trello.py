import os
import pprint
import requests

pp = pprint.PrettyPrinter(indent=4)
app_board_name='To Do App'
trello_member='brendanmcdaniel'
trello_endpoint='https://api.trello.com/1/'

class item:
    def __init__(self, id, status, title):
        self.id = id
        self.status = status
        self.title = title

class status:
    def __init__(self, id, name):
        self.id = id
        self.name = name

# Check if proxy env vars have been set
try:
    http_proxy = os.environ['http_proxy']
except KeyError:
    pp.pprint('No HTTP proxy found')
    http_proxy = ''
try:
    trello_key = os.environ['TRELLO_KEY']
    trello_token = os.environ['TRELLO_TOKEN']
except KeyError:
    pp.pprint('Trello env vars dont seem to be set')
    trello_key = ''
    trello_token = ''

# Environment variables set for trell api
try:
    https_proxy = os.environ['https_proxy']
except KeyError:
    pp.pprint('No HTTPS proxy found')
    https_proxy = ''

proxyDict = { 
            "http"  : http_proxy, 
            "https" : https_proxy
            }

headers={}

def get_item(id):
    tempItem = requests.get(trello_endpoint+'cards/'+id+'?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()
    tempItemListName = requests.get(trello_endpoint+'cards/'+id+'/list?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()
    itemList = status(tempItem['idList'], tempItemListName['name'])
    returnedItem = item(tempItem['id'],itemList, tempItem['name'])
    return returnedItem

def add_item(listId, title):
    requests.post(trello_endpoint+'cards?name='+title+'&idList='+listId+'&key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()

def delete_item(id):
    requests.delete(trello_endpoint+'cards/'+id+'?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()

def save_item(id, idList, title):
    requests.put(trello_endpoint+'cards/'+id+'?name='+title+'&key='+trello_key+'&idList='+idList+'&token='+trello_token, headers=headers, proxies=proxyDict).json()

def get_app_board(app_board_name):
    boards = requests.get(trello_endpoint+'members/'+trello_member+'/boards?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()
    for x in range(len(boards)):
        if boards[x]['name'] == app_board_name:
            board = (boards[x]['name'], boards[x]['id'])
    return board

def get_app_board_lists():
    app_board_id=get_app_board(app_board_name)[1]
    app_board_lists = requests.get(trello_endpoint+'boards/'+app_board_id+'/lists?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()
    board_lists=[]
    for x in range(len(app_board_lists)):   
        board_lists = board_lists + [status(app_board_lists[x]['id'], app_board_lists[x]['name'])]
    return board_lists

def get_board_list_cards(app_board_lists):
    cards=[]
    for status in app_board_lists:
        print(status.name)
        list_cards = requests.get(trello_endpoint+'lists/'+status.id+'/cards?key='+trello_key+'&token='+trello_token, headers=headers, proxies=proxyDict).json()      
        for x in range(len(list_cards)):
            cards = cards + [item(list_cards[x]['id'],status,list_cards[x]['name'])]
    return cards

def get_items():
    return get_board_list_cards(get_app_board_lists())
