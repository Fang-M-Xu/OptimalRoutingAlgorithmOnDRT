
"""
Created on Tue Nov  7 17:05:02 2023

@author: Fang Xu
"""
import csv

import TestData

import pandas as pd
import numpy as np


# Init
path = np.full((TestData.Jerusalem_grid.shape[0],TestData.Jerusalem_grid.shape[1]),-1000)
best_path = np.full((TestData.Jerusalem_grid.shape[0],TestData.Jerusalem_grid.shape[1]),0)
potential_moves={}

fixed_weight_file=''
variable_weight_file=''
travel_time=''


class AStarSearch:
    def __init__(self, start, goal, graph, path):
        self.cur_coord = self.get_coordinate(start)
        self.cur_str = start
        self.last_str = start
        self.cur_depth = 0
        self.goal_coord = self.get_coordinate(goal)
        self.goal_str = goal
        self.explored = {}
        self.not_explored = {}
        self.not_explored[start] = 0
        self.graph = graph
        self.path = path

    def set_successors_cost(self):
        self.last_str = self.cur_str
        successors = self.generate_successors('')
        self.not_explored={}
        for successor in successors:
            if (str(successor) not in self.explored) and (str(successor) not in self.not_explored):
                self.not_explored[str(successor)] = self.cur_depth + 1 + self.a_star_heuristic(successor)
        self.explored[self.cur_str] = 0
        return True

    def is_goal_state(self):
        if self.goal_str in self.not_explored:
            self.cur_coord = self.get_coordinate(self.goal_str)
            self.cur_depth = self.not_explored.pop(self.goal_str)
            self.path[self.cur_coord[0], self.cur_coord[1]] = self.cur_depth
            next_moves=[]
            if  potential_moves.get(self.last_str) is None:
                next_moves.append(self.goal_str)
                potential_moves[self.last_str]=next_moves
            else:
                potential_moves[self.last_str].append(self.goal_str) 
            return True
        return False

    def explore_next_move(self):
        
        sorted_not_explored = sorted(
            self.not_explored,
            key = self.not_explored.get,
            reverse = False
        )
        self.cur_str = sorted_not_explored[0]
        self.cur_coord = self.get_coordinate(self.cur_str)
        self.cur_depth = self.not_explored.pop(self.cur_str) - self.a_star_heuristic(self.cur_str)
        self.path[self.cur_coord[0], self.cur_coord[1]] = round(self.cur_depth, 1)
        next_moves=[]
        if  potential_moves.get(self.last_str) is None:
            next_moves.append(self.cur_str)
            potential_moves[self.last_str]=next_moves
        else:
            potential_moves[self.last_str].append(self.cur_str)        
        return True

    def a_star_heuristic(self, move):
        """
        A heuristic function estimates the cost from the current node to the goal position.
        """
        goal_co = self.get_coordinate(self.goal_str)
        move_co = self.get_coordinate(move)
        distance = np.abs(goal_co[0] - move_co[0])+np.abs(goal_co[1] - move_co[1])

        fixed_weight = int(fixed_weight_file.loc[fixed_weight_file['Zone_Code'] == int(move),
                                                 ['Sum_Weight']]['Sum_Weight'])
        temp_variable_cost=variable_weight_file.loc[(variable_weight_file['fromZone']==int(self.last_str)) &
                                                    (variable_weight_file['ToZone']==int(move))][travel_time]
        if len(temp_variable_cost) == 0:
            variable_cost = 0.0
        else:
            variable_cost = float(temp_variable_cost)

        #self.save_weight(move,distance,fixed_weight,variable_cost)

        return distance + fixed_weight + variable_cost


    def generate_successors(self,node):
        if(node != ''):
            return self.graph[node]
        return self.graph[self.cur_str]
    
    def generate_potential_moves(self,node):
        return potential_moves.get(node)

    def get_coordinate(self,move):
        result=[]
        for i in range(TestData.Jerusalem_grid.shape[0]):
            for j in range(TestData.Jerusalem_grid.shape[1]):
                if TestData.Jerusalem_grid[i][j] == str(move):
                    result.append(i)
                    result.append(j)
                    return result

    def save_weight(self,move,distance,fixed_weight,variable_cost):
        weight_file ="Data/Calculate_Weight.csv"
        with open(weight_file,"a+") as f:
            csv_file = csv.writer(f)
            data_weight = [move,distance,fixed_weight,variable_cost,distance + fixed_weight + variable_cost]
            csv_file.writerow(data_weight)
        #print(move,distance,fixed_weight,variable_cost,distance + fixed_weight + variable_cost)

if __name__ == "__main__":
    #===============================
    # column_names = ['100513', '100512', '100511','100510', '100509', '100508','100517', '100514', '100530','100528', '100527', '100598']
    # row_names = ['100513', '100512', '100511','100510', '100509', '100508','100517', '100514', '100530','100528', '100527', '100598']
    # area_graph_values = np.array(pd.read_excel("Data/Graph.xlsx"))
    # area_graph_keys= pd.DataFrame(area_graph_values, columns=column_names, index=row_names)
    # path = pd.DataFrame(np.full((12,12),-1000), columns=column_names, index=row_names)
    # best_path = pd.DataFrame(np.full((12,12),0), columns=column_names, index=row_names)
    #===============================



    for passenger in TestData.passenger_list:
        #ini
        path = np.full((TestData.Jerusalem_grid.shape[0], TestData.Jerusalem_grid.shape[1]), -1000)
        best_path = np.full((TestData.Jerusalem_grid.shape[0], TestData.Jerusalem_grid.shape[1]), 0)

        fixed_weight_file = ''
        variable_weight_file = ''
        travel_time = ''

        print("Passenger:"+passenger["dataset"]+"Start")
        start_node = passenger["start_node"]
        goal_node = passenger["goal_node"]
        travel_day = passenger["day"]
        travel_time = passenger["time"]
        
        # S1.Get fixed weight file
        fixed_weight_file = pd.read_csv("Data/Jerusalem_Fixed_Weight.csv")
        # S2. Get age weight file
        date_file = TestData.date_file_map[travel_day]
        variable_weight_file = pd.read_csv("Data/"+date_file)

        testdata = TestData.zone_graph["zone_graph"+passenger["dataset"]]
        astar = AStarSearch(start_node, goal_node, testdata, path)


        explored_count = 0
        while True:
            astar.set_successors_cost()
            if astar.is_goal_state():
                break
            astar.explore_next_move()
            #if explored_count % 1000 == 0:
            #     print("Explored Count: " + str(explored_count))
            #explored_count += 1
        print(path)
        current = start_node
        current_coor = astar.get_coordinate(start_node)
        goal_count = 0
        while True:
            best_path[current_coor[0], current_coor[1]] = 1
            #print(current)
            cur_hop = round(path[current_coor[0], current_coor[1]], 1)
            if current == goal_node:
                break
            #potential_moves = astar.generate_successors(current)
            potential_moves_current =astar.generate_potential_moves(current)
            potential_moves_distance={}
            for move in potential_moves_current:
                    move_coor = astar.get_coordinate(move)
                    move_hop = round(path[move_coor[0], move_coor[1]], 1)
                    if move_hop <= -1000 :
                        continue
                    x = np.array(current_coor)
                    y = np.array(move_coor)
                    dist = np.sum(np.abs(x - y))
                    potential_moves_distance[move] = dist
                    #print(dist)

            next_moves = sorted(
                potential_moves_distance,
                key = potential_moves_distance.get,
                reverse = False
            )
            
            goal_count += 1
            current = next_moves[0]
            current_coor = astar.get_coordinate(next_moves[0])

        print(best_path)
        print("Passenger:"+passenger["dataset"]+"End")



#==============test
#test = variable_weight_file.loc[(variable_weight_file['fromZone']==100552) & (variable_weight_file['ToZone']==100552)]['h22']
#print(test)














