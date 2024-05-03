import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# plt.style.use('seaborn')

with open(r'Logs\TestResults\sa_c_iter\optimization.txt', 'r') as f:
    text  = f.read()

text = text.split('RUN')[1]
text = '\n'.join([var for idx, var in enumerate(text.split('\n')) if idx != 0])
sims = text.split('#---#\n')
parameters = [game.split('\n')[0] for game in sims if game != '']

fitnesses = [float(s.split('-')[0]) for s in parameters]

max_val = fitnesses.index(max(fitnesses))
print(f'Best fitness {parameters[max_val]}')
#general figure options
fig = plt.figure(figsize=(15, 7))
ax = plt.axes(xlim=(0, len(fitnesses)), ylim=(np.min(fitnesses)-1,np.max(fitnesses)+1))
line, = ax.plot([], [], lw=2)
ax.set_title('SA results', fontsize=18)
ax.set_xlabel('Epochs', fontsize=16)
ax.set_ylabel('Fitness', fontsize=16)
ax.tick_params(labelsize=12)

epochs = [i for i in range(len(fitnesses))]

plt.plot(epochs, fitnesses)


plt.show()