#! /usr/bin/env python3


import serial
import time
import hexdump

s_port = '/dev/rs485'
b_rate = 115200

burstlength = 3.0           # One second default timeout

#open serial
ser = serial.Serial(
    port=s_port,
    baudrate=b_rate,
    timeout=0.1
)

def main():

    buff = b''
    buffpos = 0
    lasttime=time.time()

    while True:
        inp = ser.read()
        if len(inp):
            buff += inp
            lasttime = time.time()
        if ((time.time() - lasttime) > burstlength) or not(len(buff)%16):
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
    main()
