import itertools as its

words = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()-_=+[{]};:'\",<.>/?\\|"
r = its.product(words, repeat=10)
dic = open("pwd.txt", "a")

for i in r:
    dic.write("".join(i))
    dic.write("\n")

dic.close()
