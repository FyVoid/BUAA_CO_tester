filename = "code.txt"
fp = open(filename, "r+")
out = open("out.txt", "w")
fp.readline()
for line in fp:
    num = bin(int(line, 16))
    num = num[2:]
    while len(num) < 32:
        num = "0" + num
    out.write("{}\n".format(num))