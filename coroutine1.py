

# 코루틴: 루틴 실행 중 멈춤 가능 -> 특정 위치로 돌아갔다가 -> 다시 원래 위치로 돌아와 수행 가능 -> 동시성 : 코루틴 스케쥴링 오버헤드 매우 적다. 
# 싱글 스레드로 돌아간다. 가독성이 좋지 않다.
# 쓰레드: 싱글 쓰레드 -> 멀티 쓰레드 -> 복잡 -> 공유되는 자원 -> 교착 상태 발생 가능성, 컨텍스트 스위칭 비용이 든다.

def coroutine1():
    print("co started")
    i = yield
    print("co received :{}".format(i))


# c1 = coroutine1()
# next(c1)
# c1.send(6)

# 코루틴 예제2

# GEN_CREATED: 처음 대기 상태
# GEN_RUNNING: 실행 상태
# GEN_SUSPENDED: yield 대기 상태
# GEN_CLOSED: 실행 완료 상태


def co2(x):
    print('>>> co started : {}'.format(x))
    y = yield x
    print('>>> co received : {}'.format(y))
    z = yield x + y
    print('>>> co received : {}'.format(z))


# c2 = co2(10)

from inspect import getgeneratorstate # 상태 값 확인 가능

# print('EX1-2 -', getgeneratorstate(c2)) # 대기 상태
# print(next(c2))
# print('EX1-2 -', getgeneratorstate(c2)) # yield 대기 상태
# print(c2.send(15))
# print(c2.send(20))

# 데코레이터 패턴

from functools import wraps

def co3(func):
    ''' Decorator run until yield'''
    @wraps(func) # 없어도 동작한다.
    def primer(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return primer

@co3
def sumer():
    total = 0
    term = 0
    while True:
        term = yield total
        total += term


su = sumer()

# print(su.send(100))
# print(su.send(40))
# print(su.send(200))

class SampleException(Exception):
        '''설명에 사용할 예외 유형'''

def coroutine_except():
        print("started")
        try:
                while True:
                        try:
                                x = yield
                        except SampleException:
                                print('-> SampleException Handled Continuing..')
                        else:
                                print('-> coroutine received : {}'.format(x))
        finally:
                print('-> coroutine ending')


exe_co = coroutine_except()

# print(next(exe_co))
# print(exe_co.send(10))
# print(exe_co.send(100))
# print(exe_co.throw(SampleException))
# print(exe_co.close())



def averager_re():
        total = 0.0
        cnt = 0
        avg = None
        while True:
                term = yield
                if term is None:
                        break
                total += term
                cnt +=1
                avg = total / cnt
        return 'Agerage : {}'.format(avg)


avger2 = averager_re()
next(avger2)

avger2.send(10)
avger2.send(30)
avger2.send(50)



try:
        avger2.send(None)
except StopIteration as e:
        print(e.value)


        
