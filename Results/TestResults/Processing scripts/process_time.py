import os
import matplotlib.pyplot as plt

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

folder_path= 'Results\\TestResults\\MCTSTimeTests'

data = {}
p1_avg = []
p2_avg = []
wins = []
        

for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.isfile(file_path):
            print(f"Reading file: {file_name}")

            # year, time, depth = file_name.replace('.txt', '').split('_')
            # depth = int(depth)
            # data[depth] = {}

            # print(c_value)
            # Open and read the file
            with open(file_path, 'r') as file:
                text = file.read()
            lines = text.split('\n')
            for line in lines:
                if line != '' and 'ED' not in line:
                    print(line)
                    meta, time = line.split(':')
                    depth, _ = meta.split('_')
                    depth = int(depth)
                    time = float(time)
                    if depth in data.keys():
                        data[depth]['arr'].append(time)
                    else:
                        data[depth] = {}
                        data[depth]['arr'] = []
                        data[depth]['arr'].append(time)
            # data[depth]['p1'] = sum(p1_scores)/len(p1_scores)
            # data[depth]['p2'] = sum(p2_scores)/len(p2_scores)
            # data[depth]['w'] = p1_wins
            # data[depth]['l'] = 100 - p1_wins

# with open(file_path, 'r') as file:
#     text = file.read()
# lines = text.split('\n')
# for line in lines:
#     if line != '' and 'ED' in line:
#         print(line)
#         meta, time = line.split(':')
#         _, depth, _ = meta.split('_')
#         depth = int(depth)
#         time = float(time)
#         if depth in data.keys():
#             data[depth]['arr'].append(time)
#         else:
#             data[depth] = {}
#             data[depth]['arr'] = []
#             data[depth]['arr'].append(time)

for key in data.keys():
    data[key]['avg'] = sum(data[key]['arr'])/len(data[key]['arr'])
print(data)


sorted_keys = sorted(data.keys())
#wins and losses
values = [data[key]['avg'] for key in sorted_keys]
plt.plot(sorted_keys, values, label='MCTS Žaidėjo simuliacijos laikas')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('Vaikinių mazgų kiekis vienai simuliacijai')
plt.ylabel('Simuliacijos laikas sekundėmis')
# plt.title('Score vs Iterations')
plt.legend()
x = sorted_keys
# y = [i/10 for i in range(0, 11, 1)]
plt.xticks(x)
# plt.yticks(y)
# for i, txt in enumerate(values):
#     plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
plt.savefig('Results\\time_on_move.png')

