#! /usr/bin/env python3
"""sniff485

Usage:
    sniff485 [-b <dur> | --burst=<dur>] [<device>] [<baud>]

Options:
    -h --help           Show this screen.
    -b N | --burst=N    Set batched burst secs (defaults to 3 secs)

<device> is the /dev/XXX pathname to the RS-485 serial adapter,
        defaults to "/dev/rs485"
<baud> is the baud rate to sniff the bus at.  Defaults to 115200.


CLI utility to sniff bytes on a serial interface and then print
out the hex and ASCII interpretations.

Written by: Mike Petonic [2017-01-29 SUN 09:56]
"""



import serial
import time
import hexdump
import sys
from docopt import docopt


def_device    = '/dev/rs485'
def_baud      = 115200

defBurstInt   = 3.0           # One second default timeout

serialTimeout = 0.1           # Different than the burst


# Make this a global variable
arguments     = None

#open serial

def main():
    global arguments            # Use the global so main can see it

    buff = b''
    buffpos = 0
    lasttime=time.time()

    #----> Contents of arguments when "sniff485 -b 12
    #
    # #(Pdb++) arguments
    # {'--burst': ['12'],
    #  '<baud>': None,
    #  '<device>': None}

    ################################################################
    # Parse the command-line arguments
    ################################################################

    baud = def_baud

    s_baud = arguments['<baud>']
    if s_baud:
        try:
            baud = int(s_baud)
        except ValueError:
            print("Baud must be an INT, not <{}>".
                format(s_baud),
                file=sys.stderr)
            sys.exit(1)

    device = def_device
    s_device = arguments['<device>']
    if s_device:
            device = s_device
            # We'll do the open check later.
            #

    burstinterval = defBurstInt
    s_burst = arguments['--burst']
    if s_burst:
        try:
            import pdb; pdb.set_trace()
            burstinterval = float(s_burst[0])
        except (ValueError, FloatingPointError):
            print("BurstInt must be an FLOAT, not <{}>".
                format(s_burst),
                file=sys.stderr)
            sys.exit(1)

    ################################################################
    # Initialize the serial device
    ################################################################

    try:
        ser = serial.Serial(
            port=device,
            baudrate=baud,
            timeout=0.1         # Different than the burst interval
        )
    except IOError as e:
        print("sniff485: IO error opening <{}>: {}".
              format(device, e),
              file=sys.stderr)
        sys.exit(2)



    ################################################################
    # Enter infinite loop.  Exit with keyboard interrupt (^c)
    ################################################################

    while True:
        inp = ser.read()
        if len(inp):
            buff += inp
            lasttime = time.time()
        if ((time.time() - lasttime) > burstinterval) or not(len(buff)%16):
            # import pdb; pdb.set_trace()
            if len(buff):
                # print("Len of buff is {}", len(buff))
                outstring = hexdump.hexdump(buff, result='return')
                print("{:08x}: {}".format(       # Don't print meaningless address
                        buffpos, outstring[10:]))
                buffpos += len(buff)
                buff = b''
                lasttime=time.time()




if __name__ == '__main__':
    arguments = docopt(__doc__, version='sniff485 v1.0')
    main()
