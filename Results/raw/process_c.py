import os
import matplotlib.pyplot as plt

folder_path= 'C_value\Results'

c_values = []
p1_avg = []
p2_avg = []
wins = []
for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")
            num, dec = file_name.replace('.txt', '').split('_')
            c_value = int(num) + int(dec)/10
            c_values.append(c_value)
            # print(c_value)
            # Open and read the file
            with open(file_path, 'r') as file:
                text = file.read()
            numbers = text.split('\n')
            p1_scores = []
            p2_scores = []
            p1_wins = 0
            for pair in numbers:
                p1, p2 = pair.split(' ')
                p1_scores.append(int(p1))
                p2_scores.append(int(p2))
                if int(p1) > int(p2):
                    p1_wins += 1
            p1_avg.append(sum(p1_scores)/len(p1_scores))
            p2_avg.append(sum(p2_scores)/len(p2_scores))
            wins.append(p1_wins)

print(c_values)
print(p1_avg)
print(p2_avg)
print(wins)

# plt.plot(c_values, p1_avg, label='MCTS Player Average')
# plt.plot(c_values, p2_avg, label='Random Player Average')
plt.plot(c_values, wins, label='Wins')


plt.xlabel('C Value')
plt.ylabel('Score')
plt.title('Score vs C Value')
plt.legend()

plt.xticks(c_values)
plt.savefig('C_value\c_value_graph.png')
plt.show()

