

# 순차 실행 concurrent.futures 방법1,2

import os
import time
import sys
import csv

# 순차 실행
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
def separate_many(nt_list):
    for nt in sorted(nt_list):
        # 분리 데이터
        data = get_sales_data(nt)
        # 상황을 출력
        show(nt)
        # 파일 저장
        save_csv(data,nt.lower()+ '.csv')
    return len(nt_list)

# 시간 측정 및 메인 함수
def main(separate_many):

    # 시작 시간
    start_tm = time.time()
    # 결과 건수
    result_cnt = separate_many(NATION_LS)
    # 종료 시간
    end_tm = time.time() - start_tm

    msg = '\n{} csv separated in {:.2f}s'
    
    # 최종 결과 출력
    print(msg.format(result_cnt,end_tm))


# 실행


if __name__ == '__main__':
    main(separate_many)