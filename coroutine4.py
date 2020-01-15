# StopIteration 자동 처리 yield from (3.7 -> await) 
# 중첩 코루틴 처리



def gen1():
    for x in 'AB':
        yield x # A -> B -> 1 -> 2 -> 3 
    for y in range(1,4):
        yield y

t1 = gen1()

# print(next(t1))
# print(next(t1))
# print(next(t1))
# print(next(t1))
# print(next(t1))
# print(next(t1))
t2 = gen1()

print(list(t2)) # ['A','B',1,2,3]


# gen1을 yield from 으로 만든 gen2
def gen2():
    yield from 'AB'
    yield from range(1,4)

t3 = gen2()

print(next(t3))
print(next(t3))
print(next(t3))
print(next(t3))
print(next(t3))

# print(next(t3))


t4 = gen2()
print(list(t4))


def gen3_sub():
    print('sub coroutine')
    x = yield 10
    print('recv:',str(x))
    x = yield 100
    print('recv:',str(x))

def gen4_main():
    yield from gen3_sub()



t5 = gen4_main()

print(next(t5))
print(t5.send(7))
print(t5.send(77))