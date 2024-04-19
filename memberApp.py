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

        self. join_btn.clicked.connect(self.member_join)    # 회원가입 버튼이 클릭되면 가입함수 호출
        self.joinreset_btn.clicked.connect(self.join_reset)     # 초기화 버튼이 클릭되면 입력내용 초기화



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
        else:
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

    def id_check(self):

        input_id = self.joinid_edit.text()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())