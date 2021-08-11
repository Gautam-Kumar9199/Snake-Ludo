import random
from queue import Queue
class graph:
    
    def __init__(self,v:"iter",e:"iter" , directed = False):
        self.vertices = set(v)
        self.directed = directed
        if directed:
            self.edges = set(e)
            self.Indegree = {}
            self.Outdegree = {}
        else:
            self.edges = set(frozenset((u,v)) for u,v in e)
        self.nbrs = {}
        for x in self.vertices:
            self.AddVertex(x)
        for u,v in self.edges:
            self.AddEdges(u,v)
    
    def AddVertex(self,v):
        if v not in self.nbrs:
            self.nbrs[v] = set({})
            self.vertices.add(v)
        if self.directed:
            self.Indegree[v] = 0
            self.Outdegree[v] = 0
        
    def AddEdges(self,u,v):
        self.AddVertex(u)
        self.AddVertex(v)
        if self.directed:
            self.nbrs[u].add(v)
            self.edges.add((u,v))
            self.Outdegree[u] = self.Outdegree[u] + 1
            self.Indegree[v] = self.Indegree[v] + 1
        else:
            self.nbrs[u].add(v)
            self.nbrs[v].add(u)
            self.edges.add(frozenset((u,v)))
            self.edges.add(frozenset((v,u)))

    def dfs(self,v):
        visited = set()
        visited.add(v)
        stack = [v]
        stack.append(v)
        dfs_list = [v]
        pq = v
        c=0
        while len(stack)!=0 or c==2:
            for x in list(self.nbrs[pq]):
                if x not in  visited:
                    visited.add(x)
                    dfs_list.append(x)
                    stack.append(x)
                    break
            pq = stack.pop()
            if len(stack)==0:
                c +=1
        return dfs_list


    def bfs(self , v):
        visited = set()  
        minimum_distance = {}
        minimum_distance[v] = 0
        bfs = []      
        q = Queue()
        q.put(v)
        visited.add(v)
        bfs.append(v)
        while not q.empty():
            element = q.get()
            for x in self.nbrs[element]:
                if x not in visited:
                    q.put(x)
                    bfs.append(x)
                    visited.add(x) 
                    minimum_distance[x] =  1 + minimum_distance[element]
        print(minimum_distance)
        return bfs                       
        
    def get_graph(self):
        return self.nbrs

vertex = [x for x in range(1,101)]
stair_snake = {3:20,11:28,16:35,22:37,26:10,39:5,51:6,49:67,54:36,
              56:1,57:76,60:23,61:78,73:86,75:13,90:48,88:91,85:59,
              83:45,81:98,92:25,97:66,99:63,52:71}
stair = {3:20,11:28,16:35,22:37,49:67,61:78,73:86,88:91,81:98}

edges = set()
for x in vertex:
    if x not in stair_snake:
        for y in range(1,7):
            r =x+y
            if r<101:
                if (x+y) in stair_snake:
                    edges.add((x,stair_snake[x+y])) 
                else:
                    edges.add((x,x+y))

p = graph(vertex,edges,True) # creating ludo of size 100


def trace_dice_value(a,b,pl):
    if b-a>6:  # for stair
        for x in range(1,7):
            if (a+x) in stair_snake:
                if stair_snake[a+x]==b:
                    if pl:
                        print("Stair Found for player_1")
                    else:
                        print("Stair Found for player_2")
                    #print("Dice Value is : ",x)
                    return x
    elif a>b: # for snake bite
        for x in range(1,7):
            if (a+x) in stair_snake:
                if stair_snake[a+x]==b:
                    if pl:
                        print("Snake Mil Gaya Gandu player_1")
                    else:
                        print("Snake Mil Gaya Gandu player_2")
                    #print("Dice Value is : ",x)
                    return x
    else:
        #print("Dice Value is : ",b-a)
        return b-a

def find_snake(starting_point , ending_point):
    for x in range(starting_point,ending_point+1):
        if x in stair_snake:
            if stair_snake[x] < x:
                return x
    return False

def generate_probability_set(prob):
    probiliy = set()
    for x in range(0,prob,10):
        probiliy.add(True)
    for x in range(prob,100,10):
        probiliy.add(False)
    return probiliy

# for player 2

def get_targeted_move_for_sanke_bite(p,player_2):
    if player_2 in stair:
        return (False , False)
    else:
        #print("player is in position : ",player_2)
        cheating_range = [5,7,8,12,15,16]
        starting_point = [1,2,3,4,5,6,7]
        cheating_range_random = random.choice(cheating_range)
        starting_point_random = player_2 + random.choice(starting_point)
        end_point_random = starting_point_random + cheating_range_random
        #print("starting_point_random : " , starting_point_random)
        #print("cheating_range_random : " , cheating_range_random)
        #print("end_point_random : " , end_point_random)
        pq =  find_snake(starting_point_random,end_point_random)
        #print("value where snake is present : ",pq)
        while pq==False:
            #print("running")
            end_point_random +=1
            pq =  find_snake(starting_point_random,end_point_random)
        target = pq - player_2
        #print("target value for snake bite : ",target)
        if target>6:
            #print("running target condition")
            move  = random.choice(list(p.nbrs[player_2]))
            #print("random next move from : ",player_2 ,move)
            while move>(player_2 + 6):
                move  = random.choice(list(p.nbrs[player_2]))
                #print("random next move from : ",player_2 ,move)
            if move<player_2:
                return (False , move)
            else:
                target = pq - move
                return (target ,move)
        else:
            return (False , stair_snake[player_2+target])

def generate_cheating_size(player_position):
    if player_position <10:
        return 5
    elif player_position >16 and player_position<27:
        return 3
    elif player_position >29 and player_position<40:
        return 2
    else:
        return 4

def create_cheating_queue(k,player):
    count = 8
  
    size = generate_cheating_size(player)
    while count>size:
        targeted_list = []
        count =1
        #print("starting***********again")
        kl = get_targeted_move_for_sanke_bite(p,player)
        if kl[0]==False and kl[1] == False:
            return False
        targeted_list.append(kl)
        #print("***************")
        while kl[0]!=False:
            count +=1
            kl = get_targeted_move_for_sanke_bite(p,kl[1])
            if kl[0]==False and kl[1] == False:
                break
                return False
            targeted_list.append(kl)
            #print("value of kl : ",kl)
            #print("***************")
    return targeted_list

#print(create_cheating_queue(p,27))
def play_fair(p): # used to play fair ludo game
    player_1 =1
    player_2 =1
    print("Player1 is on : ",player_1," Player 2 is on :",player_2)
    while player_1 !=100 and player_2!=100: 
        player_1_next = random.choice(list(p.nbrs[player_1]))
        dice_value_1 = trace_dice_value(player_1,player_1_next, True)
        player_1 = player_1_next
        player_2_next = random.choice(list(p.nbrs[player_2]))
        dice_value_2 = trace_dice_value(player_2,player_2_next, False)
        player_2=player_2_next
        print("Player1 got : ",dice_value_1," Player 2 got :",dice_value_2)
        print("Player1 is on : ",player_1," Player 2 is on :",player_2)

def start_playing(p:"ludo",cheating,probability,range_to_apply_probability): # for playing ludo
    
    if cheating == False:
        play_fair(p)
    else:
        cheating_in_progress = False
        target_move = []
        player_1 =1
        player_2 =1
        print("Player1 is on : ",player_1," Player 2 is on :",player_2)
        while player_1 !=100 and player_2!=100: 
            player_1_next = random.choice(list(p.nbrs[player_1])) # player 1 move
            dice_value_1 = trace_dice_value(player_1,player_1_next, True)
            player_1 = player_1_next
            if cheating_in_progress: 
                xyz = target_move.pop(0)
                print("cheating in progress")
                player_2_next = xyz[1]
                dice_value_2 = trace_dice_value(player_2,player_2_next, False)
                player_2 = player_2_next
                print("Player1 got : ",dice_value_1," Player 2 got :",dice_value_2)
                print("Player1 is on : ",player_1," Player 2 is on :",player_2)
                if len(target_move)==0:
                    cheating_in_progress = False
                    print("cheating terminated")
            else:
                player_2_next = random.choice(list(p.nbrs[player_2])) # player 2 move
                
                dice_value_2 = trace_dice_value(player_2,player_2_next, False)
                player_2=player_2_next
                print("Player1 got : ",dice_value_1," Player 2 got :",dice_value_2)
                print("Player1 is on : ",player_1," Player 2 is on :",player_2)
                if player_2-player_1>range_to_apply_probability: # checking condition for cheating
                    
                    get = random.choice(probability)
                    if get:
                        cheating_in_progress = True
                        target_move = create_cheating_queue(p,player_2)
                        print("cheating started")
                        print("cheating with targeted move : ",target_move)
                  
            
probability = [False , False , False , False , False ,True ,False ,False , False , False]
range_ = 10
start_playing(p,True,probability,range_)
#print(p.nbrs[98])kha busy hai



         
    

    


    
        







    