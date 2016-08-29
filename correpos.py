#!/usr/bin/python
# -*- coding: sjis -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import datetime
import cv2




# --- �萔 ---

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_SIZE = (1200, 600)

BUTTON_SIZE = (100, 23)    # �t�H���g23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_CAP = "�B�e"
TXT_RECAP = "�ĎB�e"

TXT_NEXT = "����"

width_s = 0
height_s = 0

cascade_path = "haarcascade_frontalface_alt.xml"

#�J�X�P�[�h���ފ�̓����ʂ��擾����
cascade = cv2.CascadeClassifier(cascade_path) 

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
        self.capButton = QPushButton(TXT_CAP, self)                    # �����A�L���v�V����
        self.capButton.clicked.connect(self.on_clicked_cap)            # �N���b�N���̓���
        self.capButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )        # �T�C�Y�ݒ�
        self.capButton.move(BUTTON_CAP_POS[0], BUTTON_CAP_POS[1])    # �ʒu
        
        # Next�{�^��
        self.nextButton = QPushButton(TXT_NEXT, self)                    # ����
        self.nextButton.clicked.connect(self.on_clicked_next)            # �N���b�N��
        self.nextButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )                # �T�C�Y
        self.nextButton.move(BUTTON_NEXT_POS[0], BUTTON_NEXT_POS[1])    # �z�u
        self.nextButton.setEnabled(False)                                # ������

        
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
        self.capButton.setText(TXT_CAP)        # �B�e�{�^��
        self.nextButton.setEnabled(False)    # ���փ{�^��
        
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
        self.capButton.setText(TXT_RECAP)    # �e�L�X�g�ύX
        self.nextButton.setEnabled(True)    # ToDo "����"�{�^���L����
        
        
        color = (255, 255, 255) #��
        #���̔F���i��F���j�̎��s
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        #���W�擾
        for rec in facerect:
            width_s = rec[2]
            height_s = rec[3]
  
        
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
            ret, self.frame1 = self.cvCap.read()    # �L���v�`��
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # ���T�C�Y
            frame2 = frame2[:,::-1]                    # ���E���]
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # �F�ϊ� BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage����
            pix = QPixmap.fromImage(img)            # QPixmap����
            self.videoLabel.setPixmap(pix)            # �摜�\��t��





# --- ���쒆��� ---
class driveSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.b = QPushButton("test2", self)
        self.b.clicked.connect(self.on_clicked)
        self.text = QTextEdit(self)
        self.text.move(10,10)
        self.text.resize(140,140)
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(400,300)        
        self.videoLabel.move(500,100)
        
    def on_clicked(self):
        print("clicked @ sheet2")
        self.parent.setSheet(0)
  
    def start(self):
        super().start()
        self.auto()
        self.cvCap = cv2.VideoCapture(0)
        self.check = 0


          
    def stop(self):
        super().stop()
        # �J���������[�X
        self.cvCap.release()
        self.cvCap = None
        
        
    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")
        #self.text.append(daystr)        
        
    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
           
    def timeout(self):
        print ("hoge")
        self.nekose_check()
        self.time_draw()
        self.timer.setInterval(10)
        self.timer.start()
        
    def nekose_check(self):
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        #���W�擾
        for rec in facerect:
            self.width = rec[2]
            self.height = rec[3]    
        
        if self.width >= width_s*1.5 and self.height >= height_s*1.5:
            self.check = self.check + 1
            print(self.check)

    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()    # �L���v�`��
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # ���T�C�Y
            frame2 = frame2[:,::-1]                    # ���E���]
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # �F�ϊ� BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage����
            pix = QPixmap.fromImage(img)            # QPixmap����
            self.videoLabel.setPixmap(pix)            # �摜�\��t��





# --- �E�B���h�E ---
class myWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # �E�B���h�E�ݒ�
        self.setWindowTitle(APPNAME)                        # �L���v�V����
#        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])    # �T�C�Y
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