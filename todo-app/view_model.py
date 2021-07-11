CARD_DONE_STATUS = 'Done'
CARD_TODO_STATUS = 'To-do'
CARD_DOING_STATUS = 'Doing'

def filterbyvalue(items, value):
    for item in items:
        if item.status.name==value:
            yield item

class ViewModel:

    def __init__(self, items, statuses):
        self._items = items
        self._statuses = statuses
    
    @property
    def items(self):
        return self._items
    @property
    def statuses(self):
        return self._statuses
    @property
    def doneItems(self):
        doneItems = filterbyvalue(self._items, 'Done')
        return doneItems
    @property
    def todoItems(self):
        todoItems=filterbyvalue(self._items, 'To Do')
        return todoItems
    @property
    def doingItems(self):
        doingItems=filterbyvalue(self._items, 'Doing')
        return doingItems