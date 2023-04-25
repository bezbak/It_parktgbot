FILE_PATH = 'chat_ids.txt'
with open(FILE_PATH, 'r') as f:
    lines = f.readlines() 
        
list_of_groups = [line.strip() for line in lines]
print(list_of_groups)