from random import randrange

class Player:

    def __init__(self, starting_position, energy):
        self.grid = None
        self.position = starting_position
        self.energy = energy
        self.score = 0

    def step(self, decay_rate):
        # we update the energy and score
        old_energy = self.energy
        self.energy += self.grid[self.position[0]][self.position[1]]
        self.score = (self.energy-old_energy) - (self.energy > 0)*1000
        # we set the cell energy to 0
        self.grid[self.position[0]][self.position[1]] = -decay_rate

    
    def init_grid(self, decay_rate, reward_strategy, nb_of_lever, width, height):
        random_couple = lambda : (randrange(height), randrange(width))
        levers = [random_couple for i in range(nb_of_lever)]
        grid = [
            [ -decay_rate for i in range(width)] for j in range(height)
        ]
        for (a,b) in levers :
            grid[a][b] = reward_strategy
        self.grid = grid
