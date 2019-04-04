from collections import namedtuple
import random
import torch

Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))

class MemoryReplayStructure:

    def __init__(self, batch_size, max_capacity):
        self.batch_size = batch_size
        self.max_capacity = max_capacity
        self.memory = []
        self.position = 0
    
    def push(self, *args):
        """ saves a transition """
        if len(self.memory) < self.max_capacity:
            self.memory.append(None)
        
        self.memory[self.position] = Transition(*args)
        self.position = (self.position + 1) % self.max_capacity

    def sample(self):
        sample = random.sample(self.memory, self.batch_size)
        batch = Transition(*zip(*sample))
        return batch

    def canSample(self):
        return len(self.memory) >= self.batch_size

    def __len__(self):  
        return len(self.memory)