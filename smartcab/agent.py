import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

# action shorthand constants
F = 'forward'
L = 'left'
R = 'right'
S = None
ACTIONS = [F, L, R, S]

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        # initialize any additional variables here

    def reset(self, destination=None):
        self.planner.route_to(destination)

        # prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # update state
        self.state = {
            'light':    inputs['light'],
            'next':     self.next_waypoint,
            'oncoming': inputs['oncoming'],
            'left':     inputs['left'],
            'right':    inputs['right']
        }

        # select action according to your policy
        action = random.choice(ACTIONS)

        # execute action and get reward
        reward = self.env.act(self, action)

        # learn policy based on state, action, reward

        print "[update] d: {}, s: {}, a: {}, r: {}".format(deadline, self.state, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: you can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.5, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: to speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: to quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
