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

class myWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		# �E�B���h�E�ݒ�
		self.setWindowTitle(APPNAME)						# �L���v�V����
#		self.move(300,100)									# �ʒu
#		self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])	# �T�C�Y
		self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

		# �B�e�{�^��
		self.capButton = QPushButton(TXT_CAP, self)					# �����A�L���v�V����
		self.capButton.clicked.connect(self.on_clicked_cap)			# �N���b�N���̓���
		self.capButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )		# �T�C�Y�ݒ�
		self.capButton.move(BUTTON_CAP_POS[0], BUTTON_CAP_POS[1])	# �ʒu
		
		# Next�{�^��
		self.nextButton = QPushButton(TXT_NEXT, self)					# ����
		self.nextButton.clicked.connect(self.on_clicked_next)			# �N���b�N��
		self.nextButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )				# �T�C�Y
		self.nextButton.move(BUTTON_NEXT_POS[0], BUTTON_NEXT_POS[1])	# �z�u
		self.nextButton.setEnabled(False)								# ������

		# �J����		
		self.cvCap = cv2.VideoCapture(0)
		
		# �f���\��
		self.label1 = QLabel(self)
		self.label1.move(IMG1_POS[0], IMG1_POS[1])
		self.label1.resize(IMG_SIZE[0], IMG_SIZE[1])
		
		# �X�N�V���\��
		self.label2 = QLabel(self)
		self.label2.move(IMG2_POS[0], IMG2_POS[1])
		self.label2.resize(IMG_SIZE[0], IMG_SIZE[1])
		
		
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
		print("next")

	# �ĕ`��C�x���g
	def paintEvent(self, event):
		ret, frame1 = self.cvCap.read()	# �L���v�`��
		frame2 = cv2.resize(frame1, IMG_SIZE )	# ���T�C�Y
		frame2 = frame2[:,::-1]

            for rect in facerect:
        #���o��������͂ދ�`�̍쐬
           cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)
		
		self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)	# �F�ϊ� BGR -> RGB
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)	# QImage����
		pix = QPixmap.fromImage(img)		# QPixmap����
		self.label1.setPixmap(pix)			# �摜�\��t��

	

def main():
	app = QApplication(sys.argv)

	initWindow = myWindow()

	sys.exit(app.exec_())

if __name__ == '__main__':
	main()