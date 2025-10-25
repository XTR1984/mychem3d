#!/usr/bin/python3.9
import time
from math import sin,cos,log,sqrt
import os, sys
import json
from json import encoder
from PIL import ImageGrab
from mychem_atom import Atom
from mychem_space import Space
from mychem_gl import GLWidget
from mychem_functions import OnOff,UndoStack,bond_atoms,double_info
import glm
import random
import OpenGL.GL as gl
from molex import load_sdf
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, \
                            QVBoxLayout, QWidget, QShortcut,QHBoxLayout,QStatusBar, \
                            QSlider,QFileDialog, QMessageBox,QLabel,QDialog,QCheckBox, \
                            QMenu,QComboBox,QPushButton,QInputDialog,QLineEdit,QDoubleSpinBox,\
                            QScrollArea

from PyQt5.QtCore import Qt

class mychemApp(QApplication):
    def __init__(self,a=[]):
        super().__init__(a)
        self.space = Space()

    def run(self):
        self.root = MainWindow(self, self.space)
        self.space.pause = True
        self.exec()


class MainWindow(QMainWindow):
    def __init__(self,app,space):
        super(MainWindow, self).__init__()
        self.app = app
        self.space = space
        self.resetdata = self.space.make_export()
        self.setWindowTitle("MyChem 3D")
        self.undostack = UndoStack(limit=30)
        self.init_menu()
        self.lastX = 512
        self.lastY = 300
        self.motion = False
        self.optionsframe = None
        #QShortcut( '1', self ).activated.connect(self.handle_add_atom2)
        #QShortcut( '2', self ).activated.connect(self.handle_add_atom2)
        #QShortcut( '3', self ).activated.connect(self.handle_add_atom2)
        #QShortcut( '4', self ).activated.connect(self.handle_add_atom2)        
        #QShortcut( '5', self ).activated.connect(self.handle_add_atom2)
        #QShortcut( '6', self ).activated.connect(self.handle_add_atom2)
        #QShortcut( 'Space', self ).activated.connect(self.handle_space)
        #QShortcut( 'Alt+r', self ).activated.connect(self.handle_reset)
        #QShortcut( 'Alt+i', self ).activated.connect(self.handle_invert)
        #QShortcut( 'Alt+n', self ).activated.connect(self.file_new)        
        #QShortcut( 'Alt+o', self ).activated.connect(self.file_open)        
        #QShortcut( 'Alt+s', self ).activated.connect(self.file_save)                
        #QShortcut( 'Alt+o', self ).activated.connect(self.file_open)                
        #QShortcut( 'm', self ).activated.connect(self.file_merge)                
        #QShortcut( 'l', self ).activated.connect(self.file_merge_recent)                
        #QShortcut( 'Ctrl+Alt+s', self ).activated.connect(self.file_save_selected)                        
        #self..bind("<Button-1>", self.handle_mouseb1)
        #self.bind("<Button-2>", self.handle_mouseb2)
        #self.bind("<Button-3>", self.handle_mouseb3)
        QShortcut( 'Enter', self ).activated.connect(self.handle_enter)                
        QShortcut( 'Esc', self ).activated.connect(self.handle_escape)                
        QShortcut( 'Delete', self ).activated.connect(self.handle_delete)                
        #QShortcut( 's', self ).activated.connect(self.handle_shake)                        
        QShortcut( 'x', self ).activated.connect(lambda : self.handle_movemode("x"))                        
        QShortcut( 'y', self ).activated.connect(lambda : self.handle_movemode("y"))                        
        QShortcut( 'z', self ).activated.connect(lambda : self.handle_movemode("z"))                        
        QShortcut( 'r', self ).activated.connect(lambda : self.handle_movemode("r"))                        
        QShortcut( 'g', self ).activated.connect(lambda : self.handle_movemode("g"))                        
        QShortcut( 'a', self ).activated.connect(self.handle_axis)                                
        QShortcut( 'b', self ).activated.connect(self.handle_bond)                                
        QShortcut( 'f', self ).activated.connect(self.handle_fix) 
        QShortcut( 'u', self ).activated.connect(self.handle_unfix) 
        QShortcut( 'Alt+t', self ).activated.connect(self.handle_test) 
        #QShortcut( 'Alt+l', self ).activated.connect(self.handle_random_recent) 
        #QShortcut( 'Alt+g', self ).activated.connect(self.handle_gravity) 
        QShortcut( 'Ctrl+z', self ).activated.connect(self.handle_undo)         
        #QShortcut( '0', self ).activated.connect(self.handle_zero)         
        #self.bind("<Map>", self.handle_mapunmap)
        #self.bind("<Unmap>", self.handle_mapunmap)
        self.qw = QWidget(self)
        self.layout = QHBoxLayout()
        self.glframe = GLWidget(space)        
        self.glframe.main = self
        self.layout.addWidget(self.glframe)
        self.qw.setLayout(self.layout)
        self.resize(1024, 600)
        self.setCentralWidget(self.qw)
        #self.glframe.bind("<B1-Motion>", self.handle_mouse1move)
        #self.glframe.bind("<B3-Motion>", self.handle_mouse3move)
        #self.glframe.bind("<Motion>", self.handle_motion)
        #self.glframe.bind("<ButtonRelease-1>", self.handle_release1)
        #self.glframe.bind("<MouseWheel>", self.handle_scroll)
        self.space.glframe = self.glframe
        print("glframe created")
        self.recentdata = None
        self.merge_mode = False
        self.ttype = "mx"
        self.heat = QSlider()
        self.heat.setMinimum(-150)
        self.heat.setMaximum(150)
        self.heat.setMinimumHeight(300)
        self.heat.setMaximumWidth(20)
        self.heat.valueChanged.connect(self.setHeat)
        self.heat.setPageStep(1)
        self.heat.setOrientation(0)
        self.layout.addWidget(self.heat)
        self.status_bar = StatusBar()
        self.setStatusBar(self.status_bar)
        self.glframe.status_bar = self.status_bar
        if not os.path.exists('output'):
            os.makedirs('output')
        if not os.path.exists('output/data'):
            os.makedirs('output/data')
        #self.run()
        self.showMaximized()
        self.show()
        self.status_bar.set("Ready")


    def init_menu(self):
        space:Space
        self.menu_bar = self.menuBar()
        file_menu = self.menu_bar.addMenu("File")
        file_menu.addAction(QAction('New', self, triggered=self.file_new, shortcut='Alt+N'))
        file_menu.addAction(QAction('Open', self, triggered=self.file_open, shortcut='o'))
        file_menu.addAction(QAction('Import SDF (limited)', self, triggered=self.file_import))
        file_menu.addAction(QAction('Merge', self, triggered=self.file_merge, shortcut='m'))
        file_menu.addAction(QAction('Merge recent', self, triggered=self.file_merge_recent, shortcut='l'))        
        file_menu.addAction(QAction('Merge recent random X', self, triggered=self.handle_random_recent, shortcut='Alt+l'))        
        file_menu.addAction(QAction('Save', self, triggered=self.file_save, shortcut='Alt+s'))
        file_menu.addAction(QAction('Save selected', self, triggered=self.file_save_selected, shortcut='Ctrl+Alt+s'))
        file_menu.addAction(QAction('Exit', self, triggered=self.file_exit, shortcut='Alt+Q'))        
        sim_menu = self.menu_bar.addMenu("Simulation")
        sim_menu.addAction(QAction("Go/Pause",self,triggered=self.handle_space, shortcut="Space"))
        sim_menu.addAction(QAction("Reset",self,triggered=self.handle_reset, shortcut="Alt+r"))
        sim_menu.addAction(QAction("Invert velocities",self,triggered=self.handle_invert, shortcut="Alt+i"))
        self.shake_action = QAction("Random shake",self,triggered=self.handle_shake, shortcut="s",checkable=True)
        sim_menu.addAction(self.shake_action)
        self.shake_action.setChecked(self.space.shake)
        
        self.gravity_action = QAction("Gravity",self,triggered=self.handle_gravity, shortcut="Alt+g",checkable=True)
        self.gravity_action.setChecked(self.space.gravity)
        sim_menu.addAction(self.gravity_action)
        
        self.efield_action = QAction("E-field",self,triggered=self.handle_efield, shortcut="Alt+e",checkable=True)
        self.efield_action.setChecked(self.space.efield)
        sim_menu.addAction(self.efield_action)

        self.highlight_unbond_action = QAction("Highlight unbond",self,triggered=self.handle_highlight_unbond, checkable=True)        
        self.highlight_unbond_action.setChecked(self.space.highlight_unbond)
        sim_menu.addAction(self.highlight_unbond_action)
        self.redox_action = QAction("Two zone redox",self,triggered=self.handle_redox,checkable=True)
        self.redox_action.setChecked(self.space.redox)
        sim_menu.addAction(self.redox_action)
        self.recording_action = QAction("Record image",self,triggered=self.handle_recording,checkable=True)
        self.recording_action.setChecked(self.space.recording)
        sim_menu.addAction(self.recording_action)
        self.record_data_action = QAction("Record data",self,triggered=self.handle_record_data,checkable=True)
        self.record_data_action.setChecked(self.space.record_data)
        sim_menu.addAction(self.record_data_action)
        sim_menu.addAction(QAction("Clear records",self,triggered=self.handle_clear_records))
        add_menu = self.menu_bar.addMenu("Add")
        add_menu.addAction(QAction("H",self,triggered=lambda:self.handle_add_atom(keysym="1"), shortcut="1"))
        add_menu.addAction(QAction("O",self,triggered=lambda:self.handle_add_atom(keysym="2"), shortcut="2"))
        add_menu.addAction(QAction("N",self,triggered=lambda:self.handle_add_atom(keysym="3"), shortcut="3"))
        add_menu.addAction(QAction("C",self,triggered=lambda:self.handle_add_atom(keysym="4"), shortcut="4"))
        add_menu.addAction(QAction("P",self,triggered=lambda:self.handle_add_atom(keysym="5"), shortcut="5"))
        add_menu.addAction(QAction("S",self,triggered=lambda:self.handle_add_atom(keysym="6"), shortcut="6"))
        add_menu.addAction(QAction("Mixer",self,triggered=self.handle_zero, shortcut="0"))
        self.menu_bar.addAction(QAction("Options",self,triggered=self.options_window ))
        examples_menu = self.menu_bar.addMenu("Examples")
        self.create_json_menu(examples_menu,"examples/")


    def create_json_menu(self,menu, lpath):
        files_last = []
        for filename in sorted(os.listdir(lpath)):
            filepath = os.path.join(lpath, filename)
            if os.path.isdir(filepath):
                submenu = menu.addMenu(filename)
                self.create_json_menu(submenu, filepath)
            elif os.path.splitext(filename)[-1] == ".json":
                files_last.append((filename,filepath))
        for (f,p) in files_last:				
            menu.addAction(QAction(f,self,triggered=lambda _state,p2=p: self.file_merge(p2) ))

    
    def handle_undo(self):
        print("Undo")
        data = self.undostack.pop()
        if data is not None:
            self.space.load_data(data)
            self.resetdata = data
            self.space.atoms2compute()
            self.status_bar.set('Undo')

    def setHeat(self, value):
        self.space.heat = value
        self.status_bar.set('heat = ' + str(value))
        self.glframe.update_uniforms = True

    def handle_test(self,checked):
        self.space.test = not self.space.test
        self.glframe.update_uniforms = True            

    def handle_efield(self,checked):
        if checked:
            self.space.efield = True
        else:
            self.space.efield = False
        self.status_bar.set("E-field is "+ OnOff(self.space.efield))            
        self.glframe.update_uniforms = True            


    def sim_run(self):
        self.space.pause = False
        self.glframe.start = time.time()
        self.glframe.nframes = 0
        self.unselect()
        self.status_bar.set("Running")

    def sim_pause(self):
        self.space.compute2atoms()
        self.space.pause = True
        #self.glframe.animate = 0
        self.status_bar.settime(self.space.t)
        self.update_status()
        self.status_bar.set("Paused")


    def update_status(self):
        N = len(self.space.atoms)
        info = f"Number of atoms: {N}, Ek={self.space.Ek:.2f}"
        if (N!=0): info += f" Ekavg={self.space.Ek/len(self.space.atoms):.2f} "
        self.status_bar.setinfo(info )


    def handle_recording(self,checked):
        if checked:
            self.space.recording = True
            if not os.path.exists('output/data'):
                os.makedirs('output/data')
        else:
            self.space.recording = False
        self.status_bar.set("Recording frames to disk is "+ OnOff(self.space.recording))

    def handle_record_data(self,checked):
        if checked:
            self.space.record_data = True
            if not os.path.exists('output/data'):
                os.makedirs('output/data')
        else:
            self.space.record_data = False
        self.status_bar.set("Recording dataframes to disk is "+ OnOff(self.space.record_data))

    def handle_clear_records(self,event=None):
            print("Delete records")
            self.glframe.rframes = 0
            directory_to_clean = 'output/'
            for filename in os.listdir(directory_to_clean):
                file_path = os.path.join(directory_to_clean, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print("Cannot delete {}".format(file_path), e)

            directory_to_clean = 'output/data/'
            for filename in os.listdir(directory_to_clean):
                file_path = os.path.join(directory_to_clean, filename)
                try:
                    if os.path.isfile(file_path):
                        os.unlink(file_path)
                except Exception as e:
                    print("Cannot delete {}".format(file_path), e)
        
    def handle_space(self,event=None):
        if self.space.pause:
            self.sim_run()
        else:
            self.sim_pause()

    
    def handle_g(self):
        self.handle_movemode("g")

    def handle_r(self):
        self.handle_movemode("r")



    def unselect(self):
        self.space.select_mode = 0
        self.space.selected_atoms = []

    def selectmode(self,m):
        self.merge_mode = False
        self.merge_atoms = []
        self.space.select_mode = m
    
    def mergemode(self):
        self.unselect()
        self.merge_mode = True
        self.space.merge_center = self.space.get_mergeobject_center()
        print(self.space.merge_center)


    def mergefinish(self):
        pass

    

    def handle_movemode(self,keysym):
        if self.space.select_mode:
           self.undostack.push(self.space.make_export())
           self.space.selected2merge()
           self.space.atoms2compute()
           self.mergemode()
        if not self.merge_mode: return
        if keysym == "r":
           self.ttype = "r" + self.ttype[1]
           self.status_bar.set("Rotate "+ self.ttype[1] )
           return
        if keysym == "g":
           self.ttype ="m" + self.ttype[1]
           self.status_bar.set("Move "+ self.ttype[1] )
           return
#        if keysym == "a":
#           self.ttype ="ra" 
#           self.status_bar.set("Rotate by defined axis" )
#           return
        self.ttype=self.ttype[0]
        if keysym == "x":
            self.ttype+="x"
        if keysym == "y":
            self.ttype+="y"
        if keysym == "z":
            self.ttype+="z"
        if keysym == "a":
            self.ttype="ra"
        if self.ttype[0]=="r":
            self.status_bar.set("Rotate "+ self.ttype[1] )
        else:
            self.status_bar.set("Move "+ self.ttype[1] )

    def handle_axis(self):
        if self.space.select_mode:
            if len(self.space.selected_atoms)==1:
                a=self.space.atoms[self.space.selected_atoms[0]]
                if not a.nodeselect==-1:
                    self.space.axis = glm.normalize(a.get_node_rpos(a.nodeselect))
                    self.space.axis_origin = a.pos
        self.handle_movemode("a")


    def handle_shake(self,checked):
        if checked:
            self.space.shake = True
        else:
            self.space.shake = False
        self.status_bar.set("Random shake is "+ OnOff(self.space.shake))
        self.glframe.update_uniforms = True

    def handle_redox(self,checked):
        if checked:
            self.space.redox = True
        else:
            self.space.redox = False
        self.status_bar.set("Two zone redox is "+ OnOff(self.space.redox))
        self.glframe.update_uniforms = True

    def handle_gravity(self,checked):
        if checked:
            self.space.gravity = True
        else:
            self.space.gravity = False
        self.status_bar.set("Gravity is "+ OnOff(self.space.gravity))
        self.glframe.update_uniforms = True

    def handle_highlight_unbond(self,checked):
        if checked:
            self.space.highlight_unbond = True
        else:
            self.space.highlight_unbond = False
        self.status_bar.set("Unbond highlight is "+ OnOff(self.space.highlight_unbond))
        self.glframe.update_uniforms = True


    def handle_zero(self,event=None):
        self.space.compute2atoms()
        self.undostack.push(self.space.make_export())
        self.space.appendmixer(1)
        #self.resetdata = self.space.make_export()
        self.space.atoms2compute()


    def handle_bondlock(self,checked):
        if checked:
            self.space.bondlock = True
        else:
            self.space.bondlock = False
        self.status_bar.set("Bondlock is "+ OnOff(self.space.bondlock))
        self.glframe.update_uniforms = True


    def file_new(self,event=None):
        self.space.t = -1
        self.glframe.nframes = 0
#        self.recordtime = 0
        self.sim_pause()
        self.space.atoms = []	
        self.space.mixers = []
        self.space.merge_pos = self.space.box/2
        self.space.merge_rot = glm.quat()
        self.space.merge_atoms = []
        self.unselect()
        self.merge_mode = False
        self.status_bar.set("New file")

    def file_open(self,event=None):
        fileName, _filter = QFileDialog.getOpenFileName(self,"Select file", "", "Json files (*.json)")
        print(fileName)
        if not fileName:	
            return
        self.file_new()
        f =  open(fileName,"r")		
        self.resetdata = json.loads(f.read())
        self.space.load_data(self.resetdata)
        self.space.atoms2compute()
        self.status_bar.set("File loaded")
        f.close()



    def file_merge(self,path=None):
        self.sim_pause()
        self.undostack.push(self.space.make_export())
        print("Merge path=",path)
        if path:
            fileName=path
        else:
            fileName, _filter = QFileDialog.getOpenFileName(self,"Select file", "", "Json files (*.json)")
            if not fileName:	
                return
        f =  open(fileName,"r")		
        self.space.merge_atoms = []
        mergedata = json.loads(f.read())
        self.recentdata = mergedata
        r = self.space.load_data(mergedata, merge=True)
        self.space.move_atoms(self.space.merge_atoms,(self.space.box/2-self.space.get_mergeobject_center()))
        self.mergemode()
                              

        #self.space.atoms2compute()
        #self.canvas.configure(cursor="hand2")
        if r: 
            self.status_bar.set("import errors!  Merging mode")            
            QMessageBox.warning(self,"error",f"Import errors, check console!")

        else:
            self.status_bar.set("Merging mode")
        f.close()

# https://www.molinstincts.com/
    def file_import(self,event=None, path=None):
        self.sim_pause()
        if path:
            print(path)
            fileName=path
        else:
            #fileName = filedialog.askopenfilename(title="Select file", filetypes=(("SDF", "*.sdf"), ("All Files", "*.*")))
            fileName, _filter = QFileDialog.getOpenFileName(self,"Select file", "", "SDF (*.sdf *.mol);;All files(*.*)")
            if not fileName:	
                return
        f =  open(fileName,"r")		
        self.space.merge_atoms = []
#        try:
        result = load_sdf(f,self.space.merge_atoms)
        f.close()
        mergedata = self.space.make_export(self.space.merge_atoms)
#        except Exception as e:
#            print(e)
#            print("Fail to load sdf")


        self.recentdata = mergedata
        self.mergemode()
        self.space.atoms2compute()
        if result:
            self.status_bar.set("Imported")
        else:
            self.status_bar.set("Imported with errors")




    def file_merge_recent(self,event=None):
        if not self.recentdata:
            return
        self.sim_pause()
        self.undostack.push(self.space.make_export())
        self.space.merge_atoms = []
        self.space.load_data(self.recentdata, merge=True)
        #self.space.atoms2compute()
        self.space.merge_pos+=glm.vec3(20,0,0)    
        self.space.move_atoms(self.space.merge_atoms,(self.space.box/2-self.space.get_mergeobject_center()))
        self.mergemode()
        self.status_bar.set("Merging mode")
        self.update_status()
        
    def handle_random_recent(self,event=None):
        if not self.recentdata:
            return
        self.sim_pause()
        self.undostack.push(self.space.make_export())
        self.space.load_data(self.recentdata, merge=True)
        self.unselect()
        (center,distant) = self.space.get_atoms_distant(self.space.merge_atoms)
        number, ok = QInputDialog.getInt(None, "Input number", "How many?")        
        if not ok :
            return
        for i in range(0,number):
            self.space.merge_atoms = []
            distant = glm.round(distant)
            x= random.randint(distant.x+10,self.space.WIDTH-distant.x-10)
            y= random.randint(distant.y+10,self.space.HEIGHT-distant.y-10)
            z= random.randint(distant.z+10,self.space.DEPTH-distant.z-10)
            self.space.load_data(self.recentdata, merge=True)
            ##self.space.move_atoms(self.space.merge_atoms,(self.space.box/2-self.space.get_mergeobject_center()))
            self.space.move_atoms(self.space.merge_atoms, glm.vec3(x,y,z)-self.space.get_mergeobject_center())
            f = random.random()*3.1415
            rot = glm.normalize(glm.quat(cos(f/2), sin(f/2)* glm.vec3(random.random(),random.random(),random.random())))
            c = self.space.get_mergeobject_center()
            self.space.rotate_atoms(self.space.merge_atoms, c, rot)
            self.space.merge_rot = rot
            self.space.merge2atoms()
        self.space.merge_pos = self.space.box/2
        self.space.merge_rot = glm.quat()
        self.resetdata = self.space.make_export()
        self.space.atoms2compute()
        self.merge_mode = False
        self.update_status()



    def file_save(self,event=None):
        self.sim_pause()
        fileName, _filter = QFileDialog.getSaveFileName(self,"Select file", "", "Json files (*.json)")
        if not (fileName.endswith(".json") or fileName.endswith(".JSON")):
            fileName+=".json"
        f = open(fileName, "w")
        self.resetdata = self.space.make_export()
        f.write(json.dumps(self.resetdata))
        f.close()
        self.status_bar.set("File saved")

    def file_save_selected(self,event=None):
        if self.space.select_mode==1 and len(self.space.selected_atoms)>0:
            atoms = []
            for i in self.space.selected_atoms:
                atoms.append(self.space.atoms[i])
            center = self.space.get_atoms_center(atoms)                
            for a in atoms:
                a.pos -= center
            fileName, _filter = QFileDialog.getSaveFileName(self,"Select file", "", "Json files (*.json)")
            if not (fileName.endswith(".json") or fileName.endswith(".JSON")):
                fileName+=".json"
            f = open(fileName, "w")
            export = self.space.make_export(atoms)
            f.write(json.dumps(export))
            f.close()
            self.status_bar.set("File saved")
            self.unselect()

    def handle_fix(self,event=None):
        if self.space.select_mode:
            self.space.compute2atoms()
            for s in self.space.selected_atoms:
                self.space.atoms[s].fixed = True
            self.space.atoms2compute()
            self.status_bar.set("fix selected atoms")

    def handle_unfix(self,event=None):
        if self.space.select_mode:
            self.space.compute2atoms()
            for s in self.space.selected_atoms:
                self.space.atoms[s].fixed = False
            self.space.atoms2compute()
            self.status_bar.set("unfix selected atoms")
    
    def handle_duplicate(self,event=None):
        if self.space.select_mode:
            self.undostack.push(self.space.make_export())
            self.space.selected2merge(duble=True)
            self.space.move_atoms(self.space.merge_atoms, glm.vec3(30,0,0))
            self.mergemode()
            

    def handle_mouseb3(self,event=None):
        if self.space.select_mode:
            self.space.compute2atoms()
            self.atom_context_menu = QMenu(self)
            if len(self.space.selected_atoms)==2:
                self.atom_context_menu.addAction(QAction("Bond", self, triggered=self.handle_bond))
            self.atom_context_menu.addAction(QAction("Duplicate", self, triggered=self.handle_duplicate))
            self.atom_context_menu.addAction(QAction("Move", self, triggered=self.handle_g))
            self.atom_context_menu.addAction(QAction("Rotate", self, triggered=self.handle_r))
            self.atom_context_menu.addAction(QAction("Set Merge position", self, triggered=self.handle_mergepos2selected))
            self.atom_context_menu.addAction(QAction("Fix", self, triggered=self.handle_fix))
            self.atom_context_menu.addAction(QAction("Unfix", self, triggered=self.handle_unfix))
            self.atom_context_menu.addAction(QAction("Delete", self, triggered=self.handle_delete))
            if len(self.space.selected_atoms)==1:
                #a = self.space.atoms[self.space.selected_atoms[0]]
                self.atom_context_menu.addAction(QAction("Properties", self, triggered=lambda: self.show_atom_properties(self.space.atoms[self.space.selected_atoms[0]])))
            #self.glframe.mapFromGlobal(self.mapToGlobal(event.pos()))
            self.atom_context_menu.exec_(event.pos())

    def show_atom_properties(self,a:Atom):
        ap = AtomProperties(self,a)
        if ap.exec_() == QDialog.Accepted:
            print("saved")
            self.space.atoms2compute()
        else:
            print("not saved")
    
    def handle_mergepos2selected(self):
        a = self.space.atoms[self.space.selected_atoms[0]]
        self.space.merge_pos = a.pos
        self.status_bar.set("Merge position moved to selected")

    def handle_bond(self,event=None):
        if self.space.select_mode==1 and len(self.space.selected_atoms)==2:
            r= bond_atoms(self.space.atoms[self.space.selected_atoms[0]],
                       self.space.atoms[self.space.selected_atoms[1]],
                       self.space.atoms[self.space.selected_atoms[0]].nodeselect,
                       self.space.atoms[self.space.selected_atoms[1]].nodeselect
                       )
            if r: 
                self.status_bar.set("Bond atoms ok")
                self.space.atoms[self.space.selected_atoms[0]].nodeselect=-1
                self.space.atoms[self.space.selected_atoms[1]].nodeselect=-1
                self.space.atoms2compute()
            else: 
                self.status_bar.set("Bond atoms fail")
                


    def file_exit(self,event=None):
        self.app.exit()

    def handle_cursor(self,event=None):
        if self.merge_mode: return
        if not self.space.pause: self.sim_pause()
        self.selectmode(1)
        N = len(self.space.atoms)
        if event.keysym == "Left":
            self.space.select_i -=1
            if self.space.select_i < 0:
                self.space.select_i=N-1
        if event.keysym == "Right":
            self.space.select_i +=1
            if self.space.select_i >=N:
                self.space.select_i =0

    def handle_reset(self,event=None):
        if not self.resetdata:
            return
        self.file_new()
        self.space.load_data(self.resetdata)
        self.space.atoms2compute()
        self.status_bar.set("Reset to previos loaded")

    def handle_invert(self,event=None):
        self.space.compute2atoms()
        for a in self.space.atoms:
            a.v = -a.v
            a.rotv = glm.inverse(a.rotv)
        self.space.atoms2compute()

    def handle_add_atom2(self,event=None):
        self.handle_add_atom(keysym=event.keysym)

    def handle_add_atom(self,keysym=""):
        self.sim_pause()
        if keysym in ["1","2","3","4","5","6"]:
           table = {1:1, 2:8, 3:7, 4:6, 5:15, 6:16 }
           createtype = table[int(keysym)]

        if self.space.select_mode==1:  #extending molecule by new atom
            self.undostack.push(self.space.make_export())
            if len(self.space.selected_atoms)>1:
                return
            a = self.space.atoms[self.space.selected_atoms[0]]
            if a.nodeselect==-1:
                a.select_first_unbond()
            n1i = a.nodeselect
            if a.nodes[n1i].bonded: return
            n1pos = a.get_node_rpos(n1i)
            a2 = Atom(500,500,500,createtype)
            a2.pos = a.pos + (a.r + a2.r)*glm.normalize(n1pos) 
            n2pos = a2.nodes[0].pos
            a2.rot = glm.quat(n2pos,-n1pos)
            bond_atoms(a,a2,n1i,0)
            a.select_first_unbond()
            a2.select_first_unbond()
            self.space.appendatom(a2)
            self.space.selected_atoms=[len(self.space.atoms)-1]
            self.space.atoms2compute()
            self.status_bar.set("Extended")
            

        else:
            self.undostack.push(self.space.make_export())
            self.space.merge_pos.x +=25
            self.ttype = "mx"
            if keysym in ["1","2","3","4","5","6"]:
                table = {1:1, 2:8, 3:7, 4:6, 5:15, 6:16 }
                createtype = table[int(keysym)]
                a = Atom(0,0,0,createtype)
            self.space.merge_atoms = [a]
            self.space.move_atoms(self.space.merge_atoms, self.space.merge_pos)
            self.mergemode()



    def handle_escape(self,event):
        if self.merge_mode:
            self.merge_mode = False
            self.space.merge_atoms = []


    def handle_delete(self,event=None):
        if self.merge_mode:
            self.undostack.push(self.space.make_export())
            self.resetdata = self.space.make_export()
            self.merge_mode = False
            self.space.merge_atoms = []
        if self.space.select_mode:
            self.undostack.push(self.space.make_export())
            self.space.selected2merge()
            self.space.merge_atoms = []
            #self.merge_mode = True
            self.space.atoms2compute()
            self.unselect()

    
    def mousePressEvent(self, event):
        pos = event.pos()
        self.lastX = pos.x()
        self.lastY = pos.y()
        #if event.button() == Qt.LeftButton:
        #    self.handle_mouseb1(event)
        #if event.button() == Qt.RightButton:
        #    self.handle_mouseb3(event)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.handle_release1(event)
        elif event.button() == Qt.RightButton:
            self.handle_mouseb3(event)
        elif event.button() == Qt.MiddleButton:
            self.handle_mouseb2(event)



    def handle_release1(self,event):
        if self.motion:
            self.motion = False
            return
        if self.merge_mode:
            self.handle_enter(event)
            self.update_status()
            return
        modifiers = event.modifiers() 
        shift = modifiers & Qt.ShiftModifier
        ctrl = modifiers & Qt.ControlModifier
        mpos = self.glframe.mapFromGlobal(self.mapToGlobal(event.pos()))
        #print(f"eventpos={event.pos()} glgrame.width={self.glframe.width()} glframe.height={self.glframe.height()} mpos={mpos}")
        self.space.compute2atoms()
        N = len(self.space.atoms)
        y = self.glframe.height() - mpos.y()
        self.glframe.makeCurrent()
        z = gl.glReadPixels(mpos.x(), y, 1, 1, gl.GL_DEPTH_COMPONENT, gl.GL_FLOAT)
        (x,y,z) = glm.unProject(glm.vec3(mpos.x(), y,z),self.glframe.view,self.glframe.projection, (0,0,self.glframe.width(),self.glframe.height()))
        pos = glm.vec3(x,y,z) / self.glframe.factor
        near_atom_i= -1
        for i in range(0,N):
             a = self.space.atoms[i] 
             d = glm.distance(a.pos,  pos)
             if d<=a.r+1:
                 near_atom_i=i
        if near_atom_i != -1:
            if not self.space.pause: self.sim_pause()
            self.space.atoms[near_atom_i].info()
            if ctrl:
                if near_atom_i in self.space.selected_atoms:
                    self.space.selected_atoms.remove(near_atom_i)    
                    self.show_selected_q()
                else:
                    self.space.selected_atoms.append(near_atom_i)
                    self.show_selected_q()
                if len(self.space.selected_atoms)==2:
                    double_info(self.space.atoms[self.space.selected_atoms[0]],self.space.atoms[self.space.selected_atoms[1]],self.space)
                    #self.space.atoms[self.space.selected_atoms[1]].select_first_unbond()
            else:
                if near_atom_i in self.space.selected_atoms:
                    self.handle_enter(event)
                    return
                self.space.selected_atoms = [near_atom_i]
                self.show_selected_q()
            self.selectmode(1)
            if self.space.atoms[self.space.selected_atoms[0]].nodeselect==-1:
                self.space.atoms[self.space.selected_atoms[0]].select_first_unbond()
            if len(self.space.selected_atoms)==2:
                if self.space.atoms[self.space.selected_atoms[1]].nodeselect==-1:
                    self.space.atoms[self.space.selected_atoms[1]].select_first_unbond()

        else:
            self.unselect()
        self.update_status()

    def show_selected_q(self):
            q = 0
            for i in self.space.selected_atoms:
                q+= self.space.atoms[i].q
            self.status_bar.set(f"q of selected = {q:.3f} ")
    
    def handle_enter(self,event):
        if self.space.select_mode==1:
            self.sim_pause()
            self.undostack.push(self.space.make_export())
            self.space.selected2merge()
            self.mergemode()
            self.space.atoms2compute()
            self.space.selected_atoms = []
            return
        if self.merge_mode:
            self.space.compute2atoms()
            #self.undostack.push(self.space.make_export())
            self.merge_mode = False 
            self.space.merge2atoms()
            self.resetdata = self.space.make_export()
            self.space.atoms2compute()
            #self.resetdata = self.space.make_export()
            self.status_bar.set("Merged")


    def handle_mouseb2(self,event):
        if self.space.select_mode:
            if len(self.space.selected_atoms)==1:
                self.space.atoms[self.space.selected_atoms[0]].select_next_node()
            #self.handle_enter(event)

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.handle_mouse1move(event)
        if event.buttons() & Qt.RightButton:
            self.handle_mouse3move(event)
        

    def handle_mouse1move(self,event):
        modifiers = event.modifiers() 
        shift = modifiers & Qt.ShiftModifier
        ctrl = modifiers & Qt.ControlModifier
        pos = event.pos()
        
        self.motion = True
        offsetx = pos.x() - self.lastX 
        offsety = pos.y() - self.lastY
        self.lastX = pos.x()
        self.lastY = pos.y()
        sense = 0.1
        if shift:
            sense = 0.01
        offsetx *= sense
        offsety *= sense
        self.glframe.pitch -=offsety
        self.glframe.yaw += offsetx
        if self.glframe.pitch > 89:
           self.glframe.pitch = 89
        if self.glframe.pitch < -89:
           self.glframe.pitch = -89
        #print(f'yaw={self.glframe.yaw} pitch{self.glframe.pitch} pos={self.glframe.cameraPos}')


    def handle_mouse3move(self,event):
        modifiers = event.modifiers() 
        shift = modifiers & Qt.ShiftModifier
        ctrl = modifiers & Qt.ControlModifier
        pos = event.pos()
        offsetx = pos.x() - self.lastX 
        offsety = pos.y() - self.lastY
        self.lastX = pos.x()
        self.lastY = pos.y()
        sense = 0.1
        if shift:        
            sense = 0.01
        offsetx *= sense
        offsety *= sense
        
        self.glframe.cameraPos -= glm.normalize(glm.cross(self.glframe.cameraFront, self.glframe.cameraUp)) * offsetx*0.05
        self.glframe.cameraPos += self.glframe.cameraUp * offsety*0.05



    def wheelEvent(self, event):
         delta = event.angleDelta().y()  # Получаем направление прокрутки
         modifiers = event.modifiers() 
         shift = modifiers & Qt.ShiftModifier
         ctrl = modifiers & Qt.ControlModifier
         if self.merge_mode and not ctrl:
            self.space.merge_center = self.space.get_mergeobject_center()
            if not shift:
                offset = 15
                angle = 5
            else:
                offset = 1
                angle = 1
            if delta>0:
                angle*=-1
                offset*=-1
            if self.ttype=="mx":
                self.space.move_atoms(self.space.merge_atoms, glm.vec3(-offset,0,0))
            if self.ttype=="my":
                self.space.move_atoms(self.space.merge_atoms, glm.vec3(0,-offset,0))
            if self.ttype=="mz":
                self.space.move_atoms(self.space.merge_atoms, glm.vec3(0,0,-offset))
            if self.ttype=="rx":
                self.space.rotate_atoms(self.space.merge_atoms, self.space.merge_center, glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(1,0,0))  )
            if self.ttype=="ry":
                self.space.rotate_atoms(self.space.merge_atoms, self.space.merge_center, glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(0,1,0))  )
            if self.ttype=="rz":
                self.space.rotate_atoms(self.space.merge_atoms, self.space.merge_center, glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*glm.vec3(0,0,1))  )
            if self.ttype=="ra":
                self.space.rotate_atoms(self.space.merge_atoms, self.space.axis_origin, glm.quat(cos(glm.radians(angle)), sin(glm.radians(angle))*self.space.axis) )
         elif self.space.select_mode==1: #select molecule
            if delta>0:
                new_selected = self.glframe.expand_selection(self.space.selected_atoms)
                self.space.selected_atoms += new_selected
                if len(self.space.selected_atoms)==2:
                    double_info(self.space.atoms[self.space.selected_atoms[0]],self.space.atoms[self.space.selected_atoms[1]],self.space)
            else:
                if len(self.space.selected_atoms)>0:
                    self.space.selected_atoms.pop()
                if len(self.space.selected_atoms)==0:
                    self.unselect()
            self.show_selected_q()
         else:
            if shift:
                cameraSpeed = 0.01
            else:
                cameraSpeed = 0.1
            if delta>0:
                self.glframe.cameraPos += cameraSpeed * self.glframe.cameraFront
            else:
                self.glframe.cameraPos -= cameraSpeed * self.glframe.cameraFront   

           

    def options_window(self):
        print("options")
        if not self.optionsframe == None:
            self.optionsframe.show()
            self.optionsframe.raise_()
        else:
            self.optionsframe = OptionsFrame(self)
            self.optionsframe.show()
            #self.optionsframe.exec()

    def closeEvent(self, event):  
        for window in QApplication.topLevelWidgets():
            if window != self:
                window.close()
        event.accept()
        


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
        self.create_slider("Interact koeff", 0, 10000, int(self.space.INTERACT_KOEFF), self.set_interk)
        self.create_slider("Repulsion sigma", -15, 50, int(self.space.REPULSION_SIGMA), self.set_repulsek1)
        self.create_slider("Repulsion power", 1, 15, int(self.space.REPULSION_POW), self.set_repulsek2)
        self.create_slider("Repulsion eps", 1, 300, int(self.space.REPULSION_EPS*100), self.set_repulsek3)
        self.create_slider("Attracion koeff", 0, 200, int(self.space.ATTRACTION_KOEFF), self.set_attraction)
        self.create_slider("Bond koeff", 1, 1000, self.space.BOND_KOEFF, self.set_bondk)
        self.create_slider("Rotation koeff", 1, 200, int(self.space.ROTA_KOEFF), self.set_rotk)
        self.create_slider("Mass koeff", 1, 50, self.space.MASS_KOEFF, self.set_massk)
        self.create_slider("E-Field koeff", 1, 100, self.space.FIELD_KOEFF, self.set_fieldk)
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


    def set_interk(self, value):
        self.space.INTERACT_KOEFF = float(value)
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


    def set_size(self, value):
        sx = self.sizex.value()
        sy = self.sizey.value()
        sz = self.sizez.value()
        self.space.setSize(sx * 100, sy * 100, sz * 100)
        self.space.glframe.updateContainerSize()
        self.glframe.update_uniforms = True

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

import traceback
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        sys.exit(0)
    #print(f"Exception: {exc_value}")
    traceback.print_last()
#sys.excepthook = handle_exception


if __name__ == '__main__':
    a = mychemApp()
    time.sleep(1)
    a.run()
    