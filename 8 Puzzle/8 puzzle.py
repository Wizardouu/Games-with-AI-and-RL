import math
from math import sqrt
import time
import tkinter as tk
import random
from tkinter import *
from queue import PriorityQueue
from tkinter import messagebox
class Queue:
    def __init__(self):
        self.queue_set = set()

    def enqueue(self, item):
        self.queue_set.add(item)

    def dequeue(self):
        if not self.is_empty():
            item = next(iter(self.queue_set))
            self.queue_set.remove(item)
            return item
        else:
            raise IndexError("dequeue from empty queue")

    def top(self):
        if not self.is_empty():
            return next(iter(self.queue_set))
        else:
            raise IndexError("top of empty queue")

    def is_empty(self):
        return len(self.queue_set) == 0

    def contain(self, value):
        return value in self.queue_set


nodes_expanded = 0
parents = []
astar_path=[]
class Stack:
    def __init__(self):
        self.set = set()  # Initialize the set

    def push(self, item):
        self.set.add(item)  # Add item to the set

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        item = self.top()  # Get the top item
        self.set.remove(item)  # Remove the top item from the set
        return item

    def top(self):
        if self.is_empty():
            raise IndexError("top from an empty stack")
        # Since sets are unordered, returning an arbitrary element
        return next(iter(self.set))

    def is_empty(self):
        return len(self.set) == 0

    def contain(self, value):
        return value in self.set

class aStarNode:
    def __init__(self, value, weight,parent):
        self.value = value
        self.weight = weight
        self.parent = parent

    def __lt__(self, other):
        return self.weight < other.weight
    


def swap(i,j,grid):
    temp= list(grid)
    copied=temp[:]
    temp2=copied[i]
    copied[i]=copied[j]
    copied[j]=temp2
    return copied

def get_manhattan_distance(state):
    distance = 0
    for i in range(9):
        current_row = i/3
        current_col = i%3
        goal_row = state[i] /3
        goal_col = state[i]%3
        diff = abs(current_col-goal_col) + abs (current_row - goal_row)
        distance += diff
    return distance

def get_euclidean_distance(state):
    distance = 0
    for i in range(9):
        current_row = i/3
        current_col = i%3
        goal_row = state[i] /3
        goal_col = state[i]%3
        x = (current_col-goal_col)
        y = (current_row - goal_row)
        diff = sqrt(x*x + y*y)
        distance += diff
    return distance

def update_priority(pq, node_value, new_weight):
    temp_pq = PriorityQueue()
    updated = False
    while not pq.empty():
        node = pq.get()
        if node.value == node_value:
            if node.weight > new_weight:
                node.weight = new_weight
                updated = True
            temp_pq.put(node)
        else:
            temp_pq.put(node)
    if updated:
        pq.queue = temp_pq.queue

def get_possible_moves(grid_state):
    grid_temp=list(grid_state)
    possible=[]
    if(grid_state.index("0")==0):
        possible.append(''.join(swap(0,1,grid_temp)))
        possible.append(''.join(swap(0,3, grid_temp)))
    elif(grid_state.index("0")==1):
        possible.append(''.join(swap(1, 0, grid_temp)))
        possible.append(''.join(swap(1, 2, grid_temp)))
        possible.append(''.join(swap(1, 4, grid_temp)))
    elif (grid_state.index("0") == 2):
        possible.append(''.join(swap(2, 1, grid_temp)))
        possible.append(''.join(swap(2, 5, grid_temp)))
    elif (grid_state.index("0") == 3):
        possible.append(''.join(swap(3, 0, grid_temp)))
        possible.append(''.join(swap(3, 4, grid_temp)))
        possible.append(''.join(swap(3, 6, grid_temp)))
    elif (grid_state.index("0") == 4):
        possible.append(''.join(swap(4, 1, grid_temp)))
        possible.append(''.join(swap(4, 3, grid_temp)))
        possible.append(''.join(swap(4, 5, grid_temp)))
        possible.append(''.join(swap(4, 7, grid_temp)))
    elif (grid_state.index("0") == 5):
        possible.append(''.join(swap(5, 2, grid_temp)))
        possible.append(''.join(swap(5, 4, grid_temp)))
        possible.append(''.join(swap(5, 8, grid_temp)))
    elif (grid_state.index("0") == 6):
        possible.append(''.join(swap(6, 3, grid_temp)))
        possible.append(''.join(swap(6, 7, grid_temp)))
    elif (grid_state.index("0") == 7):
        possible.append(''.join(swap(7, 4, grid_temp)))
        possible.append(''.join(swap(7, 6, grid_temp)))
        possible.append(''.join(swap(7, 8, grid_temp)))
    elif (grid_state.index("0") == 8):
        possible.append(''.join(swap(8, 5, grid_temp)))
        possible.append(''.join(swap(8, 7, grid_temp)))
    return possible

def reconstruction(target):
    global parents
    global steps
    parent=""
    child=""
    while(parent != "None"):
        for i in range(len(parents)):
            family=str(parents[i]).split(',')
            parent=family[0]
            child=family[1]
            if(child==target and child not in steps):
                steps.append(child)
                target=parent
                break
    print(steps)
def get_path_length(target):
    global parents
    arr=[]
    parent=""
    child=""
    while(parent != "None"):
        for i in range(len(parents)):
            family=str(parents[i]).split(',')
            parent=family[0]
            child=family[1]
            if(child==target):
                arr.append(child)
                target=parent
                break
    return len(arr)
def get_max_depth():
    global parents
    for i in range(len(parents)):
        family = str(parents[i]).split(',')
        parent = family[0]
        child = family[1]

def get_leaves():
    global parents
    parent = ""
    child = ""
    fathers=[]
    children=[]
    for i in range(len(parents)):
        family = str(parents[i]).split(',')
        fathers.append(family[0])
        children.append(family[1])
    leaves = list(set(children) - set(fathers))
    print(children)
    return leaves

def Breadth_Frist_Search():
    start_time = time.time()
    global nodes_expanded
    global grid_state
    global steps
    global parents
    global grid_var
    global astar_path
    grid_state = grid_var.get()
    if (not isSolvable(grid_state)):
        messagebox.showinfo("Alert", "This case can not be solved")
        return
    adjust_buttons()
    frontier = Queue()
    explored = set()
    frontier.enqueue(grid_state)
    parents.append("None," + grid_state)
    while (not frontier.is_empty()):
        state = frontier.dequeue()
        explored.add(state)
        steps.append(state)
        if (state =="012345678"):
            end_time = time.time()
            execution_time = end_time - start_time
            reconstruction("012345678")
            steps.reverse()
            astar_path = steps
            set_results(len(steps))
            print("Execution time:", execution_time, "seconds")
            return True
        possible_grids = get_possible_moves(state)
        possible_grids.reverse()
        nodes_expanded = nodes_expanded + 1
        for neighbor in get_possible_moves(state):
            parents.append(state + "," + neighbor)
            if not frontier.contain(neighbor) and not neighbor in explored:
                frontier.enqueue(neighbor)

    return False

def depth_first_search():
    start_time = time.time()
    global nodes_expanded
    global grid_state
    global steps
    global parents
    global grid_var
    global astar_path
    grid_state=grid_var.get()
    if(not isSolvable(grid_state)):
        messagebox.showinfo("Alert","This case can not be solved")
        return
    adjust_buttons()
    explored = set()  # Change explored to a set
    frontier = Stack()
    frontier.push(grid_state)
    parents.append("None,"+grid_state)
    lengths=list()
    while not frontier.is_empty():
        state = frontier.pop()
        explored.add(state)  # Add state to the set
        if state == "012345678":
            end_time = time.time()
            execution_time = end_time - start_time
            reconstruction("012345678")
            steps.reverse()
            astar_path=steps
            leaves=get_leaves()
            #print(leaves)
            for k in range(len(leaves)):
                lengths.append(get_path_length(leaves[k]))
            set_results(max(lengths))
            print("Execution time:", execution_time, "seconds")
            return True
        possible_grids = get_possible_moves(state)
        possible_grids.reverse()
        nodes_expanded += 1
        for path in possible_grids:
            parents.append(state+","+path)
            if path not in explored and not frontier.contain(path):
                frontier.push(path)
    return False



def getInvCount(arr):
    inv_count = 0
    empty_value = '0'
    for i in range(9):
        for j in range(i + 1, 9):
            if arr[j] != empty_value and arr[i] != empty_value and arr[i] > arr[j]:
                inv_count += 1
    return inv_count


def isSolvable(puzzle):
    inv_count = getInvCount(puzzle)
    return (inv_count % 2 == 0)


def aStar(initial_state, goal_state, heuristic):
    global grid_state
    global astar_path
    grid_state=initial_state
    if (not isSolvable(grid_state)):
        messagebox.showinfo("Alert", "This case can not be solved")
        return
    adjust_buttons()
    frontier = PriorityQueue()
    explored = set()
    predecessors = {initial_state: (None, 0, 0)}
    max_depth = 1
    start_time = time.time()
    frontier.put((heuristic(initial_state, goal_state), initial_state))
    explored_nodes = 0
    while not frontier.empty():
        current_cost, current_state = frontier.get()
        current_depth = predecessors[current_state][2]

        if current_state == goal_state:
            end_time = time.time()
            search_time = end_time - start_time
            set_results_aStar(current_cost, search_time, explored_nodes, current_depth, max_depth)
            reconstruct= reconstruct_path(predecessors,
                                    current_state), current_cost, search_time, explored_nodes, current_depth, max_depth
            steps=reconstruct[0]
            steps.pop(0)
            astar_path=steps
            print(steps)

        explored.add(current_state)
        explored_nodes += 1
        for successor_state in generate_successors(current_state):
            if successor_state in explored:
                continue

            new_cost = predecessors[current_state][1] + 1
            new_depth = current_depth + 1  # Update the cost for the successor state
            max_depth = max(max_depth, new_depth)

            if successor_state not in predecessors or new_cost < predecessors[successor_state][1]:
                # Update the predecessor if this path is shorter
                predecessors[successor_state] = (current_state, new_cost, new_depth)
                priority = new_cost + heuristic(successor_state, goal_state)
                frontier.put((priority, successor_state))

    return None, None, None, None, None, None


def manhattan_dist(state, goal_state):
    # Manhattan distance heuristic
    distance = 0
    for k in range(9):
        value = state[k]
        if value != '0':
            goal_position = find_position(goal_state, value)
            goal_row, goal_col = divmod(goal_position, 3)
            i, j = divmod(k, 3)
            distance += abs(i - goal_row) + abs(j - goal_col)
    return distance


def euclidean_dist(state, goal_state):
    distance = 0
    for k in range(9):
        value = state[k]
        if value != '0':
            goal_position = find_position(goal_state, value)
            goal_row, goal_col = divmod(goal_position, 3)
            i, j = divmod(k, 3)
            x = (i - goal_row)
            y = (j - goal_col)
            distance += sqrt(x * x + y * y)
    return distance


def find_position(state, value):
    return state.index(value)


def generate_successors(state):
    successors = []
    empty_position = state.index('0')
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]  # right, left, down, up

    for direction in directions:
        new_row, new_col = divmod(empty_position + direction[0] * 3 + direction[1], 3)
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_state = list(state)
            new_state[empty_position], new_state[new_row * 3 + new_col] = new_state[new_row * 3 + new_col], new_state[
                empty_position]
            successors.append(''.join(new_state))
    return successors


def reconstruct_path(predecessors, goal_state):
    path = []
    current_state = goal_state
    while current_state in predecessors:
        path.insert(0, current_state)
        current_state = predecessors[current_state][0]
    path.insert(0, current_state)
    return path



def transition_step(type):
    global i
    global steps
    global Buttons
    global astar_path
    steps=astar_path
    print(steps)
    if(type == "next"):
        i=i+1
        if (i > len(steps)-1):
            i = i - 1
            return
    else:
        i=i-1
        if(i<0):
            i=i+1
            return
    for k in range(9):
        Buttons[k].config(text=steps[i][k])
def adjust_buttons():
    global Buttons
    global grid_state
    for k in range(9):
        Buttons[k].config(text=grid_state[k])
def set_results(max_deep):
    global cost_blank
    global node_blank
    global search_blank
    global goal_blank
    global steps
    global nodes_expanded
    cost_blank.config(text=len(steps)-1)
    node_blank.config(text=nodes_expanded)
    search_blank.config(text=max_deep-1)
    goal_blank.config(text=len(steps)-1)
def set_results_aStar(cost, search_time, num_nodes, goal_depth, max_depth):

    global cost_blank
    global node_blank
    global search_blank
    global goal_blank
    global steps
    global nodes_expanded
    print("Execution time:", search_time, "seconds")
    cost_blank.config(text=cost)
    node_blank.config(text=num_nodes)
    search_blank.config(text=max_depth-1)
    goal_blank.config(text=goal_depth)

grid_state=""
steps=[]
Buttons=list()
r = tk.Tk()
grid_var=tk.StringVar()
i=0
r.geometry("1300x800")
name_label = tk.Label(r, text='Enter the Grid', font=('calibre', 18, 'bold'))
grid_entry = tk.Entry(r, textvariable=grid_var, font=('calibre', 18, 'normal'))
cost = tk.Label(r, text='Cost :', font=('calibre', 18, 'bold'))
cost_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
nodes_expand = tk.Label(r, text='Nodes Expanded :', font=('calibre', 18, 'bold'))
node_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
search_depth = tk.Label(r, text='Search depth :', font=('calibre', 18, 'bold'))
search_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
goal_depth = tk.Label(r, text='Goal depth :', font=('calibre', 18, 'bold'))
goal_blank = tk.Label(r, text='', font=('calibre', 18, 'bold'))
grid_list=list(grid_state)
e0 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="0",font=25)
e1 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="1",font=25)
e2 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="2",font=25)
e3 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="3",font=25)
e4 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="4",font=25)
e5 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="5",font=25)
e6 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="6",font=25)
e7 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="7",font=25)
e8 = Button(r,width=15,height=5, bg='#f5b488', fg='white',text="8",font=25)
next_button = Button(r,width=25,height=5, bg='#aa22ff', fg='white',text="Next",font=25,command=lambda: transition_step("next"))
previous = Button(r,width=25,height=5, bg='#aa22ff', fg='white',text="Previous",font=25,command=lambda: transition_step("previous"))
start_dfs = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="DFS",font=25,command=lambda: depth_first_search())
start_bfs = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="BFS",font=25,command=lambda: Breadth_Frist_Search())
start_Astar = Button(r,width=15,height=5, bg='#0c0201', fg='white',text="A *",font=25,command=lambda: aStar(grid_var.get(),"012345678",euclidean_dist))
Buttons.append(e0)
Buttons.append(e1)
Buttons.append(e2)
Buttons.append(e3)
Buttons.append(e4)
Buttons.append(e5)
Buttons.append(e6)
Buttons.append(e7)
Buttons.append(e8)
r.title('8 puzzle')
name_label.grid(row=0, column=3,padx=5,pady=10)
grid_entry.grid(row=0, column=4,padx=5,pady=10)
cost.grid(row=1, column=3,padx=5,pady=10)
cost_blank.grid(row=1, column=4,padx=5,pady=10)
nodes_expand.grid(row=2, column=3,padx=5,pady=10)
node_blank.grid(row=2, column=4,padx=5,pady=10)
search_depth.grid(row=3, column=3,padx=5,pady=10)
search_blank.grid(row=3, column=4,padx=5,pady=10)
goal_depth.grid(row=4, column=3,padx=5,pady=10)
goal_blank.grid(row=4, column=4,padx=5,pady=10)
e0.grid(row=0, column=0,padx=5,pady=10)
e1.grid(row=0, column=1,padx=5,pady=10)
e2.grid(row=0, column=2,padx=5,pady=10)
e3.grid(row=1, column=0,padx=5,pady=10)
e4.grid(row=1, column=1,padx=5,pady=10)
e5.grid(row=1, column=2,padx=5,pady=10)
e6.grid(row=2, column=0,padx=5,pady=10)
e7.grid(row=2, column=1,padx=5,pady=10)
e8.grid(row=2, column=2,padx=5,pady=10)
next_button.grid(row=3,column=0,padx=5,pady=10)
previous.grid(row=3,column=2,padx=5,pady=10)
start_dfs.grid(row=4,column=0,padx=5,pady=10)
start_bfs.grid(row=4,column=1,padx=5,pady=10)
start_Astar.grid(row=4,column=2,padx=5,pady=10)
r.mainloop()

