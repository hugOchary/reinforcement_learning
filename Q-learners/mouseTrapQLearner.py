from random import randrange, choice

MOVES = [(0,1), (0,-1), (1,0), (-1,0)]

def convert_movement(self, index):
        return MOVES[index]

class QLearner:
    ''' first try at reinforcement learning with a simplified mouseTrape game
    the level is fixed and the games stops when stepping on a lever or dying'''

    def __init__(self, dim, grid, learning_rate = 0.7, discount_rate = 0.9):
        self.dim = dim
        self.qTable = self.init_QTable()
        self.game_state = grid
        self.exploration_rate = 100
        self.learning_rate = learning_rate
        self.last_choice = None
        self.discount_rate = discount_rate
    
    def init_QTable(self):
        # the coordinate of grid[i][j] is i*self.dim[1] + j
        qTable = [
            [ 0 for j in range(4)] for i in range(self.dim[1]*self.dim[0]) 
        ]
        #for i in range(self.dim[0]):
        #    qTable[i][0] = None
        #    qTable[i][self.dim[1]] = None
        #for j in range(self.dim[1]):
        #    qTable[0][j] = None
        #    qTable[self.dim[0]][j] = None
        
        return qTable
    
    def max_of_state(self, state_x, state_y):
        m = max(self.qTable[state_x*self.dim[1] + state_y])
        max_list = [i for i, j in enumerate(self.qTable[state_x*self.dim[1] + state_y]) if j == m ]
        return choice(max_list)

    def decision(self, position):
        (x,y) = position
        chosen_move = None
        p = randrange(100)
        if p > self.exploration_rate:
            chosen_move = self.max_of_state(x, y)
        else:
            chosen_move = randrange(4)
        self.last_choice = chosen_move
        return MOVES[chosen_move]

    def update_QTable(self, former_position, reward, new_position):
        former_x, former_y = former_position
        new_x, new_y = new_position

        # we save the former qvalue for the state / action tuple
        former_qvalue = (1-self.learning_rate)*self.qTable[
            former_x*self.dim[1] + former_y
            ][self.last_choice]

        self.qTable[former_x*self.dim[1] + former_y][self.last_choice] = former_qvalue + self.learning_rate*(reward + self.discount_rate * max(
            self.qTable[new_x*self.dim[1] + new_y]
        ))
    
    def decrease_exploration(self, rate = 0.99):
        self.exploration_rate *= rate
    
    def set_to_play(self):
        self.exploration_rate = 0
    
    def __str__(self):
        result = ""
        for index, l in enumerate(self.qTable):
            result = result + "cell : [" + str(index//self.dim[1]) + str(index%self.dim[1]) + "] : "
            result += str(l)
            result += " \n "
        return result
