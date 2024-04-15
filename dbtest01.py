import pymysql  # mysql과 연동시켜주는 라이브러리

"""
파이썬과 mysql 서버간의 커넥션 생성
1. 계정 : root(관리자 계정)
2. 비밀번호 : 12345
3. 데이터베이스가 설치된 컴퓨터의 IP 주소
    - 본인 컴퓨터면 localhost, 다른 컴퓨터면 그 컴퓨터의 IP 주소
    - 192.168.0.100 (교수용 컴퓨터 IP)
4. 데이터베이스 스키마 이름
    - ex. shopdb
"""
# 파이썬과 mysql간의 connection 생성
dbCon = pymysql.connect(host='localhost', user='root', password='12345', db='shopdb')

sql = "SELECT * FROM membertbl"     # DB에 실행할 SQL문 생성
# ;(semicolon) 넣지 않기!

cur = dbCon.cursor()    # 커서 호출해서 변수로 저장
cur.execute(sql)    # 연결된 DB의 스키마에 지정된 SQL문이 실행됨

records = cur.fetchall()    # SQL문에서 실행된 SELECT문의 결과를 records로 받음 -> tuple

# dbCon의 사용이 종료된 후에는 반드시 닫아줄 것! (.close())
# cursor.close() -> dbConnection.close()
cur.close()
dbCon.close()

print(records)
print(records[0])       # 특정 레코드 (1행)
print(records[0][1])    # 특정 레코드의 특정 값 (ex. '이순신')

for record in records:
    # if record[1] == '이순신':
        print(record)