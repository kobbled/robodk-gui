
# import gui tools
from tkinter import *
from tkinter.ttk import Progressbar
import tkinter.font as font

#import collection types
from robodkgui.tk_types import *

# tkinter helpers
# ----------------

class tkGUI:

    """This class will create a tkinter gui from the parse tree created from
    :class:`parsejson2gui.guiparse`. The parse tree is a collection of user
    defined types specified in :mod:`tk_types`. The class should be constructed
    as a global member in a robodk script with:

    .. code-block:: python

        gui = tkGUI("Test GUI!")

    variables can be loaded from the robodk instance in order to retain memory with

    .. code-block:: python

        gui.loadVars(members, RDK, var_pack)
    
    and the gui can be created with:

    .. code-block:: python

        gui.build()

    Button must be manually created with tkinter in the robodk script itself in order
    to have access to the trigger event command in the robodk script.

    .. code-block:: python

        Button(gui.root, text='Run', font=large_font, width=20, height=4, command=function, bg='green').pack()

    Finally the tkinter spinner must be called in the robodk script in order to persist the
    GUI.

    .. code-block:: python

        gui.root.mainloop()

    
    """

    #private members

    #rdk load variables
    def _loadFloat(self, variable_name, robolink, uninit_vals, use_defaults=False):
        """Load float variable from RDK instance into python.

        :param uninit_vals: A hash of variable names as keys and default
                            values. Easier way of passing program constants/
                            globals to the tkGUI class, and doing so explicitly.
        :type uninit_vals: hash<t>
        :param use_defaults: Flag for designating if variables stored
                            in RDK file should be used, or default values
                            defined in :data:`creategui.tkGUI._loadFloat.uninit_vals`, 
                            defaults to False
        :type use_defaults: bool, optional
        """
        value = robolink.getParam(variable_name)
        if value is not None and not use_defaults:
            exec("self." + variable_name + " = " + str(value))
        elif variable_name in uninit_vals.keys():
            exec("self." + variable_name + "=" + str(uninit_vals[variable_name]))
        else:
            raise ValueError(variable_name + 'was not found.')


    def _loadBool(self, variable_name, robolink, uninit_vals, use_defaults=False):
        """Load boolean variable from RDK instance into python.

        :param uninit_vals: A hash of variable names as keys and default
                            values. Easier way of passing program constants/
                            globals to the tkGUI class, and doing so explicitly.
        :type uninit_vals: hash<t>
        :param use_defaults: Flag for designating if variables stored
                            in RDK file should be used, or default values
                            defined in :data:`creategui.tkGUI._loadBool.uninit_vals`, 
                            defaults to False
        :type use_defaults: bool, optional
        """
        value = robolink.getParam(variable_name)
        if value is not None and not use_defaults:
            exec("self." + variable_name + " = " + str(value))
        elif variable_name in uninit_vals.keys():
            exec("self." + variable_name + "=" + str(uninit_vals[variable_name]))
    

    def _loadStr(self, variable_name, robolink, uninit_vals, use_defaults=False):
        """Load string variable from RDK instance into python.

        :param uninit_vals: A hash of variable names as keys and default
                            values. Easier way of passing program constants/
                            globals to the tkGUI class, and doing so explicitly.
        :type uninit_vals: hash<t>
        :param use_defaults: Flag for designating if variables stored
                            in RDK file should be used, or default values
                            defined in :data:`creategui.tkGUI._loadStr.uninit_vals`, 
                            defaults to False
        :type use_defaults: bool, optional
        """
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
        """update class float attribute from corresponding tk widget
        """
        exec("self.%s = float(self.txt%s.get())" % (variable_name, variable_name))

    def _updateBool(self, variable_name):
        """update class boolean attribute from corresponding tk widget
        """
        exec("self.%s = bool(self.bool%s.get())" % (variable_name, variable_name))

    def _updateStr(self, variable_name):
        """update class string attribute from corresponding tk widget
        """
        exec("self.%s = self.txt%s.get()" % (variable_name, variable_name))

    def _updateRadio(self, variable_name):
        """update class attribute from radiobutton widget
        """
        exec("self.%s = self.txt%s.get()" % (variable_name, variable_name))

    #rdk save variables
    def _saveVar(self, variable_name, robolink):
        """save class attribute (variable_name) in the current
        robodk instance defined in robolink.
        """
        value = eval("self." + variable_name)
        robolink.setParam(variable_name, value)

    #public members

    def __init__(self, title):
        """Initialize Tkinter through tkGUI class.
        """
        #initialize main windows
        self.root = Tk()
        self.root.title(title)
    
    def build(self):
        """From the tkinter member dictionary created with :class:`parsejson2gui.guiparse`
           For each item create the corresponding tk widget. Using namedtuple
           user type definitions in :mod:`tk_types` to route the widget creation
           from the parse tree.
        """
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
        """Load variables from the associated robodk instance, or the default hash table
        as class attributes. Relavent members are determined from the parse tree if the 
        member is of type `tk_types.tkvars`, `tk_types.tkradio`, or `tk_types.tktoggle`.


        :param uninit_vals: A hash of variable names as keys and default
                            values. Easier way of passing program constants/
                            globals to the tkGUI class, and doing so explicitly.
        :type uninit_vals: hash<t>
        :param use_defaults: Flag for designating if variables stored
                            in RDK file should be used, or default values
                            defined in :data:`creategui.tkGUI.loadVars.uninit_vals`, 
                            defaults to False
        :type use_defaults: bool, optional
        """
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
        """Save class attributes into the associated robodk instance
        if they are of user type `tk_types.tkvars`, `tk_types.tkradio`, or 
        `tk_types.tktoggle`. This class method should be ran after 
        :func:`creategui.tkGUI.updateVars` in order to retain memory 
        of user inputs from the GUI.
        """
        for m in self.members:
            if isinstance(m, tkvars) or isinstance(m, tkradio):
                self._saveVar(m.name, robolink)
            elif isinstance(m, tktoggle):
                self._saveVar(m.name, robolink)
    
    def updateVars(self):
        """Update all class attributes to there associated tk widget value
        input by the user. This should be ran before an event trigger so that
        the robodk script is using the updated user entries.
        """
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
        """If a notification display is specified in GUI
        this method will update this display with a
        message. display attribute must be specified in 
        `widget_var`.

        :param widget_var: name of class attribute where the
                           display message should be stored.
        :type widget_var: string
        """
        try:
            exec("self." + widget_var + ".set('" + msg + "')")
            self.root.update_idletasks()
            robolink.ShowMessage(msg, False)
        except:
            print(msg)
            pass

    def updateProgress(self, widget_var, val):
        """Internal class method for updating a progress bar.
        
        :param widget_var: name of class attribute where the
                           progress bar value is stored.
        :type widget_var: string
        """
        exec("self." + widget_var + "['value'] = " + str(val))
        self.root.update_idletasks() 

    #widget creation

    def createframe(self, framename, parent="root", hide=False):
        """Create a container for a group of associated widgets. This
        is done for oranizational purposes as well as for easily hiding
        and showing a group of widgets. A `parent` tree is created during
        the parsing process in :class:`parsejson2gui.guiparse`
        """
        #add self to frame name to point inside object
        parent = "self." + parent
        framename = "self." + framename

        exec(framename + "= Frame(" + parent + ")")
        if not hide:
            exec(framename + ".pack(anchor=N, fill=BOTH, expand=True)")

    def createSpacer(self, width, height, color=None, parent="root"):
        """A spacer element defined by a width and a height to seperate
        widgets.

        :param width: width of spacer element measured by units of character
        :type width: decimal
        :param height: height of spacer element measured by units of character
        :type height: decimal
        :param color: background color of the spacer element, defaults to None
                      which renders a clear background.
        :type color: string (i.e: red, blue, yellow, green), optional
        """
        #add self to frame name to point inside object
        parent = "self." + parent

        c = ""
        if color: c = ",bg='" + color + "'"
        exec("Label("+parent+", text=' ', width="+str(width)+",height="+str(height)+c+").pack()")

    def createLabel(self, varname, type, color, parent="root"):
        """Add an output display string that the user cannot modify.
        Typically this is used to notify the user about the status of
        the program. Can be defined as various data type such as a string,
        or an int, or a float.

        :param varname: Name of the class attribute to print to display
        :type varname: string
        :param color: background color of element, defaults to None
                      which renders a clear background.
        :type color: string (i.e: red, blue, yellow, green), optional
        """
        #add self to frame name to point inside object
        parent = "self." + parent
        varname = "self." + varname

        exec(varname + " = "+ type +"()")
        if color:
            exec("Label("+parent+", textvariable="+varname+", bg='"+color+"').pack()")
        else:
            exec("Label("+parent+", textvariable="+varname+").pack()")

    def createTextbox(self, varname, label, type, parent="root"):
        """Create a textbox of data `type` that the user can input
        and modify.  

        :param varname: The associated class attribute that the textbox
                        will update.
        :type varname: string
        :param label: description text written next to the text box to
                      describe what the textbox is for.
        :type label: string
        :param type: data type input into the textbox
        :type type: various (string, int, float, bool)
        """
        #add self to frame name to point inside object
        parent = "self." + parent

        #get current value of the class attribute
        var = eval("self." + varname)
        #define variable to store the widget 
        txtvar = "self.txt" + varname
        #define data type of widget
        exec(txtvar + " = "+ type +"()")
        #set the textbox value
        if type == "StringVar":
            exec(txtvar + ".set('" + var + "')")
        else:
            exec(txtvar + ".set(" + str(var) + ")")
        #create textbox
        exec("Label("+ parent +", text='" + label + "').pack()")
        exec("Entry("+ parent +", textvariable=" + txtvar + ").pack()")

    def createButton(self, label, file, function, fnt, color, parent="root", fill=None, expand=None, side=None, height=None, width=None):
        """
        .. danger:: 

                **DO NOT USE** currently not in use due to scoping 
                issues with the command function. Manually declare
                in main scripting file.

                .. code-block:: python

                    Button(gui.root, text='Run', font=larege_font, width=20, height=4, command=run_function, bg='green').pack()
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
        """make boolean a checkbox.

        :param varname: The associated boolean class attribute that 
                        the checkbox will update.
        :type varname: string
        :param label: description of what the checkbox does
        :type label: string
        """
        #add self to frame name to point inside object
        parent = "self." + parent

        #get current value of the class attribute
        var = eval("self." + varname)
        #attribute associated with the checkbox
        txtvar = "self.bool" + varname
        #class attribute to store the checkbox widget
        boxvar = 'self.box' + varname

        exec(txtvar + " = BooleanVar()")
        exec(boxvar + " = Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar + ")")
        exec(boxvar +".pack()")
        if var:
            exec(boxvar + ".select()")

    def createFrameToggle(self, varname, label, trueFrame, falseFrame, parent="root"):
        """Create a binary toggle for showing and hiding panels. This is done to hide
           from the user irrelavent variable when a certain option is selected.

        :param varname: boolean class attribute where the option is stored.
        :type varname: string
        :param trueFrame: widget panel name to show when the option is true
        :type trueFrame: string
        :param falseFrame: widget panel name to show when the option is false
        :type falseFrame: string
        """
        #add self to frame name to point inside object
        parent = "self." + parent
        trueFrame = "self." + trueFrame
        falseFrame = "self." + falseFrame

        #create frames so that trueFrame, and falseFrame
        #are not undefined when trying to create the 
        #checkbutton. `createframe` is not called, as this
        #function handles the creation of the trueframe panel
        #and the falseframe panel
        exec(trueFrame + "= Frame(" + parent + ")")
        exec(falseFrame + "= Frame(" + parent + ")")

        #if in rdk load value else default
        #.. note:: this attribute should not be
        #          specified in the variable hash
        #          table. Therefore it uninitialized value
        #          needs to be defined here. 
        if hasattr(self, varname):
            var = eval("self." + varname)
        else:
            exec("self." + varname + "=False")
            var = False
        
        #class attribute to store checkbutton value
        txtvar = "self.bool" + varname
        #class attribute to store the checkbutton widget
        boxvar = "self.box" + varname

        #create command string
        #lambda must be two lines to show/hide on panel and hide/show the
        #other panel. Due to scoping issue with lambda through a tkwidget
        #define in a class, variables msut be passed by value into the lambda
        #to have access to them.
        true_str = "x.pack(anchor=N, fill=BOTH, expand=True)"+" if var.get() else x.pack_forget()"
        false_str = "y.pack_forget()"+" if var.get() else y.pack(anchor=N, fill=BOTH, expand=True)"

        cmdStr = "lambda x="+trueFrame+", y="+falseFrame+", var="+txtvar+": (" + true_str + "," + false_str + ")"
        
        #create check button to use as the panel toggle
        exec(txtvar + "=BooleanVar()")
        exec(boxvar + "=Checkbutton("+ parent +", text='"+ label +"', variable="+ txtvar +", command ="+ cmdStr +")")
        exec(boxvar +".pack()")
        #when the toggle is initialized have the correct panel active/hidden corresponding
        #to what the last value of the attribute was.
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
        """Make radio buttons corresponding to a dictionary defined in `modes` member of  
           `tk_types.tkradio`.

        :param varname: class attribute name where the current value of the
                        radio buttons are stored.
        :type varname: string
        :param type: data type of the value in the dictionary pair `modes`
        :type type: various
        :param modes: dictionary of key/value pair to use for the radio buttons
        :type modes: hash
        :param horizontal: make buttons horizontal intead of vertical, 
                           **Currently Does not work**. Would need to use grid
                           instead of pack which would require a refactoring of
                           entire package. defaults to False.
        :type horizontal: bool, optional

        .. todo::
            radio buttons inside a toogle currently will not hide even though the
            parent panel does hide. Do not know why this happening, or what the work
            around could be.
        
        .. todo::
            refactor with grid instead of pack in order to have horizontal radio buttons
        
        .. todo::
            expand toggle for radio buttons so that the toggle is not just a binary option,
            and works more like notebooks.
        """
        #add self to frame name to point inside object
        parent = "self." + parent

        #value of class member where the last rodio button selection
        #was stored.
        var = eval("self." + varname)
        #class attribute to store the radiobutton selection
        txtvar = "self.txt" + varname
        exec(txtvar + " = "+ type +"()")
        #set value to previously saved value
        if type == "StringVar":
            exec(txtvar + ".set('" + var + "')")
        if type  == "IntVar":
            exec(txtvar + ".set(" + str(int(var)) + ")")
        else:
            exec(txtvar + ".set(" + str(var) + ")")
        
        #class attribute to store radio button widget
        radiovar = 'self.rad' + varname
        #initialize
        exec(radiovar + "= []")
        #populate button list
        for text,mode in modes.items():
            if type == "StringVar":
                exec(radiovar + ".append(Radiobutton("+parent+", text='"+text+"', variable="+txtvar+", value='"+mode+"'))")
            else:
                exec(radiovar + ".append(Radiobutton("+parent+", text='"+text+"', variable="+txtvar+", value="+str(mode)+"))")
            exec(radiovar +"[-1].pack()")

    def createProgressBar(self, varname, length, determinate = True, parent="root"):
        """make a progress bar associate with a class attribute. The progress bar can
        be updated with:

        .. code-block:: python

            gui.updateProgress("PROG_BAR", 0)
            time.sleep(1)
            gui.updateProgress("PROG_BAR", 20)
            time.sleep(1)
            gui.updateProgress("PROG_BAR", 40)

        :param varname: class attribute to store progress bar value
        :type varname: float
        :param length: length of progress bar in terms of characters.
        :type length: int
        :param determinate: If progress bar increases in steps, or
                            does not indicate progress, defaults to True
        :type determinate: bool, optional
        """
        #add self to frame name to point inside object
        parent = "self." + parent
        varname = "self." + varname

        if determinate:
            d_str = "determinate"
        else:
            d_str = "indeterminate"
        
        exec(varname + "= Progressbar("+parent+", orient = HORIZONTAL, length = "+str(length)+", mode = '"+d_str+"')")
        exec(varname +".pack()")