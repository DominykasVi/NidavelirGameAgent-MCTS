with open('Depth\\100.txt', 'r') as f:
    text = f.read()

lines = text.split('\n')
wins = 0
p1_l = []
p2_l = []
for game in lines:
    if game == '':
        continue
    p1, p2 = game.split(' ')
    if int(p1) > int(p2):
        wins += 1
    p1_l.append(int(p1))
    p2_l.append(int(p2))

print(wins)
print(sum(p1_l)/len(p1_l))
print(sum(p2_l)/len(p2_l))  
