from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
                            QVBoxLayout, QWidget, QShortcut,QHBoxLayout,QStatusBar, \
                            QSlider,QFileDialog, QMessageBox,QLabel,QDialog,QCheckBox, \
                            QMenu,QComboBox,QPushButton,QInputDialog,QLineEdit,QDoubleSpinBox,\
                            QScrollArea

class StatusBar(QStatusBar):
     def __init__(self, ):
         super().__init__()
         pass
         #self.layout = QHBoxLayout()
         #self.setLayout(self.layout)
         status_widget = QWidget()
         layout = QHBoxLayout(status_widget)

         self.label = QLabel("Status")
         layout.addWidget(self.label)
         layout.addStretch()
         self.info = QLabel("Info")
         layout.addWidget(self.info)
         self.timelabel = QLabel("Time")
         layout.addWidget(self.timelabel)
         self.fpslabel = QLabel("FPS")
         layout.addWidget(self.fpslabel)
         #self.addWidget(status_widget)
         self.addPermanentWidget(status_widget,2)
    
     def set(self, text):
         self.label.setText(text)

     def settime(self,t):
         self.timelabel.setText("Time:"+str(t))

     def setFPS(self,f):
         self.fpslabel.setText(f"FPS:{f:3.2f}")


     def setinfo(self,info):
         self.info.setText(info)