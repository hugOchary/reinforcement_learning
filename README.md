# reinforcement_learning
Python repositoriy for all basic reinforcement learning

# The mouse trap game

The purpose is here to modelize a mice in a room that needs to go and activate a lever in order to receive food. The goal is to train it using reinforcement learning.

# mouse trap game simplified

The initial idea is more complex than I first thought so I started with the most simplistic model there is: 
```
    The mice evolves always in the same room setup needs only to reach the lever
```

In order to simulate this problem in an easy to visualize manner I coded a graphical representation of the room using [pygame](https://www.pygame.org/news), with white squarefor the ground, grey for the mice and red for the lever.

You can launch the game and control the mice by launching

```bash
python ./games/mouseTrap/mouseTrap.py
```

You can also lauch the training of a mice and watch hit go through 100 tests afterward using:

```bash
python ./games/mouseTrap/mouseTrapSimplified.py
```

The states of our system are rather simple, each positionis a different state and the different actions possible where going up, down, right and left.

I solved this problems using :

* A Q-table
* An initial exploration rate of 1
* A random starting point at each iteration of the training.

the Q-table contains the previously described states with for each 4 possible actions, with all a q-value of zero. The initial exploration rate of 1 allows for random exploration of the environment at the begining to later tend toward exploitation. Finaly to start at a random pont at each iteration of the training allows for more efficient exploration.

After the training that takes 1000 iteration the mice will go toward the lever as intended. I need know to add a degree of complexity to this model.

I added traps in the game and arguments to customize the training, see ```--help``` for more details.

# Mouse trap game intermediate

```
    Now the lever generates food on a random cell, with no traps
```

This model poses the problem of representing a dynamic environment.