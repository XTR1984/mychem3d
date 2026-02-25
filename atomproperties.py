from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
                            QVBoxLayout, QWidget, QShortcut,QHBoxLayout,QStatusBar, \
                            QSlider,QFileDialog, QMessageBox,QLabel,QDialog,QCheckBox, \
                            QMenu,QComboBox,QPushButton,QInputDialog,QLineEdit,QDoubleSpinBox,\
                            QScrollArea

from atom import Atom

class AtomProperties(QDialog):
    def __init__(self, parent, atom: Atom):
        super().__init__(parent)
        self.a = atom
        self.saved = False
        self.setWindowTitle("Atom properties")
        self.setFixedSize(420, 300)

        layout = QVBoxLayout(self)

        # Atom type
        self.type_frame = QHBoxLayout()
        self.type_frame.addWidget(QLabel("Atom type:"))
        self.type_frame.addWidget(QLabel(str(atom.type)))
        layout.addLayout(self.type_frame)

        # Position
        self.pos_frame = QHBoxLayout()
        self.pos_frame.addWidget(QLabel("Position:"))
        self.pos_frame.addWidget(QLabel(str(atom.pos)))
        layout.addLayout(self.pos_frame)

        # Charge
        self.q_frame = QHBoxLayout()
        self.q_frame.addWidget(QLabel("q = " + str(self.a.q)))
        layout.addLayout(self.q_frame)

        # Nodes
        self.fnodes = []
        self.nodes_frame = QVBoxLayout()
        self.nodes_label = QLabel("Nodes:")
        layout.addWidget(self.nodes_label)
        
        for i, node in enumerate(atom.nodes):
            node_frame = QHBoxLayout()
            node_frame.addWidget(QLabel("Type:"))
            node_frame.addWidget(QLabel(str(node.type)))
            node_frame.addStretch()
            node_frame.addWidget(QLabel("Spin:"))
            node_spin = QComboBox()
            node_spin.addItems(["-1", "0", "1"])
            node_spin.setCurrentText(str(int(node.spin)))
            node_spin.currentIndexChanged.connect(lambda _, x=i: self.node_spin_changed(x))
            node_frame.addWidget(node_spin)
            node_frame.addStretch()
            node_frame.addWidget(QLabel("q:"))
            node_q = QComboBox()
            node_q.addItems(["-1", "0", "1"])
            node_q.setCurrentText(str(int(node.q)))
            node_q.currentIndexChanged.connect(lambda _, x=i: self.node_q_changed(x))
            node_frame.addWidget(node_q)
            node_frame.addStretch()
            if atom.nodeselect == i:
                node_frame.addWidget(QLabel('Sel'))
            node_frame.addWidget(QLabel('Bonded: ' + str(node.bonded)))

            self.fnodes.append((node_spin, node_q))
            self.nodes_frame.addLayout(node_frame)

        layout.addLayout(self.nodes_frame)

        # Buttons
        self.button_frame = QHBoxLayout()
        self.button0 = QPushButton("OK")
        self.button0.clicked.connect(self.save)
        self.button_frame.addWidget(self.button0)

        self.button1 = QPushButton("Cancel")
        self.button1.clicked.connect(self.cancel)
        self.button_frame.addWidget(self.button1)

        layout.addLayout(self.button_frame)

    def node_q_changed(self, i):
        node_spin, node_q = self.fnodes[i]
        q = node_q.currentText()
        if q in ["-1", "1"]:
            new_spin = "0"
        elif q == "0":
            new_spin = "1"
        node_spin.blockSignals(True)
        node_spin.setCurrentText(new_spin)
        node_spin.blockSignals(False)

    def node_spin_changed(self, i):
        node_spin, node_q = self.fnodes[i]
        spin = node_spin.currentText()
        if spin in ["-1", "1"]:
            new_q = "0"
        elif spin == "0":
            new_q = "1"
        node_q.setCurrentText(new_q)

    def cancel(self):
        self.reject()

    def save(self):
        all_good = True
        for i, (node_spin, node_q) in enumerate(self.fnodes):
            q = float(node_q.currentText())
            spin = float(node_spin.currentText())
            if (q != 0.0 and spin != 0.0) or (q == 0.0 and spin == 0.0):
                QMessageBox.critical(self, "Error", f"Inconsistent spin and q for node {i}")
                all_good = False
                break
            self.a.nodes[i].q = q
            self.a.nodes[i].spin = spin
        if all_good:
            self.accept()
