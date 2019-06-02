from abc import ABC, abstractmethod


class Learner(ABC):

    def __init__(self):
        pass
    

    # play related methods

    @abstractmethod
    def choseAction(self, nb_action, steps_done):
        pass