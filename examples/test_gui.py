import sys 
import os

from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox

sys.path.append(os.path.abspath('C:/Users/matt/Dropbox/Git/robodk-gui/src'))
from parsejson2gui import *
from creategui import *

#variable initialization
#structure as a dict to pass
#to the gui object
var_pack = {
    "RUN_PROG" : True,
    "DROP_LOC" : 1,
    "TABLE_NAME" : "bin_table",
    "PICKOBJ_NAME" : "box",
    "ROBOT_NAME" : "Fanuc R-1000iA/80F Base",
    "IN_EMPTY" : False,
    "SORT" : False
}

#start rdk api
#for loading and saving attributes
#in robodk file.
RDK = Robolink()

#initialize tkinter object
#needs to be global to access event functions
gui = tkGUI("Test GUI!")


#create button event
def move_to_table():
    #update varibles from gui
    gui.updateVars()
    #save in robodk instance to retain
    #memory
    gui.saveVars(RDK)

    import time
    gui.ShowMsg("running...", "NOTIFY_MSG", RDK)
    gui.updateProgress("PROG_BAR", 0)
    time.sleep(1)

    gui.updateProgress("PROG_BAR", 20)
    time.sleep(1)

    gui.updateProgress("PROG_BAR", 40)
    time.sleep(1) 
  
    gui.updateProgress("PROG_BAR", 50)
    time.sleep(1) 
  
    gui.updateProgress("PROG_BAR", 60)
    time.sleep(1) 
  
    gui.updateProgress("PROG_BAR", 80)
    time.sleep(1) 
    gui.updateProgress("PROG_BAR", 100)

    gui.ShowMsg("Finished!", "NOTIFY_MSG", RDK)


def main():

    #initialize gui
    objList = guiparse("../examples/test_gui.json")
    #load variables from rdk to tkGUI
    gui.loadVars(objList.members, RDK, var_pack, use_defaults=False)
    gui.build()
    #button has to be defined outside of gui object as it depends on
    # function 'move_to_table' to operate
    Button(gui.root, text='Update', font=font.Font(family='Helvetica', size=18, weight=font.BOLD), width=20, height=4, command=move_to_table, bg='green').pack()

    gui.root.mainloop()


if __name__ == '__main__':
    main()
