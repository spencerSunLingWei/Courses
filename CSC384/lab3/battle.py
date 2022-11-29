from ast import Constant
from distutils.dep_util import newer_pairwise
from json import JSONDecodeError
from re import A
import sys
import copy
import queue
from wsgiref.util import shift_path_info

global R,C,S
R,C,S = [],[],[]
constraint_dic = {}

assigned_dic = {}
ship_lst = []

class Ship:
    size = int()
    row_dic = {}
    col_dic = {}

    def __init__(self, size, row_dic=None, col_dic=None):
        self.size = size

        if row_dic != None:
            self.row_dic = row_dic.copy()  

        if col_dic != None:
            self.col_dic = col_dic.copy()  

def read_input(input_file_path):

    with open(input_file_path) as f:
        lines = f.readlines()

        # dump constraint
        for char in lines[0]:
            if char != '\n':
                R.append(int(char))

        for char in lines[1]:
            if char != '\n':
                C.append(int(char))

        for char in lines[2]:
            if char != '\n':
                S.append(int(char))

        for num in range(0, 4-len(S)):
            S.append(0)

        # dump board with Ri = Ci = 0 constarint preprocessing, and existing row
        state = []
        len_ref = len(R)
        for i in range(0, len_ref):
            if R[i] == 0:
                sub_state = ["W"]*len_ref
            else:
                sub_state = []
                for j in range(0, len_ref):
                    if C[j] == 0:
                        sub_state.append("W")
                    else:
                        sub_state.append(lines[i+3][j])
            state.append(sub_state)


        ####################################################################
        for i in range(0, len_ref):
            for j in range(0, len_ref):
                item = state[i][j]
                N = len_ref-1

                if item == "S":
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right
                    if i-1>=0:            state[i-1][j] = "W" # up
                    if i+1<=N:            state[i+1][j] = "W" # bottem
                    if j-1>=0:            state[i][j-1] = "W" # left
                    if j+1<=N:            state[i][j+1] = "W" # right

                    dic = {(i,j): True}
                    ship_lst.append(Ship(size=1, row_dic=dic))
                    dic.pop((i,j))
                    assigned_dic[len(ship_lst)-1] = True
                    
                elif item == "L": # no right
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right
                    if i-1>=0:            state[i-1][j] = "W" # up
                    if i+1<=N:            state[i+1][j] = "W" # bottem
                    if j-1>=0:            state[i][j-1] = "W" # left

                    constraint_dic[(i,j)] = "L"

                elif item == "R": # no left
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right
                    if i-1>=0:            state[i-1][j] = "W" # up
                    if i+1<=N:            state[i+1][j] = "W" # bottem
                    if j+1<=N:            state[i][j+1] = "W" # right

                    constraint_dic[(i,j)] = "R"
                
                elif item == "T": # no bottom
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right
                    if i-1>=0:            state[i-1][j] = "W" # up
                    if j-1>=0:            state[i][j-1] = "W" # left
                    if j+1<=N:            state[i][j+1] = "W" # right

                    constraint_dic[(i,j)] = "T"

                elif item == "B": # no up
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right
                    if i+1<=N:            state[i+1][j] = "W" # bottem
                    if j-1>=0:            state[i][j-1] = "W" # left
                    if j+1<=N:            state[i][j+1] = "W" # right

                    constraint_dic[(i,j)] = "B"

                elif item == "M": # no up bottem left right
                    if i-1>=0 and j-1>=0: state[i-1][j-1] = "W" # up left
                    if i-1>=0 and j+1<=N: state[i-1][j+1] = "W" # up right
                    if i+1<=N and j-1>=0: state[i+1][j-1] = "W" # bottem left
                    if i+1<=N and j+1<=N: state[i+1][j+1] = "W" # bottem right

                    constraint_dic[(i,j)] = "M"
    

        #####################################################################
        sub_dic = {}
        des_row_dic, des_col_dic = {}, {}
        cru_row_dic, cru_col_dic = {}, {}
        bat_row_dic, bat_col_dic = {}, {}

        for i in range(0, len(state[-1])):
            for j in range(0, len(state[-1])):
                item = state[i][j]
                N = len(state[-1])-1

                if item == "0":
                    sub_dic[(i,j)] = True

                if item == "0" or item == "L":
                    if j+1<=N and (state[i][j+1]=="0" or state[i][j+1]=="R"): 
                        des_row_dic[(i,j)] = True # row, 1+1
                    
                    if j+1<=N and (state[i][j+1]=="0" or state[i][j+1]=="M") and j+2<=N and (state[i][j+2]=="0" or state[i][j+2]=="R"):
                        cru_row_dic[(i,j)] = True # row, 1+2
                    
                    if j+1<=N and (state[i][j+1]=="0" or state[i][j+1]=="M") and j+2<=N and (state[i][j+2]=="0" or state[i][j+2]=="M") and j+3<=N and (state[i][j+3]=="0" or state[i][j+3]=="R"):
                        bat_row_dic[(i,j)] = True # row, 1+3

                if item == "0" or item == "T":
                    if i+1<=N and (state[i+1][j]=="0" or state[i+1][j]=="B"): 
                        des_col_dic[(i,j)] = True # col, 1+1
                    
                    if i+1<=N and (state[i+1][j]=="0" or state[i+1][j]=="M") and i+2<=N and (state[i+2][j]=="0" or state[i+2][j]=="B"):
                        cru_col_dic[(i,j)] = True # col, 1+2
                    
                    if i+1<=N and (state[i+1][j]=="0" or state[i+1][j]=="M") and i+2<=N and (state[i+2][j]=="0" or state[i+2][j]=="M") and i+3<=N and (state[i+3][j]=="0" or state[i+3][j]=="B"):
                        bat_col_dic[(i,j)] = True # col, 1+3


        #####################################################################
        for num in range(0, S[0]-len(ship_lst)):
            sub = Ship(size=1, row_dic=sub_dic)
            ship_lst.append(sub)
        
        for num in range(0, S[1]):
            des = Ship(size=2, row_dic=des_row_dic, col_dic=des_col_dic)
            ship_lst.append(des)

        for num in range(0, S[2]):
            cru = Ship(size=3, row_dic=cru_row_dic, col_dic=cru_col_dic)
            ship_lst.append(cru)

        for num in range(0, S[3]):
            bat = Ship(size=4, row_dic=bat_row_dic, col_dic=bat_col_dic)
            ship_lst.append(bat)


        # ####################################################################
        # for ship in ship_lst:
        #     if len(ship.row_dic) != 0: print(ship.row_dic)
        #     if len(ship.col_dic) != 0: print(ship.col_dic)
        
        # print("assigned_dic:") 
        # print(assigned_dic)
        # print("constraint_dic:") 
        # print(constraint_dic)
        # print_state(state)

    return state

def print_state(state): # for debug
    string = " "
    for j in C:
        string += str(j)
    string += "\n"
    i = 0
    for substate in state:
        substring = str(R[i])
        i += 1
        for item in substate:
            if item == "W":
                substring += '\033[94m'
                substring += item
                substring += '\033[0m'
            elif item != "0":
                substring += '\033[93m'
                substring += item
                substring += '\033[0m'        
            else:
                substring += item
        string += substring
        string += '\n'
    print(string)

def print_output(ship_lst): # for debug
    state = []
    sub_state = [" "]
    for j in C:
        sub_state.append(str(j))
    state.append(sub_state)
    for i in R:
        sub_state = []
        sub_state.append(str(i))
        for j in R:
            sub_state.append("\033[94mW\033[0m")
        state.append(sub_state)

    for ship in ship_lst:
        if len(ship.row_dic) == 1:
            for only_i, only_j in ship.row_dic:
                if ship.size == 1:
                    state[only_i+1][only_j+1] = "\033[93mS\033[0m"
                elif ship.size == 2:
                    state[only_i+1][only_j+1] = "\033[93mL\033[0m"
                    state[only_i+1][only_j+2] = "\033[93mR\033[0m"
                elif ship.size == 3:
                    state[only_i+1][only_j+1] = "\033[93mL\033[0m"
                    state[only_i+1][only_j+2] = "\033[93mM\033[0m"
                    state[only_i+1][only_j+3] = "\033[93mR\033[0m"
                else:
                    state[only_i+1][only_j+1] = "\033[93mL\033[0m"
                    state[only_i+1][only_j+2] = "\033[93mM\033[0m"
                    state[only_i+1][only_j+3] = "\033[93mM\033[0m"
                    state[only_i+1][only_j+4] = "\033[93mR\033[0m"
        else:
            for only_i, only_j in ship.col_dic:
                if ship.size == 1:
                    state[only_i+1][only_j+1] = "\033[93mS\033[0m"
                elif ship.size == 2:
                    state[only_i+1][only_j+1] = "\033[93mT\033[0m"
                    state[only_i+2][only_j+1] = "\033[93mB\033[0m"
                elif ship.size == 3:
                    state[only_i+1][only_j+1] = "\033[93mT\033[0m"
                    state[only_i+2][only_j+1] = "\033[93mM\033[0m"
                    state[only_i+3][only_j+1] = "\033[93mB\033[0m"
                else:
                    state[only_i+1][only_j+1] = "\033[93mT\033[0m"
                    state[only_i+2][only_j+1] = "\033[93mM\033[0m"
                    state[only_i+3][only_j+1] = "\033[93mM\033[0m"
                    state[only_i+4][only_j+1] = "\033[93mB\033[0m"

    for i in range(0,len(state)):
        print("".join(item for item in state[i]))

def FC(ship_lst):

    curr_R = [0] * len(R)
    curr_C = [0] * len(C)
    for assigned_idx in assigned_dic:
        assigned_ship = ship_lst[assigned_idx]

        if len(assigned_ship.col_dic) == 0: # only variable in row_dic
            # print(assigned_ship.row_dic)
            for only_i, only_j in assigned_ship.row_dic:
                curr_R[only_i] += assigned_ship.size
                for size in range(0, assigned_ship.size):
                    curr_C[only_j+size] += 1
        else: # only variable in col_dic
            # print(assigned_ship.col_dic)
            for only_i, only_j in assigned_ship.col_dic:
                curr_C[only_j] += assigned_ship.size
                for size in range(0, assigned_ship.size):
                    curr_R[only_i+size] += 1
    # print(curr_R, curr_C)


    # if all variable are assigned
    is_end = True
    for ship in ship_lst:
        if len(assigned_dic) != len(ship_lst):
            is_end = False
            break
    if is_end:
        is_constraint_match = True
        for i in range(0, len(R)):
            if R[i] != curr_R[i]:
                is_constraint_match = False
                break

            if C[i] != curr_C[i]:
                is_constraint_match = False
                break

        if not is_constraint_match:
            return False, []
        else:
            return True, ship_lst
    
    # forward check algorithm & pick a variable as ship
    for idx in range(0, len(ship_lst)):
        if len(ship_lst)-(idx+1) in assigned_dic:
            continue # already elminated to only one value 

        ship = ship_lst[-(idx+1)]
        # print(ship.size)

        # all current row0/col constarint
        # curr_R = [0] * len(R)
        # curr_C = [0] * len(C)
        # print("current_assigned_dic")
        # print(assigned_dic)
        # for assigned_idx in assigned_dic:
        #     assigned_ship = ship_lst[assigned_idx]

        #     if len(assigned_ship.col_dic) == 0: # only variable in row_dic
        #         print(assigned_ship.row_dic)
        #         for only_i, only_j in assigned_ship.row_dic:
        #             curr_R[only_i] += assigned_ship.size
        #             for size in range(0, assigned_ship.size):
        #                 curr_C[only_j+size] += 1
        #     else: # only variable in col_dic
        #         print(assigned_ship.col_dic)
        #         for only_i, only_j in assigned_ship.col_dic:
        #             curr_C[only_j] += assigned_ship.size
        #             for size in range(0, assigned_ship.size):
        #                 curr_R[only_i+size] += 1
        # print(curr_R, curr_C)


        for key in ship.row_dic:

            DWO, i, j = False, key[0], key[1]

            # for each constraint C over variable-ship
            # check if I placed this ship here, it will not exceed related row constraint
            # print(key, curr_R[i], ship.size, R[i])
            if curr_R[i] + ship.size > R[i]:  # cannot place this ship
                continue

            # check if I placed this ship here, it will not exceed every related col constraint
            is_col_ok = True
            for size in range(0, ship.size):
                if j+size < len(C) and curr_C[j+size] + 1 > C[j+size]:
                    is_col_ok = False
                    break
            if not is_col_ok:  # cannot place this ship
                continue

            # if satisfy row/col constraint, then I can place it here, and will surround by water
            new_ship_lst = copy.deepcopy(ship_lst)    
            new_ship_lst[-(idx+1)].row_dic.clear()
            new_ship_lst[-(idx+1)].col_dic.clear()
            new_ship_lst[-(idx+1)].row_dic[(i,j)] = True
            assigned_dic[len(ship_lst)-(idx+1)] = True
            
            # elminate the other ship's domain cannot be surrounded by water
            water_set = set()
            for size in range(-1, ship.size+1):
                water_set.add((i-1, j+size))
                water_set.add((i, j+size))
                water_set.add((i+1, j+size))

            for new_idx in range(0, len(ship_lst)):
                if len(ship_lst)-(new_idx+1) in assigned_dic:
                    continue # already elminated to only one value 
                
                new_ship = ship_lst[-(new_idx+1)]

                water_addition = set()
                if new_ship.size >= 2:
                    water_addition.add((i-1, j-2))
                    water_addition.add((i, j-2))
                    water_addition.add((i+1, j-2))
                if new_ship.size >= 3:
                    water_addition.add((i-1, j-3))
                    water_addition.add((i, j-3))
                    water_addition.add((i+1, j-3))
                if new_ship.size == 4:
                    water_addition.add((i-1, j-4))
                    water_addition.add((i, j-4))
                    water_addition.add((i+1, j-4))

                for new_key in new_ship.row_dic:
                    if new_key in water_set:
                        new_ship_lst[-(new_idx+1)].row_dic.pop(new_key)
                    
                    if new_key in water_addition:
                        new_ship_lst[-(new_idx+1)].row_dic.pop(new_key)

                water_addition = set()
                if new_ship.size >= 2:
                    water_addition.add((i-2, j-1))
                    water_addition.add((i-2, j))
                    water_addition.add((i-2, j+1))
                    if ship.size > 1: 
                        water_addition.add((i-2, j+2))
                        if ship.size > 2:
                            water_addition.add((i-2, j+3))
                            if ship.size > 3:
                                water_addition.add((i-2, j+4))

                if new_ship.size >= 3:
                    water_addition.add((i-3, j-1))
                    water_addition.add((i-3, j))
                    water_addition.add((i-3, j+1))
                    if ship.size > 1: 
                        water_addition.add((i-3, j+2))
                        if ship.size > 2:
                            water_addition.add((i-3, j+3))
                            if ship.size > 3:
                                water_addition.add((i-3, j+4))

                if new_ship.size == 4:
                    water_addition.add((i-4, j-1))
                    water_addition.add((i-4, j))
                    water_addition.add((i-4, j+1))
                    if ship.size > 1: 
                        water_addition.add((i-4, j+2))
                        if ship.size > 2:
                            water_addition.add((i-4, j+3))
                            if ship.size > 3:
                                water_addition.add((i-4, j+4))

                for new_key in new_ship.col_dic:
                    if new_key in water_set:
                        new_ship_lst[-(new_idx+1)].col_dic.pop(new_key)
                    
                    if new_key in water_addition:
                        new_ship_lst[-(new_idx+1)].col_dic.pop(new_key)
                    
                # if any ship DWO, then DWO
                if len(new_ship.row_dic) + len(new_ship.col_dic) == 0:
                    DWO = True
                    break

            # if not DWO, then next level with curr_key with this curr_ship
            if DWO:
                assigned_dic.pop(len(ship_lst)-(idx+1))
                # print("poped assigned_dic")
                # print(assigned_dic)
            else:
                # make sure constraint point has ship
                is_valid = if_need_check_constraint_dic(new_ship_lst)
                if not is_valid:
                    assigned_dic.pop(len(ship_lst)-(idx+1))
                    # print("poped assigned_dic" + str(len(ship_lst)-(idx+1)))
                    # print(assigned_dic)
                else:
                    is_terminal, result_lst = FC(new_ship_lst) 
                    if is_terminal:
                        return True, result_lst
                    else:
                        assigned_dic.pop(len(ship_lst)-(idx+1))
                        # print("poped assigned_dic" + str(len(ship_lst)-(idx+1)))
                        # print(assigned_dic)

        for key in ship.col_dic:
            DWO, i, j = False, key[0], key[1]

            # for each constraint C over variable-ship
            # check if I placed this ship here, it will not exceed related col constraint
            if curr_C[j] + ship.size > C[j]:  # cannot place this ship
                continue

            # check if I placed this ship here, it will not exceed every related row constraint
            is_row_ok = True
            for size in range(0, ship.size):
                if i+size < len(R) and curr_R[i+size] + 1 > R[i+size]:
                    is_row_ok = False
                    break
            if not is_row_ok:  # cannot place this ship
                continue

            # if satisfy row/col constraint, then I can place it here, and will surround by water
            new_ship_lst = copy.deepcopy(ship_lst)    
            new_ship_lst[-(idx+1)].row_dic.clear()
            new_ship_lst[-(idx+1)].col_dic.clear()
            new_ship_lst[-(idx+1)].col_dic[(i,j)] = True
            assigned_dic[len(ship_lst)-(idx+1)] = True

            # elminate the other ship's domain cannot be surrounded by water
            water_set = set()
            for size in range(-1, ship.size+1):
                water_set.add((i+size, j-1))
                water_set.add((i+size, j))
                water_set.add((i+size, j+1))

            for new_idx in range(0, len(ship_lst)):
                if len(ship_lst)-(new_idx+1) in assigned_dic:
                    continue # already elminated to only one value 
                
                new_ship = ship_lst[-(new_idx+1)]

                water_addition = set()
                if new_ship.size >= 2:
                    water_addition.add((i-1, j-2))
                    water_addition.add((i, j-2))
                    water_addition.add((i+1, j-2))
                    if ship.size > 1: 
                        water_addition.add((i+2, j-2))
                        if ship.size > 2:
                            water_addition.add((i+3, j-2))
                            if ship.size > 3:
                                water_addition.add((i+4, j-2))

                if new_ship.size >= 3:
                    water_addition.add((i-1, j-3))
                    water_addition.add((i, j-3))
                    water_addition.add((i+1, j-3))
                    if ship.size > 1: 
                        water_addition.add((i+2, j-3))
                        if ship.size > 2:
                            water_addition.add((i+3, j-3))
                            if ship.size > 3:
                                water_addition.add((i+4, j-3))

                if new_ship.size == 4:
                    water_addition.add((i-1, j-4))
                    water_addition.add((i, j-4))
                    water_addition.add((i+1, j-4))
                    if ship.size > 1: 
                        water_addition.add((i+2, j-4))
                        if ship.size > 2:
                            water_addition.add((i+3, j-4))
                            if ship.size > 3:
                                water_addition.add((i+4, j-4))

                for new_key in new_ship.row_dic:
                    if new_key in water_set:
                        new_ship_lst[-(new_idx+1)].row_dic.pop(new_key)
                        # print(new_key)
                    if new_key in water_addition:
                        new_ship_lst[-(new_idx+1)].row_dic.pop(new_key)

                water_addition = set()
                if new_ship.size >= 2:
                    water_addition.add((i-2, j-1))
                    water_addition.add((i-2, j))
                    water_addition.add((i-2, j+1))
                if new_ship.size >= 3:
                    water_addition.add((i-3, j-1))
                    water_addition.add((i-3, j))
                    water_addition.add((i-3, j+1))
                if new_ship.size == 4:
                    water_addition.add((i-4, j-1))
                    water_addition.add((i-4, j))
                    water_addition.add((i-4, j+1))

                for new_key in new_ship.col_dic:
                    if new_key in water_set:
                        new_ship_lst[-(new_idx+1)].col_dic.pop(new_key)
                    
                    if new_key in water_addition:
                        new_ship_lst[-(new_idx+1)].col_dic.pop(new_key)

                # if any ship DWO, then DWO
                if len(new_ship.row_dic) + len(new_ship.col_dic) == 0:
                    DWO = True
                    break
                
            # if not DWO, then next level with curr_key with this curr_ship
            if DWO:
                assigned_dic.pop(len(ship_lst)-(idx+1))
                # print("poped assigned_dic" + str(len(ship_lst)-(idx+1)))
                # print(assigned_dic)
            else:
                # print("--------------")
                is_valid = if_need_check_constraint_dic(new_ship_lst)
                if not is_valid:
                    assigned_dic.pop(len(ship_lst)-(idx+1))
                    # print("poped assigned_dic" + str(len(ship_lst)-(idx+1)))
                    # print(assigned_dic)
                else:
                    is_terminal, result_lst = FC(new_ship_lst) 
                    if is_terminal:
                        return True, result_lst
                    else:
                        assigned_dic.pop(len(ship_lst)-(idx+1))
                        # print("poped assigned_dic" + str(len(ship_lst)-(idx+1)))
                        # print(assigned_dic)


        # touch bottom stop    
        if len(ship_lst)-(idx+1) not in assigned_dic:
            break

    return False, []       

## make sure if the current assigned ship does not contain constraint point, the rest of the unassgiend ship has domain cover this
def if_need_check_constraint_dic(ship_lst):

    # check if current assigned ship contains all constraint point
    to_return_dic = {}
    to_return_dic = constraint_dic.copy()

    for fixed_i, fixed_j in constraint_dic: 
        constraint_letter = constraint_dic[(fixed_i, fixed_j)] 
        
        for assigned_idx in assigned_dic:
            should_break = False
            assigned_ship = ship_lst[assigned_idx]

            if len(assigned_ship.col_dic) == 0: # only variable in row_dic
                for only_i, only_j in assigned_ship.row_dic: #LRM

                    if assigned_ship.size > 1 and constraint_letter == "L":
                        if only_i == fixed_i and only_j == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))
                                should_break = True

                    if assigned_ship.size > 1 and constraint_letter == "R":
                        if only_i == fixed_i and only_j+assigned_ship.size-1 == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))
                                should_break = True

                    if assigned_ship.size > 2 and constraint_letter == "M":
                        if only_i == fixed_i and only_j+1 == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))
                                # print("here1")
                                should_break = True
                        
                        if assigned_ship.size == 4:
                            if only_i == fixed_i and only_j+2 == fixed_j:
                                # this constarint key & postion pair is already in assign list which is valid
                                if (fixed_i, fixed_j) in to_return_dic:
                                    to_return_dic.pop((fixed_i, fixed_j))
                                    # print("here2")
                                    should_break = True

            else: # only variable in col_dic 
                for only_i, only_j in assigned_ship.col_dic: #TBM
                    # print(only_i, only_j)

                    if assigned_ship.size > 1 and constraint_letter == "T":
                        if only_i == fixed_i and only_j == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))   
                                should_break = True 

                    if assigned_ship.size > 1 and constraint_letter == "B":
                        if only_i+assigned_ship.size-1 == fixed_i and only_j == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))
                                should_break = True

                    if assigned_ship.size > 2 and constraint_letter == "M":
                        if only_i+1 == fixed_i and only_j == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                to_return_dic.pop((fixed_i, fixed_j))
                                should_break = True
                                # print(fixed_i, fixed_j)
                                # print("here3")
                        
                        if assigned_ship.size == 4:
                            if only_i+2 == fixed_i and only_j == fixed_j:
                                # this constarint key & postion pair is already in assign list which is valid
                                if (fixed_i, fixed_j) in to_return_dic:
                                    to_return_dic.pop((fixed_i, fixed_j))
                                    should_break = True
                                    # print("here4")

            if should_break:
                break

    
    for fixed_i, fixed_j in to_return_dic: 
        is_satisfy = False
        constraint_letter = to_return_dic[(fixed_i, fixed_j)] 

        for idx in range(0, len(ship_lst)):
            if len(ship_lst)-(idx+1) in assigned_dic:
                continue # already elminated to only one value 
            
            should_break = False
            ship = ship_lst[-(idx+1)]

            for only_i, only_j in ship.row_dic: #LRM

                if ship.size > 1 and constraint_letter == "L":
                    if only_i == fixed_i and only_j == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True

                if ship.size > 1 and constraint_letter == "R":
                    if only_i == fixed_i and only_j+ship.size-1 == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True

                if ship.size > 2 and constraint_letter == "M":
                    if only_i == fixed_i and only_j+1 == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True
                    
                    if ship.size == 4:
                        if only_i == fixed_i and only_j+2 == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                should_break = True
            
            if should_break:
                is_satisfy = True
                break
 
            for only_i, only_j in ship.col_dic: #TBM
                # print(only_i, only_j)

                if ship.size > 1 and constraint_letter == "T":
                    if only_i == fixed_i and only_j == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True 

                if ship.size > 1 and constraint_letter == "B":
                    if only_i+ship.size-1 == fixed_i and only_j == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True

                if ship.size > 2 and constraint_letter == "M":
                    if only_i+1 == fixed_i and only_j == fixed_j:
                        # this constarint key & postion pair is already in assign list which is valid
                        if (fixed_i, fixed_j) in to_return_dic:
                            should_break = True
        
                            # print(fixed_i, fixed_j)
                            # print("here3")
                    
                    if ship.size == 4:
                        if only_i+2 == fixed_i and only_j == fixed_j:
                            # this constarint key & postion pair is already in assign list which is valid
                            if (fixed_i, fixed_j) in to_return_dic:
                                should_break = True
                                # print("here4")

            if should_break:
                is_satisfy = True
                break
            
        if not is_satisfy:
            return False
    
    return True

def write_output(output_file_name, ship_lst):
    state = []
    for i in R:
        sub_state = []
        for j in R:
            sub_state.append("W")
        state.append(sub_state)

    for ship in ship_lst:
        if len(ship.row_dic) == 1:
            for only_i, only_j in ship.row_dic:
                if ship.size == 1:
                    state[only_i][only_j] = "S"
                elif ship.size == 2:
                    state[only_i][only_j] = "L"
                    state[only_i][only_j+1] = "R"
                elif ship.size == 3:
                    state[only_i][only_j] = "L"
                    state[only_i][only_j+1] = "M"
                    state[only_i][only_j+2] = "R"
                else:
                    state[only_i][only_j] = "L"
                    state[only_i][only_j+1] = "M"
                    state[only_i][only_j+2] = "M"
                    state[only_i][only_j+3] = "R"
        else:
            for only_i, only_j in ship.col_dic:
                if ship.size == 1:
                    state[only_i][only_j] = "S"
                elif ship.size == 2:
                    state[only_i][only_j] = "T"
                    state[only_i+1][only_j] = "B"
                elif ship.size == 3:
                    state[only_i][only_j] = "T"
                    state[only_i+1][only_j] = "M"
                    state[only_i+2][only_j] = "B"
                else:
                    state[only_i][only_j] = "T"
                    state[only_i+1][only_j] = "M"
                    state[only_i+2][only_j] = "M"
                    state[only_i+3][only_j] = "B"

    # write output path to file
    with open(output_file_name, 'w') as f:
        for i in range(0,len(state)):
            if i < len(state)-1:
                f.write("".join(item for item in state[i]) + "\n")
            else:
                f.write("".join(item for item in state[i]))

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    # for i in range(0,16):
    #     print(i)
        
    # input_file_name = "/Users/spencersun/Desktop/CSC384/lab3/Validation/" + str(i)+".txt"
    # output_file_name = "/Users/spencersun/Desktop/CSC384/lab3/Output/"+str(i)+".txt"

    read_input(input_file_name)
    have_solution, solution = FC(ship_lst)
    # print(have_solution)
    if have_solution:
    # for a in solution:
    #     print(a.col_dic)
    #     print(a.row_dic)
        # print_output(solution)
        write_output(output_file_name, solution)

if __name__ == '__main__':
    main()



