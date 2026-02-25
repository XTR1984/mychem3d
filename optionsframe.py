from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
                            QVBoxLayout, QWidget, QShortcut,QHBoxLayout,QStatusBar, \
                            QSlider,QFileDialog, QMessageBox,QLabel,QDialog,QCheckBox, \
                            QMenu,QComboBox,QPushButton,QInputDialog,QLineEdit,QDoubleSpinBox,\
                            QScrollArea

from PyQt5.QtCore import Qt


class OptionsFrame(QDialog):
    def __init__(self, app):
        super().__init__()
        self.space = app.space
        self.glframe = app.glframe
        self.setWindowTitle("Fine tuning (options)")
        self.setFixedSize(420, 500)

        main_layout = QVBoxLayout()

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        options_widget = QWidget()
        self.options_layout = QVBoxLayout(options_widget)

        # Создание слайдеров и меток
        self.create_slider("Update delta", 1, 150, self.space.update_delta, self.set_delta)
        self.create_slider("Charge koeff", 0, 5000, int(self.space.CHARGE_KOEFF), self.set_chargek)
        self.create_slider("Spin koeff", 0, 200, int(self.space.SPIN_KOEFF), self.set_spink)
        self.create_slider("Repulsion sigma", -15, 50, int(self.space.REPULSION_SIGMA), self.set_repulsek1)
        self.create_slider("Repulsion power", 1, 15, int(self.space.REPULSION_POW), self.set_repulsek2)
        self.create_slider("Repulsion eps", 1, 300, int(self.space.REPULSION_EPS*100), self.set_repulsek3)
        self.create_slider("Attracion koeff", 0, 200, int(self.space.ATTRACTION_KOEFF), self.set_attraction)
        self.create_slider("Bond koeff", 0, 500, self.space.BOND_KOEFF, self.set_bondk)
        self.create_slider("Rotation koeff", 1, 200, int(self.space.ROTA_KOEFF), self.set_rotk)
        self.create_slider("Mass koeff", 1, 50, self.space.MASS_KOEFF, self.set_massk)
        self.create_slider("E-Field koeff", 1, 100, self.space.FIELD_KOEFF, self.set_fieldk)
        self.create_slider("Stickybox", 0, 100, self.space.stickybox, self.set_stickybox)
        self.create_slider("Select expand param", 20, 500, self.space.select_param, self.set_selectparam)
        self.sizex = self.create_slider("Container size X", 1, 50, int(self.space.WIDTH / 100), self.set_size)
        self.sizey = self.create_slider("Container size Y", 1, 50, int(self.space.HEIGHT / 100), self.set_size)
        self.sizez = self.create_slider("Container size Z", 1, 50, int(self.space.DEPTH / 100), self.set_size)
        self.create_field("TDELTA", 0.0, 1.0, self.space.TDELTA, self.set_tdelta)

        self.show_nodes_checkbox = QCheckBox("Show nodes")
        self.show_nodes_checkbox.setChecked(self.glframe.drawnodes)
        self.show_nodes_checkbox.stateChanged.connect(self.set_shownodes)
        self.options_layout.addWidget(self.show_nodes_checkbox)

        self.double_radius_checkbox = QCheckBox("Double radius")
        self.double_radius_checkbox.setChecked(self.glframe.nicefactor==2.0)
        self.double_radius_checkbox.stateChanged.connect(self.set_doubleradius)
        self.options_layout.addWidget(self.double_radius_checkbox)


        self.side_heat_checkbox = QCheckBox("Side heat")
        self.side_heat_checkbox.setChecked(self.space.sideheat)
        self.side_heat_checkbox.stateChanged.connect(self.set_sideheat)
        self.options_layout.addWidget(self.side_heat_checkbox)

        self.options_layout.addStretch(1)
        
        scroll_area.setWidget(options_widget)
        
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def create_field(self, label_text, min_value, max_value, initial, callback):
        field_frame = QWidget()
        h_layout = QHBoxLayout(field_frame)
        self.options_layout.addWidget(field_frame)
        label = QLabel(label_text)
        h_layout.addWidget(label)
        input_field = QDoubleSpinBox(self)
        input_field.setRange(min_value, max_value)
        input_field.setDecimals(5)
        input_field.setSingleStep(0.1)
        input_field.setValue(initial)
        input_field.valueChanged.connect(callback)
        h_layout.addWidget(input_field)

    def create_slider(self,label_text, min_value, max_value, initial_value, callback):
        slider_frame = QWidget()
        h_layout = QHBoxLayout(slider_frame)
        self.options_layout.addWidget(slider_frame)
        label = QLabel(label_text)
        h_layout.addWidget(label)

        slider = QSlider()
        slider.setOrientation(1)  # 1 - горизонтальный
        slider.setRange(min_value, max_value)
        slider.setValue(int(initial_value))
        slider.valueChanged.connect(callback)
        slider.setPageStep(1)
        h_layout.addWidget(slider)
        label = QLabel(str(slider.value()))
        h_layout.addWidget(label)
        slider.valueChanged.connect(lambda  value: label.setText(str(value)))
        return slider

    def set_tdelta(self,value):
        self.space.TDELTA = float(value)
        self.glframe.update_uniforms = True

    def set_delta(self, value):
        self.space.update_delta = int(value)


    def set_chargek(self, value):
        self.space.CHARGE_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_spink(self, value):
        self.space.SPIN_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_stickybox(self, value):
        self.space.stickybox = float(value)
        self.glframe.update_uniforms = True


    def set_repulsek1(self, value):
        self.space.REPULSION_SIGMA = float(value)
        self.glframe.update_uniforms = True

    def set_repulsek2(self, value):
        self.space.REPULSION_POW = float(value)
        self.glframe.update_uniforms = True

    def set_repulsek3(self, value):
        self.space.REPULSION_EPS = float(value)*0.01
        self.glframe.update_uniforms = True


    def set_attraction(self, value):
        self.space.ATTRACTION_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_bondk(self, value):
        self.space.BOND_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_rotk(self, value):
        self.space.ROTA_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_massk(self, value):
        self.space.MASS_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_fieldk(self, value):
        self.space.FIELD_KOEFF = float(value)
        self.glframe.update_uniforms = True

    def set_sideheat(self,checked):
        if checked:
            self.space.sideheat = True
        else:
            self.space.sideheat = False
        self.glframe.update_uniforms = True

    

    def set_shownodes(self,checked):
        if checked:
            self.glframe.drawnodes = True
        else:
            self.glframe.drawnodes = False

    def set_doubleradius(self,checked):
        if checked:
            self.glframe.nicefactor = 2.0
        else:
            self.glframe.nicefactor = 1.0

    def set_selectparam(self,value):
        self.space.select_param=value 

    def set_size(self, value):
        sx = self.sizex.value()
        sy = self.sizey.value()
        sz = self.sizez.value()
        self.space.setSize(sx * 100, sy * 100, sz * 100)
        self.space.glframe.updateContainerSize()
        self.glframe.update_uniforms = True
