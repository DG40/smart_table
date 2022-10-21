import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


class ShiftRegister:
    register_type = '74HC595'
    #  data_pin => GPIO 4 to the 74HC595
    #  latch_pin => GPIO 9 to the 74HC595
    #  clock_pin => GPIO 10 to the 74HC595

    def __init__(self, data_pin=4, latch_pin=9, clock_pin=10):
        self.data_pin = data_pin
        self.latch_pin = latch_pin
        self.clock_pin = clock_pin
        GPIO.setup(self.data_pin, GPIO.OUT)
        GPIO.setup(self.latch_pin, GPIO.OUT)
        GPIO.setup(self.clock_pin, GPIO.OUT)
        self.outputs = [GPIO.LOW] * 8

    #  output_number => Value from 0 to 7 pointing to the output pin on the 74HC595
    #  0 => Q0 pin 15 on the 74HC595
    #  1 => Q1 pin 1 on the 74HC595
    #  2 => Q2 pin 2 on the 74HC595
    #  3 => Q3 pin 3 on the 74HC595
    #  4 => Q4 pin 4 on the 74HC595
    #  5 => Q5 pin 5 on the 74HC595
    #  6 => Q6 pin 6 on the 74HC595
    #  7 => Q7 pin 7 on the 74HC595

    #  value => a state to pass to the pin, could be HIGH or LOW

    def set_output(self, output_number, value):
        try:
            self.outputs[output_number] = value
        except IndexError:
            raise ValueError("Invalid output number. Can be only an int from 0 to 7")

    def set_outputs(self, outputs):
        if 8 != len(outputs):
            raise ValueError("Outputs must be an array with 8 elements")
        self.outputs = outputs

    def latch(self):
        GPIO.output(self.latch_pin, GPIO.LOW)
        for i in range(7, -1, -1):
            GPIO.output(self.clock_pin, GPIO.LOW)
            GPIO.output(self.data_pin, self.outputs[i])
            GPIO.output(self.clock_pin, GPIO.HIGH)
        GPIO.output(self.latch_pin, GPIO.HIGH)

    def test(self):
        flag = True
        for _ in range(4):
            data = [0] * 8
            if flag:
                data[0] = 1
            else:
                data[0] = 0
            print(data, '\n')
            self.set_outputs(data)
            self.latch()
            time.sleep(1)

            flag = not flag

    def switch(self, flag):
        data = [0] * 8
        if flag:
            data[0] = 1
        else:
            data[0] = 0
        print(data, '\n')
        self.set_outputs(data)
        self.latch()
