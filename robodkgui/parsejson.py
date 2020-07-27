import os
import json

#import collection types
from robodkgui.tk_types import *


class guiparse:
    """ This class will parse a json file into a parse tree constisting
    of user defined types that can be found in :mod:`tk_types`. The parse
    tree can then be used by :class:`creategui.tkGUI` to create a tkinter
    GUI within a robodk script.

    prase tree can be created with:

    .. code-block:: python

        objList = guiparse("path/to/json_file.json")

    parse tree can then be accessed through:

    .. code-block:: python

        objList.members

    """

    #private
    def _parseprogress(self, items, key="root"):
        """Progress bars can be defined as:

        .. code-block:: json

            "progress" : {
                "variable" : "PROG_BAR",
                "length" : 100,
                "determinate" : true
            }

        The progress bar can be defined as determinate, or
        indeterminate.

        """
        self.members.append(tkprogbar(
                    name=items["variable"],
                    type="DoubleVar",
                    length=items["length"],
                    determinate=items["determinate"],
                    parent=key
                ))

    def _parseradio(self, items, key="root"):
        """Radio buttons can be defined with numerous options, i.e.

        .. code-block:: json

            "radio" : {
                        "variable" : "RADIO_VAR",
                        "type" : "IntVar",
                        "modes" : {"option1": 1,
                                   "option2": 2,
                                   "option3": 3}
                    }

        These options are stored as a dictionary key/value pair, in 
        `tkradio.modes`.
        """
        self.members.append(tkradio(
                    name=items["variable"],
                    type=items["type"],
                    modes=items["modes"],
                    parent=key
                ))

    def _parsebutton(self, items, key="root"):
        """
        .. danger:: 

                **DO NOT USE** currently not in use due to scoping 
                issues with the command function. Manually declare
                in main scripting file.

                .. code-block:: python

                    Button(gui.root, text='Run', font=larege_font, width=20, height=4, command=run_function, bg='green').pack()


        Include a pushbutton that is bound to an event trigger function,
        `items["command"]`. Options included are `fill`, `expand`, `side`,
        `width`, and `height`.
        """

        options = items["options"]
        fill = options["fill"] if ("fill" in options.keys()) else None
        expand = options["expand"] if ("expand" in options.keys()) else None
        side = options["side"] if ("side" in options.keys()) else None
        width = options["width"] if ("width" in options.keys()) else None
        height = options["height"] if ("height" in options.keys()) else None

        self.members.append(tkbutton(
                    label=items["label"],
                    file=items["file"],
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
        """Input a spacer of size width x height. To seperate
        widgets. Can also input a color for the spacer if specified.

        .. code-block:: json

            "spacer" : {"options" : {"width" : 20, "height" : 1}, "color" : "yellow"}

        """
        # if color is undefined use default
        color = items["color"] if ("color" in items.keys()) else ""


        self.members.append(tkspacer(
                    width=items["options"]["width"],
                    height=items["options"]["height"],
                    color=color,
                    parent=key
                ))

    def _parsedisplay(self, item, key="root"):
        """display is used to display information to the
        user through the GUI interface. In JSON this can be
        defined as:

        .. code-block:: json

            "display" : {
                "variable" : "NOTIFY_MSG",
                "type" : "StringVar",
                "color" : "green"
            }
        """

        # if color is undefined use default
        color = item["color"] if ("color" in item.keys()) else ""

        self.members.append(tkdisp(
                    name=item["variable"],
                    type=item["type"],
                    color=color,
                    parent=key
                ))
    
    def _parsetoggle(self, items, key="root"):
        """toggling panels is done by specifying the checkbox,
        with an attribute name, and a label. The panels or frames
        that this checkbox controls are defined in the toggle block
         as the `trueframe` or the `falseframe`. the value of the
         trueframe, or the falseframe are written just as you would
         for defining a panel, and its internal contents.

         .. code-block:: json

            "toggle" : {
                "variable" : "TOGGLE1",
                "label": "toggle example",
                "trueframe" : {
                    "name" : "frame_name1",
                    "members" : {
                    "VAR1" : ["Variable Name 1", "StringVar"]
                    }
                },
                "falseframe" : {
                    "name" : "frame_name2",
                    "members" : {
                    "VAR2" : ["Variable Name 2", "StringVar"]
                    }
                }
            }

        """
        #create toogle
        trueframe = items["trueframe"]["name"]
        falseframe = items["falseframe"]["name"]

        self.members.append(tktoggle(
                name=items["variable"],
                type="BooleanVar",
                label=items["label"],
                trueframe=trueframe,
                falseframe=falseframe,
                parent=key
            ))
        

        #.. warning:: Do not store trueframe, or falseframe as a tkframe instance in parse
        #             tree. The creation of these frames is handled in tktoggle itself.

        #store frame name that should show when the toggle is true
        del items["trueframe"]["name"]
        #add the internals of the trueframe, or falseframe panels
        #to the parse tree.
        self._parsepanels(items["trueframe"], trueframe)
        
        #store frame name that should hide when the toggle is true
        del items["falseframe"]["name"]
        self._parsepanels(items["falseframe"], falseframe)


    def _parsemembers(self, item, key="root"):
        """variables are stored as a dictionary list specifying
        there class attribute name as the key, and their label, 
        and value type as their value. Numerous variables can
        be neatly stored in this fashion.

        .. code-block:: json

            "members" : {
                "VAR1" : ["Variable Name 1", "StringVar"],
                "VAR2" : ["Variable Name 2", "StringVar"],
                "VAR3" : ["Variable Name 3", "StringVar"]
            }
        """
        for k,v in item.items():
            self.members.append(tkvars(
                        name=k,
                        label=v[0],
                        type=v[1],
                        parent=key
                    ))
    
    def _parsepanels(self, item, key="root"):
        """Routing for creating a parse tree depending on what
        the key name of the dictionary item is. If the keyname is
        not a specified keyword, it will assume that the current item
        is declaring a new frame/container.
        """
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
            elif k == "radio":
                self._parseradio(v, key)
            elif k == "progress":
                self._parseprogress(v, key)
            #else assume is a new frame
            else:
                self.members.append(tkframe(name=k, parent=key, toggle=False))
                self._parsepanels(v, k)

    def _parsejson(self):
        #do not store json dictionary as a class attribute
        #it will immediately be converted into a user type list.
        interface = json.load(open(self.filename), object_pairs_hook=collections.OrderedDict) if os.path.isfile(
                self.filename) else json.loads(self.filename, object_pairs_hook=collections.OrderedDict)
        #create variable members list
        self.members = []
        for panel in interface["root"]:
            self._parsepanels(panel)

    #public
    def __init__(self, filename):
        """Constructor will load a specified json file, and convert
        it to a python dictionary. Each member in the ordered dictionary
        is then parsed and added to the parse tree, `members`.
        """
        #load and parse json file
        self.filename = filename
        self._parsejson()
