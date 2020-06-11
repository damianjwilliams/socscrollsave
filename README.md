# Socscrollsave

Python application for creating a real-time scrolling plot and storing data from a websocket.
Most of the code is from  Sebastián Sepúlveda's excellent [RTplot](https://github.com/ssepulveda/esp_32). socscrollsave is a simplified version of RTplot, which also can use sockets and serial connections.


## Requirements
- [websocket-client](https://pypi.org/project/websocket_client/)

- [pyqtgraph](http://www.pyqtgraph.org/)

- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) (for older versions of macOS, it may be necessary to install an old version of PyQt5 `pip install PyQt5==5.13.0` )


## Usage
From a terminal, on the root folder of the application, run `python -m socscrollsave`.

The client IP address (and port), can be found on line 43 of `~/socscrollsave/SocketClient.py`.

Incoming data should be in csv format.

Currently plots data from 4 variables from the same csv stream. The number of plots can be changed at  `/socscrollsave/ui/mainWindow.py` line 89.

Data is stored as a `.csv` file in `~/data`.

For an examples using ESP-32 microcontroller see link below.

## Links


## License
The project is distributed under MIT License
