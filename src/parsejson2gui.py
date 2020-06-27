import os
import json

#import collection types
from tk_types import *


class guiparse:
    #private
    def _parseprogress(self, items, key="root"):
        self.members.append(tkprogbar(
                    name=items["variable"],
                    type="DoubleVar",
                    length=items["length"],
                    determinate=items["determinate"],
                    parent=key
                ))

    def _parseradio(self, items, key="root"):
        self.members.append(tkradio(
                    name=items["variable"],
                    type=items["type"],
                    modes=items["modes"],
                    parent=key
                ))

    def _parsebutton(self, items, key="root"):
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
        self.members.append(tkspacer(
                    width=items["options"]["width"],
                    height=items["options"]["height"],
                    color=items["color"],
                    parent=key
                ))

    def _parsedisplay(self, item, key="root"):
        self.members.append(tkdisp(
                    name=item["variable"],
                    type=item["type"],
                    color=item["color"],
                    parent=key
                ))
    
    def _parsetoggle(self, items, key="root"):
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
        
        #create true frame
        #self.members.append(tkframe(name=trueframe, parent=key, toggle=True))
        del items["trueframe"]["name"]
        self._parsepanels(items["trueframe"], trueframe)
        
        #create false frame
        #self.members.append(tkframe(name=falseframe, parent=key, toggle=False))
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
            elif k == "radio":
                self._parseradio(v, key)
            elif k == "progress":
                self._parseprogress(v, key)
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

    #public
    def __init__(self, filename):
        #load and parse json file
        self.filename = filename
        self._parsejson()
