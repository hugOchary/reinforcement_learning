import numpy as np
from numpy.random import seed, randint
import random
import time

from game import Game
seed(int(time.time()))


class FixedMouseGame(Game):

    def __init__(self, id, name):
        super(FixedMouseGame, self).__init__(id, name)
        self.width = 10
        self.height = 10
        self.board = np.zeros((10,10), np.int32)
        self.state = randint(0,10,2)
        self.score = 100
        self.occupied = None
        self.reset()
    
    def reset(self):
        self.score = 100
        board = np.zeros((10,10),np.int32)
        positions = randint(0,10,16, dtype=np.int32)
        self.occupied = positions
        for i in range(1,8):
            board[positions[2*i]][positions[2*i+1]] = -1
        board[positions[0]][positions[1]] = 1
        self.state = randint(0,10,2, dtype=np.int32)
        self.board = board
    
    def getBoard(self):
        return self.board

    def setState(self):
        self.state = randint(0,10,2, dtype=np.int32)

    def setActions(self):
        self.actions = [[1,0],[0,1],[-1,0],[0,-1]]

    def getScore(self):
        return self.score
    
    def gameOver(self):
        if (self.board[self.state[0]][self.state[1]] == -1 ) :
            return 3
        elif (self.board[self.state[0]][self.state[1]] == 1 ) :
            return 2
        elif (self.score <= 0)  :
            return 1
        else :
            return 0
    
    def play(self, input):
        previousScore = self.score
        self.score -= 1
        action = self.actions[input]
        new_x = max(0, min(self.state[0]+action[0], 9))
        new_y = max(0, min(self.state[1]+action[1], 9))
        self.state[0] = new_x
        self.state[1] = new_y
        self.score += 10 * self.board[new_x][new_y]
        return (self.score - previousScore, self.gameOver())

    

