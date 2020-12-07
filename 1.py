import fileinput

xs = [int(x.strip()) for x in fileinput.input()]
for i in range(len(xs)):
    for j in range(i+1, len(xs)):
        for k in range(j+1, len(xs)):
            z = xs[i]+xs[j]+xs[k]
            if z == 2020:
                print(xs[i]*xs[j]*xs[k])
                break
