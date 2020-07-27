Simple GUI Creation for Robodk Scripts
=======================================

Incorperating tkinter into robodk scripts adds unnessecary complexity and
confusion to otherwise simple scripts. This complexity made it difficult 
to modify the GUI, and make it harder for new users to figure out what's 
going on in the robodk script. This package attempts to alleviate the 
overhead of tkinter by instead defining the GUI in a seperate json file.
The functionality of this package is very streamlined and limited. If more
complex GUI design is needed consult other packages such as 
`pytkgen <https://github.com/tmetsch/pytkgen>`_.


Install
--------

.. code-block:: powershell

    git clone https://github.com/kobbled/robodk-gui
    cd robodk-gui
    pip3 install .


Usage
--------

use by importing the module

.. code-block:: python

    from robodkgui.parsejson import *
    from robodkgui.create import *

First the JSON file must be parsed into the proper data format.
This is done with the :mod:`parsejson2gui` module, and can be constructed
with:

.. code-block:: python

    objList = guiparse("path/to/json_file.json")


The parse tree can then be accessed through:

.. code-block:: python

    objList.members

The GUI is then created with the :mod:`creategui` module, and can be invoked
with:

.. code-block:: python

    gui = tkGUI("Test GUI!")

Make sure this is done globally in the script so all members have access to it.

Variables can be loaded from a robodk save file with:

.. code-block:: python

    gui.loadVars(members, RDK, var_pack)

where *RDK* is the robolink to the robodk file i.e.:

.. code-block:: python

    RDK = Robolink()

the gui is then created with:

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


unitialized varaibles should be stored as a dictionary instead of raw members to pass
to the :class:`creategui.tkGUI` object like:

.. code-block:: python

    var_pack = {
        "BOOL1" : True,
        "RADIO1" : 1,
        "STRING1" : "foo",
        "STRING2" : "bar"
    }

.. note::

    Do not include frame variables, progress bar variables, or frame toggle 
    variables in this packet.

In the robodk script reference the members through the :class:`creategui.tkGUI` class.
For instance if the object is called :data:`gui` call *BOOL1* with *gui.BOOL1*

In order to use the user input values into the gui, before proceeding with trigger
events make sure you update the class attributes with:

.. code-block:: python

    gui.updateVars()

And then save them to your robodk instance with:

.. code-block:: python

    gui.saveVars(RDK)

.. note::

    tk buttons must be made explicitly in the robodk script. This is because of 
    scoping issues outside the :class:`creategui.tkGUI` class. For example the
    button can be created with:
    
    .. code-block:: python

        Button(gui.root, text='Run', font=larege_font, width=20, height=4, command=run_function, bg='green').pack()


Test Example
-------------

`examples <./examples>`_ folder contains a test example to verify the install. 
*test_gui.json* contains the json structure for creating a GUI. *test_gui.py*
contains the python code for the script which basically opens the GUI defined
in *test_gui.json*, and when the event button is pressed will display a message
and then increments the progress bar every second until complete, and display a
message at the end.

To run:

.. code-block:: powershell

    cd path/to/robodk-gui/examples
    python test_gui.py

Alternatively open up the robodk file and run the program.

Variable will remember their state, as they are saved in the robodk instance, as 
long as the event trigger button is pressed to save them.


Tk functionality
------------------

Textboxes/Checkboxes
^^^^^^^^^^^^^^^^^^^^^^

Variables are stored as a dictionary list specifying
there class attribute name as the key, and their label, 
and value type as their value. Numerous variables can
be neatly stored in this fashion.

.. code-block:: json

    "members" : {
        "VAR1" : ["Variable Name 1", "StringVar"],
        "VAR2" : ["Variable Name 2", "StringVar"],
        "VAR3" : ["Variable Name 3", "StringVar"]
    }


frames
^^^^^^^^

Frame containers are used to organize the gui layout, with a general structure of:

.. code-block:: json

    {"root" : [{
        "panel" : {
            "frm1" : {
            },
            "frm2" : {
            }
        }

        }]
    }

`root` must be the first thing declares in the json file.



Frame toggle
^^^^^^^^^^^^^

Toggling panels is done by specifying the checkbox,
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

Display Notification
^^^^^^^^^^^^^^^^^^^^^^^

Display is used to display information to the
user through the GUI interface. In JSON this can be
defined as:

.. code-block:: json

    "display" : {
        "variable" : "NOTIFY_MSG",
        "type" : "StringVar",
        "color" : "green"
    }

Progess bar
^^^^^^^^^^^^^

Progress bars can be defined as:

.. code-block:: json

    "progress" : {
        "variable" : "PROG_BAR",
        "length" : 100,
        "determinate" : true
    }

The progress bar can be defined as determinate, or
indeterminate.

Radio buttons
^^^^^^^^^^^^^^^

Radio buttons can be defined with numerous options, i.e.

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

Spacer
^^^^^^^^

Input a spacer of size width x height. To seperate
widgets. Can also input a color for the spacer if specified.

.. code-block:: json

    "spacer" : {"options" : {"width" : 20, "height" : 1}, "color" : "yellow"}


