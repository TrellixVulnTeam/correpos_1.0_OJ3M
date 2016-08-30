#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import numpy as np
import datetime
import pyaudio
import wave
import cv2
import math
import copy


# --- 定数 ---

APPNAME = "CORREPOS"
VERSION = "0.0.1"

WINDOW_SIZE = (1200, 600)

BUTTON_SIZE = (100, 23)    # フォント23
BUTTON_CAP_POS = (250, 489)
BUTTON_NEXT_POS = (600 + BUTTON_CAP_POS[0], BUTTON_CAP_POS[1] )

IMG_SIZE = (400, 300)
IMG1_POS = (100, 150)
IMG2_POS = (600 + IMG1_POS[0], IMG1_POS[1])


TXT_DESC1 = "正しい姿勢で座り、[撮影]を押します"
TXT_DESC2 = "再度撮影する場合は[撮影]、猫背検知を開始するには[次へ]を押します"

TXT_CAP = "撮影"
TXT_RECAP = "再撮影"

TXT_NEXT = "次へ"

width_s = 0
height_s = 0

cascade_path = "haarcascade_frontalface_alt.xml"

#カスケード分類器の特徴量を取得する
cascade = cv2.CascadeClassifier(cascade_path) 

# --- シートテンプレ ---
class sheet(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.resize(0,0)
        
    def start(self):
        # 有効化
        self.resize(self.parent.width(), self.parent.height() )
        self.setVisible(True)
        
    def stop(self):
        # 無効化
        self.resize(0,0)
        self.setVisible(False)



# --- 初期画面 ---
class initSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
        # --- ボタン配置 ---
        # 撮影ボタン
        self.capButton = QPushButton(TXT_CAP, self)                    # 生成、キャプション
        self.capButton.clicked.connect(self.on_clicked_cap)            # クリック時の動作
        self.capButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )        # サイズ設定
        self.capButton.move(BUTTON_CAP_POS[0], BUTTON_CAP_POS[1])    # 位置
        
        # Nextボタン
        self.nextButton = QPushButton(TXT_NEXT, self)                    # 生成
        self.nextButton.clicked.connect(self.on_clicked_next)            # クリック時
        self.nextButton.resize(BUTTON_SIZE[0], BUTTON_SIZE[1] )                # サイズ
        self.nextButton.move(BUTTON_NEXT_POS[0], BUTTON_NEXT_POS[1])    # 配置
        self.nextButton.setEnabled(False)                                # 無効化

        # --- ラベル配置 ---
        self.descLabel = QLabel(self)
        self.descLabel.move(100, 50)
        self.descLabel.resize(1100, 30)
        
        # --- 画像配置 ---
        # 映像表示
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
        self.videoLabel.move(IMG1_POS[0], IMG1_POS[1])
        
        # スクショ表示
        self.capLabel = QLabel(self)
        self.capLabel.move(IMG2_POS[0], IMG2_POS[1])
        self.capLabel.resize(IMG_SIZE[0], IMG_SIZE[1])
        
        self.cvCap = None
        
    # 動作開始
    def start(self):
        super().start()
        
        # カメラ使用
        self.cvCap = cv2.VideoCapture(0)
        
        # ボタン初期化
        self.capButton.setText(TXT_CAP)        # 撮影ボタン
        self.nextButton.setEnabled(False)    # 次へボタン
        
        # ラベル
        self.descLabel.setText(TXT_DESC1)
        
    # 動作終了
    def stop(self):
        super().stop()
        
        # カメラリリース
        self.cvCap.release()
        self.cvCap = None
        
        # 画像廃棄
        self.capLabel.setPixmap(QPixmap())
    
    
    # 撮影ボタンの動作
    def on_clicked_cap(self):
    	# テキスト変更
        self.capButton.setText(TXT_RECAP)    # テキスト変更
        self.descLabel.setText(TXT_DESC2)
        
        # [次へ]有効化
        self.nextButton.setEnabled(True)
        
        
        # カメラ映像キャプチャ
        frame2 = cv2.resize(self.frame1, IMG_SIZE )		# リサイズ
        frame2 = frame2[:,::-1]							# 左右反転
        frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
        img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pix = QPixmap.fromImage(img)
        self.capLabel.setPixmap(pix)	# 画像貼り付け
        
        # 顔のサイズ取得
        global width_s,height_s
        color = (255, 255, 255) # 白
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))	# 顔認識
        # サイズ取り出し
        for rec in facerect:
            width_s = rec[2]
            height_s = rec[3]
            
        
        
    # Nextボタンの動作
    def on_clicked_next(self):
        # 処理
        print("next")
        self.parent.setSheet(1)
    
    # 再描画イベント：タイマーにしたい
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()			# キャプチャ
            frame = copy.deepcopy(self.frame1)				# フレームのコピー
            
            #物体認識（顔認識）の実行
            facerect = cascade.detectMultiScale(frame, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))

            color = (255, 255, 255) # 白
            for rect in facerect:
                #検出した顔を囲む矩形の作成
                cv2.rectangle(frame, tuple(rect[0:2]),tuple(rect[0:2] + rect[2:4]), color, thickness=2)

            
            frame2 = cv2.resize(frame, IMG_SIZE )		# リサイズ
            frame2 = frame2[:,::-1]							# 左右反転
            
            frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け





# --- 動作中画面 ---
class driveSheet(sheet):
    def __init__(self, parent):
        super().__init__(parent)
        
       # self.b = QPushButton("test2", self)
        #self.b.clicked.connect(self.on_clicked)
        self.text = QTextEdit(self)
        self.text.move(50,400)
        self.text.resize(400,150)
        self.videoLabel = QLabel(self)
        self.videoLabel.resize(400,300)        
        self.videoLabel.move(50,50)
        
        # deb:再設定
        self.b = QPushButton("再設定", self)
        self.b.clicked.connect(self.on_clicked)
        
    def on_clicked(self):
        print("clicked @ sheet2")
        self.parent.setSheet(0)
  
    def start(self):
        super().start()
        self.auto()
        self.cvCap = cv2.VideoCapture(0)
        self.check = 1


          
    def stop(self):
        super().stop()
        # カメラリリース
        self.cvCap.release()
        self.cvCap = None
        
        # タイマー終了
        self.timer.stop()
        
        
    def time_draw(self):
        d = datetime.datetime.today()
        daystr=d.strftime("%Y-%m-%d %H:%M:%S")        
        self.text.append(daystr+"猫背を検知！")      
        
        #タイマーの起動
    def auto(self):
        self.timer = QTimer()
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.timeout)
        self.timer.start()
           
           #タイムアウト処理
    def timeout(self):
        self.nekose_check()
        self.timer.setInterval(10)
        self.timer.start()
        
        #猫背をチェックする
    def nekose_check(self):
        ret, self.frame1 = self.cvCap.read() 
        facerect = cascade.detectMultiScale(self.frame1, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10))
        #座標取得
        for rec in facerect:
            self.width = rec[2]
            self.height = rec[3]    
        
        # 猫背チェック
#        if self.width >= width_s*1.5 and self.height >= height_s*1.5:
        if(self.evalNekose(self.width, self.height, width_s, height_s)):
            self.check = (self.check + 1)%50
            print(self.check)
            if self.check == 0:
                self.play_kenti("dog01",100)
                self.time_draw()
                
        else:
            if self.check > 0:            
                self.check = self.check - 1

    # 猫背評価
    def evalNekose(self, w1, h1, w0, h0):
        s1 = w1 * h1	# 現在の面積
        s0 = w0 * h0	# 基準の面積
        th = 35			# 閾値
        
        # 評価
        ev = abs( (s1 - s0) / s0 * 100 )
        
        # 出力
        print(ev)
        
        # 判定
        return ev > th
        
    def paintEvent(self, event):
        if not(self.cvCap is None):
            ret, self.frame1 = self.cvCap.read()    # キャプチャ
            frame2 = cv2.resize(self.frame1, IMG_SIZE )    # リサイズ
            frame2 = frame2[:,::-1]                    # 左右反転
        
            self.frame = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)    # 色変換 BGR -> RGB
            img = QImage(self.frame.data, self.frame.shape[1], self.frame.shape[0], QImage.Format_RGB888)    # QImage生成
            pix = QPixmap.fromImage(img)            # QPixmap生成
            self.videoLabel.setPixmap(pix)            # 画像貼り付け


        # 音をだす
    def play_kenti(self, wav, mTime):        
        wavfile="./wav_SE/"+wav+".wav"
        wf = wave.open(wavfile, "r")
        # ストリーム開始
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)

        data = wf.readframes(1024)
        t=0;
        while(t<mTime):
            stream.write(data)
            data = wf.readframes(1024)
            t=t+1
        stream.close()      # ストリーム終了
        p.terminate()
            




# --- ウィンドウ ---
class myWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # ウィンドウ設定
        self.setWindowTitle(APPNAME)                        # キャプション
        self.setFixedSize(WINDOW_SIZE[0], WINDOW_SIZE[1])    # サイズ
 #       self.resize(WINDOW_SIZE[0], WINDOW_SIZE[1])

        # シート作成
        self.sheets = []
        self.sheets.append(initSheet(self) )
        self.sheets.append(driveSheet(self) )
        
        self.current = 0
        self.sheets[self.current].start()
        
        # ウィンドウ表示
        self.show()
        
    # シート切り替え
    def setSheet(self, num):
        self.sheets[self.current].stop()
        self.current = num
        self.sheets[self.current].start()
            





# --- メイン処理 ---
def main():
    app = QApplication(sys.argv)
    initWindow = myWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
