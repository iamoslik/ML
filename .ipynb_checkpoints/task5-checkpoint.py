def primes():
    x = 2
    while 1:
        for i in range(2, x // 2 + 1):
            if x % i == 0:
                break
        else:
            yield x
        x += 1
