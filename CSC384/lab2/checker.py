from json.encoder import INFINITY
import string
import sys
import copy
import queue
from tokenize import String
from xmlrpc.client import boolean
MAX_DEPTH = 11

global cache_dic
cache_dic = {}

def read_input(input_file_path):
    # read the input puzzle from file to a double list of each grid
    input_state = []
    with open(input_file_path) as f:
        lines = f.readlines()
        for line in lines:
            line_lst = []
            for char in line:
                if char != '\n':
                    line_lst.append(char)
            input_state.append(line_lst)

    return input_state

def write_output(output_file_name, state):
    # write output path to file
    with open(output_file_name, 'w') as f:
        for i in range(0,len(state)):
            if i < len(state)-1:
                f.write("".join(item for item in state[i]) + "\n")
            else:
                f.write("".join(item for item in state[i]))

def terminal(state, is_MAX):
    # check for goal state
    black_num = 0
    red_num = 0

    for substate in state:
        for item in substate:
            if item == 'b' or item == "B":
                black_num += 1
            if item == "r" or item == "R":
                red_num += 1
    
    if black_num == 0 or red_num == 0:
        return True

    if find_successor(state, not is_MAX, is_termination=True).qsize() == 0:
        return True
    
    return False

def utility(state):
    # check current state value
    value_to_return = 0

    for substate in state:
        for item in substate:
            if item == 'b':
                value_to_return -= 1
            elif item == "B":
                value_to_return -= 2
            elif item == "r":
                value_to_return += 1
            elif item == "R":
                value_to_return += 2
    
    return value_to_return

def own_heuristic(state, is_MAX, is_queue=True):
    
    # return 0
    # 1. Number of pawns;
    pawn_r = 0
    pawn_b = 0

    # 2. Number of Kings;
    king_R = 0
    king_B = 0

    # 3. Number of safe pawns;
    safe_r = 0
    safe_b = 0

    # 4. Number of safe Kings;
    safe_R = 0
    safe_B = 0

    # 5. Number of moveable pawns
    mov_r = 0
    mov_b = 0

    # 6. Number of moveable Kings
    mov_R = 0
    mov_B = 0

    # 7. Aggregated distance of the pawns to promotion line
    distance_r = 0
    distance_b = 0

    # 8. Number of unoccupied fields on promotion line.
    space_for_r = 0
    space_for_b = 0

    for x in range(0,len(state)):
        for y in range(0,len(state[x])):
            item = state[x][y]
            if item == ".":
                if x == 0 and y%2 == 1:
                    space_for_r += 1
                elif x == 7 and y%2 == 0:
                    space_for_b += 1
                continue
            else:
                if item == "r":
                    pawn_r += 1
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        safe_r += 1
                    
                    if x != 0:
                        distance_r += 1

                    if x-2 >= 0 and y-2 >= 0 and state[x-2][y-2] == ".":
                        mov_r += 1
                    if x-2 >= 0 and y+2 <= 7 and state[x-2][y+2] == ".":
                        mov_r += 1

                if item == 'b':
                    pawn_b += 1
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        safe_b += 1

                    if x != 7:
                        distance_r += 1
                    
                    if x+2 <= 7 and y-2 >= 0 and state[x+2][y-2] == ".":
                        mov_b += 1
                    if x+2 <= 7 and y+2 <= 7 and state[x+2][y+2] == ".":
                        mov_b += 1

                if item == "R":
                    king_R += 1
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        safe_R += 1

                    if x-2 >= 0 and y-2 >= 0 and state[x-2][y-2] == ".":
                        mov_R += 1
                    if x-2 >= 0 and y+2 <= 7 and state[x-2][y+2] == ".":
                        mov_R += 1
                    if x+2 <= 7 and y-2 >= 0 and state[x+2][y-2] == ".":
                        mov_R += 1
                    if x+2 <= 7 and y+2 <= 7 and state[x+2][y+2] == ".":
                        mov_R += 1

                if item == "B":
                    king_B += 1
                    if x == 0 or x == 7 or y == 0 or y == 7:
                        safe_B += 1

                    if x-2 >= 0 and y-2 >= 0 and state[x-2][y-2] == ".":
                        mov_B += 1
                    if x-2 >= 0 and y+2 <= 7 and state[x-2][y+2] == ".":
                        mov_B += 1
                    if x+2 <= 7 and y-2 >= 0 and state[x+2][y-2] == ".":
                        mov_B += 1
                    if x+2 <= 7 and y+2 <= 7 and state[x+2][y+2] == ".":
                        mov_B += 1

    if pawn_r == 0:
        space_for_r = 0
    if pawn_b == 0:
        space_for_b = 0

    value =  1*(pawn_r - pawn_b + 2*(king_R - king_B)) + 0*(safe_r - safe_b + 2*(safe_R - safe_B)) + 0*(mov_r - mov_b + 2*(mov_R - mov_B)) + 0*(distance_r - distance_b) + 0*(space_for_r - space_for_b) 

    if not is_queue:
        return value
    else:
        if is_MAX:
            if pawn_b + king_B == 0:       
                value = -1000
            return -1*value
        else:
            if pawn_r + king_R == 0:
                value = 1000
            return value    

def find_by_recursion(successor_lst: queue.PriorityQueue, state: list, i: list, type: String, can_push: boolean, is_MAX: boolean, is_termination):
    is_end = True

    if type == "R" or type == "r":
        jump_type_0 = "b"
        jump_type_1 = "B"
    else:
        jump_type_0 = "r"
        jump_type_1 = "R"       
    
    if type == "r":
        dx_dy_lst = [[-2,-2],[-2,+2]]
    elif type == "b":
        dx_dy_lst = [[+2,-2],[+2,+2]]
    else:
        dx_dy_lst = [[-2,-2],[-2,+2],[+2,-2],[+2,+2]]

    # check jump
    for dx,dy in dx_dy_lst:
        x,y = i[0],i[1]
        
        if x+dx < 0 or x+dx > 7 or y+dy < 0 or y+dy > 7:
            continue

        if state[x+dx][y+dy] == '.':
            if state[x+int(dx/2)][y+int(dy/2)] == jump_type_0 or state[x+int(dx/2)][y+int(dy/2)] == jump_type_1:
                next_state = copy.deepcopy(state)
                if type == "r" and x+dx == 0:
                    next_state[x+dx][y+dy] = "R"
                elif type == "b" and x+dx == 7:
                    next_state[x+dx][y+dy] = "B"
                else:
                    next_state[x+dx][y+dy] = type
                next_state[x+int(dx/2)][y+int(dy/2)] = '.'
                next_state[x][y] = '.'

                is_end = False
                if is_termination and successor_lst.qsize() != 0:
                    return successor_lst
                find_by_recursion(successor_lst, next_state, [x+dx,y+dy], type, True, is_MAX, is_termination)

    if is_end and can_push:
        successor_lst.put((own_heuristic(state, is_MAX), successor_lst.qsize(), state))

def find_successor(state, is_MAX, is_termination=False):
    successor_lst = queue.PriorityQueue()

    for i in range(0,len(state)):
        for j in range(0,len(state[i])):
            item = state[i][j] # "R" "r" "B" "b" "."

            if is_MAX:     # MAX -> move Red
                if item == "R":
                    find_by_recursion(successor_lst, state, [i,j], "R", False, is_MAX, is_termination)
                    if is_termination and successor_lst.qsize() != 0:
                        return successor_lst

                if item == "r":
                    find_by_recursion(successor_lst, state, [i,j], "r", False, is_MAX, is_termination)
                    if is_termination and successor_lst.qsize() != 0:
                        return successor_lst

            else:     # MIN -> move Black
                if item == "B":
                    find_by_recursion(successor_lst, state, [i,j], "B", False, is_MAX, is_termination)  
                    if is_termination and successor_lst.qsize() != 0:
                        return successor_lst

                if item == "b":
                    find_by_recursion(successor_lst, state, [i,j], "b", False, is_MAX, is_termination)               
                    if is_termination and successor_lst.qsize() != 0:
                        return successor_lst

    if successor_lst.empty():
        for i in range(0,len(state)):
            for j in range(0,len(state[i])):
                item = state[i][j] # "R" "r" "B" "b" "."

                if item == ".":
                    continue

                if is_MAX:     # MAX -> move Red
                    if item == "R":
                        # check side empty
                        R = [i,j]
                        for x,y in [[R[0]-1, R[1]-1], [R[0]-1, R[1]+1], [R[0]+1, R[1]-1], [R[0]+1, R[1]+1]]:
                            if x == R[0]-1 and x < 0:
                                continue
                            if x == R[0]+1 and x > 7:
                                continue
                            if y == R[1]-1 and y < 0:
                                continue
                            if y == R[1]+1 and y > 7:
                                continue 

                            if state[x][y] == ".":
                                next_state = copy.deepcopy(state)
                                next_state[x][y] = 'R'
                                next_state[R[0]][R[1]] = '.'

                                successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                if is_termination:
                                    return successor_lst

                    if item == "r":
                        # check side empty
                        r = [i,j]
                        if r[0]-1 < 0: 
                            print("something wrong") # should be R not r
                        else:
                            x = r[0]-1 
                            if r[1]-1 >= 0:
                                y = r[1]-1
                                if state[x][y] == ".":
                                    next_state = copy.deepcopy(state)
                                    if x == 0:
                                        next_state[x][y] = 'R'
                                    else:
                                        next_state[x][y] = 'r'
                                    next_state[r[0]][r[1]] = '.'

                                    successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                    if is_termination:
                                        return successor_lst
                            
                            if r[1]+1 <= 7:
                                y = r[1]+1
                                if state[x][y] == ".":
                                    next_state = copy.deepcopy(state)
                                    if x == 0:
                                        next_state[x][y] = 'R'
                                    else:
                                        next_state[x][y] = 'r'
                                    next_state[r[0]][r[1]] = '.'

                                    successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                    if is_termination:
                                        return successor_lst
                
                else:
                    if item == "B":
                        # check side empty
                        B = [i,j]
                        for x,y in [[B[0]-1, B[1]-1], [B[0]-1, B[1]+1], [B[0]+1, B[1]-1], [B[0]+1, B[1]+1]]:
                            if x == B[0]-1 and x < 0:
                                continue
                            if x == B[0]+1 and x > 7:
                                continue
                            if y == B[1]-1 and y < 0:
                                continue
                            if y == B[1]+1 and y > 7:
                                continue 

                            if state[x][y] == ".":
                                next_state = copy.deepcopy(state)
                                next_state[x][y] = 'B'
                                next_state[B[0]][B[1]] = '.'

                                successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                if is_termination:
                                    return successor_lst
            
                    if item == "b":
                        # check side empty
                        b = [i,j]
                        if b[0]+1 > 7: 
                            print("something wrong") # should be B not b
                        else:
                            x = b[0]+1 
                            if b[1]-1 >= 0:
                                y = b[1]-1
                                if state[x][y] == ".":
                                    next_state = copy.deepcopy(state)
                                    if x == 7:
                                        next_state[x][y] = 'B'
                                    else:
                                        next_state[x][y] = 'b'
                                    next_state[b[0]][b[1]] = '.'

                                    successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                    if is_termination:
                                        return successor_lst
                            
                            if b[1]+1 <= 7:
                                y = b[1]+1
                                if state[x][y] == ".":
                                    next_state = copy.deepcopy(state)
                                    if x == 7:
                                        next_state[x][y] = 'B'
                                    else:
                                        next_state[x][y] = 'b'
                                    next_state[b[0]][b[1]] = '.'

                                    successor_lst.put((own_heuristic(next_state, is_MAX), successor_lst.qsize(), next_state))
                                    if is_termination:
                                        return successor_lst

    return successor_lst

def print_state(state): # for debug
    for substate in state:
        print("".join(item for item in substate))
    print()

def convert_to_cache_key(state, is_MAX):
    # as key for explored state dictionary
    return str(is_MAX) + ''.join(''.join(i) for i in state)

def AlphaBeta(state, alpha, beta, is_MAX, depth):
    global cache_dic
    # next move that is considered best to return
    best_state = None

    # check goal state for termination
    if terminal(state, is_MAX) or depth == MAX_DEPTH:
        return best_state, own_heuristic(state, is_MAX, is_queue=False)

    # assign initial MINMAX value
    if is_MAX: 
        value = -INFINITY
    else:
        value = INFINITY
    
    next_queue = find_successor(state, is_MAX)

    if next_queue.qsize() == 0:
        return best_state, own_heuristic(state, is_MAX, is_queue=False)

    while not next_queue.empty():
        next_state = next_queue.get()[-1]
        
        # caching state
        key_string = convert_to_cache_key(next_state, not is_MAX)
        if cache_dic.get(key_string) and depth+1 >= cache_dic[key_string][1]:
            next_value = cache_dic.get(key_string)[0]
        else:
            next_value = AlphaBeta(next_state, alpha, beta, not is_MAX, depth+1)[1]
            cache_dic[key_string] = next_value, depth+1

        if is_MAX:
            if value < next_value:
                best_state, value = next_state, next_value
            if value >= beta:
                return best_state,value
            alpha = max(alpha, value)
        else:
            if value > next_value:
                best_state, value = next_state, next_value
            if value <= alpha:
                return best_state,value
            beta = min(beta, value)

    return best_state,value

def main():
    input_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    input_state = read_input(input_file_name)
    output_state, value = AlphaBeta(input_state, -INFINITY, INFINITY, True, 0)
    if output_state == None:
        write_output(output_file_name, input_state)
    else:
        write_output(output_file_name, output_state)

if __name__ == '__main__':
    main()
