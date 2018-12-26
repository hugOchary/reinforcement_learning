import argparse
from random import randrange

# path setup
import sys
sys.path.insert(0, '../../Q-learners/')

from mouseTrapQLearner import QLearner

import pygame
from pygame.locals import *

# Argument parsing

parser = argparse.ArgumentParser()
parser.add_argument('--n_training', type=int, default=1000, help='number of training the player will go through')
parser.add_argument('--n_play', type=int, default=20, help='number of play the player will go through after training')
parser.add_argument('--traps', type=bool, default=True, help='Do we use traps in the game')
parser.add_argument('--n_traps', type=int, default=6, help='Number of traps to use in the game')
parser.add_argument('--rnd_lever', type=bool, default=True, help='Is the lever position set randomly')
opt = parser.parse_args()

# pygame constants intialisation

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
GREY = (100, 100, 100)
SCREENRECT = pygame.Rect(0,0,640,480)
SCORE = 0
ALLOWEDMOVE = [K_UP, K_DOWN, K_LEFT, K_RIGHT]
SIZE = 30

class MouseTrap:

    def __init__(self, starting_position = [0,0], energy = 100, decay_rate = -1, reward_strategy = 10):
        self.grid = None
        self.height = None
        self.width = None
        self.position = starting_position
        self.energy = energy
        self.decay_rate = decay_rate
        self.reward_strategy = reward_strategy
        self.lever_position =None

    def step(self):
        '''
        Compute the evolution of the energy and score of the game
        according to its position.
        '''
        if self.grid[self.position[0]][self.position[1]] == 10:
            return 1
        self.score = 0
        # We handle the stepping on a trap
        if self.grid[self.position[0]][self.position[1]] == -self.reward_strategy:
            return 1
        # we update the energy and score
        old_energy = self.energy
        self.energy += self.grid[self.position[0]][self.position[1]]
        self.score = (self.energy-old_energy) - (self.energy > 0)
        return int(self.energy < 0)

    def pick_trap(self, taken_positions):
        new_position = [randrange(self.height), randrange(self.width)]
        if new_position not in taken_positions:
            return new_position
        else:
            return self.pick_trap(taken_positions)
    
    def init_grid(self, width, height):
        '''
        Init the grid cells with a lever
        '''
        self.width = width
        self.height = height

        # We init the lever position and the grid
        self.lever_position = (self.height//2, self.width//2)
        if opt.rnd_lever:    
            self.lever_position = (randrange(height), randrange(width))
        grid = [
            [ self.decay_rate for i in range(width)] for j in range(height)
        ]
        grid[self.lever_position[0]][self.lever_position[1]] = 10

        # We now add some traps to the map
        if opt.traps:
            taken_positions = [self.lever_position]
            for i in range(opt.n_traps):
                taken_positions.append(self.pick_trap(taken_positions))
            taken_positions.pop(0)
            for position in taken_positions:
                grid[position[0]][position[1]] = -self.reward_strategy

        self.grid = grid

    def move(self, arg):
        '''
        compute the move given an entry, won't move if move not allowed
        '''
        (x,y) = arg
        new_x = self.position[0]+x
        new_y = self.position[1]+y
        if not (new_x < 0 or new_x >= self.height):
            self.position[0] = new_x
        if not (new_y < 0 or new_y >= self.width):
            self.position[1] = new_y
    
    def next(self, arg):
        '''
        Combine movement and evolution
        '''
        if arg != None:
            self.move(arg)
            return self.step()

    
    def pick_color(self, cell_value):
        '''
        Return a color given a integer value
        '''
        if cell_value == self.decay_rate:
            return WHITE
        elif cell_value == self.reward_strategy:
            return RED
        elif cell_value == -self.reward_strategy:
            return GREEN
        elif cell_value == 0:
            return BLUE
    
    def reset(self):
        self.position = [randrange(self.height) ,randrange(self.width)]
        while self.position == self.lever_position:
            self.position = [randrange(self.height) ,randrange(self.width)]
        self.energy = 100
        self.score = 0

    def draw(self, screen):
        '''
        Draw the grid on the screen
        '''
        x = self.position[0]
        y = self.position[1]
        for i in range(self.height):
            for j in range(self.width):
                color = self.pick_color(self.grid[i][j])
                pygame.draw.rect(screen, color, (SIZE*i+i, SIZE*j+j, SIZE, SIZE))
        pygame.draw.rect(screen, GREY, (SIZE*x+x, SIZE*y+y, SIZE, SIZE))

def wait():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE) :
                pygame.quit()
                sys.exit()
            if (event.type == KEYDOWN and event.key in ALLOWEDMOVE):
                return pygame.key.get_pressed()

def training(player, mouseTrapGame):

    terminate = 0

    while terminate == 0:

        # we save the state before play
        former_position = [mouseTrapGame.position[0], mouseTrapGame.position[1]]
        move = player.decision(former_position)
        new_position = mouseTrapGame.position

        # we play according to the player's choice
        terminate = mouseTrapGame.next(move)
        
        # We update the player
        player.update_QTable(former_position,
            mouseTrapGame.grid[mouseTrapGame.position[0]][mouseTrapGame.position[1]],
            mouseTrapGame.position)
        

    return player

def play(player, mouseTrapGame, screen, clock):

    terminate = 0
    print(mouseTrapGame.position)

    while terminate == 0:

        # we save the state before play
        former_position = [mouseTrapGame.position[0], mouseTrapGame.position[1]]
        move = player.decision(former_position)

        # we play according to the player's choice
        terminate = mouseTrapGame.next(move)

        # we update the screen
        mouseTrapGame.draw(screen)
        pygame.display.update()
        clock.tick(10)
        
    

def main():
    
    #Initialization of our game
    mouseTrapGame = MouseTrap()
    mouseTrapGame.init_grid(10, 10)

    #Initialisation of QLearner
    player = QLearner((mouseTrapGame.height, mouseTrapGame.width), mouseTrapGame.grid)

    for i in range(opt.n_training):

        mouseTrapGame.reset()

        player = training(player, mouseTrapGame)
        player.decrease_exploration()
    
    print(player)
    
    #initializing pygame
    pygame.init()
    clock = pygame.time.Clock()

    
    #initializing screen
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Initialisation of the screen
    mouseTrapGame.draw(screen)
    pygame.display.update()

    player.set_to_play()
    for i in range(opt.n_play):
        
        mouseTrapGame.reset()
        play(player, mouseTrapGame, screen, clock)

if __name__ == '__main__' :
    main()