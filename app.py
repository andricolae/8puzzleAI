import time
from time import sleep

class Node:
    
    def __init__(self,data,level,fval):
        self.data = data
        self.level = level
        self.fval = fval

    def generate_child(self):
        # Pos of the blank cell
        x, y = self.find(self.data,'_')
        
        # Values for the 4 movements available
        val_list = [[x,y-1],[x,y+1],[x-1,y],[x+1,y]]
        children = []
        
        for i in val_list:
            child = self.shuffle(self.data,x,y,i[0],i[1])
            if child is not None:
                child_node = Node(child,self.level+1,0)
                children.append(child_node)
        return children
        
    def shuffle(self,puz,x1,y1,x2,y2):
        # Move blank space in given direction
        if x2 >= 0 and x2 < len(self.data) and y2 >= 0 and y2 < len(self.data):
            temp_puz = []
            temp_puz = self.copy(puz)
            temp = temp_puz[x2][y2]
            temp_puz[x2][y2] = temp_puz[x1][y1]
            temp_puz[x1][y1] = temp
            return temp_puz
        else:
            return None
            
    def copy(self,root):
        temp = []
        for i in root:
            t = []
            for j in i:
                t.append(j)
            temp.append(t)
        return temp    
            
    def find(self,puz,x):
        for i in range(0,len(self.data)):
            for j in range(0,len(self.data)):
                if puz[i][j] == x:
                    return i,j


class Puzzle:
    
    def __init__(self,size):
        self.dim = size
        self.open = []
        self.closed = []

    def accept(self):
        puz = []
        for i in range(0,self.dim):
            temp = input().split(" ")
            puz.append(temp)
        return puz

    def f(self,start,goal):
        # Compute heuristic value f(x) = h(x) + g(x)
        return self.h(start.data,goal)+start.level

    def h(self,start,goal):
        # Compute identity between start and goal puzzle
        temp = 0
        for i in range(0,self.dim):
            for j in range(0,self.dim):
                if start[i][j] != goal[i][j] and start[i][j] != '_':
                    temp += 1
        return temp

    def run(self, start):
        #start = self.accept()
        goal = [['1', '2', '3'], ['4', '5', '6'],[ '7', '8', '_']]
        #goal = self.accept()
        
        start = Node(start,0,0)
        start.fval = self.f(start,goal)
        
        self.open.append(start)
        print("\n")
        counter = 0
        while True:
            cur = self.open[0]
            counter += 1
            print("\n")
            print("  %s" % counter)
            print("  | ")
            print("  | ")
            print(" \\\'/ ")
            for i in cur.data:
                for j in i:
                    print(j,end=" ")
                print("")
            
            if(self.h(cur.data,goal) == 0):
                break
            for i in cur.generate_child():
                i.fval = self.f(i,goal)
                self.open.append(i)
            self.closed.append(cur)
            del self.open[0]

            self.open.sort(key = lambda x:x.fval,reverse=False)
            
application = Puzzle(3)
print("Waiting for the start puzzle...\n")
start = application.accept()

# Test if init puzzle is solvable  
def isSolvable(puzzle) :
    inv_count = 0
    arr = [j for sub in puzzle for j in sub]
    for i in range(0, 9):
        for j in range(i + 1, 9):
            if arr[j] == '_' or arr[i] == '_':
                continue
            if int(arr[i]) > int(arr[j]):
                inv_count += 1
    return (inv_count % 2 == 0)

if(isSolvable(start)) :
    print("Input puzzle solvable! Running...")
    sleep(1)
    start_time = time.time()
    application.run(start)
    print("")
    print("%s seconds" % (time.time() - start_time))
else :
    while(isSolvable(start) == False) :
        print("Input puzzle not solvable! Try another input...")
        start = application.accept()
    print("Input puzzle solvable! Running...")
    sleep(0.75)
    start_time = time.time()
    application.run(start)
    print("")
    print("%s seconds" % (time.time() - start_time))