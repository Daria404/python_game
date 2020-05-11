import random
import pickle

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


def open_score_list():
    # load the previous score if it exists
    try:
        with open('score.dat', 'rb') as file:
            score = pickle.load(file)
    except:
        score = [0]
    return score    


def score_to_list(result):
    scores = open_score_list()
    scores.append(result)
    # save the score
    with open('score.dat', 'wb') as file:
        pickle.dump(scores, file)
        
    return scores


def clear_score_list():
    with open('score.dat', "w"):
        pass

    
def record_res():
    score_list = open_score_list()
    return max(score_list)



