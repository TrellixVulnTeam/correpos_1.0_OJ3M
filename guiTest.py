#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_W = 1200
WINDOW_H = 600

TXT_CAP = "�B�e"
TXT_RECAP = "�ĎB�e"

TXT_NEXT = "����"

class myWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# �E�B���h�E�ݒ�
		self.setWindowTitle(APPNAME)			# �L���v�V����
#		self.move(300,100)						# �ʒu
		self.setFixedSize(WINDOW_W, WINDOW_H)	# �T�C�Y

		# �B�e�{�^��
		self.capButton = QPushButton(TXT_CAP, self)			# �����A�L���v�V����
		self.capButton.clicked.connect(self.on_clicked_cap)	# �N���b�N���̓���
		self.capButton.resize(self.capButton.sizeHint() )	# �T�C�Y�ݒ�
		self.capButton.move(50,50)							# �ʒu
		
		# Next�{�^��
		self.nextButton = QPushButton(TXT_NEXT, self)			# ����
		self.nextButton.clicked.connect(self.on_clicked_next)	# �N���b�N��
		self.nextButton.resize(self.nextButton.sizeHint() )		# �T�C�Y
		self.nextButton.move(50, 100)							# �z�u
		self.nextButton.setEnabled(False)						# ������
		
		# �E�B���h�E�\��
		self.show()

	# �B�e�{�^���̓���
	def on_clicked_cap(self):
		self.capButton.setText(TXT_RECAP)	# �e�L�X�g�ύX
		# ToDo �J�����f���L���v�`��
		self.nextButton.setEnabled(True)	# ToDo "����"�{�^���L����
		
		
	# Next�{�^���̓���
	def on_clicked_next(self):
		# ����
		print("hello")


def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()