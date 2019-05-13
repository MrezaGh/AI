import time
import gym
import random
import numpy as np
from copy import deepcopy

env = gym.make('Acrobot-v1')

num_states = 20000
max_episode_steps = 500


def discretizer(x, portion):
    if x < portion[0]: return 0
    for i in range(len(portion) - 1):
        if portion[i] <= x < portion[i + 1]: return i + 1
    if x >= portion[-1]: return len(portion)


def env_state_to_Q_state(stat):
    [cos_theta1, sin_theta1, cos_theta2, sin_theta2, thetaDot1, thetaDot2] = stat

    cos_theta1 = discretizer(cos_theta1, [-2 / 3, -1 / 3, 0, 1 / 3, 2 / 3])
    sin_theta1 = discretizer(sin_theta1, [-2 / 3, -1 / 3, 0, 1 / 3, 2 / 3])

    cos_theta2 = discretizer(cos_theta2, [-2 / 3, -1 / 3, 0, 1 / 3, 2 / 3])
    sin_theta2 = discretizer(sin_theta2, [-2 / 3, -1 / 3, 0, 1 / 3, 2 / 3])

    thetaDot1 = discretizer(thetaDot1, [0])
    thetaDot2 = discretizer(thetaDot2, [0])

    state = int(cos_theta1 + 6 * sin_theta1 + 36 * cos_theta2 + 216 * sin_theta2 + 1296 * thetaDot1 + 2592 * thetaDot2)
    return state


def action_selection(action_Qvalues, epsilon):
    chance = random.random()
    action = 0
    if chance < epsilon:
        action = random.randint(-1, 1)
    elif action_Qvalues[0] >= action_Qvalues[1] and action_Qvalues[0] >= action_Qvalues[-1]:
        action = 0
    elif action_Qvalues[1] >= action_Qvalues[0] and action_Qvalues[1] >= action_Qvalues[-1]:
        action = 1
    elif action_Qvalues[-1] >= action_Qvalues[0] and action_Qvalues[-1] >= action_Qvalues[1]:
        action = -1

    return action


def check_convergence(old_Qval, new_Qval):
    max_dif = float('-inf')
    print(old_Qval == new_Qval)
    for i in range(num_states):
        dif = abs(old_Qval[i][1] - new_Qval[i][1]) + abs(old_Qval[i][0] - new_Qval[i][0]) + abs(old_Qval[i][-1] - new_Qval[i][-1])
        max_dif = max(max_dif, dif)
    print("dif: =========>" + str(max_dif))
    if max_dif < 10**-4:
        print('convergence happened')
        return True
    return False


def Train():
    Qval = [[0] * 3 for i in range(num_states)]
    gama = 0.9
    alpha = 0.01
    epsilon = 1

    # convergence = False

    counter = 0  # for exiting and not running infinitely
    while True:
        state = env_state_to_Q_state(env.reset())
        done = False
        step_count = 0

        counter += 1  # I added

        while (not done) and step_count < max_episode_steps:
            # time.sleep(0.04)

            action = action_selection(Qval[state], epsilon)

            previous_state = state
            new_Qval = Qval.copy()

            state, reward, done, _ = env.step(action)
            state = env_state_to_Q_state(state)
            step_count += 1

            sample = reward + gama*max(Qval[state][-1], Qval[state][0], Qval[state][1])
            new_Qval[previous_state] = Qval[previous_state].copy()
            new_Qval[previous_state][action] = Qval[previous_state][action] + alpha*(sample - Qval[previous_state][action])
            # if step_count % 100 == 0 and counter % 10 == 0 and check_convergence(Qval, new_Qval):
            #     print('steps: ' + str(counter))
            #     convergence = True
            Qval = new_Qval

            # env.render()
        if counter % 5 == 0:
            print("progress: " + str(counter/100))
            epsilon *= 0.9954
            print(epsilon)
        # if convergence:
        #     break
        if counter > 5000:  # for exiting and not running infinitely
            break
    Policy = [0] * num_states

    for i in range(num_states):
        if Qval[i][0] >= Qval[i][1] and Qval[i][0] >= Qval[i][-1]:
            Policy[i] = 0
        elif Qval[i][1] >= Qval[i][0] and Qval[i][1] >= Qval[i][-1]:
            Policy[i] = 1
        elif Qval[i][-1] >= Qval[i][0] and Qval[i][-1] >= Qval[i][1]:
            Policy[i] = -1

    print("Policy : ", Policy)
    np.save('q_saved', Policy)


def cos_theta1_difference(action, minus_sin_theta1):
    if action == 0:
        return 0
    elif action == 1:
        return 1
    elif action == -1:
        return -1


def Train_by_feature():
    Qval = [[0] * 3 for i in range(num_states)]
    gama = 0.9
    alpha = 0.01
    epsilon = 1

    # convergence = False

    counter = 0  # for exiting and not running infinitely

    w_cos1 = 0
    w_cos2 = 0
    w_sin1 = 0
    w_sin2 = 0
    w_theta1 = 0
    w_theta2 = 0
    while True:
        state = env.reset()
        done = False
        step_count = 0

        counter += 1  # I added

        while (not done) and step_count < max_episode_steps:

            action = action_selection(Qval[state], epsilon)

            previous_state = state
            new_Qval = Qval.copy()

            state, reward, done, _ = env.step(action)
            [cos_theta1, sin_theta1, cos_theta2, sin_theta2, thetaDot1, thetaDot2] = state
            state = env_state_to_Q_state(state)

            new_Qval[previous_state][action] = w_cos1*cos_theta1 + w_sin1*sin_theta1 + w_cos2*cos_theta2 + w_sin2*sin_theta2 + w_theta1*thetaDot1 + w_theta2*thetaDot2
            new_Qval[previous_state][action] = w_cos1*cos_theta1_difference(-sin_theta1) + w_sin1*sin_theta1 + w_cos2*cos_theta2 + w_sin2*sin_theta2 + w_theta1*thetaDot1 + w_theta2*thetaDot2
            sample = reward + gama * max(Qval[state][-1], Qval[state][0], Qval[state][1])
            difference = sample - new_Qval[previous_state][action]
            w_cos1 = w_cos1 + alpha*difference*cos_theta1
            w_cos2 = w_cos2 + alpha*difference*cos_theta2
            w_sin1 = w_sin1 + alpha*difference*sin_theta1
            w_sin2 = w_sin2 + alpha*difference*sin_theta2
            w_theta1 = w_theta1 + alpha*difference*thetaDot1
            w_theta2 = w_theta2 + alpha*difference*thetaDot2

            Qval = new_Qval

            # env.render()
        if counter % 1000 == 0:
            print("progress: " + str(counter / 100))
            epsilon *= 0.975
            print(epsilon)
        # if convergence:
        #     break
        if counter > 10000:  # for exiting and not running infinitely
            break
    Policy = [0] * num_states

    for i in range(num_states):
        if Qval[i][0] >= Qval[i][1] and Qval[i][0] >= Qval[i][-1]:
            Policy[i] = 0
        elif Qval[i][1] >= Qval[i][0] and Qval[i][1] >= Qval[i][-1]:
            Policy[i] = 1
        elif Qval[i][-1] >= Qval[i][0] and Qval[i][-1] >= Qval[i][1]:
            Policy[i] = -1

    print("Policy : ", Policy)
    np.save('approximate_q_saved', Policy)


def Play_featured():
    scores = []
    Policy = np.load('approximate_q_saved.npy')
    print("Policy : ", Policy)

    for episode_count in range(100):
        episode_count += 1
        print('******Episode ', episode_count)
        state = env_state_to_Q_state(env.reset())

        score = 0
        done = False
        step_count = 0
        while (not done) and step_count < max_episode_steps:
            # time.sleep(0.04)
            action = Policy[state]
            state, reward, done, _ = env.step(action)
            state = env_state_to_Q_state(state)
            step_count += 1
            score += int(reward)
            # env.render()  # render current state of environment

        print('Score:', score)
        scores.append(score)

    print("Average score over 1000 run : ", np.array(scores).mean())


def Play():
    scores = []
    Policy = np.load('q_saved.npy')
    print("Policy : ", Policy)

    for episode_count in range(1000):
        episode_count += 1
        print('******Episode ', episode_count)
        state = env_state_to_Q_state(env.reset())

        score = 0
        done = False
        step_count = 0
        while (not done) and step_count < max_episode_steps:
            time.sleep(0.04)
            action = Policy[state]
            state, reward, done, _ = env.step(action)
            state = env_state_to_Q_state(state)
            step_count += 1
            score += int(reward)
            env.render()  # render current state of environment

        print('Score:', score)
        scores.append(score)

    print("Average score over 1000 run : ", np.array(scores).mean())


# better hyper parameters:
# alpha = 0.12
# gamma = 0.99

if __name__ == '__main__':
    # Train()
    Play()
