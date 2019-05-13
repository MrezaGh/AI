import gym
import pickle
import time


def decode(i):
    #  (taxi_row, taxi_col, passenger_location, destination)
    out = [i % 4]

    i = i // 4
    out.append(i % 5)
    i = i // 5
    out.append(i % 5)
    i = i // 5
    out.append(i)
    assert 0 <= i < 5
    return list(reversed(out))


def calculate_execution_time(f):
    def timer(*args):
        start = time.time()
        f(*args)
        end = time.time()
        time_execution_took = end - start
        return time_execution_took
    return timer


@calculate_execution_time
def value_iteration(P, gamma, num_of_actions, num_of_states, delta):
    print("finding and optimal policy for 'Taxi-v2' using 'Value_Iteration'")
    print("gamma: {gamma} \nnumber of states: {states}".format(gamma=gamma, states=num_of_states))
    print("number of actions: {actions}\ndelta: {delta}".format(actions=num_of_actions, delta=delta))

    Q_value = {state: {action: 0 for action in range(num_of_actions)} for state in range(num_of_states)}
    V_value = [0 for i in range(num_of_states)]
    iterations_passed = 0

    # if convergence does not happen after 1000 iterations we leave it and return current best policy
    for i in range(1000):  # calculating Q_value and V_value for all states and actions
        new_V_value = [0 for _ in range(num_of_states)]
        for state in range(num_of_states):
            max_Q = float('-inf')
            for action in range(num_of_actions):
                p, s_prime, reward, done = P[state][action][0]

                Q_value[state][action] = p * (reward + gamma * V_value[s_prime])
                max_Q = max(max_Q, Q_value[state][action])
            new_V_value[state] = max_Q
        iterations_passed += 1
        difference = [abs(couple[0]-couple[1]) for couple in zip(new_V_value, V_value)]
        if max(difference) < delta:  # convergence happened
            V_value = new_V_value.copy()
            break

        V_value = new_V_value.copy()

    policy = [0 for _ in range(num_of_states)]

    # calculating arg max
    for state in range(num_of_states):
        best_action = 0
        max_Q = float('-inf')
        for action in range(num_of_actions):
            if Q_value[state][action] > max_Q:
                max_Q = Q_value[state][action]
                best_action = action
        policy[state] = best_action

    file = open('./value_iteration_policy.pkl', mode='wb')
    pickle.dump(policy, file)

    print("Convergence happened after '{}' iterations".format(iterations_passed))
    # print("value of states: ")
    # print(V_value)
    print("policy: ")
    print(policy)
    print("==================")

    return V_value, policy


@calculate_execution_time
def policy_iteration(P, gamma, num_of_actions, num_of_states, delta):
    print("finding and optimal policy for 'Taxi-v2' using 'Policy_Iteration'")
    print("gamma: {gamma} \nnumber of states: {states}".format(gamma=gamma, states=num_of_states))
    print("number of actions: {actions}\ndelta: {delta}".format(actions=num_of_actions, delta=delta))

    policy = [0 for i in range(num_of_states)]
    V_value = [0 for i in range(num_of_states)]

    iterations_passed = 0
    new_policy = [0 for _ in range(num_of_states)]
    # if convergence does not happen after 1000 iterations we leave it and return current best policy
    for i in range(1000):  # calculating V_value for fixed policy and improving policy
        for j in range(1000):  # policy evaluation
            new_V_value = [0 for _ in range(num_of_states)]
            for state in range(num_of_states):
                action = policy[state]
                p, s_prime, reward, done = P[state][action][0]
                new_V_value[state] = p * (reward + gamma * V_value[s_prime])
            difference = [abs(couple[0] - couple[1]) for couple in zip(new_V_value, V_value)]
            if max(difference) < delta:  # convergence happened
                V_value = new_V_value.copy()
                # print("inner iteration:" + str(j))
                break

            V_value = new_V_value.copy()

        for state in range(num_of_states):  # policy improvement
            best_action = 0
            best_action_value = float('-inf')
            for action in range(num_of_actions):
                p, s_prime, reward, done = P[state][action][0]
                action_value = p * (reward + gamma*V_value[s_prime])
                if action_value > best_action_value:
                    best_action_value = action_value
                    best_action = action
            new_policy[state] = best_action

        iterations_passed += 1

        if new_policy == policy:  # convergence happened
            break

        policy = new_policy.copy()

    file = open('./policy_iteration_policy.pkl', mode='wb')
    pickle.dump(policy, file)
    print("Convergence happened after '{}' iterations".format(iterations_passed))
    # print("value of states: ")
    # print(V_value)
    print("policy: ")
    print(policy)
    print("==================")

    return V_value, policy


def main():
    """
    Welcome Mreza here
    This is 'Taxi-v2' game that I've solved it with 'Value-Iteration' and 'Policy-Iteration' methods.
    keep calm and enjoy the wonders of science
    some more info:
        -number of states: 500
        -number of actions: 6 (i.e 0: south, 1: north, 2: east, 3: west, 4: pickup, 5: dropoff)
        -gamma: 0.99 (or 1 for comparing with 0.99 and learn more)
        -delta: 0.001
    """

    env = gym.make("Taxi-v2")
    num_of_actions = env.action_space.n  # number of actions(i.e 6)
    num_of_states = env.observation_space.n  # number of states(i.e 500)
    gamma = 0.99  # gamma is used for discounted utility
    # gamma = 1
    delta = 0.01  # delta is used to distinguish convergence
    P = env.env.P  # P[state][action] = array of (probability, next_state, reward, done)

    print("Hi, Mreza says \'Hello\'... \t lets go!")
    print("==================")

    value_iter_exec_time = value_iteration(P, gamma, num_of_actions, num_of_states, delta)
    policy_iter_exec_time = policy_iteration(P, gamma, num_of_actions, num_of_states, delta)

    print("value_iteration took '{0:.2f}'ms to execute".format(value_iter_exec_time*1000))
    print("policy_iteration took '{0:.2f}'ms to execute".format(policy_iter_exec_time*1000))


if __name__ == '__main__':
    main()
