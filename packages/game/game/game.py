from abc import ABC, abstractmethod

class Game(ABC):

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.actions = None
        self.state = None
        self.setActions()
        self.setState()
    
    # settings methods

    @abstractmethod
    def reset(self):
        pass
    
    @abstractmethod
    def setActions(self):
        pass
    
    @abstractmethod
    def setState(self):
        pass
    
    @abstractmethod
    def gameOver(self):
        pass

    # get methods

    def getActions(self):
        return self.actions
    
    def getState(self):
        return self.state
    
    # play related methods
    
    @abstractmethod
    def play(self, input):
        pass