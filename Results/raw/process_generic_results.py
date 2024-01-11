with open(r'Results\raw\WL_res_2\20240108_162419_1.5_200.txt', 'r') as f:
    text = f.read()

lines= text.split('\n')
p1_res = []
p2_res = []
wins = 0
for line in lines:
    if line != '':
        p1, p2 = line.split(' ')
        p1 = int(p1)
        p2 = int(p2)
        if p1 > p2:
            wins += 1
        p1_res.append(p1)
        p2_res.append(p2)
p1_avg = sum(p1_res)/len(p1_res)
p2_avg = sum(p2_res)/len(p2_res)

print("Player 1 avg: ", p1_avg)
print("Player 2 avg: ", p2_avg)
print("Player 1 wins: ", wins)
