import serial
tx_buf = serial.Serial('/dev/ttyS1', 9600, timeout=1)

while True:

    #read data from serial port
    tx_buf = tx_buf.readline()

    #if there is smth do smth
    if len(tx_buf) >= 1:
        print(tx_buf.decode("utf-8"))