import os
import matplotlib.pyplot as plt

folder_path= 'Depth\Results'

depths = {}
p1_avg = []
p2_avg = []
wins = []
for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")
            num = file_name.replace('.txt', '')
            # depth = int(num)
            depths[int(num)] = {}
            # print(c_value)
            # Open and read the file
            with open(file_path, 'r') as file:
                text = file.read()
            numbers = text.split('\n')
            p1_scores = []
            p2_scores = []
            p1_wins = 0
            for pair in numbers:
                if pair != '':
                    p1, p2 = pair.split(' ')
                    p1_scores.append(int(p1))
                    p2_scores.append(int(p2))
                    if int(p1) > int(p2):
                        p1_wins += 1
            depths[int(num)]['p1'] = sum(p1_scores)/len(p1_scores)
            depths[int(num)]['p2'] = sum(p2_scores)/len(p2_scores)
            depths[int(num)]['w'] = p1_wins

print(depths)


sorted_keys = sorted(depths.keys())
p1_values = [depths[key]['p1'] for key in sorted_keys]
p2_values = [depths[key]['p2'] for key in sorted_keys]

# plt.plot(sorted_keys, p1_values, label='MCTS Player Average')
# plt.plot(sorted_keys, p2_values, label='Random Player Average')
# # plt.plot(c_values, wins, label='Wins')


# plt.xlabel('Iteration count')
# plt.ylabel('Score')
# plt.title('Score vs Iterations')
# plt.legend()

# plt.xticks(sorted_keys)
# plt.savefig('Depth\\value_graph.png')
# plt.show()

