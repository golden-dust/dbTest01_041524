import pymysql

dbConn = pymysql.connect(user='root', password='12345', host='localhost', db='shopdb')

while True:
    print("******** 회원 관리 프로그램 ********")
    print("1 : 회원 가입")
    print("2 : 회원 정보 수정")
    print("3 : 회원 탈퇴")
    print("4 : 전체 회원목록 조희")
    print("5 : 프로그램 종료")
    print("*********************************")
    menuNum = input("메뉴 중 한가지를 선택하세요(1~5) : ")

    if menuNum == "1":
        print("회원정보를 입력하세요.")
        memberID = input("1) 회원아이디를 입력하세요 : ")
        memberName = input("2) 회원이름을 입력하세요 : ")
        address = input("3) 회원주소를 입력하세요 : ")

        cur = dbConn.cursor()
        sql = f"INSERT INTO membertbl VALUES ('{memberID}', '{memberName}', '{address}')"
        result = cur.execute(sql)

        if result == 1:
            print("축하합니다! 회원가입이 완료되었습니다.")
            dbConn.commit()
        else:
            print("회원가입에 실패하였습니다.")

        cur.close()

    elif menuNum == '2':
        memberID = input("수정할 회원의 아이디를 입력하세요 : ")
        print("-------------------------------")
        print("1) 이름")
        print("2) 주소")
        choice = input("수정할 회원 정보 번호를 입력하세요 (1~2) : ")
        cur = dbConn.cursor()

        if choice == "1":
            memberName = input("수정할 회원 이름을 입력하세요 : ")
            sql = f"UPDATE membertbl SET memberName = '{memberName}' WHERE memberID = '{memberID}'"
            result = cur.execute(sql)
            dbConn.commit()
        elif choice == "2":
            address = input("수정할 회원 주소를 입력하세요 : ")
            sql = f"UPDATE membertbl SET memberAddress = '{address}' WHERE memberID = '{memberID}'"
            result = cur.execute(sql)
            dbConn.commit()
        else:
            print("잘못 입력하셨습니다.")

        if result == 1:
            print("회원정보가 수정되었습니다")
        else:
            print("회원정보 수정에 실패하였습니다")

        cur.close()

    elif menuNum == "3":

        memberID = input("탈퇴할 회원 아이디를 입력하세요 : ")
        memberName = input("탈퇴할 회원 이름을 입력하세요 : ")

        sql = f"DELETE FROM membertbl WHERE memberID = '{memberID}' AND memberName = '{memberName}'"
        try:
            cur = dbConn.cursor()
            result = cur.execute(sql)
            dbConn.commit()
            if result == 1:
                print("탈퇴에 성공하였습니다!")
            else:
                print("잘못된 이름 또는 존재하지 않는 아이디입니다")
        except:
            print("탈퇴에 실패하였습니다")

        cur.close()

    elif menuNum == '4':
        cur = dbConn.cursor()
        sql = f"SELECT * FROM membertbl"
        cur.execute(sql)

        members = cur.fetchall()

        print("*********** 회원 리스트 ***********")
        for member in members:
            print(f"ID: {member[0]}, 이름: {member[1]}, 주소: {member[2]}")
        print("*********************************")

        cur.close()

    elif menuNum == '5':
        dbConn.close()
        break;
    else:
        print("잘못 입력하셨습니다. 다시 입력해주세요.")
