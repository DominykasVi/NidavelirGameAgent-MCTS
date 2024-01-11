import os
import matplotlib.pyplot as plt

folder_path= 'Results\\raw\\C_optimization'

c_values = {}
p1_avg = []
p2_avg = []
wins = []
for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")
            if 'ts' in file_name:
                _, c_value, depth = file_name.replace('.txt', '').split('_')
            else:
                year, time, c_value, depth = file_name.replace('.txt', '').split('_')
            try:
                dec, num = c_value.split('.')
            except:
                dec = c_value
                num = 0
            c_value = int(dec) + int(num)/10
            c_values[c_value] = {}
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
            c_values[c_value]['p1'] = sum(p1_scores)/len(p1_scores)
            c_values[c_value]['p2'] = sum(p2_scores)/len(p2_scores)
            c_values[c_value]['w'] = p1_wins
            c_values[c_value]['l'] = 100 - p1_wins
print(c_values)


sorted_keys = sorted(c_values.keys())
p1_values = [c_values[key]['w'] for key in sorted_keys]
p2_values = [c_values[key]['l'] for key in sorted_keys]

plt.plot(sorted_keys, p1_values, label='MCTS Žaidėjo rezultatai')
plt.plot(sorted_keys, p2_values, label='Atsitiktinio Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')


plt.xlabel('Laimėtų žaidimų procentas')
plt.ylabel('Žaidėjo surinkti taškai')
# plt.title('Score vs Iterations')
plt.legend()

plt.xticks(sorted_keys)
plt.savefig('Results\\c_values_graphs_10.png')
plt.show()


