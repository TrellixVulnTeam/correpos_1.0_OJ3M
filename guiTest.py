#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import cv2

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_W = 1200
WINDOW_H = 600

BUTTON_CAP_X = 100
BUTTON_CAP_Y = 500

BUTTON_NEXT_X = 600
BUTTON_NEXT_Y = 500

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
#		self.setFixedSize(WINDOW_W, WINDOW_H)	# �T�C�Y
		self.resize(WINDOW_W, WINDOW_H)

		# �B�e�{�^��
		self.capButton = QPushButton(TXT_CAP, self)			# �����A�L���v�V����
		self.capButton.clicked.connect(self.on_clicked_cap)	# �N���b�N���̓���
		self.capButton.resize(self.capButton.sizeHint() )	# �T�C�Y�ݒ�
		self.capButton.move(BUTTON_CAP_X, BUTTON_CAP_Y)							# �ʒu
		
		# Next�{�^��
		self.nextButton = QPushButton(TXT_NEXT, self)			# ����
		self.nextButton.clicked.connect(self.on_clicked_next)	# �N���b�N��
		self.nextButton.resize(self.nextButton.sizeHint() )		# �T�C�Y
		self.nextButton.move(BUTTON_NEXT_X, BUTTON_NEXT_Y)							# �z�u
		self.nextButton.setEnabled(False)						# ������

		# �f���r�����[		
		self.cvCap = cv2.VideoCapture(0)
		
		self.label1 = QLabel(self)
		self.label1.move(100,100)
		self.label1.resize(320,240)
		
		self.label2 = QLabel(self)
		self.label2.move(500,100)
		self.label2.resize(320,240)
		
		
		# �E�B���h�E�\��
		self.show()

	# �B�e�{�^���̓���
	def on_clicked_cap(self):
		self.capButton.setText(TXT_RECAP)	# �e�L�X�g�ύX
		# ToDo �J�����f���L���v�`��
		self.nextButton.setEnabled(True)	# ToDo "����"�{�^���L����
		
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.label2.setPixmap(pix)
		
	# Next�{�^���̓���
	def on_clicked_next(self):
		# ����
		print("hello")

	# �ĕ`��C�x���g
	def paintEvent(self, event):
		ret, self.frame = self.cvCap.read()
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.label1.setPixmap(pix)

	

def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()