import os
import json
import collections

from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox

# import gui tools
from tkinter import *

#import helpers
from tk_helpers import *

#start rdk api
RDK = Robolink()

#rdk helpers
#------------

#rdk load variables
def _loadFloat(variable_name):
    value = RDK.getParam(variable_name)
    if value is not None:
        exec(variable_name + " = " + str(value))

def _loadBool(variable_name):
    value = RDK.getParam(variable_name)
    if value is not None:
        exec(variable_name + " = " + value)

def _loadStr(variable_name):
    value = RDK.getParam(variable_name)
    if value is not None:
        exec(variable_name + " = '" + str(value) + "'")

#rdk update variables
#run before processing an event
def _updateFloat(variable_name):
    exec("%s = float(txt%s.get())" % (variable_name, variable_name), globals())

def _updateBool(variable_name):
    exec("%s = txt%s.get()" % (variable_name, variable_name), globals())

def _updateStr(variable_name):
    exec("%s = bool(txt%s.get())" % (variable_name, variable_name), globals())

#rdk save variables
def _saveVar(variable_name):
    value = eval(variable_name)
    RDK.setParam(variable_name, value)


tkvars = collections.namedtuple('tkvars', 'name label type parent')

tkdisp = collections.namedtuple('tkdisp', 'name type parent')

tkspacer = collections.namedtuple('tkspacer', 'width height color parent')

tkframe = collections.namedtuple('tkframe', 'name parent toggle')

tktoggle = collections.namedtuple('tktoggle',
    'name label '
    'trueframe falseframe '
    'parent'         
)

tkbutton = collections.namedtuple('tkbutton',
    'name label command '
    'font color '
    'expand fill side '
    'width height '
    'parent'         
)


class rdkGUI:
    #private
    def _parsebutton(self, items, key="root"):
        options = items["options"]
        fill = options["fill"] if ("fill" in options.keys()) else None
        expand = options["expand"] if ("expand" in options.keys()) else None
        side = options["side"] if ("side" in options.keys()) else None
        width = options["width"] if ("width" in options.keys()) else None
        height = options["height"] if ("height" in options.keys()) else None

        self.members.append(tkbutton(
                    name=items["variable"],
                    label=items["label"],
                    command=items["command"],
                    parent=key,
                    font= items["font"],
                    color=items["color"],
                    fill=fill,
                    expand=expand,
                    side=side,
                    width=width,
                    height=height
                ))

    def _parsespacer(self, items, key="root"):
        self.members.append(tkspacer(
                    width=items["options"]["width"],
                    height=items["options"]["height"],
                    color=items["color"],
                    parent=key
                ))

    def _parsedisplay(self, item, key="root"):
        for k,v in item.items():
            self.members.append(tkdisp(
                        name=k,
                        type=v,
                        parent=key
                    ))
    
    def _parsetoggle(self, items, key="root"):
        #create toogle
        trueframe = items["trueframe"]["name"]
        falseframe = items["falseframe"]["name"]
        self.members.append(tktoggle(
                name=items["variable"],
                label=items["label"],
                trueframe=items["trueframe"]["name"],
                falseframe=items["falseframe"]["name"],
                parent=key
            ))
        
        #create true frame
        var = not eval(items["variable"])
        self.members.append(tkframe(name=trueframe, parent=key, toggle=var))
        del items["trueframe"]["name"]
        self._parsepanels(items["trueframe"], trueframe)
        
        #create false frame
        var = not var
        self.members.append(tkframe(name=falseframe, parent=key, toggle=var))
        del items["falseframe"]["name"]
        self._parsepanels(items["falseframe"], falseframe)


    def _parsemembers(self, item, key="root"):
        for k,v in item.items():
            self.members.append(tkvars(
                        name=k,
                        label=v[0],
                        type=v[1],
                        parent=key
                    ))
    
    def _parsepanels(self, item, key="root"):
        for k,v in item.items():
            if k == "panel":
                self._parsepanels(v, key)
            elif k == "members":
                self._parsemembers(v, key)
            elif k == "toggle":
                self._parsetoggle(v, key)
            elif k == "button":
                self._parsebutton(v, key)
            elif k == "display":
                self._parsedisplay(v, key)
            elif k == "spacer":
                self._parsespacer(v, key)
            #else assume is a new frame
            else:
                self.members.append(tkframe(name=k, parent=key, toggle=False))
                self._parsepanels(v, k)

    def _parsejson(self):
        interface = json.load(open(self.filename), object_pairs_hook=collections.OrderedDict) if os.path.isfile(
                self.filename) else json.loads(self.filename, object_pairs_hook=collections.OrderedDict)
        #create variable members list
        self.members = []
        for panel in interface["root"]:
            self._parsepanels(panel)

    def _buildgui(self):
        for m in self.members:
            if isinstance(m, tkvars):
                if m.type == 'BooleanVar':
                    createCheckbox(m.name, m.label, m.parent)
                else:
                    createTextbox(m.name, m.label, m.type, m.parent)
            if isinstance(m, tkframe):
                createframe(m.name, m.parent, m.toggle)
            if isinstance(m, tktoggle):
                createFrameToggle(m.name, m.label, m.trueframe, m.falseframe, m.parent)
            if isinstance(m, tkbutton):
                createButton(m.label, m.command, m.font, m.color, parent=m.parent,
                             fill=m.fill, expand=m.expand, side=m.side,
                             height=m.height, width=m.width)
            if isinstance(m, tkspacer):
                createSpacer(m.width, m.height, m.color, m.parent)
            if isinstance(m, tkdisp):
                createLabel(m.name, m.parent)


    #public
    def __init__(self, filename, title='Tk'):
        #initialize main windows
        global root
        root = Tk()
        root.title(title)
        #load and parse json file
        self.filename = filename
        self._parsejson()
        #load variables
        self.loadVars()
        #create gui
        self._buildgui()


    def loadVars(self):
        for m in self.members:
            if isinstance(m, tkvars):
                if m.type == 'StringVar':
                    _loadStr(m.name)
                elif m.type == 'DoubleVar':
                    _loadFloat(m.name)
                elif m.type == 'BooleanVar':
                    _loadBool(m.name)
    
    def saveVars(self):
        for m in self.members:
            if isinstance(m, tkvars):
                _saveVar(m.name)
    
    def updateVars(self):
        for m in self.members:
            if isinstance(m, tkvars):
                if m.type == 'StringVar':
                    _updateStr(m.name)
                elif m.type == 'DoubleVar':
                    _updateFloat(m.name)
                elif m.type == 'BooleanVar':
                    _updateBool(m.name)



    def ShowMsg(self, widget_var, msg):
        print(msg)
        widget_var.set(msg)
        root.update_idletasks()
        RDK.ShowMessage(msg, False)

#create fake button event
def btnUpdate():
    pass

def main():

    #initialize gui
    frame = rdkGUI("../examples/test_gui.json","Test GUI!")
    frame.ShowMsg(NOTIFY_MSG, "Hello!")


if __name__ == '__main__':
    main()
    root.mainloop()


