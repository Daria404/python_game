import random

def set_random_coord():
    flag = True 
    while flag == True:
        coord = []
        for i in range(2):
            x = random.randrange(50, 450)
            y = random.randrange(-250, 0)
            coord.append((x,y))
        if abs(coord[0][0] - coord[1][0]) < 100:
            flag = True
        else: flag = False
        
    return coord


