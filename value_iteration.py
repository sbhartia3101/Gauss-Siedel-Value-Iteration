import copy
import math
import operator

import numpy as np, pprint


def turn_left(action):
    switcher = {
        (-1, 0): (0, -1),
        (0, 1): (-1, 0),
        (1, 0): (0, 1),
        (0, -1): (1, 0)

    }
    return switcher.get(action)


def turn_right(action):
    switcher = {
        (-1, 0): (0, 1),
        (0, 1): (1, 0),
        (1, 0): (0, -1),
        (0, -1): (-1, 0)

    }
    return switcher.get(action)


def addTwoTuples(a, b):
    return tuple(map(operator.add, a, b))


def argmax(seq, fn):
    best = seq[0]
    best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score > best_score:
            best, best_score = x, x_score
    return best


def go(current_state, action, grid_size):
    state1 = addTwoTuples(current_state, action)
    x_coord = state1[0]
    y_coord = state1[1]
    if x_coord < 0 or x_coord >= grid_size or y_coord < 0 or y_coord >= grid_size:
        return current_state
    else:
        return state1


def play(env, policy):
    utility_values = []
    for j in range(10):
        pos = env.start_loc
        utility = 0
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k = 0
        while pos != env.terminal_loc:
            move = policy[pos]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)

            k += 1
            pos = go(pos, move, env.grid_size)
            utility += env.get_reward(pos)
        utility_values.append(utility)
    # print utility_values
    cost = int(math.floor(sum(utility_values) / len(utility_values)))
    return cost



class GridMDP:

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.action_dim = (4,)
        # North, south, East, West
        self.action_coordinates = [(-1, 0), (1, 0), (0, 1), (0, -1)]
        self.rewards = [[-1 for x in range(grid_size)] for y in range(grid_size)]
        self.gamma = 0.9
        self.epsilon = 0.1
        self.states = [(x, y) for x in range(grid_size) for y in range(grid_size)]
        self.utility = None
        self.policy = None

        self.T = None

    def __deepcopy__(self, memodict={}):
        copy_object = GridMDP(self.grid_size)
        copy_object.rewards = copy.deepcopy(self.rewards)
        copy_object.T = dict(self.T)
        # copy_object.T = self.generate_trans_matrix()
        copy_object.policy = copy.deepcopy(self.policy)
        return copy_object


    # For every obstacle add a -101 as reward
    def add_obstacles(self, list_of_obstacles):
        for obstacle in list_of_obstacles:
            self.rewards[obstacle[0]][obstacle[1]] = -101

    # Keep a track of every start location
    def add_start_location(self, start_loc):
        self.start_loc = start_loc

    # Update the reward as 99 for every end location
    def add_end_location(self, end_loc):
        self.terminal_loc = end_loc
        self.rewards[end_loc[0]][end_loc[1]] = 99

        end_loc_no = end_loc[0] * self.grid_size + end_loc[1]
        action_list = {}
        # No of action co-ordinates
        for i in range(4):
            action_list[i] = self.turn(end_loc, None)

        self.T[end_loc_no] = action_list

    def get_reward(self, state):
        return self.rewards[state[0]][state[1]]

    def get_actions(self, state):
        if state == self.terminal_loc:
            return [None]
        else:
            return self.action_coordinates

    def go(self, current_state, action):
        return go(current_state, action, self.grid_size)

    def turn(self, current_state, action):
        if action is None:
            return [(0, current_state)]
        else:
            return [(0.7, self.go(current_state, action)),
                    (0.1, self.go(current_state, turn_right(action))),
                    (0.1, self.go(current_state, turn_left(action))),
                    (0.1, self.go(current_state, turn_left(turn_left(action))))]


    def run_with_trans_matrix(self):
        utility1 = dict([(s, 0) for s in self.states])
        while True:
            delta = 0
            revised_utility1 = utility1
            for s in self.states:
                state_no = s[0] * self.grid_size + s[1]
                u = utility1[s]
                max_util = - float("inf")
                for i in range(len(self.action_coordinates)):
                    # a = self.action_coordinates[i]
                    util = 0
                    for (p, s1) in self.T[state_no][i]:
                        util += (p * revised_utility1[s1])
                    if util > max_util:
                        max_util = util
                utility1[s] = self.get_reward(s) + self.gamma * max_util

                delta = max(delta, abs(u - utility1[s]))

            if delta < self.epsilon * (1 - self.gamma) / self.gamma:
                break

        self.utility = utility1
        pi = self.get_policy()
        return pi

    def get_policy(self):
        policy = {}
        for s in self.states:
            policy[s] = argmax(self.get_actions(s), lambda a: self.expected_utility(a, s, self.utility))
        self.policy = policy
        return policy

    def expected_utility(self, a, s, utility):
        return sum([p * utility[s1] for (p, s1) in self.turn(s, a)])

    def generate_trans_matrix(self):
        transmat = {}
        action_list = {}
        for s in range(self.grid_size * self.grid_size):
            x_coord = s // self.grid_size
            y_coord = s % self.grid_size
            state = (x_coord, y_coord)
            for i in range(len(self.action_coordinates)):
                action_list[i] = self.turn(state, self.action_coordinates[i])

            transmat[s] = action_list
            action_list = {}

        self.T = transmat


def read_file(input_file_name):
    with open(input_file_name, "r") as file:
        # Read 1st line for the grid size
        line = file.readline().rstrip()
        grid_size = int(line)
        environment = GridMDP(grid_size)

        # Read 2nd line for the no. of cars
        line = file.readline().rstrip()
        no_of_cars = int(line)

        # Read 3rd line for the no. of obstacles
        line = file.readline().rstrip()
        no_of_obstacles = int(line)

        location_of_obstacles = []
        car_locations = {}
        for i in range(0, no_of_cars):
            car_locations[i] = {}

        # Read all the obstacles co-ordinates
        while len(location_of_obstacles) != no_of_obstacles:
            loc = map(int, file.readline().rstrip().split(",")[::-1])
            location_of_obstacles.append(tuple(loc))

        car_cnt = 0
        # Read all the car start location co-ordinates
        while car_cnt < no_of_cars:
            loc = map(int, file.readline().rstrip().split(",")[::-1])
            car_locations[car_cnt]["Start"] = tuple(loc)
            car_cnt += 1

        car_cnt = 0
        # Read all the car terminal location co-ordinates
        while car_cnt < no_of_cars:
            loc = map(int, file.readline().rstrip().split(",")[::-1])
            car_locations[car_cnt]["End"] = tuple(loc)
            car_cnt += 1

    if len(location_of_obstacles) > 0:
        environment.add_obstacles(location_of_obstacles)

    environment.generate_trans_matrix()

    return [environment, car_locations]

def execute(inputfile="grading_case/input30.txt"):
    original_grid, car_locations = read_file(inputfile)
    endloc_policy = {}
    # f = open("output.txt", "w")
    for car, locations in car_locations.items():
        start_loc = locations["Start"]
        end_loc = locations["End"]
        if start_loc == end_loc:
            cost = 100
        else:
            if end_loc in endloc_policy:
                grid = copy.deepcopy(endloc_policy[end_loc])
                grid.add_end_location(end_loc)
                pi = grid.policy
            else:
                grid = copy.deepcopy(original_grid)
                grid.add_end_location(end_loc)
                pi = grid.run_with_trans_matrix()
                endloc_policy[end_loc] = grid

            grid.add_start_location(start_loc)

            cost = play(grid, pi)
        print cost
        # f.write(str(cost) + "\n")
    # f.close()


if __name__ == "__main__":
    execute()
