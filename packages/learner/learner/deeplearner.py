from abc import abstractmethod
from .learner import Learner


class DeepLearner(Learner):

    def __init__(self):
        super(Learner).__init__(self)
        self.policy_net = None
        self.target_net = None
        self.optimizer = None
        self.loss_function = None
    
    # setters

    @abstractmethod
    def setNetworks(self, net_class, *args):
        pass
    
    @abstractmethod
    def setOptimizer(self, optimizer):
        pass
    
    @abstractmethod 
    def setLossFunction(self, loss_function):
        pass
    
    # training
    @abstractmethod
    def choseAction(self):
        pass

    @abstractmethod
    def computeLoss(self):
        pass
    
    @abstractmethod
    def train(self):
        pass
    
    # Loading and saving model

    @abstractmethod
    def loadModel(self):
        pass

    @abstractmethod
    def saveModel(self):
        pass
