f = open("./log/simul-power.txt", 'r')
cnt = 0
sums = [0, 0, 0, 0]
while True:
    line = f.readline()
    if not line:
        break
    print(line)

    words = line.split()
    for i in range(4):
        sums[i] += float(words[i])

    cnt += 1

f.close()

print("\n*** print results ***")
print("average e value:", sums[0] / cnt)
print("average PQV vs equal similarity:", sums[1] / cnt, "%")
print("average PQV vs linear similarity:", sums[2] / cnt, "%")
print("average PQV vs QV similarity:", sums[3] / cnt, "%")
