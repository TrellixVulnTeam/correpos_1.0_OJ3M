# CORREPOS
====
CORREPOSはデスクワーカー向けの猫背矯正アプリケーションです。

## Description
PCのフロントカメラによってユーザの猫背を検出し、通知することでユーザに姿勢矯正を促します。
通知方法は音とポップアップから選択でき、場所を問わず使用が可能となっています。
そして通知音や、猫背の判定の厳しさをユーザの好みに変更するができるため、
モチベーションを維持しながら猫背矯正を行うことが出来ます。

***DEMO:***
![Demo](demo.gif)

## Requirement
* Python 3.5  
* OpenCV 3.1.0

## Usage
1. 以下のコマンドでアプリケーションを実行する 。  
    $ cd correpos  
    $ python main.py
2. 基準となる正しい姿勢を撮影する。
3. 撮影が完了したら「次ぎへ」をクリックし、もう一度撮影する場合は「再撮影」をクリックする。
4. 猫背が検出されると、画面右の設定に則った通知方法で通知を行う。

## Installation
    $ git clone https://github.com/achutane/correpos_1.0
