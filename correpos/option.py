#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QPushButton) 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from glob import glob
from os.path import join, relpath



def option(self):
    
    #self.option = QApplication(sys.argv)
    self.subwindow = QWidget()
    self.subwindow.setWindowTitle("OPTION")
    #self.button = QPushButton('button', self.subwindow)
    

    self.noticeEnable = QCheckBox(self)	# 通知オン・オフ
    self.noticeEnable.setText("通知する")
    self.noticeEnable.setTristate(False)
    self.message_boxEnable = QCheckBox(self)	# ポップアップ通知オン・オフ
    self.message_boxEnable.setText("バルーン通知")
    self.message_boxEnable.setTristate(False)        
    # 作業終了時刻の設定
    self.workHourButton = QCheckBox(self)                      # 有効・無効設定
    self.workHourButton.setText("作業終了通知：")
    self.workHourButton.setTristate(False)
    self.workHourEdit = QDateTimeEdit(self)                    # 時刻設定
    self.workHourEdit.setDisplayFormat("hh:mm")
    self.grid_message=QGridLayout() #グリッド作成
    self.grid_message.addWidget(self.noticeEnable, 0, 0)
    self.grid_message.addWidget(self.message_boxEnable, 1, 0)
    self.grid_message.addWidget(self.workHourButton, 2, 0)
    self.grid_message.addWidget(self.workHourEdit, 2, 1)
    self.message_Widget=QWidget(self)
    self.message_Widget.setLayout(self.grid_message) 
    
    
    #通知音設定
    self.descLabel = QLabel(self)
    self.descLabel.setText("通知音設定 ： ")
    self.combo_selectSE = QComboBox(self) #ComboBoxの作成
    path='wav_SE'
    list = [relpath(x, path) for x in glob(join(path, '*.wav'))] #wav_SEのファイル名を抽出
    for file in list:
        self.combo_selectSE.addItem(file)
    self.selectSE=list[0] #select_SEに文字列を代入　後でwavplayで使用
    self.combo_selectSE.activated[str].connect(self.selectSE_onActivated) #ComboBoxで選んだ時の動作
    self.selectSE_frame=QHBoxLayout(self)
    self.selectSE_frame.addWidget(self.descLabel)
    self.selectSE_frame.addWidget(self.combo_selectSE)
    self.selectSE_widget=QWidget(self)
    self.selectSE_widget.setLayout(self.selectSE_frame) #レイアウトをｗに突っ込む    
    
    self.slider = QSlider(Qt.Horizontal)  #スライダの向き
    self.slider.setRange(0, 100)  # スライダの範囲
    self.slider.setValue(50)  # 初期値
    self.slider_label = QLabel('音量 :'+str(self.slider.value())) #volume:スライダの値
    self.slider.valueChanged.connect(self.text_draw) #スライダの値が変わったらtext_drawを実行                
    self.checkbutton = QPushButton("音量テスト") #音量の確認ボタン
    self.checkbutton.setFocusPolicy(Qt.NoFocus)
    self.checkbutton.clicked.connect(self.button_clicked) #音量テストのボタンを押すとbutton_clicked実行        
    self.changevolume=QHBoxLayout(self) #音量テストをまとめる横方向のレイアウトの作成
    self.changevolume.addWidget(self.slider_label)
    self.changevolume.addWidget(self.slider)
    self.changevolume.addWidget(self.checkbutton)
    self.volume_widget=QWidget(self) #音量設定の枠volume_widgetの作成
    self.volume_widget.setLayout(self.changevolume) #レイアウトをvolume_widgetに突っ込む

    #判定厳しさ調整のラジオボタン作成
    self.checklevel = QLabel(self)
    self.checklevel.setText("判定レベル:")
    self.levelyurui = QLabel(self)
    self.levelyurui.setText("緩")
    self.clevel1=QRadioButton("", self)    #判定レベル　ラジオボタン作成
    self.clevel2=QRadioButton("", self)
    self.clevel3=QRadioButton("", self)
    self.levelgen = QLabel(self)
    self.levelgen.setText("厳")
    self.clevelgroup=QButtonGroup(self)    #ラジオボタン　グループ作成
    self.clevelgroup.addButton(self.clevel1)
    self.clevelgroup.addButton(self.clevel2)
    self.clevelgroup.addButton(self.clevel3)
    self.clevelbuttom_frame=QHBoxLayout(self)
    self.clevelbuttom_frame.addWidget(self.levelyurui)
    self.clevelbuttom_frame.addWidget(self.clevel1)
    self.clevelbuttom_frame.addWidget(self.clevel2)
    self.clevelbuttom_frame.addWidget(self.clevel3)
    self.clevelbuttom_frame.addWidget(self.levelgen)
    self.clevelgroup_widget=QWidget(self)
    self.clevelgroup_widget.setLayout(self.clevelbuttom_frame) #レイアウトをvolume_widgetに突っ込む
    self.checklevel_frame=QHBoxLayout(self) #音量テストをまとめる横方向のレイアウトの作成
    self.checklevel_frame.addWidget(self.checklevel)
    self.checklevel_frame.addWidget(self.clevelgroup_widget)
    self.checklevel_widget=QWidget(self)
    self.checklevel_widget.setLayout(self.checklevel_frame) 
    
    #ゲージ増加調整のラジオボタン作成
    self.sldlevel = QLabel(self)
    self.sldlevel.setText("ゲージ増加レベル:")
    self.levelslow = QLabel(self)
    self.levelslow.setText("遅")
    self.level1=QRadioButton("", self)    #判定レベル　ラジオボタン作成
    self.level2=QRadioButton("", self)
    self.level3=QRadioButton("", self)
    self.levelquick = QLabel(self)
    self.levelquick.setText("早")
    self.levelgroup=QButtonGroup(self)    #ラジオボタン　グループ作成
    self.levelgroup.addButton(self.level1)
    self.levelgroup.addButton(self.level2)
    self.levelgroup.addButton(self.level3)
    self.levelbuttom_frame=QHBoxLayout(self)
    self.levelbuttom_frame.addWidget(self.levelslow)
    self.levelbuttom_frame.addWidget(self.level1)
    self.levelbuttom_frame.addWidget(self.level2)
    self.levelbuttom_frame.addWidget(self.level3)
    self.levelbuttom_frame.addWidget(self.levelquick)
    self.levelgroup_widget=QWidget(self)
    self.levelgroup_widget.setLayout(self.levelbuttom_frame) #レイアウトをvolume_widgetに突っ込む
    self.gaugelevel_frame=QHBoxLayout(self) #音量テストをまとめる横方向のレイアウトの作成
    self.gaugelevel_frame.addWidget(self.sldlevel)
    self.gaugelevel_frame.addWidget(self.levelgroup_widget)
    self.gaugelevel_widget=QWidget(self)
    self.gaugelevel_widget.setLayout(self.gaugelevel_frame) 
     
    
    #判定レベル、状態画像表示に関する変数初期化
    self.picturechange = 0
    self.level = 2
    self.count = 50
    self.multi = 2
    self.th = 35       #顔の距離の閾値
    self.multi_y = 0.3   #顔の上下の判定
    
    self.mainWidget=QWidget(self) #音量設定の枠wの作成
    self.mainWidget=QVBoxLayout(self) #音量テストをまとめる横方向のレイアウトの作成
    self.mainWidget.addWidget(self.message_Widget)
    self.mainWidget.addWidget(self.selectSE_widget)
    self.mainWidget.addWidget(self.volume_widget)
    self.mainWidget.addWidget(self.checklevel_widget)
    self.mainWidget.addWidget(self.gaugelevel_widget)
    
    



    self.subwindow.setLayout(self.mainWidget) #レイアウトをｗに突っ込む

    
    # スロットを設定
    #self.button.clicked.connect(self.subwindow.close)
    
    self.subwindow.show()
    #sys.exit(app.exec_())