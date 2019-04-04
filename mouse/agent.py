import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

import torchvision
import torchvision.transforms as transforms

import copy
import numpy as np
import random 
import math
import time

# homemade package

from learner import DeepBoardLearner 
from memory_replay_structure import MemoryReplayStructure
from fixedMouseGame import FixedMouseGame


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
class Network(nn.Module):
    def __init__(self):
        super(Network, self).__init__()
        self.fc1 = nn.Linear(10*10, 50)
        self.fc2 = nn.Linear(50, 50)
        self.out = nn.Linear(50,4)

    def forward(self, input):
        x = F.relu(self.fc1(input))
        x = F.relu(self.fc2(x))
        x = self.out(x)
        return F.log_softmax(x)


player = DeepBoardLearner(int(time.time()))

player.setNetworks(Network)

player.setLossFunction(F.smooth_l1_loss)
player.setOptimizer(optim.RMSprop)

player.setLearningParameters(0.9,0.05, 2000, 0.999)

game = FixedMouseGame(int(time.time()), 'mouse game trainer')

memory = MemoryReplayStructure(128, 10000)

# the training 

NB_EPOCH = 10000

NB_ACTION = len(game.getActions())

nb_actions = 0

score_memory = [0,0,0]

counter = 0

steps_done = 0

final_score_memory = []

for epoch in range(NB_EPOCH):
    #print("=================\n")
    #print("begining new epoch ", epoch)
    game.reset()
    nb_actions = 0
    steps_done += 1
    game_status = 0 
    while game_status == 0:
        state = torch.from_numpy(game.getBoard()).to(device).flatten().float()
        action = player.choseAction(state, NB_ACTION, steps_done)
        reward, game_status = game.play(action.item())
        nb_actions += 1
#        try:
        action_reward = torch.tensor([action], device=device)
        tensor_reward = torch.tensor([reward], device=device, dtype=torch.float)
#        except:
#            print("action : ", action, "\nreward : ", reward)
#            inp = input("what to do?")
        memory.push(state, action , torch.from_numpy(game.getBoard()).to(device).flatten().float(), tensor_reward)
        if memory.canSample():
            batch = memory.sample()
            player.train(batch)
    
    if counter == 100:
        final_score_memory.append(score_memory)
        score_memory = [0,0,0]
        counter = 0
        #print("number of actions : ", nb_actions)
        #print("\n")
    else :
        score_memory[game_status-1] = score_memory[game_status-1]+1
        counter+=1

f= open("final_score.txt","w+")
for score_memory in final_score_memory:
    f.write(str(score_memory)+"\n")
f.close()

player.saveModel("./model")


