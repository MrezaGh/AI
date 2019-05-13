import gym
import pickle
env = gym.make("Taxi-v2")

file = open('./policy_iteration_policy.pkl', mode='rb')
policy = pickle.load(file)

state = env.reset()
score = 0

env.render()
while True:
    action = policy[state]
    state, reward, done, info = env.step(action)
    score += reward
    env.render()
    if done:
        # state = env.reset()
        break

print("score: ", score)
env.close()
