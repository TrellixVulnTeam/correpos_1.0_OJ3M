#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from titlesheet import titleSheet
from initsheet import initSheet
from drivesheet import driveSheet
from appsheet import appSheet
from logsheet import logSheet

import cv2
import config

# --- 定数 ---

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_SIZE = (1200, 600)

# --- ウィンドウ ---
class myWindow(QWidget):

    def __init__(self):
        super().__init__()
        
        # カメラ変数
        self.cvCap = cv2.VideoCapture(0)
        
         #設定用変数の初期化
        self.notice_num = 1    #通知はON
        self.popup_num = 1    #ポップアップはON
        self.se_num = "!.wav"
        self.volume_num = 50    #音量の初期値は50
        self.worktime = "0"    #作業時間はとりあえず"0"
        self.work_num = 0    #作業時間はOFF
        self.bar_num = 1    #バーの増加レベルはふつう
        self.judgelevel_num = 1    #判定レベルはふつう
        self.tweet_num = 0 #twitter用

        self.setWindowFlags(Qt.WindowStaysOnTopHint) # 常に前面に表示        
        self.initUI()
        

    def initUI(self):
        # ウィンドウ設定
        self.setWindowTitle(APPNAME)                        # キャプション
        self.setWindowIcon(QIcon('img/correpos_icon.png'))
#        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])    # サイズ
#       self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        color = QColor(100,100,100,100)
        color.setAlpha(150)

        palette = QPalette()
        # palette.setColor(QPalette.Background, Qt.black)
        backgroundImage = QPixmap("img/backgroundImage.jpg")
        brash = QBrush(color, backgroundImage)
        palette.setBrush(palette.Background, brash)
        # self.setAutoFillBackground(True)
        self.setPalette(palette)

        # シート作成
        self.sheets = []
        self.sheets.append(initSheet(self) )
        self.sheets.append(driveSheet(self) )
        #self.sheets.append(logSheet(self) )
        self.sheets.append(titleSheet(self) )
        self.sheets.append(appSheet(self) )
        

        self.current = 2
        self.sheets[self.current].start()
        
        self.center()
        
        # ウィンドウ表示
        self.show()
        self.setFixedSize( self.width(), self.height() )	# サイズ固定

        # バルーンのためのアイコン（右下に常駐）
        config.trayIcon = QSystemTrayIcon(self)
        config.trayIcon.setIcon(QIcon("img/correpos_icon.png")) # とりあえず適当にこの画像
        config.trayIcon.show()

        
    # シート切り替え
    def setSheet(self, num):
        self.sheets[self.current].stop()
        self.current = num
        self.sheets[self.current].start()
        self.repaint()
        
        g0 = self.frameGeometry()
        
        self.setMinimumSize(0,0)			# サイズ可変化
        self.setMaximumSize(10000,10000)	#
        self.adjustSize()									# サイズ調整
        self.setFixedSize( self.width(), self.height() )	# サイズ固定
        
        g1 = self.frameGeometry()
        # サイズ調整の前後で中心位置を合わせる, ただしウィンドウ左上が画面に収まるようにする
        # ** マルチ画面環境だと変になる可能性 **
        x = max(0, g1.x() - (g1.width() - g0.width() ) /2 )
        y = max(0, g1.y() - (g1.height() - g0.height() ) /2 )
        self.move(x, y)

    # ウィンドウを閉じるとき発生するイベント
    # 参考URL  http://17-m.seesaa.net/article/247521232.html
    def closeEvent(self, event):
        config.trayIcon.hide()

        # 全シートに対して閉じる処理を実行(closeEvent発生)
        for s in self.sheets:
            s.close()
            
    def center(self):

        # ウィンドウ全体の情報を取得した長方形qrを作成
        qr = self.frameGeometry()
        # ウィンドウの中心を取得
        cp = QDesktopWidget().availableGeometry().center()
        # 長方形qrをウィンドウの中心へ移動
        qr.moveCenter(cp)
        #　長方形qrの左上と画面の左上を合わせる
        self.move(qr.topLeft()) #bottomRight 右下


# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = myWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
