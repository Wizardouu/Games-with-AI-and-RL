import numpy as np
from ac3 import *
from collections import deque
from tkinter import messagebox
from h import *
class SudokuGame:
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    This is Game instance
    """

    def __init__(self, board, output_file):
        self.start_puzzle = board
        self.grid = np.array(board)
        self.step = 0
        self.previous_domains = 0
        self.output_file = output_file
        
    def print_to_file(self, *args, **kwargs):
        with open(self.output_file, 'a') as f:
            print(*args, file=f, **kwargs)

    def start(self):
        self.game_over = False
        self.puzzle = [row[:] for row in self.start_puzzle]
        
    def clear(self):
        self.grid= [row[:] for row in self.start_puzzle]

    def create_domains(self):
        domains=[]
        for i in range(9):
            for k in range(9):
                if(self.grid[i][k]!=0):
                   domains.append([self.grid[i][k]])
                else:
                    domains.append([1,2,3,4,5,6,7,8,9])
        return domains
    
    def revise(self,Xi,Xj,domains):
        revised = False
        for k in range(len(domains[Xi])-1,-1,-1):
            flag=False
            for j in range(len(domains[Xj])):
                if(domains[Xi][k] != domains[Xj][j]):
                    flag=True
                    break
            if(flag == False):
                row1=Xi // 9
                column1=Xi % 9
                row2=Xj // 9
                column2=Xj % 9
                self.step+=1
                old_dom = domains[Xi].copy()
                #a = arc_const_object(old_dom,None,domains[Xi][k],[row1, column1], [row2, column2],self.step)
                #self.print_to_file("No Arc consistency between (" + str(row1) + "," + str(column1) + ") --> (" + str(row2) + "," + str(column2) + ")")
                del (domains[Xi][k])
                #a.new_domain = domains[Xi]
                #a.print_ac3()
                revised = True

        return revised
    
    def get_neighbours(self,i,j):
        queue=[]
        Xi = i * 9 + j
        #column
        for k in range(9):
            if(k!=i):
                queue.append(k*9+j)
        #row
        for k in range(9):
            if(k != j):
                queue.append(i*9+k)
        #3x3 subgrid
        box= (i//3)*3 + (j//3)
        starts=[0,3,6,27,30,33,54,57,60]
        queue.append(starts[box])
        queue.append(starts[box]+1)
        queue.append(starts[box]+2)
        queue.append(starts[box]+9)
        queue.append(starts[box]+10)
        queue.append(starts[box]+11)
        queue.append(starts[box]+18)
        queue.append(starts[box]+19)
        queue.append(starts[box]+20)
        queue = list(set(queue))
        queue.remove(Xi)
        return queue

    def arc_consistency(self, i, j, domains):
        m = i
        n = j
        Xi = i * 9 + j
        queue = self.get_neighbours(i, j)
        neighbours = queue.copy()
        while (queue):
            Xj = queue.pop(0)
            row = Xj // 9
            column = Xj % 9
            old_dom = domains[Xi].copy()
            #self.print_to_file("Now try arc consistency between (" + str(m) + "," + str(n) + ") --> (" + str(row) + "," + str(column) + ")")
            #self.print_to_file("(" + str(m) + "," + str(n) + ") old domain is ", domains[Xi])
            if (self.revise(Xi, Xj, domains)):
                new_dom = domains[Xi].copy()
                a = arc_const_object(old_dom, new_dom, (m,n), (row, column))
                a.print_ac3()
                #self.print_to_file("New domains of (" + str(m) + "," + str(n) + ")", domains[Xi])
                if (len(domains[Xi]) == 0):
                    return False
                back_neighbours = neighbours.copy()
                back_neighbours.remove(Xj)
                for i in range(len(back_neighbours)):
                    queue.append(back_neighbours[i])
            #else:
                #a = arc_const_object(old_dom, old_dom, (m,n), (row, column))
                
                #print()
                #self.print_to_file("(" + str(m) + "," + str(n) + ") --> (" + str(row) + "," + str(column) + ") are arc consistent so no domain change")
        
        return True

    def reduce_domain(self,remaining,domains):
        if(remaining==81):
            return True
        row=remaining // 9
        column=remaining % 9
        if(self.arc_consistency(row,column,domains)):
            result=self.reduce_domain(remaining+1,domains)
            if(result == True): return True
        return False
    
    def is_valid(self, i, j, num):
        # Check the row
        for k in range(9):
            if self.grid[i][k] == num:
                return False

        for k in range(9):
            if self.grid[k][j] == num:
                return False
        queue=[]
        box = (i // 3) * 3 + (j // 3)
        starts = [0, 3, 6, 27, 30, 33, 54, 57, 60]
        queue.append(starts[box])
        queue.append(starts[box] + 1)
        queue.append(starts[box] + 2)
        queue.append(starts[box] + 9)
        queue.append(starts[box] + 10)
        queue.append(starts[box] + 11)
        queue.append(starts[box] + 18)
        queue.append(starts[box] + 19)
        queue.append(starts[box] + 20)
        queue = list(set(queue))
        queue.remove(i*9+j)
        for m in range(len(queue)):
            row = queue[m] // 9
            column = queue[m] % 9
            if(self.grid[row][column] == num):
                    return False
        return True
    
    def backtrack(self,domains):
        if np.all(self.grid):
            return True
        else:
            zero_indices = np.where(self.grid == 0)
            zero_indices_pairs = list(zip(zero_indices[0], zero_indices[1]))[0]
        row, col = zero_indices_pairs

        for num in domains[row * 9 + col]:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                updated_domains = domains.copy()
                updated_domains[row * 9 + col] = [num]
                if self.arc_consistency(row , col,updated_domains):
                    if self.backtrack(updated_domains):
                        domains[row * 9 + col]=[num]
                    #print(self.domains)
                        #self.print_to_file("Finally cell (" + str(row) + "," + str(col) + ") will take value " + str(num))
                        return True
                self.grid[row][col] = 0
        #self.print_to_file("")
        #self.print_to_file( "------------------------------------------------------------------------------------------------")
        #self.print_to_file("Backtraaaack !!")
        #self.print_to_file("------------------------------------------------------------------------------------------------")
        #self.print_to_file("")
        return False

    def solve(self):
        domains = self.create_domains()
        self.reduce_domain(0,domains)
        if not(self.backtrack(domains)):
            return False
        # for i in range(9):
        #     print(self.grid[i])
        # print(self.domains)
        self.puzzle = self.grid.tolist()
        return True

    
class SudokuGameSteps(SudokuGame):
    """
    A Sudoku game, in charge of storing the state of the board and checking
    whether the puzzle is completed.
    This is Game instance
    """
    def __init__(self, board,output_file):
        super().__init__(board,output_file)
        self.states = []
        self.curr_state = self.grid.copy()
        self.num = 0
        self.ac = []
        self.temp = []
        self.stack=deque()
        self.stack2=deque()
        self.output_file=output_file
        self.curr_element = None
        self.next_elm = None
        self.flag = False


    
    def revise(self,Xi,Xj,domains):
        revised = False
        #a = None
        for k in range(len(domains[Xi])-1,-1,-1):
            flag=False
            for j in range(len(domains[Xj])):
                if(domains[Xi][k] != domains[Xj][j]):
                    flag=True
                    break
            if(flag == False):
                row1=Xi // 9
                column1=Xi % 9
                row2=Xj // 9
                column2=Xj % 9
                self.step+=1
                old_dom = domains[Xi].copy()
                new_dom = old_dom[:k] + old_dom[k+1:]
                a = arc_const_object(old_dom,new_dom,[row1, column1], [row2, column2])
                self.stack2.append(a)
                #self.print_to_file("No Arc consistency between (" + str(row1) + "," + str(column1) + ") --> (" + str(row2) + "," + str(column2) + ")")
                del (domains[Xi][k])
                #a.new_domain = self.domains[Xi]
                #a.print_ac3()
                revised = True
                
        #if a and revised:
          #  self.temp.append(a)
          #  a = None
        return revised
    
    def arc_consistency(self, i, j, domains):
        m = i
        n = j
        Xi = i * 9 + j
        queue = self.get_neighbours(i, j)
        neighbours = queue.copy()
        while (queue):
            Xj = queue.pop(0)
            row = Xj // 9
            column = Xj % 9
            #self.print_to_file("Now try arc consistency between (" + str(m) + "," + str(n) + ") --> (" + str(row) + "," + str(column) + ")")
            #old_dom = domains[Xi].copy()
            #self.print_to_file("(" + str(m) + "," + str(n) + ") old domain is ", domains[Xi])
            if (self.revise(Xi, Xj, domains)):
                #new_dom = domains[Xi].copy()
                #a = arc_const_object(old_dom,new_dom,(m,n),(row,column))
                #self.stack2.append(f"({m},{n})  New domain is  {domains[Xi]}")
                #self.stack2.append(f"Now try arc consistency between ({m},{n}) --> ({row} ,{column})")
                #self.stack2.append(f"({m},{n})  old domain is  {domains[Xi]}")
                #self.stack2.append(a)
                #a.print_ac3()
                #self.print_to_file("New domains of (" + str(m) + "," + str(n) + ")", domains[Xi])
                if (len(domains[Xi]) == 0):
                    return False
                back_neighbours = neighbours.copy()
                back_neighbours.remove(Xj)
                for i in range(len(back_neighbours)):
                    queue.append(back_neighbours[i])
            #else:
                #a = arc_const_object(domains[Xi],domains[Xi],(m,n),(row,column))
                #self.stack2.append(a)
                #self.stack2.append("(" + str(m) + "," + str(n) + ") --> (" + str(row) + "," + str(column) + ") are arc consistent so no domain change")
                #self.print_to_file("(" + str(m) + "," + str(n) + ") --> (" + str(row) + "," + str(column) + ") are arc consistent so no domain change")
        return True

    
    def backtrack(self,domains):
        if np.all(self.grid):
            return True
        else:
            zero_indices = np.where(self.grid == 0)
            zero_indices_pairs = list(zip(zero_indices[0], zero_indices[1]))[0]
        row, col = zero_indices_pairs

        for num in domains[row * 9 + col]:
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                updated_domains = domains.copy()
                self.states.append(self.grid.copy())
                self.ac.append(self.temp)
                updated_domains[row * 9 + col] = [num]
                if self.arc_consistency(row , col,updated_domains):
                    if self.backtrack(updated_domains):
                        domains[row * 9 + col]=[num]
                        #print(self.domains)
                        #self.print_to_file("Finally cell (" + str(row) + "," + str(col) + ") will take value " + str(num))
                        return True
                self.grid[row][col] = 0
                self.states.append(self.grid.copy())
                #print(self.states)
        self.ac.append(self.temp)
        self.temp = []
        self.step = 0
        #self.print_to_file("")
        #self.print_to_file( "------------------------------------------------------------------------------------------------")
        #self.print_to_file("Backtraaaack !!")
        #self.print_to_file("------------------------------------------------------------------------------------------------")
        #self.print_to_file("")
        return False
        
    def next(self):
        #print(find_first_zero_cell(self.start_puzzle.copy()))
        if self.num < len(self.states):
            self.curr_state = self.states[self.num].tolist()

            if self.num == len(self.states):
                edit_cell = find_first_zero_cell(self.grid.copy())
            else:
                edit_cell = find_difference_index(self.states[self.num],self.states[self.num-1])

            #print(f"Edit Cell {edit_cell}")
            

            if self.curr_element is None:
                self.curr_element = self.stack2.popleft()
                self.next_elm = self.stack2.popleft()
                '''
                print(f"NOT Arc-Consistent between ({self.curr_element.elm1[0]},{self.curr_element.elm1[1]}) and ({self.curr_element.elm2[0]},{self.curr_element.elm2[1]})\n")
                print(f"To become Arc-Consistency removed element {self.curr_element.removed_element} from domain of cell ({self.curr_element.elm1[0]},{self.curr_element.elm1[1]})\n")
                print(f"The domain of the cell ({self.curr_element.elm1[0]},{self.curr_element.elm1[1]})before remove {self.curr_element.old_domain} \n")
                print(f"So the new domain of the cell ({self.curr_element.elm1[0]},{self.curr_element.elm1[1]}): {self.curr_element.new_domain}\n\n")
            
                #print(self.curr_element.print_ac3())
                #print(self.curr_element.elm2)
                #print(self.curr_element.old_domain)
                #print(self.curr_element.new_domain)
                #print(self.next_elm.print_ac3())
                #print(self.next_elm.elm2)
                #print(self.next_elm.old_domain)
                #print(self.next_elm.new_domain)
                '''
                
            else:
                #self.next_elm = self.stack2.popleft()
                self.curr_element = self.next_elm
                self.next_elm = self.stack2.popleft()
                
                

            
            if not self.next_elm.is_before(edit_cell) :#and not self.curr_element.is_before(edit_cell):
                #if self.flag == False:
                print("\n!!!!!!!!!!!!!!!!!!!!!!!     Backtracking      !!!!!!!!!!!!!!!!!!!!!!!\n")
                    #self.flag == True
                #elif self.flag == True:
                self.stack2.append(self.next_elm)
                #self.next_elm = self.curr_element
                    #self.flag = False
            
            else:
            
                while self.curr_element.elm1 == self.next_elm.elm1:
                    cp = self.curr_element
                    cp.print_ac3()
                    self.curr_element = self.next_elm
                    if len(self.stack2) > 0:
                        self.next_elm = self.stack2.popleft()

                cp = self.curr_element
                cp.print_ac3()
                self.curr_element = self.next_elm
                if len(self.stack2) > 0:
                    self.next_elm = self.stack2.popleft()
                #self.curr_element.print_ac3()
                '''
                print(self.curr_element.elm1)
                print(self.curr_element.elm2)
                print(self.curr_element.old_domain)
                print(self.curr_element.new_domain)
                print(self.next_elm.elm1)
                print(self.next_elm.elm2)
                print(self.next_elm.old_domain)
                print(self.next_elm.new_domain)
                print("----------------------------")
                self.curr_elm =self.next_elm
                self.next_elm = self.stack2.popleft()
                
                #self.curr_element =self.next_elm
                #self.next_elm = self.stack2.popleft()
                '''
            
        else:
            if len(self.stack2) > 0:
                while len(self.stack2) > 0:
                    x = self.stack2.popleft()
                    x.print_ac3()
        self.num += 1

    
    def interactive_sudoko(self,row,column,value):
        domains=self.create_domains()
        s=row* 9 + column
        self.reduce_domain(0,domains)
        #print(domains)
        updated_domains = domains.copy()
        
        if value not in updated_domains[s]:
            #return False
            print("INVALID")
            messagebox.showinfo("warning","This value not valid")
            
        else:
            self.stack.append(updated_domains[s])
            updated_domains[s]=[value]
            
            if not self.is_valid(row,column,value):
                print(updated_domains[s])
                updated_domains[s]=self.stack.pop()
                print(updated_domains[s])
                messagebox.showinfo("warning","This value is incorrect")
                #return False
                
            else:
                self.grid[row][column]=value
                domains=updated_domains
                #return True
        