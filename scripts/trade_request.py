#for our TradeRequest class! This will be the object that is stored in our list of trade requests.
from scripts import helpers


class TradeRequest:
    
    def __init__(self,sender: str,recipient: str):
        
        #initialize our instance variables.
        self.sender_username = sender
        self.recipient_username = recipient
        self.sender_item = str()
        self.recipient_item = str()
    
    def set_sender_item(self, item: str):
        
        #check if the sender's chosen item is in their inventory. If it is, we set it and return True. If not, we return False.
        if item in helpers.get_inventory_list(self.sender_username):
            self.sender_item = item
            return True
        else:
            print('sender chose an invalid item!')
            return False
        
    def set_recipient_item(self, item: str):
        #check if the sender's chosen item is in the recipeint's inventory. If it is, we set it and return True. If not, we return False.
        if item in helpers.get_inventory_list(self.recipient_username):
            self.recipient_item = item
            return True
        else:
            print('sender chose an invalid item!')
            return False
    
    def get_preview(self):
        #return a text preview of the trade
        message = f"{self.sender_username}: trade their {self.sender_item} for your {self.recipient_item}"
        return message
    
    def fulfil_request(self):
        #complete the trade request by swapping the items in each person's inventory
        
        #first remove the items from each inventory
        helpers.remove_from_inventory(self.sender_username,self.sender_item)
        helpers.remove_from_inventory(self.recipient_username,self.recipient_item)

        #then add the items
        helpers.add_to_inventory(self.sender_username,self.recipient_item)
        helpers.add_to_inventory(self.recipient_username,self.sender_item)

        return