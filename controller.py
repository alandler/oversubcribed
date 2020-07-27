# User interacts with the controller

from model import Todo

class Service:
    def __init__(self):
        self.model = Todo()
    
    def sync(self):
        return self.model.sync()

    def update_item(self, item_id, estimate):
        return self.model.update_item(item_id, estimate)
    
    def get_times(self):
        return self.model.get_times()

    def aggregate_by_day(self):
        return self.model.aggregate_by_day()
