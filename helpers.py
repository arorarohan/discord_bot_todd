#this document is for helper functions
import main
import csv



#this is for checking the toddallions balance of a certain user
def check_balance(username: str):
    #open the file and get our items
    with open(main.TODDALLIONS_PATH,'r') as file:
        items = list(csv.reader(file))
    
    #get our usernames and balances out
    usernames = [item[0] for item in items]
    balances = [int(item[1]) for item in items]

    #check usernames for our username and get the corresponding balance. If they weren't found then their balance is 0
    balance = 0
    for i in range(len(usernames)):
        if usernames[i] == username:
            balance = balances[i]

    #now return whatever balance we have
    return balance


#this is for updating the toddallions balance of a certain user
def update_balance(username: str, change: int):
    
    #open the file and get our lists
    with open(main.TODDALLIONS_PATH,'r') as file:
        items = list(csv.reader(file))
    #our usernames are the first item in each row, and balances are the second.
    usernames = [item[0] for item in items]
    balances = [int(item[1]) for item in items]

    #check if the user already has a balance
    if username in usernames:
        #change the balance
        for i in range(len(usernames)):
            if usernames[i] == username:
                balances[i] += change

    else:
        #add them in as a new entry
        usernames.append(username)
        balances.append(change)
        
    #now we need to rewrite the file with our updated lists
    with open(main.TODDALLIONS_PATH,'w',newline='') as file:
        writer = csv.writer(file)
        for i in range(len(usernames)):
            writer.writerow([usernames[i],balances[i]])
    
    #return from the function once done
    return
    

#this one will be for checking our inventory, and returning the items (excluding username) as a list
#the inventory will be 1 row per user. The first item will be their username and the rest of the columns will be items.
def get_inventory_list(username: str):
    #open the inventory file and get our list of items
    with open(main.INVENTORY_PATH,'r') as file:
        items = list(csv.reader(file))
    
    #now find the sublist associated with the user
    output_list = []
    for item in items:
        #item[0] is the username
        if item[0] == username:
            #item[1:] should be every time except the username
            output_list = item[1:]
            break
    
    #return our output_list, if the inventory is empty then we are just returning an empty list
    return output_list

#this one will be for adding things to the inventory, for example, when something is bought
def add_to_inventory(username: str, to_add: str):
    #we don't really give a shit if something is already in there, we're just gonna add it again as a duplicate!! yeah
    
    #let's get our list of items, and get a list of usernames out of that. Entries is a list of lists.
    with open(main.INVENTORY_PATH,'r') as file:
        entries = list(csv.reader(file))

    usernames = [entry[0] for entry in entries]

    #if the user has an empty inventory, they might not be in our file so we will add them in! And while we're at it, may as well add the item.
    if username not in usernames:
        entries.append([username,to_add])
    
    #if the user was already in the list, we need to find their sublist first then add to it.
    else:
        for i in range(len(usernames)):
            if usernames[i] == username:
                entries[i].append(to_add)
                break
    
    #by this stage, we have added the item to our list! now we just have to rewrite the csv file with the new data.
    with open(main.INVENTORY_PATH,'w',newline='') as file:
        writer = csv.writer(file)
        for entry in entries:
            writer.writerow(entry)