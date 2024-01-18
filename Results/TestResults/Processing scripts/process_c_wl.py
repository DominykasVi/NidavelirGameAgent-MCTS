import os
import matplotlib.pyplot as plt

folder_path= 'Results\\TestResults\\CValueTestWL'

data = {}
p1_avg = []
p2_avg = []
wins = []
for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")
            _, _, c_value = file_name.replace('.txt', '').split('_')

            c_value = float(c_value)
            data[c_value] = {}
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
            data[c_value]['p1'] = sum(p1_scores)/len(p1_scores)
            data[c_value]['p2'] = sum(p2_scores)/len(p2_scores)
            data[c_value]['w'] = p1_wins
            data[c_value]['l'] = 100 - p1_wins
print(data)


sorted_keys = sorted(data.keys())
# sorted_keys = [i for i in sorted_keys if (i%10 ==0 or i==1)]
#wins and losses
p1_values = [data[key]['p1'] for key in sorted_keys]
p2_values = [data[key]['p2'] for key in sorted_keys]
plt.plot(sorted_keys, p1_values, label='MCTSWL Žaidėjo rezultatai')
plt.plot(sorted_keys, p2_values, label='Atsitiktinio Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('C reikšmė')
plt.ylabel('Žaidėjo surinkti taškai')
# plt.title('Score vs Iterations')
plt.legend()
plt.xticks(sorted_keys)
plt.savefig('Results\\c_values_wl_points_0_2.png')
plt.clf()

p1_values = [data[key]['w'] for key in sorted_keys]
p2_values = [data[key]['l'] for key in sorted_keys]
plt.plot(sorted_keys, p1_values, label='MCTSWL Žaidėjo rezultatai')
plt.plot(sorted_keys, p2_values, label='Atsitiktinio Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('C reikšmė')
plt.ylabel('Laimėtų žaidimų procentas')
# plt.title('Score vs Iterations')
plt.legend()
plt.xticks(sorted_keys)
plt.savefig('Results\\c_values_wl_wins_0_2.png')


