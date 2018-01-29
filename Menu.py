#!/usr/bin/python3

import socket, sys, struct, binascii

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def init():
    while True:
        try:
            server_address = ("127.0.0.1", 44444)
            print("Connecting to {} port {}".format(*server_address))
            sock.connect(server_address)
            print("Connected.")
            break
        # except socket.error:
        except ValueError:
            print('Failed to Connect, Retrying...')


def test():
    init()
    # values = (56, 9, -300, 0, 0) # Find route to specified coordinate
    values = (55, 9, 0, 0, 1)  # Move to absolute coordinate, using backwards movement
    print(values)
    packer = struct.Struct(">B H i i B")
    packed_data = packer.pack(*values)
    print(packed_data)

    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
    finally:
        print("Closing socket")
        sock.close()


def moveTo(x, y, dir):
    if dir == 1 or dir == 0:
        values = (55, 9, x, y, dir)
        # print(values)
        packer = struct.Struct(">B H i i B")
        packed_data = packer.pack(*values)
        # print(packed_data)
        try:
            print("Sending {!r}".format(binascii.hexlify(packed_data)))
            sock.sendall(packed_data)
        finally:
            print("Closing socket")
            sock.close()
    else:
        print("invalid Mode")


def routeTo(x, y):
    values = (56, 9, x, y, 0)
    print(values)
    packer = struct.Struct(">B H i i B")
    packed_data = packer.pack(*values)
    print(packed_data)
    try:
        print("Sending {!r}".format(binascii.hexlify(packed_data)))
        sock.sendall(packed_data)
    finally:
        print("Closing socket")
        sock.close()


def print_menu():
    print('----- Control Menu ------')
    print('1: Move To Coordinates')
    print('2: Route To Coordinates')
    print('3: Force Stop')
    print('4: Charge')
    print('5: Exit')


def menu():
    init()
    while False:
        print_menu()  # Prints Menu Options
        while True:
            # takes command input integer and validates
            try:
                command = int(raw_input("Enter Command: "))
                if 0 > command > 6:
                    raise ValueError
                else:
                    break
            except ValueError:
                print('Enter an integer 1 - 5')
        if command == 1:
            print('Selected Move To')
            while True:
                try:
                    x = int(raw_input("Enter X Coordinate: "))
                    if len(str(x)) > 4:
                        raise TypeError
                    else:
                        break
                except TypeError:
                    print('Coord not 4 bytes')
            while True:
                try:
                    y = int(raw_input("Enter Y Coordinate: "))
                    if len(str(y)) > 4:
                        raise TypeError
                    else:
                        break
                except TypeError:
                    print('Coord not 4 bytes')
            while True:
                try:
                    dir_command = raw_input("Enter f -> forwards or b -> backwards: ")
                    if dir_command == 'f':
                        direction = 0
                        break
                    elif dir_command == 'b':
                        direction = 1
                        break
                    else:
                        raise TypeError
                except TypeError:
                    print('enter "f" or "b"')
            print('Moving to ' + str(x) + ' : ' + str(y))
            moveTo(x, y, direction)
        elif command == 2:
            while True:
                try:
                    x = int(raw_input("Enter X Coordinate: "))
                    if len(str(x)) > 4:
                        raise TypeError
                    else:
                        break
                except TypeError:
                    print('Coord not 4 bytes')
            while True:
                try:
                    y = int(raw_input("Enter Y Coordinate: "))
                    if len(str(y)) > 4:
                        raise TypeError
                    else:
                        break
                except TypeError:
                    print('Coord not 4 bytes')
            print('Moving to ' + str(x) + ' : ' + str(y))
            routeTo(x, y)
            print('Selected Route to')
        elif command == 3:
            print('Force Stop')
        elif command == 4:
            print('Move to')
        elif command == 5:
            print('Exiting Program')
            break
        else:
            print('validate Command')


if __name__ == '__main__':
    command = raw_input("Do you want to run the test")
    if command == 'y':
        test()
    else:
        menu()
