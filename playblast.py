import os

from PySide2 import QtCore
from PySide2 import QtGui
from PySide2 import QtWidgets

import shot as shot;reload(shot)

import pymel.core as pm

class HLine(QtWidgets.QFrame):
	"""
	Horizal line widget
	"""
	def __init__(self):
		super(HLine, self).__init__()
		self.setFrameShape(QtWidgets.QFrame.HLine)
		self.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.setStyleSheet('border: 1px solid rgb(25,25,25)')


class HorizantalLineWithText(QtWidgets.QDialog):
	"""
	Horizantal line eith text widget
	"""
	def __init__(self, text):
		super(HorizantalLineWithText, self).__init__()
		main_layout = QtWidgets.QHBoxLayout()
		main_layout.setContentsMargins(0,0,0,0)
		self.setLayout(main_layout)
		self.div1 = HLine()
		self.label = QtWidgets.QLabel(text)
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		self.div2 = HLine()
		main_layout.addWidget(self.div1 )
		main_layout.addWidget(self.label )
		main_layout.addWidget(self.div2 )

class Playblast(QtWidgets.QDialog):
	"""
	Playblast tool
	"""

	RESOLUTION = {"HD 1080": (1920, 1080), "HD 720": (1280, 720), "HD 540": (960, 540)}
		
	VIDEO_ENCODER = {"mov": "H.264", "mp4": "H.264"}
	
	def __init__(self, parent = None):
			super(Playblast, self).__init__(parent)
			self.shot_obj = shot.MayaShot()
			self.initUi()
			self.initConnections()
			
			
	def initUi(self):
		self.setWindowTitle("Playblast")
		self.setFixedWidth(350)
		
		border1 = HLine()
		self.playblast_label = QtWidgets.QLabel("<b>Playblast Tool v1.0</b>")
		self.playblast_label.setAlignment(QtCore.Qt.AlignCenter)
		border2 = HLine()
		
		hline1 = HorizantalLineWithText("playblast options")
		
		res_hLay = QtWidgets.QHBoxLayout()
		self.resolution_lbl = QtWidgets.QLabel("Resolution")
		self.resolution_cb = QtWidgets.QComboBox()
		self.resolution_cb.addItems(self.RESOLUTION.keys())
		res_hLay.addWidget(self.resolution_lbl)
		res_hLay.addWidget(self.resolution_cb)
		
		encodeing_lay = QtWidgets.QHBoxLayout()
		self.encoding_lbl = QtWidgets.QLabel("Encoding")
		self.encoding_cb = QtWidgets.QComboBox()
		self.encoding_cb.addItems(self.VIDEO_ENCODER.keys())
		encodeing_lay.addWidget(self.encoding_lbl)
		encodeing_lay.addWidget(self.encoding_cb)
		
		
		op_lay = QtWidgets.QHBoxLayout()
		self.output_label = QtWidgets.QLabel("Output Path")
		
		self.output_dir_path_le = QtWidgets.QLineEdit()
		self.output_dir_path_le.setPlaceholderText("Choose output path")
		output_path = self.shot_obj.get_playblast_dir()
		self.output_dir_path_le.setText(output_path)
		

		self.output_dir_path_show_folder_btn = QtWidgets.QPushButton(QtGui.QIcon(":fileOpen.png"), "")
		self.output_dir_path_show_folder_btn.setFixedSize(24, 19)
		self.output_dir_path_show_folder_btn.setToolTip("Show in Folder")
		op_lay.addWidget(self.output_label)
		op_lay.addWidget(self.output_dir_path_le)
		op_lay.addWidget(self.output_dir_path_show_folder_btn)
		
		file_lay = QtWidgets.QHBoxLayout()
		self.file_label = QtWidgets.QLabel("File Name")
		self.file_name_le = QtWidgets.QLineEdit()
		self.file_name_le.setPlaceholderText("File Name")
		filename = self.shot_obj.shot_name
		self.file_name_le.setText(filename)
		file_lay.addWidget(self.file_label)
		file_lay.addWidget(self.file_name_le)
		
		hline2 = HorizantalLineWithText("Output Options")
	
		self.showOrnaments = QtWidgets.QCheckBox("Show Ornaments")
		self.showOrnaments.setChecked(True)
		
		quality_lay = QtWidgets.QHBoxLayout()
		self.quality_lbl = QtWidgets.QLabel("Quality")
		self.quality = QtWidgets.QComboBox()
		self.quality.addItems(["100%", "50%"])
		quality_lay.addWidget(self.quality_lbl)
		quality_lay.addWidget(self.quality)
		
		border3 = HLine()
		
		self.process_btn = QtWidgets.QPushButton("Process")
		
		main_layout = QtWidgets.QVBoxLayout()
		main_layout.addWidget(border1)
		main_layout.addWidget(self.playblast_label)
		main_layout.addWidget(border2)
		main_layout.addWidget(hline1)
		main_layout.addLayout(res_hLay)
		main_layout.addLayout(encodeing_lay)
		main_layout.addLayout(quality_lay)
		main_layout.addWidget(self.showOrnaments)
		main_layout.addWidget(hline2)
		main_layout.addLayout(op_lay)
		main_layout.addLayout(file_lay)
		main_layout.addWidget(border3)
		main_layout.addWidget(self.process_btn)
		
		self.setLayout(main_layout)
		
	def initConnections(self):
		self.output_dir_path_show_folder_btn.clicked.connect(self.outputPath)
		self.process_btn.clicked.connect(self.final_process)
		
		
	def outputPath(self):
		new_dir_path = QtWidgets.QFileDialog.getExistingDirectory(self,"Open a folder",os.path.expanduser("~"),QtWidgets.QFileDialog.ShowDirsOnly)
		self.output_dir_path_le.setText(new_dir_path)
		
	def final_process(self):
		resolution_cb = self.resolution_cb.currentText()
		width_height = self.RESOLUTION[resolution_cb]
		
		output_dir = self.output_dir_path_le.text()
		file_name = self.file_name_le.text()
		encoding = self.encoding_cb.currentText()
		pb_path = os.path.join(output_dir, file_name+"."+encoding)
		
		ornament = self.showOrnaments .isChecked()
		
		compression = self.VIDEO_ENCODER[encoding]
		
		quality = int(self.quality.currentText().split("%")[0])
		
		
		pm.playblast(widthHeight=width_height, format='qt', forceOverwrite=1, filename=pb_path,  sequenceTime=False,  clearCache=False,  viewer =False,  showOrnaments =ornament,  offScreen=True, framePadding=4,  percent=100,  compression=compression,  quality=quality)
		
		os.startfile(os.path.dirname(pb_path))
		pm.confirmDialog(b="Ok", m="Playblast Done \nPlayBlast is saved in below path\n {}".format(pb_path))

		
		
		
		

window = Playblast()
window.show()



""""
import sys
__path = r"D:\anim_test\Playblast"
sys.path.append(__path)
import playblast as pb;reload(pb)
"""

