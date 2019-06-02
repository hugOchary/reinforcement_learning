from collections import namedtuple
from .learner import Learner
import torch

import math
import random

LearningParameters = namedtuple('LearningParameters',
                                ('EPS_START', 'EPS_END', 'EPS_DECAY', 'GAMMA'))


def explorationOrExplotation(learning_parameters, steps_done):
    draw = random.random()
    eps_threshold = learning_parameters.EPS_END + (learning_parameters.EPS_START - learning_parameters.EPS_END) * math.exp(-1 * steps_done / learning_parameters.EPS_DECAY)
    return (draw >= eps_threshold)


class DeepBoardLearner(Learner):

    def __init__(self, id):
        super(Learner, self).__init__()
        self.policy_net = None
        self.target_net = None
        self.optimizer = None
        self.loss_function = None
        self.learning_parameters = None
        self.counter = 0

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # setters

    def setNetworks(self, net_class, *args):
        try:
            self.policy_net = net_class(*args).to(self.device)
            self.target_net = net_class(*args).to(self.device)
            self.target_net.load_state_dict(self.policy_net.state_dict())
            return True
        except:
            return False

    def resetCounter(self):
        self.counter = 0

    def update(self):
        self.target_net.load_state_dict(self.policy_net.state_dict())

    def setOptimizer(self, optimizer):
        self.optimizer = optimizer(self.policy_net.parameters())

    def setLossFunction(self, loss_function):
        self.loss_function = loss_function

    def setLearningParameters(self, *args):
        self.learning_parameters = LearningParameters(*args)

    # Training

    def choseAction(self, state, nb_action, steps_done):
        if explorationOrExplotation(self.learning_parameters, steps_done):
            with torch.no_grad():
                self.counter += 1
                return self.policy_net(state).max(1)[1].view(1)

        else:
            return torch.tensor([random.randrange(nb_action)], device=self.device, dtype=torch.long)

    def train(self, batch):
        '''
        This transition_batch is expected to have four attributes :
            - batch.state
            - batch.action
            - batch.next_state
            - batch.reward
        
        See MemoryReplayStructure for more details
        '''

        state_batch = torch.stack(batch.state)
        action_batch = torch.stack(batch.action)
        next_states = torch.stack(batch.next_state)
        reward_batch = torch.stack(batch.reward)

        action_q_values = self.policy_net(state_batch).gather(1, action_batch)
        next_state_max_q_values = self.target_net(next_states).max(1)[1].detach()

        bellman_expected_q_value = (next_state_max_q_values.float() * self.learning_parameters.GAMMA) + reward_batch

        loss = self.loss_function(action_q_values, bellman_expected_q_value.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()

        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)

        self.optimizer.step()

        return loss

    # Loading and saving model

    def loadModel(self, path):
        self.policy_net.load_state_dict(torch.load(path))

    def saveModel(self, path):
        torch.save(self.policy_net.state_dict(), path)
