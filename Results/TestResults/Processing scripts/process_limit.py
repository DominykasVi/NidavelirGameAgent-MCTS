import os
import matplotlib.pyplot as plt

folder_path= 'Results\\TestResults\\LimitTests'

data = {}
p1_avg = []
p2_avg = []
wins = []
for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")
            _, _, limit = file_name.replace('.txt', '').split('_')

            limit = int(limit)
            data[limit] = {}
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
            data[limit]['p1'] = sum(p1_scores)/len(p1_scores)
            data[limit]['p2'] = sum(p2_scores)/len(p2_scores)
            data[limit]['w'] = p1_wins
            data[limit]['l'] = 100 - p1_wins
print(data)


sorted_keys = sorted(data.keys())
# sorted_keys = [i for i in sorted_keys if i < 21]
#wins and losses
p1_values = [data[key]['p1'] for key in sorted_keys]
p2_values = [data[key]['p2'] for key in sorted_keys]
plt.plot(sorted_keys, p1_values, label='MCTSLM Žaidėjo rezultatai')
plt.plot(sorted_keys, p2_values, label='Atsitiktinio Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('Vieno mazgo vaikinių mazgų limitas')
plt.ylabel('Žaidėjo surinkti taškai')
# plt.title('Score vs Iterations')
plt.legend()
plt.xticks(sorted_keys)
plt.savefig('Results\\limit_points.png')
plt.clf()

p1_values = [data[key]['w'] for key in sorted_keys]
p2_values = [data[key]['l'] for key in sorted_keys]
plt.plot(sorted_keys, p1_values, label='MCTSLM Žaidėjo rezultatai')
plt.plot(sorted_keys, p2_values, label='Atsitiktinio Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('Vieno mazgo vaikinių mazgų limitas')
plt.ylabel('Laimėtų žaidimų procentas')
# plt.title('Score vs Iterations')
plt.legend()
plt.xticks(sorted_keys)
plt.savefig('Results\\limit_wins.png')


