import sys
import copy
import queue

class Node:
    state = [
        [], #empty   , input 0
        [], #size 2x2, input 1
        [], #size horizontal, input 2-6
        [], #size vertical, input 2-6
        [], #size 1x1, input 7
    ]

    def __init__(self, state, hval, gval, parent):
        self.state = state
        self.hval = hval
        self.gval = gval
        self.parent = parent

def read_input_puzzle(input_file_path):
    # read the input puzzle from file to a double list of integer type
    input_puzzle = []
    with open(input_file_path) as f:
        lines = f.readlines()
        for line in lines:
            line_lst = []
            for char in line:
                if char != '\n':
                    line_lst.append(int(char))
            input_puzzle.append(line_lst)

    state = [
        [], #empty   , input 0
        [], #size 2x2, input 1
        [], #size horizontal, input 2-6
        [], #size vertical, input 2-6
        [], #size 1x1, input 7
    ]
    for i in range(0,8):
        for x in range(0,len(input_puzzle)):
            for y in range(0, len(input_puzzle[x])):
                if input_puzzle[x][y] == i:
                    if i == 0:
                        state[0].append([x,y])
                    elif i == 7:
                        state[4].append([x,y])
                    elif i == 1 and len(state[1]) == 0:
                        state[1].append([x,y])
                    elif i in [2,3,4,5,6]:
                        if y+1 < 4 and input_puzzle[x][y+1] == i:
                            state[2].append([x,y])
                        elif x+1 < 5 and input_puzzle[x+1][y] == i:
                            state[3].append([x,y])   
    
    node = Node(copy.deepcopy(state), 0, 0, None)
    return node

def print_puzzle_to_output(state):
    # from any state to print a current puzzle to output form
    output_table = [['','','',''],['','','',''],['','','',''],['','','',''],['','','','']]
    for i in range(0,len(state)):
        sub_state = state[i]
        for block in sub_state:
            if i == 0:
                output_table[block[0]][block[1]] = '0'
            elif i == 1:
                output_table[block[0]][block[1]] = '1'
                output_table[block[0]+1][block[1]] = '1'
                output_table[block[0]][block[1]+1] = '1'
                output_table[block[0]+1][block[1]+1] = '1'
            elif i == 2:
                output_table[block[0]][block[1]] = '2'
                output_table[block[0]][block[1]+1] = '2'
            elif i == 3:
                output_table[block[0]][block[1]] = '3'
                output_table[block[0]+1][block[1]] = '3'
            else:
                output_table[block[0]][block[1]] = '4'

    return '\n'.join(''.join(i) for i in output_table)

def convert_puzzle_to_string(state):
    # as key for explored state dictionary
    output_table = [['','','',''],['','','',''],['','','',''],['','','',''],['','','','']]
    for i in range(0,len(state)):
        sub_state = state[i]
        for block in sub_state:
            if i == 0:
                output_table[block[0]][block[1]] = '0'
            elif i == 1:
                output_table[block[0]][block[1]] = '1'
                output_table[block[0]+1][block[1]] = '1'
                output_table[block[0]][block[1]+1] = '1'
                output_table[block[0]+1][block[1]+1] = '1'
            elif i == 2:
                output_table[block[0]][block[1]] = '2'
                output_table[block[0]][block[1]+1] = '2'
            elif i == 3:
                output_table[block[0]][block[1]] = '3'
                output_table[block[0]+1][block[1]] = '3'
            else:
                output_table[block[0]][block[1]] = '4'

    return ''.join(''.join(i) for i in output_table)

def write_output_puzzle(output_file_path, length, queue):
    # write output path to file
    with open(output_file_path, 'w') as f:
        f.write("Cost of the solution: " + str(length) + "\n")
        while not queue.empty():
            f.write(print_puzzle_to_output(queue.get()) + "\n\n")

def get_path(node):
    # back trace the path from the goal node to initial node
    output_length = 0
    output_queue = queue.LifoQueue()
    while node != None:
        output_queue.put(node.state)
        node = node.parent
        output_length += 1
    return output_length-1, output_queue

def find_cost(state):
    # A* heuristic function
    h_val_to_return = 0
    
    x = state[1][0][0]
    y = state[1][0][1]

    if [x,y] not in [[3,3],[4,0],[4,1],[4,2],[4,3]]:
        h_val_to_return = h_val_to_return + abs(x-3) + abs(y-1)
    else:
        print("wrong")

    return h_val_to_return

def find_successor(curr_node, is_astar):
    state_lst_to_return = []

    curr_state = copy.deepcopy(curr_node.state)
    blank = curr_state[0]
    for i in range(1,len(curr_state)):
        sub_state = curr_state[i]
        for j in range(0,len(sub_state)):
            block = sub_state[j]

            if i == 1: # 2x2
                # left has space
                if block[1]-1 > -1 and [block[0],block[1]-1] in blank and [block[0]+1,block[1]-1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][1]+=2
                    state[0][1][1]+=2
                    state[i][j][1]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # right has space
                if block[1]+1 < 4 and [block[0],block[1]+2] in blank and [block[0]+1, block[1]+2] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][1]-=2
                    state[0][1][1]-=2
                    state[i][j][1]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)
                    
                # up has space
                if block[0]-1 > -1 and [block[0]-1,block[1]] in blank and [block[0]-1,block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][0]+=2
                    state[0][1][0]+=2
                    state[i][j][0]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)        

                # bottom has space
                if block[0]+1 < 5 and [block[0]+2,block[1]] in blank and [block[0]+2,block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][0]-=2
                    state[0][1][0]-=2
                    state[i][j][0]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

            elif i == 2: # horizontal
                # left has space
                if block[1]-1 > -1 and [block[0],block[1]-1] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0],block[1]-1] == blank[0]:
                        state[0][0][1]+=2
                    else:
                        state[0][1][1]+=2
                    state[i][j][1]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # right has space
                if block[1]+1 < 4 and [block[0],block[1]+2] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0],block[1]+2] == blank[0]:
                        state[0][0][1]-=2
                    else:
                        state[0][1][1]-=2
                    state[i][j][1]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # up has space
                if block[0]-1 > -1 and [block[0]-1,block[1]] in blank and [block[0]-1,block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][0]+=1
                    state[0][1][0]+=1
                    state[i][j][0]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # bottom has space
                if block[0]+1 < 5 and [block[0]+1,block[1]] in blank and [block[0]+1,block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][0]-=1
                    state[0][1][0]-=1
                    state[i][j][0]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)
                    
            elif i == 3: # vertical
                # left has space
                if block[1]-1 > -1 and [block[0],block[1]-1] in blank and [block[0]+1,block[1]-1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][1]+=1
                    state[0][1][1]+=1
                    state[i][j][1]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)
                    
                # right has space
                if block[1]+1 < 4 and [block[0],block[1]+1] in blank and [block[0]+1,block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    state[0][0][1]-=1
                    state[0][1][1]-=1
                    state[i][j][1]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # up has space
                if block[0]-1 > -1 and [block[0]-1,block[1]] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0]-1,block[1]] == blank[0]:
                        state[0][0][0]+=2
                    else:
                        state[0][1][0]+=2                       
                    state[i][j][0]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # bottom has space
                if block[0]+1 < 5 and [block[0]+2,block[1]] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0]+2,block[1]] == blank[0]:
                        state[0][0][0]-=2
                    else:
                        state[0][1][0]-=2
                    state[i][j][0]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

            elif i == 4: # 1x1
                # left has space
                if block[1]-1 > -1 and [block[0],block[1]-1] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0],block[1]-1] == blank[0]:
                        state[0][0][1]+=1
                    else:
                        state[0][1][1]+=1
                    state[i][j][1]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # right has space
                if block[1]+1 < 4 and [block[0],block[1]+1] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0],block[1]+1] == blank[0]:
                        state[0][0][1]-=1
                    else:
                        state[0][1][1]-=1
                    state[i][j][1]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # up has space
                if block[0]-1 > -1 and [block[0]-1,block[1]] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0]-1,block[1]] == blank[0]:
                        state[0][0][0]+=1
                    else:
                        state[0][1][0]+=1
                    state[i][j][0]-=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)

                # bottom has space
                if block[0]+1 < 5 and [block[0]+1,block[1]] in blank:
                    state = copy.deepcopy(curr_state)
                    if [block[0]+1,block[1]] == blank[0]:
                        state[0][0][0]-=1
                    else:
                        state[0][1][0]-=1
                    state[i][j][0]+=1
                    if not is_astar:
                        sus_node = Node(copy.deepcopy(state), 0, 0, curr_node)
                    else:
                        h_val = find_cost(state)
                        g_val = curr_node.gval + 1
                        sus_node = Node(copy.deepcopy(state), h_val, g_val, curr_node)
                    state_lst_to_return.append(sus_node)
    
    return state_lst_to_return

def depth_first_search(initial_node, is_astar):

    # data structure
    frontier = queue.LifoQueue()
    frontier.put(initial_node)
    
    # data structure
    explored = {}

    while not frontier.empty():
        # select and remove state Curr from Frontier
        # curr_node = Node()
        curr_node = frontier.get()

        # check if Curr is NOT in explored
        key_string = convert_puzzle_to_string(curr_node.state)
        if not explored.get(key_string):
            explored[key_string] = True

            # check if Curr is a goal state
            if curr_node.state[1][0] == [3,1]:
                return curr_node

            # add Curr's Successors to Frontier
            successor_lst = find_successor(curr_node, is_astar)
            for item in successor_lst:
                frontier.put(item)

class PriorityQueue(object):
    def __init__(self):
        self.queue = []
    
    def empty(self):
        return len(self.queue) == 0
    
    def put(self, node):
        self.queue.append(node)
    
    def get(self):
        min_idx = 0
        min_f = self.queue[0].hval + self.queue[0].gval 
        for i in range (1, len(self.queue)):
            curr_f = self.queue[i].hval + self.queue[i].gval 
            if curr_f < min_f:
                min_idx = i
                min_f = curr_f
            
        min_state = self.queue[min_idx]
        del self.queue[min_idx]
        return min_state

def a_star_search(initial_node, is_astar):

    # data structure
    frontier = PriorityQueue()
    frontier.put(initial_node)

    # data structure
    explored = {}

    while not frontier.empty():
        # select and remove state Curr from Frontier
        # curr_node = Node()
        curr_node = frontier.get()

        # check if Curr is NOT in explored
        key_string = convert_puzzle_to_string(curr_node.state)
        if not explored.get(key_string):
            explored[key_string] = True

            # check if Curr is a goal state
            if curr_node.state[1][0] == [3,1]:
                return curr_node

            # add Curr's Successors to Frontier
            successor_lst = find_successor(curr_node, is_astar)
            for item in successor_lst:
                frontier.put(item)

def advanced_heuristic_function(state):
    # own heuristic function

    # manhatten heuristic function
    h_manhatten = 0
    x = state[1][0][0]
    y = state[1][0][1]

    if [x,y] not in [[3,3],[4,0],[4,1],[4,2],[4,3]]:
        h_manhatten = h_manhatten + abs(x-3) + abs(y-1)
    else:
        print("wrong")
    
    # horizontal heuristic part
    h_horizontal = 0
    for item in state[2]:
        if item[0] in [3,4]:
            h_horizontal += 1

    # other part
    h_other = 0
    for index in [3,4]:
        for item in state[index]:
            if item in [[3,1],[3,2],[4,1],[4,2]]:
                h_other += 1

    return h_manhatten + h_horizontal + h_other

def main():
    input_file_name = sys.argv[1]
    output_file_name_dfs = sys.argv[2]
    output_file_name_astar = sys.argv[3]

    input_file_path = input_file_name
    output_file_path_dfs = output_file_name_dfs
    output_file_path_astar = output_file_name_astar

    node = read_input_puzzle(input_file_path)
    
    final_node = depth_first_search(node, False)
    length, queue = get_path(final_node)
    write_output_puzzle(output_file_path_dfs, length, queue)

    final_node = a_star_search(node, True)
    length, queue = get_path(final_node)
    write_output_puzzle(output_file_path_astar, length, queue)

if __name__ == '__main__':
    main()
