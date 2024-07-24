import serial
import time

# Configure serial port
serial_port = 'COM8'  # Replace with your ESP-32 serial port
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
            # Add your Manim visualization code here
        time.sleep(0.001)  # Adjust as necessary to stabilize reading

except KeyboardInterrupt:
    print("Serial communication stopped by user")

finally:
    ser.close()
