"""
module creates navigation
for json files
"""
import json


def file_read():
    """
    function reads the path to the json file
    """
    correct = False
    path = input('Please, type the path to the json file first:')
    while 'json' not in path:
        print('The file format has to be json')
        path = input('Please, type the path to the json file first:')
    try:
        with open (path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    except:
        while correct is False:
            path = input('Please, type the valid path to the json file:')
            try:
                with open (path, 'r', encoding='utf-8') as file:
                  data = json.load(file)
            except:
                continue
            correct = True
    return data



    


def choose_the_elem(elem_ls:list, add='list'):
    """
    function takes the element from the user
    """
    if add == 'dict':
        print('Here is a list of keys in the dictionary')

    print('Please, choose the element from the list:')
    print(elem_ls)
    response = input('')
    if response == 'exit':
        return 'exit'
    if response not in elem_ls:
        while response not in elem_ls:
            print(elem_ls)
            print('There is no such element in the list')
            print('Try choosing once more:')
            response = input('')
    return response


def list_elem_idx(the_list:list):
    """
    function chooses the index of element in the list
    """
    correct = False
    while correct is False:
        max_ind = len(the_list)-1
        try:
            response = int(input(''))
            if response == 'exit':
                return 'exit'
        except:
            print('The index does not exist')
        if response > max_ind or response < 0:
            print('The index does not exist')
        else:
            correct = True
    return response
        
        
    
        


def yes_no_answer():
    """
    function interacts with simple user's
    yes/no answers
    """
    response = input('')
    if response == 'exit':
        return 'exit'
    if  response == 'y':
        return True
    elif response == 'n':
        return False
    else:
        while response!= 'y' and response!= 'n':
            print('Please, type y or n for the answer')
            response = input('')
            if  response == 'y':
                return True
            elif response == 'n':
                return False


def json_navigation(path:str):
    """
    function takes the path to json
    and creates a navigation for the user
    """
    with open (path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    curr_path = data
    while True:
        if curr_path == data:
            print('You are currently on the upper json level')
        else:
            print(f"You are currently in the '{choice}', {type(curr_path)}")


        if isinstance(curr_path, dict) is True:
            choice = choose_the_elem(curr_path.keys(), add='dict')
            if choice == 'exit':
                break
        elif isinstance(curr_path, list) is True:
            print('Please, enter the index of the element in a list')
            print(f"(0-{len(curr_path)-1})")
            resp = list_elem_idx(curr_path)
            choice = resp
            if resp == 'exit':
                break

        else:
            print('There is no way to enter this object')
            break
        if choice == 'exit':
            break


        curr_path, previous_path = curr_path[choice], curr_path
        print(f'The element you chose is a {type(curr_path)}')


        if isinstance(curr_path, dict):
            print(f'This dictionary has {len(list(curr_path.keys()))} keys')  # description of a dictionary
            if len(list(curr_path.keys())) == 0:
                print('This dictionary is empty')
                print('Move to the upper level? (y/n)')
                resp = yes_no_answer()
                if resp == 'exit':
                    break
                if resp is True:
                    curr_path = previous_path
            else:
                pass


        
        elif isinstance(curr_path, list):
            print(f'The list can be quite long. Print it anyways? (type y/n)')
            resp = yes_no_answer()
            if resp == 'exit':
                break
            if resp is True:
                print(curr_path)


        else:   # it is not a list or dict
            print(curr_path)
            print('Here is a chosen object')
            print("If it is the file you've been looking for, type exit or n to stop the search.")
            print('If you want to return to the previous location, type y')
            resp = yes_no_answer()
            if resp is True:
                curr_path = previous_path
            else:
                break



        
def main():
    """
    the main navigation function
    """
    print('Welcome to json navigation program')
    print('Follow the guide to move through file')
    print("Type 'exit' to input to stop the searching")
    path = file_read()
    json_navigation(path)

# main()