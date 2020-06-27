
# import gui tools
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.font as font

#import collection types
from tk_types import *

# tkinter helpers
# ----------------

class tkGUI:

    #private members

    #rdk load variables
    def _loadFloat(self, variable_name, robolink, uninit_vals, use_defaults=False):
        value = robolink.getParam(variable_name)
        if value is not None and not use_defaults:
            exec("self." + variable_name + " = " + str(value))
        elif variable_name in uninit_vals.keys():
            exec("self." + variable_name + "=" + str(uninit_vals[variable_name]))
        else:
            raise ValueError(variable_name + 'was not found.')


    def _loadBool(self, variable_name, robolink, uninit_vals, use_defaults=False):
        value = robolink.getParam(variable_name)
        if value is not None and not use_defaults:
            exec("self." + variable_name + " = " + str(value))
        elif variable_name in uninit_vals.keys():
            exec("self." + variable_name + "=" + str(uninit_vals[variable_name]))
    

    def _loadStr(self, variable_name, robolink, uninit_vals, use_defaults=False):
        value = robolink.getParam(variable_name)
        if value is not None and not use_defaults:
            exec("self." + variable_name + " = '" + value + "'")
        elif variable_name in uninit_vals.keys():
            exec("self." + variable_name + "='" + uninit_vals[variable_name]+ "'")
        else:
            raise ValueError(variable_name + 'was not found.')
    
    #rdk update variables
    #run before processing an event
    def _updateFloat(self, variable_name):
        exec("self.%s = float(self.txt%s.get())" % (variable_name, variable_name))

    def _updateBool(self, variable_name):
        exec("self.%s = bool(self.bool%s.get())" % (variable_name, variable_name))

    def _updateStr(self, variable_name):
        exec("self.%s = self.txt%s.get()" % (variable_name, variable_name))

    def _updateRadio(self, variable_name):
        exec("self.%s = self.txt%s.get()" % (variable_name, variable_name))

    #rdk save variables
    def _saveVar(self, variable_name, robolink):
        value = eval("self." + variable_name)
        robolink.setParam(variable_name, value)

    #public members

    def __init__(self, title):
        #initialize main windows
        self.root = Tk()
        self.root.title(title)
    
    def build(self):
        for m in self.members:
            if isinstance(m, tkvars):
                if m.type == 'BooleanVar':
                    self.createCheckbox(m.name, m.label, m.parent)
                else:
                    self.createTextbox(m.name, m.label, m.type, m.parent)
            if isinstance(m, tkframe):
                self.createframe(m.name, m.parent, m.toggle)
            if isinstance(m, tktoggle):
                self.createFrameToggle(m.name, m.label, m.trueframe, m.falseframe, m.parent)
            if isinstance(m, tkbutton):
                self.createButton(m.label, file=m.file, function=m.command, fnt=m.font, color=m.color, parent=m.parent,
                             fill=m.fill, expand=m.expand, side=m.side,
                             height=m.height, width=m.width)
            if isinstance(m, tkspacer):
                self.createSpacer(m.width, m.height, m.color, m.parent)
            if isinstance(m, tkdisp):
                self.createLabel(m.name, m.type, m.color, m.parent)
            if isinstance(m, tkradio):
                self.createRadioButtons(m.name, m.type, m.modes, m.parent)
            if isinstance(m, tkprogbar):
                self.createProgressBar(m.name, m.length, m.determinate, m.parent)

    #rdk functions

    def loadVars(self, members, robolink, uninit_vals, use_defaults = False):
        #store members in object
        self.members = members
        #load variables
        for m in members:
            if hasattr(m, 'type') and (isinstance(m, tkvars) or isinstance(m, tkradio) or isinstance(m, tktoggle)):
                if m.type == 'StringVar':
                    self._loadStr(m.name, robolink, uninit_vals, use_defaults)
                elif m.type == 'DoubleVar':
                    self._loadFloat(m.name, robolink, uninit_vals, use_defaults)
                elif m.type == 'IntVar':
                    self._loadFloat(m.name, robolink, uninit_vals, use_defaults)
                elif m.type == 'BooleanVar':
                    self._loadBool(m.name, robolink, uninit_vals, use_defaults)
    
    def saveVars(self, robolink):
        for m in self.members:
            if isinstance(m, tkvars) or isinstance(m, tkradio):
                self._saveVar(m.name, robolink)
            elif isinstance(m, tktoggle):
                self._saveVar(m.name, robolink)
    
    def updateVars(self):
        for m in self.members:
            if isinstance(m, tkvars) or isinstance(m, tkradio) or isinstance(m, tktoggle):
                if m.type == 'StringVar':
                    self._updateStr(m.name)
                elif m.type == 'DoubleVar':
                    self._updateFloat(m.name)
                elif m.type == 'IntVar':
                    self._updateFloat(m.name)
                elif m.type == 'BooleanVar':
                    self._updateBool(m.name)
    
    #tk interfaces

    def ShowMsg(self, msg, widget_var, robolink):
        try:
            print(msg)
            exec("self." + widget_var + ".set('" + msg + "')")
            self.root.update_idletasks()
            robolink.ShowMessage(msg, False)
        except:
            pass

    def updateProgress(self, widget_var, val):
        exec("self." + widget_var + "['value'] = " + str(val))
        self.root.update_idletasks() 

    #widget creation

    def createframe(self, framename, parent="root", hide=False):
        #add self to frame name to point inside object
        parent = "self." + parent
        framename = "self." + framename

        exec(framename + "= Frame(" + parent + ")")
        if not hide:
            exec(framename + ".pack(anchor=N, fill=BOTH, expand=True)")

    def createSpacer(self, width, height, color=None, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent

        c = ""
        if color: c = ",bg='" + color + "'"
        exec("Label("+parent+", text=' ', width="+str(width)+",height="+str(height)+c+").pack()")

    def createLabel(self, varname, type, color, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent
        varname = "self." + varname

        exec(varname + " = "+ type +"()")
        exec("Label("+parent+", textvariable="+varname+", bg='"+color+"').pack()")

    def createTextbox(self, varname, label, type, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent

        var = eval("self." + varname)
        txtvar = "self.txt" + varname
        exec(txtvar + " = "+ type +"()")
        if type == "StringVar":
            exec(txtvar + ".set('" + var + "')")
        else:
            exec(txtvar + ".set(" + str(var) + ")")
        exec("Label("+ parent +", text='" + label + "').pack()")
        exec("Entry("+ parent +", textvariable=" + txtvar + ").pack()")

    def createButton(self, label, file, function, fnt, color, parent="root", fill=None, expand=None, side=None, height=None, width=None):
        """**depreciated** currently not in use due to scoping issues with the command
        """
        #add self to frame name to point inside object
        parent = "self." + parent

        options = ""
        if fill: options = options+",fill="+fill
        if expand: options = options+",expand="+str(expand)
        if side: options = options+",side="+side
        if height: options = options+",height="+str(height)
        if width: options = options+",width="+str(width)

        exec("Button("+ parent +", text='" + label + "', font="+fnt+", command="+ function +", bg='"+ color +"'"+options+").pack()")

    def createCheckbox(self, varname, label, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent

        var = eval("self." + varname)
        txtvar = "self.bool" + varname
        boxvar = 'self.box' + varname

        exec(txtvar + " = BooleanVar()")
        exec(boxvar + " = Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar + ")")
        exec(boxvar +".pack()")
        if var:
            exec(boxvar + ".select()")

    def createFrameToggle(self, varname, label, trueFrame, falseFrame, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent
        trueFrame = "self." + trueFrame
        falseFrame = "self." + falseFrame

        exec(trueFrame + "= Frame(" + parent + ")")
        exec(falseFrame + "= Frame(" + parent + ")")

        #if in rdk load value else default
        if hasattr(self, varname):
            var = eval("self." + varname)
        else:
            exec("self." + varname + "=False")
            var = False
        
        txtvar = "self.bool" + varname
        boxvar = "self.box" + varname

        #create command string
        true_str = "x.pack(anchor=N, fill=BOTH, expand=True)"+" if var.get() else x.pack_forget()"
        false_str = "y.pack_forget()"+" if var.get() else y.pack(anchor=N, fill=BOTH, expand=True)"

        cmdStr = "lambda x="+trueFrame+", y="+falseFrame+", var="+txtvar+": (" + true_str + "," + false_str + ")"
        
        exec(txtvar + "=BooleanVar()")
        exec(boxvar + "=Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar +", command ="+ cmdStr +")")
        exec(boxvar +".pack()")
        if var:
            exec(boxvar + ".select()")
            exec(trueFrame + ".pack(anchor=N, fill=BOTH, expand=True)")
            exec(falseFrame + ".pack_forget()")
            return
        else:
            exec(falseFrame + ".pack(anchor=N, fill=BOTH, expand=True)")
            exec(trueFrame + ".pack_forget()")
            return

    def createRadioButtons(self, varname, type, modes, horizontal = False, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent

        var = eval("self." + varname)
        txtvar = "self.txt" + varname
        exec(txtvar + " = "+ type +"()")
        if type == "StringVar":
            exec(txtvar + ".set('" + var + "')")
        if type  == "IntVar":
            exec(txtvar + ".set(" + str(int(var)) + ")")
        else:
            exec(txtvar + ".set(" + str(var) + ")")
        
        radiovar = 'self.rad' + varname
        exec(radiovar + "= []")
        for text,mode in modes.items():
            if type == "StringVar":
                exec(radiovar + ".append(Radiobutton("+parent+", text='"+text+"', variable="+txtvar+", value='"+mode+"'))")
            else:
                exec(radiovar + ".append(Radiobutton("+parent+", text='"+text+"', variable="+txtvar+", value="+str(mode)+"))")
            exec(radiovar +"[-1].pack()")

    def createProgressBar(self, varname, length, determinate = True, parent="root"):
        #add self to frame name to point inside object
        parent = "self." + parent
        varname = "self." + varname

        if determinate:
            d_str = "determinate"
        else:
            d_str = "indeterminate"
        
        exec(varname + "= Progressbar("+parent+", orient = HORIZONTAL, length = "+str(length)+", mode = '"+d_str+"')")
        exec(varname +".pack()")