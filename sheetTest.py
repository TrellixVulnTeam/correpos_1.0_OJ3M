#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import cv2
import copy


APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_SIZE = (1200, 600)

BUTTON_SIZE = (100, 23)	# �t�H���g23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_CAP = "�B�e"
TXT_RECAP = "�ĎB�e"

TXT_NEXT = "����"

# --- �V�[�g�e���v�� ---
class sheet(QFrame):
	def __init__(self, parent):
		super().__init__(parent)
		self.parent = parent
		self.resize(0,0)
		
	def start(self):
		# �L����
		self.resize(self.parent.width(), self.parent.height() )
		self.setVisible(True)
		
	def stop(self):
		# ������
		self.resize(0,0)
		self.setVisible(False)
		
	def copy(self):
		copy.copy(self)

# �������
class initSheet(sheet):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.btn = QPushButton("taesg", self)
		self.btn.clicked.connect(self.on_clicked)
		
	def on_clicked(self):
		print("clicked @ sheet1")
		self.parent.setSheet(1)

# --- ���쒆��� ---
class driveSheet(sheet):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.b = QPushButton("test2", self)
		self.b.clicked.connect(self.on_clicked)
		
	def on_clicked(self):
		print("clicked @ sheet2")
		self.parent.setSheet(0)


class myWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# �E�B���h�E�ݒ�
		self.setWindowTitle(APPNAME)						# �L���v�V����
#		self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])	# �T�C�Y
		self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

		# �V�[�g�쐬
		self.sheets = []
		self.sheets.append(initSheet(self) )
		self.sheets.append(driveSheet(self) )
		
		self.current = 0
		self.sheets[self.current].start()
		
		# �E�B���h�E�\��
		self.show()
		
	def setSheet(self, num):
		self.sheets[self.current].stop()
		self.current = num
		self.sheets[self.current].start()
			

def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()