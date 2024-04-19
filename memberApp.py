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




    def member_join(self):  # 회원 가입 이벤트 처리 함수
        input_id = self. joinid_edit.text()     # 유저가 입력한 회원아이디 텍스트 가져오기
        input_pw = self.joinpw_edit.text()
        input_name = self.joinname_edit.text()
        input_email = self.joinemail_edit.text()
        input_age = int(self.joinage_edit.text())

        dbConn = pymysql.connect(user="root", password="12345", host="localhost", db="shopdb")

        sql = f"INSERT INTO appmember VALUES ('{input_id}', '{input_pw}', '{input_name}', '{input_email}', '{input_age}')"

        cur = dbConn.cursor()
        result = cur.execute(sql)
        cur.close()
        dbConn.commit()
        dbConn.close()



    def id_check(self):

        input_id = self.joinid_edit.text()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    app.exit(app.exec_())