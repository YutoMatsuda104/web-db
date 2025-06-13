class User:
    def __init__(self):
        self.id = None
        self.username = None
        self.password = None

    def __repr__(self):
        return "<User %r>" % self.id

class Item:
    def __init__(self):
        self.id = None
        self.owner_id = None
        self.ownername = None
        self.itemname = None
        self.price = None

    def __repr__(self):
        return "<Item %r>" % self.id

class Order:
    def __init__(self):
        self.id = None
        self.order_code = None
        self.user_id = None
        self.item_id = None
        self.amount = None
        self.price = None

    def __repr__(self):
        return "<Order %r>" % self.id
    
class Order:
    def __init__(self):
        self.id = None
        self.order_code = None
        self.user_id = None
        self.username = None   ### added
        self.item_id = None
        self.itemname = None   ### added
        self.amount = None
        self.price = None