with open('tests.py', 'r') as f:
    text = f.read()

lines = text.split('\n')
for line in lines:
    if 'def' in line:
        print(line.replace('dev ', ''))