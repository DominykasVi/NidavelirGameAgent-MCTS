# import itertools
# import math


# possible_combs = [i for i in itertools.permutations([0, 2, 3, 4, 5], 3)]

# print(possible_combs)
# print(len(possible_combs))

# score = 398
# iterations = 3
# constant = 2
# total_runs = 81
# # print((score/iterations) + constant * math.sqrt(math.log(total_runs)/iterations))
# # Example dictionaries
# dict1 = {'a': 1, 'b': 2, 'c': 3}
# dict2 = {'b': 4, 'c': 5, 'd': 6}

# # Find keys in dict1 but not in dict2
# unique_to_dict1 = set(dict1.keys()) - set(dict2.keys())

# print(unique_to_dict1)

# Read from file
import matplotlib.pyplot as plt
import numpy as np

# Example data
with open('100_50_MCTS.txt', 'r') as file:
    results = [tuple(map(int, line.strip().split(' '))) for line in file]

# print(tuples_list_read)
# Number of players and games
mcts_wins = 0
for game in results:
    if game[0] > game[1]:
        mcts_wins += 1

print(f"MCTS agent won {mcts_wins} times")
num_games = len(results)
num_players = len(results[0])

# Generate game numbers
game_numbers = np.arange(1, num_games + 1)



# Plotting
plt.figure(figsize=(10, 6))
for i in range(num_players):
    # Extract scores for each player across all games
    player_scores = [game[i] for game in results]
    # Plotting each player's scores
    plt.bar(game_numbers - 0.2 + i*0.4/num_players, player_scores, width=0.4/num_players, label=f'Player {i+1}')

plt.xlabel('Game Number')
plt.ylabel('Score')
plt.title('Scores of Players in Each Game')
plt.xticks(game_numbers)
plt.legend()
plt.savefig('100_50_MCTS.png')
plt.close()

print("Plot saved to '100_200_MCTS.png'")


