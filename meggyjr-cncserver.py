import serial
import cncserverclient
import argparse
import sys

# Copyright (C) 2015  Schuyler St. Leger
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


parser = argparse.ArgumentParser()
parser.add_argument("cncserver")
parser.add_argument("serialport")
parser.add_argument("-d", "--move-dist", type=int, default=1)
args = parser.parse_args()

meggy = serial.Serial(args.serialport, 115200)
client = cncserverclient.CNCServerClient(args.cncserver)

client.setPenHeight("up")
client.setPenPos(0, 0)

posChanged = False
botstatus = {"position": {"x": 0, "y": 0}, "height": "up", "color": ""}


def setColor(color, changeColor=True):
    colorName = "color{0}".format(color)    # Get color name for cncserver
    client.setPenHeight("up")   # Do not draw on the page while moving to color

    # Only go through all three waters if changing color
    waterTimes = 3 if changeColor else 1
    for i in range(0, waterTimes):   # Do brush wash
        client.setTool("water{0}".format(i))
    client.setTool(colorName)

    # Move back to original position and height
    client.setPenPos(botstatus["position"]["x"], botstatus["position"]["y"])
    client.setPenHeight(botstatus["height"])

while(True):
    command = meggy.readline().rstrip()
    if command[0] == 'b':       # Change brush height
        if command[2] == '0':
            client.setPenHeight("up")
        elif command[2] == '1':
            client.setPenHeight("draw")
    elif command[0] == 'c':     # Set color
        if command[2] == botstatus["color"]:
            setColor(command[2], False)
        else:
            setColor(command[2], True)
        botstatus["color"] = command[2]
    elif command[0] == 'u':
        posChanged = True
        botstatus["position"]["y"] = max(0, botstatus["position"]["y"] - args.move_dist)
    elif command[0] == 'd':
        posChanged = True
        botstatus["position"]["y"] = min(100, botstatus["position"]["y"] + args.move_dist)
    elif command[0] == 'l':
        posChanged = True
        botstatus["position"]["x"] = max(0, botstatus["position"]["x"] - args.move_dist)
    elif command[0] == 'r':
        posChanged = True
        botstatus["position"]["x"] = min(100, botstatus["position"]["x"] + args.move_dist)

    if posChanged:
        client.setPenPos(botstatus["position"]["x"], botstatus["position"]["y"])
        posChanged = False
