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
        #add them in as a new entry to the end
        usernames.append(username)
        balances.append(change)
    
    #let's reconstruct our list
    unsorted_list = []
    for i in range(len(usernames)):
        unsorted_list.append([usernames[i],balances[i]])
    
    #now let's sort it.
    #save the initial length of the list we are going to sort
    n_items = len(unsorted_list)

    #initialize our sorted list
    sorted_list = []
    #now we do the actual sorting, not sure what this algorithm is called but I think I'll call it 'idiot sort' because it the the dumbest approach possible
    for i in range(n_items):
        #for each iteration, the max value will initially be 0. This means it does not work with negative numbers! But we should never have a situation with negative balances, so it's fine.
        max_val = 0
        for i in range(len(unsorted_list)):
            #the value of the item is its second item as an integer
            value = int(unsorted_list[i][1])
            #find the largest value in the unsorted list, and save its index
            if value > max_val:
                max_val = value
                max_index = i
        #after we have iterated through the unsorted list and found the max index, we move the item with that value to the other list.
        to_move = unsorted_list.pop(max_index)
        sorted_list.append(to_move)
        #this will repeat as many times as there were initially elements, ensuring every element gets sorted.

        
    #now we need to rewrite the file with our updated lists
    with open(main.TODDALLIONS_PATH,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_list)
    
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

#function to sort the currency list, we will call this for sorting the list in the net worth leaderboard!
def sort_toddalions(to_sort: list):
    #initialize the lists we will be modifying
    sorted_list = []
    unsorted_list = to_sort[:]
    #save the initial length of the list
    n_items = len(unsorted_list)
    #now we do the actual sorting, not sure what this algorithm is called but I think I'll call it 'idiot sort' because it the the dumbest approach possible
    for i in range(n_items):
        #for each iteration, the max value will initially be 0. This means it does not work with negative numbers! But we should never have a situation with negative balances, so it's fine.
        max_val = 0
        for i in range(len(unsorted_list)):
            #the value of the item is its second item as an integer
            value = int(unsorted_list[i][1])
            #find the largest value in the unsorted list, and save its index
            if value > max_val:
                max_val = value
                max_index = i

        #after we have iterated through the unsorted list and found the max index, we move the item with that value to the other list.
        to_move = unsorted_list.pop(max_index)
        sorted_list.append(to_move)
    
    #now that we are done, let's return our list!
    return sorted_list


#function for adding items to the hall of fame
def add_to_hof(username: str):
    
    #get the currently existing items in the file
    with open(main.FAME_PATH,'r') as file:
                items = list(csv.reader(file))

    #find the index that we need to change   
    idx_to_change = -1
    for row_idx in range(len(items)):
        if items[row_idx][0] == username:
            idx_to_change = row_idx
            break
            
    #if we found the username in our list, idx_to_change would be >= 0.
    #in the case that the user is a first-timer to our list, we want to add them as a new row:
    if idx_to_change < 0:
        items.append([username,1])
                
            
            #in the case that the user is already in the list, we want to update the element that has the username in it:
    else:
        #update our value
        new_number = int(items[idx_to_change][1]) + 1
        items[idx_to_change][1] = str(new_number)

    #now we have added our element to the list, we need to re-sort the list. We can use the sort_toddallions function to do this as the list is of the same format
    sorted_items = sort_toddalions(items)

    #rewrite the file with our new list
    with open(main.FAME_PATH,'w',newline='') as file:
        writer = csv.writer(file)
        writer.writerows(sorted_items)
    
    #return from the function once done
    return