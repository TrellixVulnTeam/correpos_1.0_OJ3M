#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import cv2




# --- �萔 ---

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



# --- ������� ---
class initSheet(sheet):
	def __init__(self, parent):
		super().__init__(parent)
		
		# --- �{�^���z�u ---
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

		
		# --- �摜�z�u ---
		# �f���\��
		self.videoLabel = QLabel(self)
		self.videoLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
		self.videoLabel.move(IMG1_POS[0], IMG1_POS[1])
		
		# �X�N�V���\��
		self.capLabel = QLabel(self)
		self.capLabel.move(IMG2_POS[0], IMG2_POS[1])
		self.capLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
		
		self.cvCap = None
		
	# ����J�n
	def start(self):
		super().start()
		
		# �J�����g�p
		self.cvCap = cv2.VideoCapture(0)
		
		# �{�^��������
		self.capButton.setText(TXT_CAP)		# �B�e�{�^��
		self.nextButton.setEnabled(False)	# ���փ{�^��
		
	# ����I��
	def stop(self):
		super().stop()
		
		# �J���������[�X
		self.cvCap.release()
		self.cvCap = None
		
		# �摜�p��
		self.capLabel.setPixmap(QPixmap())
	
	
	# �B�e�{�^���̓���
	def on_clicked_cap(self):
		self.capButton.setText(TXT_RECAP)	# �e�L�X�g�ύX
		self.nextButton.setEnabled(True)	# ToDo "����"�{�^���L����
		
		# �J�����f���L���v�`��
		img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)
		pix = QPixmap.fromImage(img)
		self.capLabel.setPixmap(pix)
		
		
	# Next�{�^���̓���
	def on_clicked_next(self):
		# ����
		print("next")
		self.parent.setSheet(1)

	"""
	def on_clicked(self):
		print("clicked @ sheet1")
		self.parent.setSheet(1)
	"""
	
	# �ĕ`��C�x���g�F�^�C�}�[�ɂ�����
	def paintEvent(self, event):
		if not(self.cvCap is None):
			ret, frame1 = self.cvCap.read()	# �L���v�`��
			frame2 = cv2.resize(frame1, IMG_SIZE )	# ���T�C�Y
			frame2 = frame2[:,::-1]					# ���E���]
		
			self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)	# �F�ϊ� BGR -> RGB
			img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)	# QImage����
			pix = QPixmap.fromImage(img)			# QPixmap����
			self.videoLabel.setPixmap(pix)			# �摜�\��t��





# --- ���쒆��� ---
class driveSheet(sheet):
	def __init__(self, parent):
		super().__init__(parent)
		
		self.b = QPushButton("test2", self)
		self.b.clicked.connect(self.on_clicked)
		
	def on_clicked(self):
		print("clicked @ sheet2")
		self.parent.setSheet(0)





# --- �E�B���h�E ---
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
		
	# �V�[�g�؂�ւ�
	def setSheet(self, num):
		self.sheets[self.current].stop()
		self.current = num
		self.sheets[self.current].start()
			





# --- ���C������ ---
def main():
	app = QApplication(sys.argv)
	initWindow = myWindow()
	sys.exit(app.exec_())

if __name__ == '__main__':
	main()