

from PyQt5.QtWidgets import *
import sys

def main():
	app = QApplication(sys.argv)
	
	w = QWidget()
	bb = [QPushButton, QCheckBox]	# �N���X�̔z��
	b = bb[1]("test", w)			# �C���X�^���X��
	w.show()
	
	sys.exit(app.exec_() )

if __name__ == '__main__':
	main()