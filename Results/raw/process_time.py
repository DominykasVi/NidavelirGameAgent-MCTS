import os
import matplotlib.pyplot as plt

def addlabels(x,y):
    for i in range(len(x)):
        plt.text(i, y[i], y[i], ha = 'center')

file_path= 'Results\\raw\\Iterations_runs\\iterations_runs_1.txt'

data = {}
p1_avg = []
p2_avg = []
wins = []
        

print(f"Reading file: {file_path}")

with open(file_path, 'r') as file:
    text = file.read()
lines = text.split('\n')
for line in lines:
    if line != '' and 'ED' in line:
        print(line)
        meta, time = line.split(':')
        _, depth, _ = meta.split('_')
        depth = int(depth)
        time = float(time)
        if depth in data.keys():
            data[depth]['arr'].append(time)
        else:
            data[depth] = {}
            data[depth]['arr'] = []
            data[depth]['arr'].append(time)

for key in data.keys():
    data[key]['avg'] = sum(data[key]['arr'])/len(data[key]['arr'])
print(data)


sorted_keys = sorted(data.keys())
#wins and losses
values = [data[key]['avg'] for key in sorted_keys]
plt.plot(sorted_keys, values, label='MCTS Žaidėjo rezultatai')
# plt.plot(c_values, wins, label='Wins')
plt.xlabel('Iteracijų kiekis vienai simuliacijai')
plt.ylabel('Simuliacijos laikas')
# plt.title('Score vs Iterations')
plt.legend()
x = sorted_keys
y = [i/10 for i in range(0, 11, 1)]
plt.xticks(x)
plt.yticks(y)
for i, txt in enumerate(values):
    plt.annotate(txt, (x[i], y[i]), textcoords="offset points", xytext=(0,10), ha='center')
plt.savefig('Results\\time_on_move.png')

