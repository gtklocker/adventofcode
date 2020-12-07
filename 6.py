import fileinput

lines = [line.strip() for line in fileinput.input()]
questions = [None]
for line in lines:
    if line == '':
        questions.append(None)
        continue
    if questions[-1] is None:
        questions[-1] = set(line)
    else:
        questions[-1] &= set(line)

print(sum(len(qs) for qs in questions))
