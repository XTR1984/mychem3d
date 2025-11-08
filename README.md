Pseudochemical 3d simulator
- PyQt5 
- opengl 4.3 with compute shader used for parallel computation
- not release by now

for use install libraries:
- python -m pip install pillow numpy pyglm pyopengl pyqt5

Tested on:
- integrated Intel Iris Xe Graphics
- rx580 card

Be careful. This application may create misconceptions about chemical interactions

Controls:
-    Mouse + left button  -  rotate camera
-    Mouse + right button - move camera left and right
-     +shift - gently
-    Mouse wheel - move camera forward and back

 In merge mode (adding atoms or files):
- enter or click - do merge 
- mouse wheel - change parameter
- mouse wheel + shift - slow change
- mouse wheel + control - move camera forward and back
- g - move,  x,y,z for select axis
- r - rotate object, x,y,z for select rotate axis
- a - rotate object in special axis, setted in selection mode


Selection atoms
1. molecule and atoms selection mode
  -  click an atom, then use the mouse wheel to add neighboring bondes atoms to the selection
  -  shift for select unbonded atoms too with selection distance param (options) 
  -  ctrl + click  - append/remove to/from selection
  -  enter or click on selection - go to merge mode with selected atoms
  -  also "r" and "g" - go to merge mode with move and rotation
  -  <delete> - delete selected
  -  ctrl + alt + s - save selected atoms
  -  "b" - try to bond two selected atoms with selected nodes, resutl in statusbar
  -   middle button for change selected node in selected atom
  - Right mouse button on selected - context menu for actions
  - a new atom can be grown from the selected atom node using the numeric keys
  - "a" - set axis in direction of selected node

*qt5 issue*
issue error: could not find or load the Qt platform plugin "windows" in ""
resolution: set QT_QPA_PLATFORM_PLUGIN_PATH environment variable to %PythonPath%\Lib\site-packages\PyQt5\Qt5\plugins\platforms



Some examples:

!["demopic 1](images/demo1.PNG?raw=true )
!["demopic 2](images/demo2.JPG?raw=true )

