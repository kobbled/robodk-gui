
# import gui tools
from tkinter import *
import tkinter.font as font

# tkinter helpers
# ----------------

def createframe(framename, parent="root", hide=False):
    exec(framename + "= Frame(" + parent + ")", globals())
    if not hide:
        exec(framename + ".pack(anchor=N, fill=BOTH, expand=True)", globals())

def createSpacer(width, height, color=None, parent="root"):
    c = ""
    if color: c = ",bg=" + color
    exec("Label("+parent+", text=' ', width="+str(width)+",height="+str(height)+c+").pack()")

def createLabel(varname, label=None, parent="root"):
    exec(varname + "= StringVar()", globals())
    exec("Label("+parent+", textvariable="+varname+").pack()")

def createTextbox(varname, label, type, parent="root"):
    var = eval(varname)
    txtvar = "txt" + varname
    exec(txtvar + " = "+ type +"()", globals())
    if type == "StringVar":
        exec(txtvar + ".set('" + var + "')")
    else:
        exec(txtvar + ".set(" + str(var) + ")")
    exec("Label("+ parent +", text='" + label + "').pack()")
    exec("Entry("+ parent +", textvariable=" + txtvar + ").pack()")

def createButton(label, function, fnt, color, parent="root", fill=None, expand=None, side=None, height=None, width=None):
    options = ""
    if fill: options = options+",fill="+fill
    if expand: options = options+",expand="+str(expand)
    if side: options = options+",side="+side
    if height: options = options+",height="+str(height)
    if width: options = options+",width="+str(width)

    exec("Button("+ parent +", text='" + label + "', font="+fnt+", command="+ function +", bg='"+ color +"'"+options+").pack()")

def createCheckbox(varname, label, parent="root"):
    var = eval(varname)
    txtvar = "bool" + varname
    boxvar = 'box_' + varname

    exec(txtvar + " = BooleanVar()", globals())
    exec(boxvar + " = Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar + ")", globals())
    exec(boxvar +".pack()")
    if var:
        exec(boxvar + ".select()")

def createFrameToggle(varname, label, trueFrame, falseFrame, parent="root"):
    var = eval(varname)
    txtvar = "bool" + varname
    boxvar = 'box_' + varname

    true_str = trueFrame +".pack(anchor=N, fill=BOTH, expand=True)"+" if "+ txtvar +".get() else "+ trueFrame +".pack_forget()"
    false_str = falseFrame +".pack_forget()"+" if "+ txtvar +".get() else "+ falseFrame +".pack(anchor=N, fill=BOTH, expand=True)"

    cmdStr = "lambda : (" + true_str + "," + false_str + ")"
    
    exec(txtvar + " = BooleanVar()", globals())
    exec(boxvar + "=Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar +", command ="+ cmdStr +")", globals())
    exec(boxvar +".pack()")
    if var:
        exec(boxvar + ".select()")
