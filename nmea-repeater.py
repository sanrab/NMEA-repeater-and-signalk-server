#! /usr/bin/python3

import serial,time
import socket

# per RaspberryZeroW (3 nov 2024)
LCD = serial.Serial('/dev/ttyS0', 9600) # LCD Netmedia seriale 4x20 su GPIO
# LCD 5V (rosso/rosso RASPI) su GPIO 2
# LCD GND ((bianco/bianco RASPI) su GPIO 6
# LCD RX (verde/giallo RASPI) su GPIO 8

LCD.write(chr(20).encode()) # LCD backlight
LCD.write(chr(200).encode()) # LCD backlight value
LCD.write(chr(12).encode()) # LCD clear screen

LCD.write("S/Y Polaris".encode())
LCD.write(chr(10).encode()) # new line
LCD.write("DVV, Venezia, 2024".encode())
LCD.write(chr(10).encode()) # new line
LCD.write(chr(10).encode()) # new line
LCD.write("Waiting for data ...".encode())
time.sleep(5)
LCD.write(chr(12).encode()) # clear screen

dep = "NA"

while True:

# connecting to polaris, port 2000

#       s = socket.socket()
#       print ("Socket successfully created")
#       s.connect(('192.168.1.100',2000))

#       lines = (s.recv(1024).decode())
#       print (lines)

        data = s.readline()
        # console check
#       print (data[:-1])

        words = (data.split(','))

        if "DBT" in words[0]:
                dep = words[3]
        if "RMC" in words[0]:
                timestamp = words[1]
                lat = words[3]
                NS = words[4]
                lon = words[5]
                EW = words[6]
                sog = words[7]                
                LCD.write("Lat  ".encode())
                LCD.write(lat[0:2].encode())
                LCD.write(" ".encode())
                LCD.write(lat[2:9].encode())
                LCD.write(" ".encode())
                LCD.write(NS.encode())
                LCD.write("     ".encode())
                cog = words[8]
                datestamp = words[9]
                LCD.write(chr(17).encode()) # cursor position
                LCD.write(chr(0).encode()) # riga
                LCD.write(chr(0).encode()) # colonna
                LCD.write("Lat  ".encode())
                LCD.write(lat[0:2].encode())
                LCD.write(" ".encode())
                LCD.write(lat[2:9].encode())
                LCD.write(" ".encode())
                LCD.write(NS.encode())
                LCD.write("     ".encode())
          
                LCD.write(chr(1).encode()) # riga
                LCD.write(chr(0).encode()) # colonna
                LCD.write("Lon ".encode())
                LCD.write(lon[0:3].encode())
                LCD.write(" ".encode())
                LCD.write(lon[3:10].encode())
                LCD.write(" ".encode())
                LCD.write(EW.encode())
                LCD.write("     ".encode())
                LCD.write(chr(17).encode())
                
                LCD.write(chr(2).encode()) # riga
                LCD.write(chr(0).encode()) # colonna
                LCD.write("SoG ".encode())
                LCD.write(sog[0:3].encode())

                LCD.write(chr(17).encode()) # cursor position
                LCD.write(chr(2).encode()) # riga
                LCD.write(chr(10).encode()) # colonna
                LCD.write("DEP ".encode())
                LCD.write(dep.encode())

                LCD.write(chr(17).encode()) # cursor position
                LCD.write(chr(3).encode()) # riga
                LCD.write(chr(0).encode()) # colonna
                LCD.write("CoG ".encode())
                LCD.write(cog[0:3].encode())

                LCD.write(chr(17).encode()) # cursor position
                LCD.write(chr(3).encode()) # riga
                LCD.write(chr(10).encode()) # colonna
                LCD.write("UTC ".encode())
                LCD.write(timestamp[0:6].encode())

                time.sleep(2)
