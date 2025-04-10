import re
import sys
import numpy as np

ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']
ACTION_DELTA = {
    'UP': (0, 1),
    'DOWN': (0, -1),
    'LEFT': (-1, 0),
    'RIGHT': (1, 0)
}
TRANSITION_PROBABILITIES = {
    'UP': [('UP', 0.8), ('LEFT', 0.1), ('RIGHT', 0.1)],
    'DOWN': [('DOWN', 0.8), ('RIGHT', 0.1), ('LEFT', 0.1)],
    'LEFT': [('LEFT', 0.8), ('DOWN', 0.1), ('UP', 0.1)],
    'RIGHT': [('RIGHT', 0.8), ('UP', 0.1), ('DOWN', 0.1)]
}

def parse_input_file(file_path):
    path = "../txt/" + file_path
    with open(path, 'r') as f:
        content = f.read()
    dim = tuple(map(int, re.search(r'<dim>\n(\d+)\s+(\d+)', content).groups()))
    walls = re.findall(r'<walls>\n((?:\(\d+,\d+\)\n?)*)', content)
    walls = set(eval(w) for w in walls[0].split()) if walls else set()
    rewards = re.findall(r'<rewards>\n((?:\(\d+,\d+\)\s-?\d+\n?)*)', content)
    rewards_dict = {}
    if rewards:
        for line in rewards[0].strip().split('\n'):
            m = re.match(r'\((\d+),(\d+)\)\s(-?\d+)', line)
            if m:
                x, y, r = int(m[1]), int(m[2]), int(m[3])
                rewards_dict[(x, y)] = r
    return dim, walls, rewards_dict

def get_next_state(state, action, dim, walls):
    x, y = state
    dx, dy = ACTION_DELTA[action]
    nx, ny = x + dx, y + dy
    if (nx, ny) in walls or not (0 <= nx < dim[0] and 0 <= ny < dim[1]):
        return (x, y)
    return (nx, ny)

def print_board(V, dim, walls, iteration):
    print(f"\nIteration {iteration}")
    for y in reversed(range(dim[1])):  # Print top to bottom
        row = ""
        for x in range(dim[0]):
            if (x, y) in walls:
                row += "#####\t"
            else:
                val = V.get((x, y), 0.0)
                row += f"{val:5.2f}\t"
        print(row)
    print()

def value_iteration(dim, walls, rewards, discount_factor, threshold, living_reward):
    states = [(x, y) for x in range(dim[0]) for y in range(dim[1]) if (x, y) not in walls]
    V = {s: 0 for s in states}
    
    for r in rewards:
        V[r] = rewards[r]
    
    raise NotImplementedError
    '''
    TODO: Implement value iteration here.
    '''

    return V

def extract_policy(V, dim, walls, rewards):
    policy = {}
    for s in V:
        if s in rewards or s in walls:
            continue
        best_a = None
        best_val = float('-inf')
        for a in ACTIONS:
            ns = get_next_state(s, a, dim, walls)
            val = V[ns]
            if val > best_val:
                best_val = val
                best_a = a
        policy[s] = best_a
    return policy

def get_path(policy, start, rewards):
    path = []
    state = start
    while state not in rewards:
        a = policy.get(state)
        if not a:
            break
        path.append(a)
        state = get_next_state(state, a, dim, walls)
    return path

if __name__ == "__main__":
    # file_path = 'test-board-1.txt'
    # gamma = 0.9
    # theta = 0.05
    # living_reward=-0.1
    # start_x = 0
    # start_y = 0

    file_path = input("Enter environment filename (e.g., test-board-1.txt): ")
    discount_factor = float(input("Enter discount factor γ (e.g., 0.9): "))
    threshold = float(input("Enter convergence threshold θ (e.g., 0.05): "))
    living_reward = float(input("Enter living reward λ (e.g., -0.1): "))
    start_x = int(input("Enter start x: "))
    start_y = int(input("Enter start y: "))

    dim, walls, rewards = parse_input_file(file_path)
    V = value_iteration(dim, walls, rewards, discount_factor, threshold, living_reward)
    policy = extract_policy(V, dim, walls, rewards)
    path = get_path(policy, (start_x, start_y), rewards)
    print("Optimal path:", " -> ".join(path))
