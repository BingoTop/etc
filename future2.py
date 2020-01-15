

# Future 동시성
# 비동기 작업 실행
# 적합한 작업일 경우 순차 진행보다 압도적으로 성능 향상
# 지연시간(block) cpu 및 리소스 낭비 방지 -> NetWork I/O 관련 작업 동시성 활용 권장


# Google Python GIL(Global Interpreter Lock)
# GIL은 한 번에 하나의 스레드만 수행할 수 있게 인터프리터 자체에서 락을 거는 것.
import os
import time
import sys
import csv
from concurrent import futures
# concurrent.future1(ThreadPoolExecutor,ProcessPoolExcutor)
# map()
# 서로 다른 스레드 또는 프로세스에서 실행 가능
# 내부 과정 알 필요 없으며, 고수준으로 인터페이스 제공

# 국가정보
NATION_LS = ('Singapore Germany Israel Norway Italy Canada France Spain Mexico').split()
# 초기 csv 위치
TARGET_CSV = '/home/jaewon/바탕화면/Python_Advanced/resources/nations.csv'
# 저장 폴더 위치
DEST_DIR = "/home/jaewon/바탕화면/Python_Advanced/csvs"
# 기초 헤더 정보
HEADER = ['Region','Country',	'Item Type',	'Sales Channel',	'Order Priority',	'Order Date',	'Order ID',	'Ship Date',	'Units Sold',	'Unit Price',	'Unit Cost',	'Total Revenue'	,'Total Cost',	'Total Profit']

# 국가별 CSV 파일 저장
def save_csv(data,filename):

    # if not os.path.isdir(path):
    #     os.mkdir(path)

    # 최종 경로 생성
    path = os.path.join(DEST_DIR,filename)


    with open(path,'w',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=HEADER)
        # Header Write
        writer.writeheader()
        # Dict to CSV Write
        for row in data:
            writer.writerow(row)
    


# 국가별 분리
def get_sales_data(nt):
    with open(TARGET_CSV,'r') as f:
        reader = csv.DictReader(f)
        # Dict을 리스트로 적재
        data = []
        # Header 확인
        # print(reader.fieldnames)
        for r in reader:
            # OrderedDict 확인

            # print(r)
            # 조건에 맞는 국가만 삽입
            if r['Country'] == nt:
                data.append(r)
    return data
# 중간 상황 출력
def show(text):
    print(text,end=' ')
    # 중간 출력(버퍼 비우기)
    sys.stdout.flush()

# 국가별 분리 함수 실행
def separate_many(nt):
        # 분리 데이터
    data = get_sales_data(nt)
    # 상황을 출력
    show(nt)
    # 파일 저장
    save_csv(data,nt.lower()+ '.csv')

    return nt

# 시간 측정 및 메인 함수
def main(separate_many):

    # worker 개수
    worker = min(20,len(NATION_LS)) # 9개 또는 20개 중에 작은 것 => 9
    # 시작 시간
    start_tm = time.time()
    # 결과 건수
    # ProcessPoolExecutor: GIL 우회, 변경 후-> os.cpu_count() 빠르다.. 6초 밖에 안 걸린다.
    # ThreadPoolExecutor 돌렸는데 80초 나올 수도 있고 대체적으로 느리다 IO 공통적으로 작업이 일어나기 떄문에 컨텍스트 스위칭 발생
    with futures.ProcessPoolExecutor() as excutor:
        # Submit -> Callable 객체 스케쥴링(실행 예약) -> Future 
        result_cnt = excutor.map(separate_many,sorted(NATION_LS))
        # map -> 작업 순서 유지, 즉시 실행
    # result_cnt = separate_many(NATION_LS)
    # 종료 시간
    end_tm = time.time() - start_tm

    msg = '\n{} csv separated in {:.2f}s'
    
    # 최종 결과 출력
    print(msg.format(list(result_cnt),end_tm))


# 실행


if __name__ == '__main__':
    main(separate_many)