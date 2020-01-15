


# 코루틴 예제3(예외처리)

class SampleException(Exception):
    '''
    설명에 사용할 예외 유형
    '''


def coroutine_except():
    print('>> coroutine started.')
    try:
        while True:
            try:
                x = yield
            except SampleException:
                print('-> SampleException Handled. continueing')
            else:
                print('-> coroutine received : {}'.format(x))
    finally:
        print("-> coroutine ending")

exe_co = coroutine_except()

print(next(exe_co))
print(exe_co.send(50))
print(exe_co.send(100))
print(exe_co.throw(SampleException))