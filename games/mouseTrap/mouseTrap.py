from random import randrange

import pygame
from pygame.locals import *

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
        self.score = 0
        self.decay_rate = decay_rate
        self.reward_strategy = reward_strategy
        self.lever_position =None

    def step(self):
        '''
        Compute the evolution of the energy and score of the game
        according to its position.
        '''
        # We handle the stepping on a lever
        if self.grid[self.position[0]][self.position[1]] == 0:
            food_position = (randrange(self.height), randrange(self.width))
            while food_position == self.lever_position:
                food_position = (randrange(self.height), randrange(self.width))
            self.grid[randrange(self.height)][randrange(self.width)] = self.reward_strategy
        
        # We handle the stepping on a trap
        if self.grid[self.position[0]][self.position[1]] == -self.reward_strategy:
            self.energy = 0
        # we update the energy and score
        old_energy = self.energy
        self.energy += self.grid[self.position[0]][self.position[1]]
        self.score = (self.energy-old_energy) - (self.energy > 0)*1000
        # we set the cell energy to 0
        if self.grid[self.position[0]][self.position[1]] == self.reward_strategy:
            self.grid[self.position[0]][self.position[1]] = self.decay_rate

    def pick_trap(self, taken_positions):
        new_position = [randrange(self.height), randrange(self.width)]
        if new_position not in taken_positions:
            return new_position
        else:
            return self.pick_trap(taken_positions)
    
    def init_grid(self, nb_of_lever, width, height):
        '''
        Init the grid cells with a lever
        '''
        self.width = width
        self.height = height
        self.lever_position = (randrange(height), randrange(width))
        grid = [
            [ self.decay_rate for i in range(width)] for j in range(height)
        ]
        grid[self.lever_position[0]][self.lever_position[1]] = 0

        # We now add some traps to the map
        taken_positions = [self.lever_position]
        for i in range(6):
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
            self.step()
    
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

def main():
    #initializing pygame
    pygame.init()
    clock = pygame.time.Clock()

    #initializing screen
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #Initialization of our game
    mouseTrapGame = MouseTrap()
    mouseTrapGame.init_grid(3, 10, 10)

    #Initialisation of the screen
    mouseTrapGame.draw(screen)
    pygame.display.update()

    while mouseTrapGame.energy > 0:

        # move initialization
        move = None

        #Event handling
        keystate = wait()

        #Event conversion:

        x = keystate[K_RIGHT] - keystate[K_LEFT]
        y = keystate[K_DOWN] - keystate[K_UP]
        if (y != 0 or x != 0):
            move = (x,y)

        # We compute the new state of the game
        mouseTrapGame.next(move)

        # we draw the new state of the game on the screen
        mouseTrapGame.draw(screen)
        pygame.display.update()

        clock.tick(25)
    
    print("The player died, thank you for playing")

if __name__ == '__main__' :
    main()