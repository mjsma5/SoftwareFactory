#!/usr/bin/python3

import socket, sys, struct, binascii
from enum import Enum

# =============================================== Constants
FORWARD = 0
BACKWARD = 1

class Commands(Enum):
    MOVE_TO = 55
    ROUTE_TO = 56
    MOVE_TO_CHARGER = 57
    MULTIPE_TASKS = 58
    MANUAL_MOVE = 59
    CREATE_OBSTACLE = 60
    REMOVE_OBSTACLE = 61
    PROGRAM_EXIT = 62
    ASK_POSITION = 130

commands_lengths = {
    Commands.MOVE_TO: 9,
    Commands.ROUTE_TO: 9,
    Commands.MOVE_TO_CHARGER: 1,
    Commands.MULTIPE_TASKS: 1,
    Commands.MANUAL_MOVE: 2,
    Commands.CREATE_OBSTACLE: 8,
    Commands.REMOVE_OBSTACLE: 8,
    Commands.PROGRAM_EXIT: 8,
    Commands.ASK_POSITION: 10,
    -1: 0
}

class DirectionsCode(Enum):
    FORWARD = 10
    BACKWARD = 11
    LEFT = 12
    RIGHT = 13

# =============================================== Parameters
# This has to be moved in a file just for this
local_adress = ("127.0.0.1", 44444)
ojabotti_adress = ("192.168.88.162", 22222)

adress_in_use = local_adress

# ======================================== Socket management
sock = None

class ConnectionRefusedError(object):
    pass


def create_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        print("Connecting to {} port {}".format(*adress_in_use))
        sock.connect(adress_in_use)
        print("Connected")
    except ConnectionRefusedError:
        print("Enable to connect, connexion refused")
        return None
    return sock

def close_connection(sock):
    if not sock:
        print("Socket already closed or never openned")
        return

    print("Closing socket")
    sock.close()
    sock = None
    print("Socket closed")

# ================================================ Commands

# Move to (x,y) in the specified direction
def move_to(x = 0, y = 0, dir = FORWARD):
    if(dir != FORWARD and dir != BACKWARD):
        print("Direction unknown {}".format(dir))
        return

    if not sock: return

    values = (Commands.MOVE_TO, commands_lengths[Commands.MOVE_TO], x, y, dir)
    #u_char u_short int int u_char
    packed_data = struct.pack(">B H i i B", *values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
        print("Sent")
    except:
        print("Oops...Smthg went wrong when sending datas...")

# Move to (x,y) using the map to avoid obstacles
def route_to(x = 0, y = 0):
    if not sock: return

    values = (Commands.ROUTE_TO, commands_lengths[Commands.ROUTE_TO], x, y, 0)
    packed_data = struct.pack(">B H i i B", *values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
        print("Sent")
    except:
        print("Oops...Smthg went wrong when sending datas...")

# Move to the charger already set
def move_to_charger():
    if not sock: return

    #0 is for possible evolutions but it's meaningless
    values = (Commands.MOVE_TO_CHARGER, commands_lengths[Commands.MOVE_TO_CHARGER], 0)
    packed_data = struct.pack(">B H B", *values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
        print("Sent")
    except:
        print("Oops...Smthg went wrong when sending datas...")

# Manually moves the robot back and forth or rotates
def manual_move(direction = DirectionsCode.FORWARD):
    if direction not in DirectionsCode.__members__:
        print("Direction unknown {}".format(direction))
        return

    if not sock: return

    values = (Commands.MANUAL_MOVE, commands_lengths[Commands.MANUAL_MOVE], direction)
    packed_data = struct.pack(">B H B", *values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
        print("Sent")
    except:
        print("Oops...Smthg went wrong when sending data...")

# Create or remove an obstacle (create if create is True)
def manage_obstacle(x = 0, y = 0, create = True):
    if not sock: return

    c = Commands.REMOVE_OBSTACLE
    if create:
        c = Commands.CREATE_OBSTACLE

    values = (c, commands_lengths[c], x, y)
    packed_data = struct.pack(">B H i i B", *values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
        print("Sent")
    except:
        print("Oops...Smthg went wrong when sending datas...")

# =============================================== Program

if __name__ == "__main__":
    sock = create_connection()

    move_to(0, 0)

    close_connection(sock)