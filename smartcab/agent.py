from collections import defaultdict
from environment import Agent, Environment
from numpy import mean
from planner import RoutePlanner
from simulator import Simulator
import random

# constants
DEBUG = False
ACTIONS = ['forward', 'left', 'right', None]

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint

        self.alpha   = 0.9                  # learning rate
        self.epsilon = 0.1                  # exploration
        self.gamma   = 0.0                  # discount
        self.decay   = self.epsilon / 90    # exploration decay

        self.q_dict = defaultdict(lambda: {
            'forward': 0,
            'left': 0,
            'right': 0,
            None: 0
        })

        self.running_reward = 0

        self.cycles = 0
        self.violations = 0

        self.result = None
        self.results = []

    def estimate(self, state, action):
        # NOTE: since we have a myopic agent, the estimate of optimal future
        #       value is disabled (it can't see into the future!)
        return 0

    def explore(self):
        return float(random.random()) < self.epsilon

    def q_values(self):
        return self.q_dict[self.state]

    def best_actions(self):
        q_values = self.q_values()
        max_value = max(q_values.values())
        return [action for action in q_values if q_values[action] == max_value]

    def reset(self, destination=None):
        # prepare for a new trip; reset any variables here, if required
        self.planner.route_to(destination)
        self.running_reward = 0

        self.cycles = 0
        self.violations = 0
        self.epsilon -= self.decay

        if self.result != None:
            self.results.append(self.result)

    def update(self, t):
        # initialize
        action = None
        self.cycles += 1

        # gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # update state
        self.state = (
            ('light',    inputs['light']),
            ('next',     self.next_waypoint),
            ('oncoming', inputs['oncoming']),
            ('left',     inputs['left']),
            ('right',    inputs['right'])
        )

        # select action according to your policy
        if self.explore():
            if DEBUG:
                print '[explore] exploring'
            action = random.choice(ACTIONS)
        else:
            action = random.choice(self.best_actions())

        # execute action and get reward
        reward = self.env.act(self, action)
        self.running_reward += reward

        if reward < 0:
            self.violations += 1

        # learn policy based on state, action, reward
        #  Q = old + alpha * ( reward + gamma * estimate - old)
        self.q_dict[self.state][action] = self.q_values()[action] + \
            self.alpha * (
                reward \
                + self.gamma * self.estimate(self.state, action) \
                - self.q_values()[action]
            )

        if DEBUG:
            print "[update] d: {}, s: {}, a: {}, r: {}, rr: {}".format(
                deadline,
                'hide', #self.state,
                action,
                reward,
                self.running_reward)

        self.result = (self.cycles, self.running_reward, self.violations)

def run(msg = ''):
    """Run the agent for a finite number of trials."""

    # set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # specify agent to track
    # NOTE: you can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0, display=False)  # create simulator (uses pygame when display=True, if available)
    # NOTE: to speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: to quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line

    results = a.results
    average_cycles = mean([result[0] for result in results])
    average_reward = mean([result[1] for result in results])
    average_violations = mean([result[2] for result in results])
    print '=' * 10, msg
    print 'Average Cycles:', average_cycles
    print 'Average Reward:', average_reward
    print 'Average Violations:', average_violations

    return average_cycles, average_reward, average_violations

if __name__ == '__main__':
    meta_results = []
    for r in range(100):
        meta_results.append(run(str(r)))

    meta_cycles = mean([meta_result[0] for meta_result in meta_results])
    meta_reward = mean([meta_result[1] for meta_result in meta_results])
    meta_violations = mean([meta_result[2] for meta_result in meta_results])
    print '=' * 100
    print 'Average Cycles:', meta_cycles
    print 'Average Reward:', meta_reward
    print 'Average Violations:', meta_violations
