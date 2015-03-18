import serial
import cncserverclient
import argparse
import sys

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


def setColor(color):
    colorName = "color{0}".format(color)    # Get color name for cncserver
    client.setPenHeight("up")   # Do not draw on the page while moving to color

    for i in range(0, 3):   # Do brush wash
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
        botstatus["color"] = command[2]
        setColor(botstatus["color"])
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
