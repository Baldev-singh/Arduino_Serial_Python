import serial
serialArduino = serial.Serial("COM6", 9600)
while True:
      valueRead = serialArduino.readline()
      print(valueRead.decode())
      
