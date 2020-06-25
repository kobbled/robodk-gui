Simple GUI Creation for Robodk Scripts
=======================================

Incorperating tkinter into robodk scripts adds unnessecary complexity and
confusion to otherwise simple scripts. This package attempts to alleviate
the overhead of tkinter by instead defining the GUI in a seperate json file.
The functionality of this package is very streamlined and limited. If more
complex GUI design is needed consult other packages such as 
[pytkgen](https://github.com/tmetsch/pytkgen).


Install & Usage
----------------

```bash
git clone https://github.com/kobbled/robodk-gui
```

use by importing the module

```python
sys.path.append(os.path.abspath('C:/path/to/robodk-gui/src'))
import rdk-gui
```

run the test by just running **rdk-gui.py** in the src folder

```bash
cd path/to/robodk-gui/src
python rdk-gui.py
```