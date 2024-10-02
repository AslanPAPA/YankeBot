# put your python code here

n = int(input())
res = 1

while n > 99:
    res *= n // 100
    res *= n // 10 % 10
    res *= n % 10
    break

print(res)





