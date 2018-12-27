import gym
from gym import error, spaces, utils
from gym.utils import seeding

class MouseTrapEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.grid = self.init_grid()
        self.state = (1,1)
        self.energy = 100
        self.action_space = spaces.Discrete(4)

    def step(self, action):
        if action == 0 and self.state[0] > 0:
            self.state = (self.state[0]-1, self.state[1])
        elif action == 1 and self.state[0] < 9:
            self.state = (self.state[0]+1, self.state[1])
        elif action == 2 and self.state[1] > 0:
            self.state = (self.state[0], self.state[1]-1)
        elif action == 3 and self.state[1] < 9:
            self.state = (self.state[0], self.state[1]+1)
        else:
            True
        reward = self.grid[self.state[0]][self.state[1]]
        self.energy += reward
        done = self.energy == 0 or reward == 1
        new_state = 10*self.state[0] + self.state[1]
        return (new_state, reward, done, None)

    def reset(self):
        self.state = (1,1)
        self.energy = 100
        return 11

    def render(self, mode='human', close=False):
        line = ""
        for i in range(10):
            for j in range(10):
                if (i,j) == self.state:
                    line += "-"
                elif self.grid[i][j] == 0:
                    line += "O"
                elif self.grid[i][j] == -1:
                    line += "X"
                elif self.grid[i][j] == 1:
                    line += "#"
            line += "\n"
            print(line)

    # Private methods

    def init_grid(self):
        state_grid = [[ 0 for i in range(10)] for j in range(10)]
        state_grid[9][9] = 1
        for i in range(5):
            for j in range(5):
                state_grid[2*i][2*j] = -1
        return state_grid


