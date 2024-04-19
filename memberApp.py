import sys
import pymysql

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("ui/member.ui")[0]

class MainWindow(form_class, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("회원 관리 프로그램")
        self.idchecked_ = False
        self.join_btn.clicked.connect(self.member_join)    # 회원가입 버튼이 클릭되면 가입함수 호출
        self.joinreset_btn.clicked.connect(self.join_reset)     # 초기화 버튼이 클릭되면 입력내용 초기화
        self.idcheck_btn.clicked.connect(self.id_check)     # 회원 가입 여부 체크 버튼 클릭 -> 가입여부 확인
        self.membersearch_btn.clicked.connect(self.member_search)   # 회원조회 버튼 클릭 -> 회원정보 출력
        self.memberreset_btn.clicked.connect(self.memberInfo_reset)
        self.membermodify_btn.clicked.connect(self.modify_info)
        self.login_btn.clicked.connect(self.member_login)
        self.loginreset_btn.clicked.connect(self.login_reset)
        self.deletereset_btn.clicked.connect(self.delete_reset)
        self.delete_btn.clicked.connect(self.delete_member)

    def member_join(self):  # 회원 가입 이벤트 처리 함수

        input_id = self. joinid_edit.text()     # 유저가 입력한 회원아이디 텍스트 가져오기
        input_pw = self.joinpw_edit.text()
        input_name = self.joinname_edit.text()
        input_email = self.joinemail_edit.text()
        input_age = self.joinage_edit.text()


        if input_id == "" or input_pw == "" or input_name == "" or input_email == "" or input_age == "":
            QMessageBox.warning(self, "정보입력오류", "회원 정보 중 입력되지 않은 정보가 있습니다.\n모든 정보를 입력해주세요.")
        elif len(input_id) < 4 or len(input_id) > 14:
            QMessageBox.warning(self, "아이디입력오류", "아이디는 4글자 이상, 14자 이하이어야 합니다.\n다시 입력해주세요.")
        elif len(input_pw) < 4 or len(input_pw) > 14:
            QMessageBox.warning(self, "비밀번호입력오류", "비밀번호는 4글자 이상, 14자 이하이어야 합니다.\n다시 입력해주세요.")
        elif self.idchecked_ == False:
            QMessageBox.warning(self, "아이디중복확인", "입력된 아이디 확인 버튼을 눌러주세요.")
        else:
            if self.check_id_exist(input_id) == 1:
                QMessageBox.warning(self, "아이디사용불가", "이미 가입된 아이디입니다.\n다시 입력해주세요.")
                self.idchecked_ = False
            elif self.check_id_exist(input_id) == 0:
                dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shopdb")
                sql = f"INSERT INTO appmember VALUES ('{input_id}', '{input_pw}', '{input_name}', '{input_email}', '{input_age}')"

                cur = dbConn.cursor()
                result = cur.execute(sql)

                if result == 1:
                    QMessageBox.warning(self, "회원가입성공", "축하합니다!\n회원가입이 완료되었습니다.")
                    self.join_reset()   # 회원가입 성공 ok 클릭 후 입력내용 초기화
                else:
                    QMessageBox.warning(self, "회원가입실패", "회원가입에 실패하였습니다.")
                cur.close()
                dbConn.commit()
                dbConn.close()

    def join_reset(self):   # 회원가입정보 입력내용 초기화
        self.joinid_edit.clear()
        self.joinpw_edit.clear()
        self.joinname_edit.clear()
        self.joinemail_edit.clear()
        self.joinage_edit.clear()

    def id_check(self):     # 동일 아이디 존재 여부 확인 함수
        input_id = self.joinid_edit.text()
        if input_id == "":
            QMessageBox.warning(self, "아이디입력오류", "아이디를 입력해주세요")
        elif len(input_id) < 4 or len(input_id) > 14:
            QMessageBox.warning(self, "아이디입력오류", "아이디는 4글자 이상, 14자 이하이어야 합니다.\n다시 입력해주세요.")
        else:
            if self.check_id_exist(input_id) == 1:
                QMessageBox.warning(self, "아이디사용불가", "이미 가입된 아이디입니다.\n다시 입력해주세요.")
            elif self.check_id_exist(input_id) == 0:
                QMessageBox.warning(self, "아이디사용가능", "가입 가능한 아이디입니다.")
                self.idchecked_ = True

    def check_id_exist(self, input_id):
        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shopdb")
        sql = f"SELECT COUNT(*) FROM appmember WHERE memberID = '{input_id}'"
        # 실행 시 1 또는 0 반환 (기존에 가입된 아이디면 1, 아니면 0)
        cur = dbConn.cursor()
        cur.execute(sql)
        search = cur.fetchall()
        print(search)
        cur.close()
        dbConn.close()

        if search[0][0] == 1:
            return 1
        else:
            return 0

    def check_pw(self, input_id, input_pw):
        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shopdb")
        sql = f"SELECT memberPW FROM appmember WHERE memberID = '{input_id}'"
        # 실행 시 1 또는 0 반환 (기존에 가입된 아이디면 1, 아니면 0)
        cur = dbConn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        print(result)
        pw = result[0][0]
        print(pw)
        cur.close()
        dbConn.close()

        if pw == input_pw:
            return 1
        else:
            return 0


    def member_search(self):    # 아이디로 회원을 조회하는 함수
        input_id = self.memberid_edit.text()
        input_pw = self.memberpw_edit.text()
        if input_id == "" or input_pw == "":
            QMessageBox.warning(self, "입력오류", "아이디와 비밀번호를 입력해주세요.")
        elif (self.check_id_exist(input_id) == 0) or (self.check_pw(input_id, input_pw) == 0):
            QMessageBox.warning(self, "입력오류", "존재하지 않는 아이디거나 비밀번호가 올바르지 않습니다.")
        else:
            dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shopdb")
            sql = f"SELECT * FROM appmember WHERE memberID = '{input_id}'"
            cur = dbConn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            print(result)
            cur.close()
            self.memberpw_edit.setText(result[0][1])
            self.membername_edit.setText(result[0][2])
            self.memberemail_edit.setText(result[0][3])
            self.memberage_edit.setText(str(result[0][4]))

            dbConn.close()

    def modify_info(self):
        input_id = self.memberid_edit.text()
        input_pw = self.memberpw_edit.text()
        input_name = self.membername_edit.text()
        input_email = self.memberemail_edit.text()
        input_age = self.memberage_edit.text()

        dbConn = pymysql.connect(user='root', password='12345', host='localhost', db='shopdb')

        sql = f"UPDATE appmember SET memberPW = '{input_pw}', memberName = '{input_name}', memberEmail = '{input_email}', memberAge = '{input_age}' WHERE memberID = '{input_id}'"
        cur = dbConn.cursor()
        result = cur.execute(sql)

        if result == 1:
            QMessageBox.warning(self, "회원정보수정 성공", "회원정보를 성공적으로 수정했습니다!")
        else:
            QMessageBox.warning(self, "회원정보수정 실패", "회원정보 수정에 실패하였습니다.")

        dbConn.commit()
        cur.close()
        dbConn.close()

    def memberInfo_reset(self):   # 회원가입정보 입력내용 초기화
        self.memberid_edit.clear()
        self.memberpw_edit.clear()
        self.membername_edit.clear()
        self.memberemail_edit.clear()
        self.memberage_edit.clear()

    def member_login(self):
        input_id = self.loginid_edit.text()
        input_pw = self.loginpw_edit.text()
        if input_id == "" or input_pw == "":
            QMessageBox.warning(self, "입력오류", "아이디와 비밀번호를 입력해주세요.")
        elif (self.check_id_exist(input_id) == 0) or (self.check_pw(input_id, input_pw) == 0):
            QMessageBox.warning(self, "로그인 실패", "존재하지 않는 아이디이거나 비밀번호가 올바르지 않습니다.")
        else:
            dbConn = dbConn = pymysql.connect(user='root', password='12345', host='localhost', db='shopdb')
            sql = f"SELECT memberName FROM appmember WHERE memberID = '{input_id}'"
            cur = dbConn.cursor()
            cur.execute(sql)
            result = cur.fetchall()
            name = result[0][0]
            QMessageBox.warning(self, "로그인 성공", f"{name}님, 환영합니다!")

    def login_reset(self):
        self.loginid_edit.clear()
        self.loginpw_edit.clear()

    def delete_member(self):
        input_id = self.deleteid_edit.text()
        input_pw = self.deletepw_edit.text()

        if input_id == "" or input_pw == "":
            QMessageBox.warning(self, "입력오류", "탈퇴를 원하는 아이디와 비밀번호를 입력하세요.")
        elif (self.check_id_exist(input_id) == 0) or (self.check_pw(input_id, input_pw) == 0):
            QMessageBox.warning(self, "입력오류", "존재하지 않는 아이디거나 비밀번호가 올바르지 않습니다.")
        else:
            reply = QMessageBox.question(self, "탈퇴확인", "정말 탈퇴하시겠습니까?", QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                pass
            elif reply == QMessageBox.Yes:
                dbConn = pymysql.connect(host='localhost', user='root', password='12345', db='shopdb')
                sql = f"DELETE FROM appmember WHERE memberID = '{input_id}'"
                cur = dbConn.cursor()
                result = cur.execute(sql)
                cur.close()

                if result == 1:
                    QMessageBox.about(self, "탈퇴완료", f"{input_id}님의 탈퇴가 완료되었습니다.")
                    self.delete_reset()

                dbConn.commit()
                dbConn.close()

    def delete_reset(self):
        self.deleteid_edit.clear()
        self.deletepw_edit.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())