import gym
from gym.envs.registration import register

register(
    id='MouseTrap-v0',
    entry_point='gym_mouseTrap.envs:MouseTrapEnv',
)