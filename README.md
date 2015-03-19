# Meggy Jr cncserver
This software allows the use of the Meggy Jr RGB to control a WaterColorBot
with cncserver.

## Dependencies
  - Host software
    - cncserver
    - Python 2
    - Python Requests
    - pySerial

  - Meggy Jr Software
    - Arduino IDE
    - Meggy Jr library
    - FTDI cable

## Install
  The Meggy Jr needs to be programmed with the included code. This requires the
  Meggy Jr libraries be installed. Once they are installed the Meggy Jr can be
  programmed with the included code (`arduino/MeggyJr_WCB_controller/`).

## Use
  - Connect the Meggy Jr to your computer with a FTDI cable
  - Run `python http://localhost:4242 [meggyjr serial port]` or
    `python [cncserver address] [meggyjr serial port]`, substituting the serial
    port of the Meggy Jr and address of cncserver. On Linux this will probably
    be `/dev/ttyUSB0`, on Mac `/dev/tty.usbserial-*`, on Windows it should be
    `COM*`

    The '-d n' flag sets the move distance when a button is pressed to n.

## Resources
[cncserver](https://github.com/techninja/cncserver/)
[Python](https://www.python.org)
[pySerial](http://pyserial.sourceforge.net/)
[Python Requests](http://docs.python-requests.org/en/latest/)

[Arduino](http://arduino.cc/)
[Meggy Jr RGB](http://wiki.evilmadscientist.com/Meggy_Jr_RGB)
[Meggy Jr library](https://github.com/evil-mad/MeggyJrRGB/releases)
